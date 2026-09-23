"""Validate authoritative FXD control state and fail closed on drift/cost routing.

The validator checks the *meaning* of current recovery authority (Decision
0002 / Issue #87) rather than one hard-coded revision: the active gate must be
a known recovery gate with a consistent issue/PR/branch/work order, exactly one
allowed subscription builder must be selected and projected consistently,
every paid development and product-runtime request budget must be zero, and
held, stale, or conflicting states must fail closed.  Historical authority
(the Issue #66 reset, the frozen legacy registry, retired dispatchers) is
checked as immutable history, never as current work selection.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA = "fxd-control-state-v1"
# Decision 0002 / Issue #87 introduced recovery authority at revision 8.  A
# lower revision can only be stale pre-recovery state; higher revisions are
# accepted only if every semantic check below still holds.
MIN_RECOVERY_REVISION = 8
RESET_MERGE = "592876fefde118b5325bbb5b4949eeb1490cdf6c"
LEGACY_BLOB = "f667797f1ea59e508ebd46b97cc89061f56b1c1a"
IMPLEMENTATION_PR = 79
IMPLEMENTATION_BRANCH = "agent/m33-1-native-product-reconstruction"
RECOVERY_ISSUE = 87
PRESERVED_R1_HEAD = "de26501958045b5f1dd80eb40ce8f8f1f8d9cf5f"
PRESERVED_FINDINGS = ["F05", "F06", "F11"]

# Recovery gates this validator knows how to check.  An unknown gate id fails
# closed: activating a new gate must come with a reviewed validator update.
RECOVERY_GATES: dict[str, dict[str, Any]] = {
    "FXD-R0": {
        "issue": RECOVERY_ISSUE,
        "pull_request": IMPLEMENTATION_PR,
        "branch": IMPLEMENTATION_BRANCH,
        "expected_pr_state": "open_draft_recovery_offline_only",
        "state": "REPAIR",
        "work_order": "docs/FXD_RECOVERY_GATE_00.md",
    },
}

# The bounded set of subscription-backed implementation surfaces.  Adding a
# builder (or a paid/API route) is an owner decision, not a data edit.
BUILDER_LABELS = {
    "chatgpt_codex_remote": "ChatGPT Codex Remote",
    "claude_code": "Claude Code",
}

REQUIRED_AUTHORITY_FILES = (
    "CLAUDE.md",
    "docs/FXD_RECOVERY_GATE_00.md",
    "docs/decisions/0002-fxd-recovery-reset.md",
    "docs/FXD_REASSESSMENT_2026-09-22.md",
    "docs/FXD_RECOVERY_ROADMAP.md",
    "docs/USER_WORKFLOW.md",
    "docs/ARCHITECTURE_CURRENT.md",
)

CURRENT_DOCS = (
    "AGENTS.md", "CURRENT.md", "README.md", "CLAUDE.md", "docs/PRODUCT_DIRECTION.md",
    "docs/OPERATOR_PROTOCOL.md", "docs/ENGINEERING_CONSTITUTION.md",
    "docs/AI_DRIVEN_SYNTHESIS_ARCHITECTURE.md", "docs/ARCHITECTURE.md",
    "docs/MILESTONE_CONTRACT.md", "docs/ENGINEERING_TEAM.md",
    "docs/FOREMAN_SETUP.md", "docs/FXD_RECOVERY_GATE_00.md",
    "docs/decisions/0001-ai-driven-fixture-synthesis-reset.md",
)
# Operator-facing projections of the active gate.  Each must name the active
# gate, its issue, and its implementation PR.
ACTIVE_PROJECTION_DOCS = (
    "AGENTS.md", "CURRENT.md", "README.md", "CLAUDE.md", "docs/MILESTONE_CONTRACT.md",
    "docs/FOREMAN_SETUP.md", "docs/OPERATOR_PROTOCOL.md", "docs/FXD_RECOVERY_GATE_00.md",
)
# Projections that must name the currently selected builder.
BUILDER_PROJECTION_DOCS = (
    "AGENTS.md", "CURRENT.md", "README.md", "docs/MILESTONE_CONTRACT.md",
    "docs/FOREMAN_SETUP.md", "docs/FXD_RECOVERY_GATE_00.md",
)
_SELECTED_BUILDER_CLAIM = re.compile(r"selected builder[^:\n]*:[ \t]*\**[ \t]*(\S[^\n]*)", re.IGNORECASE)
STALE_RESET_CLAIMS = (
    "AWAITING_REVIEW — GOVERNANCE RESET",
    "Issue #66 is the active governance authority",
    "Implementation PR:** #67",
    "Do not begin product runtime implementation until PR #67 is accepted",
    "M33 must remain PLANNED",
    "M33.1 must remain blocked",
)
# Superseded pre-recovery current-state claims (the Sept. 7 M33.1-R1 repair
# pass and the Sept. 12 portfolio hold).  They are history now; a current
# projection that still asserts one is conflicting state.
STALE_CURRENT_CLAIMS = (
    "REPAIR — OFFLINE ONLY — M33.1",
    "HELD — COST CONTROL",
    "Implementation PR:** none yet",
    "**HOLD**",
)


def blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()  # nosec B324


def mapping(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be an object")
        return {}
    return value


def _active_workflow_text(text: str) -> str:
    """Ignore comments while preserving every executable/configuration line."""
    return "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith("#")
    )


def _validate_workflow_cost_boundary(root: Path, errors: list[str]) -> None:
    """Reject any active GitHub workflow route capable of paid OpenAI development."""
    workflows = root / ".github" / "workflows"
    if not workflows.is_dir():
        errors.append(".github/workflows is missing")
        return

    for path in sorted((*workflows.glob("*.yml"), *workflows.glob("*.yaml"))):
        active = _active_workflow_text(path.read_text(encoding="utf-8"))
        normalized = active.casefold()
        relative = path.relative_to(root)

        # Case-insensitive and secret-name-independent. These cover the Codex
        # action, conventional or alternate OPENAI_API_KEY forwarding, direct
        # OpenAI HTTP calls, and SDK/provider use paired with any GitHub secret.
        if "codex-action" in normalized:
            errors.append(f"paid development Codex action is forbidden in {relative}")
        if "openai_api_key" in normalized:
            errors.append(f"OpenAI API key forwarding is forbidden in {relative}")
        if "api.openai.com" in normalized:
            errors.append(f"direct OpenAI API endpoint use is forbidden in {relative}")
        if "openai" in normalized and "secrets." in normalized:
            errors.append(f"OpenAI workflow use paired with a GitHub secret is forbidden in {relative}")

    retired = workflows / "m33-1-codex-continue.yml"
    if not retired.exists():
        errors.append("retired M33.1 paid dispatcher control surface is missing")
    else:
        text = retired.read_text(encoding="utf-8")
        for token in (
            "RETIRED — M33.1 paid Codex dispatcher",
            "contents: read",
            "Use ChatGPT Codex Remote",
            "exit 1",
        ):
            if token not in text:
                errors.append(f"retired paid dispatcher is missing {token!r}")
        active = _active_workflow_text(text).casefold()
        for forbidden in ("push:", "codex-action", "openai_api_key", "api.openai.com"):
            if forbidden in active:
                errors.append(f"retired paid dispatcher retains active route {forbidden!r}")


def _read(root: Path, relative: str, errors: list[str]) -> str | None:
    try:
        return (root / relative).read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read {relative}: {exc}")
        return None


def _validate_projections(
        root: Path, gate_id: str, gate: dict[str, Any], selected_builder: str | None,
        errors: list[str]) -> None:
    """Require every operator projection to agree with the active gate and selected builder."""
    issue_token = f"#{gate['issue']}"
    pr_token = f"#{gate['pull_request']}"
    selected_label = BUILDER_LABELS.get(selected_builder or "")
    for relative in ACTIVE_PROJECTION_DOCS:
        text = _read(root, relative, errors)
        if text is None:
            continue
        for token in (gate_id, issue_token, pr_token):
            if token not in text:
                errors.append(f"{relative} does not project active gate {gate_id}: missing {token!r}")
        for stale in STALE_CURRENT_CLAIMS:
            if stale.casefold() in text.casefold():
                errors.append(f"{relative} retains superseded pre-recovery claim {stale!r}")
        # Any explicit "selected builder: X" claim must name the builder that
        # current control actually selects -- never the unselected one.
        if selected_label is not None:
            for match in _SELECTED_BUILDER_CLAIM.finditer(text):
                claimed = match.group(1).lstrip("*").strip()
                if not claimed.startswith(selected_label):
                    errors.append(
                        f"{relative} claims a selected builder that conflicts with control state "
                        f"{selected_label!r}: {match.group(0).strip()!r}"
                    )
    if selected_label is not None:
        for relative in BUILDER_PROJECTION_DOCS:
            text = _read(root, relative, errors)
            if text is not None and selected_label not in text:
                errors.append(f"{relative} does not name the selected builder {selected_label!r}")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads((root / "docs/CONTROL_STATE.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load docs/CONTROL_STATE.json: {exc}"]

    for key, expected in {
        "schema_version": SCHEMA,
        "operator_protocol": "docs/OPERATOR_PROTOCOL.md",
        "current_human_surface": "CURRENT.md",
    }.items():
        if data.get(key) != expected:
            errors.append(f"{key} must be {expected!r}, got {data.get(key)!r}")
    revision = data.get("revision")
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < MIN_RECOVERY_REVISION:
        errors.append(
            f"revision must be an integer >= {MIN_RECOVERY_REVISION} (recovery authority), got {revision!r}"
        )

    # --- active gate: a known recovery gate, consistent everywhere ----------
    gate = mapping(data, "active_gate", errors)
    gate_id = gate.get("id")
    known = RECOVERY_GATES.get(gate_id) if isinstance(gate_id, str) else None
    if known is None:
        errors.append(f"active_gate.id {gate_id!r} is not a known recovery gate; failing closed")
        known = RECOVERY_GATES["FXD-R0"]
        gate_id = "FXD-R0"
    if gate.get("lane") != "product":
        errors.append("active_gate.lane must be 'product'")
    for key in ("issue", "pull_request", "branch", "expected_pr_state"):
        if gate.get(key) != known[key]:
            errors.append(f"active_gate.{key} must be {known[key]!r} for {gate_id}, got {gate.get(key)!r}")
    objective = gate.get("objective")
    if not isinstance(objective, str) or "without any live provider request" not in objective:
        errors.append("active_gate.objective must keep the gate free of any live provider request")
    if data.get("state") != known["state"]:
        errors.append(f"state must be {known['state']!r} for {gate_id}, got {data.get('state')!r}")
    if data.get("authority_issue") != known["issue"]:
        errors.append(f"authority_issue must be {known['issue']!r}, got {data.get('authority_issue')!r}")
    if not (root / known["work_order"]).is_file():
        errors.append(f"active work order is missing: {known['work_order']}")

    # --- hold: lifted by the active authority, never silently re-held -------
    if data.get("product_implementation_held") is not False:
        errors.append("product_implementation_held must be false while a recovery gate is active")
    hold = mapping(data, "hold", errors)
    if hold.get("authority") != "owner":
        errors.append("hold history must be owner-authorized")
    if not isinstance(hold.get("lifted_at_utc"), str) or hold.get("lifted_by_issue") != known["issue"]:
        errors.append(f"historical hold must record its lift by active Issue #{known['issue']}")

    recovery = mapping(data, "product_recovery", errors)
    recovery_gate = recovery.get("active_gate")
    if recovery.get("status") != "ACTIVE" or not isinstance(recovery_gate, dict) or (
        recovery_gate.get("id"), recovery_gate.get("issue"), recovery_gate.get("status")
    ) != (gate_id, known["issue"], known["state"]):
        errors.append(f"product_recovery.active_gate must match active gate {gate_id} / Issue #{known['issue']}")
    reset_2 = mapping(data, "recovery_reset", errors)
    if reset_2.get("issue") != RECOVERY_ISSUE:
        errors.append(f"recovery_reset.issue must be {RECOVERY_ISSUE}")
    for key in ("reassessment", "decision", "roadmap"):
        value = reset_2.get(key)
        if not isinstance(value, str) or not (root / value).is_file():
            errors.append(f"recovery_reset.{key} must name an existing authority document")
    for relative in REQUIRED_AUTHORITY_FILES:
        if not (root / relative).is_file():
            errors.append(f"required recovery authority is missing: {relative}")

    # --- builder: exactly one bounded, subscription-backed builder ----------
    execution = mapping(data, "development_execution", errors)
    allowed = execution.get("allowed_subscription_builders")
    if not isinstance(allowed, list) or sorted(allowed) != sorted(BUILDER_LABELS):
        errors.append(
            f"development_execution.allowed_subscription_builders must be exactly {sorted(BUILDER_LABELS)!r}"
        )
    selected = execution.get("selected_builder")
    if selected not in BUILDER_LABELS:
        errors.append(f"development_execution.selected_builder {selected!r} is not an allowed builder")
        selected = None
    if execution.get("default_builder") not in BUILDER_LABELS:
        errors.append("development_execution.default_builder must be an allowed builder")
    for key, expected in {
        "one_builder_per_gate": True,
        "repository_api_key_for_development": False,
        "github_paid_codex_dispatchers_allowed": False,
        "product_runtime_api_requires_explicit_review_control_authorization": True,
        "builder_cannot_independently_approve_own_work": True,
    }.items():
        if execution.get(key) is not expected:
            errors.append(f"development_execution.{key} must be {expected!r}")

    # --- implementation authorization: offline, bounded, no self-advance ----
    authorization = mapping(data, "implementation_authorization", errors)
    for key, expected in {
        "authority": "owner",
        "issue": known["issue"],
        "mode": "offline_only",
        "pass_id": gate_id,
        "work_order": known["work_order"],
        "stop_state": "AWAITING_REVIEW",
        "synchronize_current_main": True,
        "product_merge_authorized_after_independent_acceptance": True,
        "next_gate_authorized": False,
    }.items():
        if authorization.get(key) != expected:
            errors.append(f"implementation_authorization.{key} must be {expected!r}, got {authorization.get(key)!r}")
    if selected is not None and authorization.get("selected_builder") != selected:
        errors.append("implementation_authorization.selected_builder must match development_execution")

    # --- cost boundary: every request budget is zero -----------------------
    runtime = mapping(data, "product_runtime_authorization", errors)
    if runtime.get("authorized") is not False or runtime.get("live_requests") != 0:
        errors.append("product_runtime_authorization must deny all live requests in this gate")
    budgets = mapping(data, "budgets", errors)
    for key in (
        "development_api_requests", "repository_paid_development_dispatchers",
        "product_runtime_live_requests", "automatic_provider_retries", "repair_requests",
    ):
        value = budgets.get(key)
        if isinstance(value, bool) or value != 0:
            errors.append(f"budgets.{key} must be 0, got {value!r}")

    # --- preserved R1 foundation ------------------------------------------
    preserved = mapping(data, "preserved_foundation", errors)
    for key, expected in {
        "pull_request": IMPLEMENTATION_PR,
        "reviewed_head": PRESERVED_R1_HEAD,
        "accepted_bounded_findings": PRESERVED_FINDINGS,
    }.items():
        if preserved.get(key) != expected:
            errors.append(f"preserved_foundation.{key} must be {expected!r}")

    # --- history: immutable, never current ---------------------------------
    reset = mapping(data, "accepted_reset", errors)
    for key, expected in {
        "issue": 66,
        "pull_request": 67,
        "merge_commit": RESET_MERGE,
        "decision": "docs/decisions/0001-ai-driven-fixture-synthesis-reset.md",
        "authority": "historical_foundation",
    }.items():
        if reset.get(key) != expected:
            errors.append(f"accepted_reset.{key} must be {expected!r}")

    superseded = data.get("superseded_execution_authority")
    if not isinstance(superseded, list):
        errors.append("superseded_execution_authority must be an array")
        superseded = []
    for issue, extra, disposition in (
        (69, ("gate", "M33.1"), "historical_foundation_preserve_evidence"),
        (68, ("milestone", "M33"), "historical_product_reset_preserve_evidence"),
        (57, ("pull_request", 54), "closed_unmerged_selective_salvage_only"),
    ):
        if not any(
            isinstance(item, dict) and item.get("issue") == issue
            and item.get(extra[0]) == extra[1] and item.get("disposition") == disposition
            for item in superseded
        ):
            errors.append(f"superseded_execution_authority is missing Issue #{issue} ({disposition})")

    legacy = mapping(data, "legacy_milestone_registry", errors)
    if legacy.get("path") != "docs/MILESTONE_STATE.json" or legacy.get("authority") != "historical_only":
        errors.append("legacy milestone registry must remain historical-only at docs/MILESTONE_STATE.json")
    try:
        actual_blob = blob_sha((root / "docs/MILESTONE_STATE.json").read_bytes())
    except OSError as exc:
        errors.append(f"cannot read legacy milestone registry: {exc}")
    else:
        if legacy.get("git_blob_sha") != LEGACY_BLOB or actual_blob != LEGACY_BLOB:
            errors.append("legacy milestone registry changed from the frozen pre-reset blob")

    current = _read(root, "CURRENT.md", errors) or ""
    for token in (
        "OFFLINE ONLY",
        "**Implementation PR:** #79",
        "**Product-runtime requests:** 0",
        "**Development API requests:** 0",
        "**CONTINUE**",
    ):
        if token not in current:
            errors.append(f"CURRENT.md is missing {token!r}")

    next_action = data.get("next_valid_action")
    if not isinstance(next_action, str) or not next_action.startswith("CONTINUE"):
        errors.append("next_valid_action must be bounded CONTINUE")
    elif any(token not in next_action for token in (
            gate_id, f"#{known['issue']}", f"PR #{known['pull_request']}",
            "F05/F06/F11", "AWAITING_REVIEW", "remain 0")):
        errors.append(
            "next_valid_action must name the active gate, issue, PR, preserved F05/F06/F11, "
            "AWAITING_REVIEW stop, and zero-request budgets"
        )

    for relative in CURRENT_DOCS:
        text = _read(root, relative, errors)
        if text is None:
            continue
        for forbidden in ("M32 is the sole Active", "PR #54 is the active implementation"):
            if forbidden.casefold() in text.casefold():
                errors.append(f"{relative} retains forbidden current claim: {forbidden}")
        if relative in ACTIVE_PROJECTION_DOCS:
            for stale in STALE_RESET_CLAIMS:
                if stale.casefold() in text.casefold():
                    errors.append(f"{relative} retains stale activation claim: {stale}")

    _validate_projections(root, gate_id, known, selected, errors)

    foreman = (root / ".github/workflows/fxd-foreman.yml").read_text(encoding="utf-8")
    for token in ("RETIRED BY ISSUE #66", "contents: read", "exit 1"):
        if token not in foreman:
            errors.append(f"retired Foreman is missing {token!r}")
    for forbidden in (
        "openai/codex-action", "contents: write", "pull-requests: write",
        "issues: write", "gh pr create", "git push",
    ):
        if forbidden in foreman:
            errors.append(f"retired Foreman retains {forbidden!r}")

    _validate_workflow_cost_boundary(root, errors)

    selector = (root / "scripts/fxd-backlog.mjs").read_text(encoding="utf-8")
    if "automatic milestone selection is retired by Issue #66" not in selector:
        errors.append("legacy selector does not fail closed")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        print("FXD control-state validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    data = json.loads((root / "docs/CONTROL_STATE.json").read_text(encoding="utf-8"))
    gate = data["active_gate"]
    builder = BUILDER_LABELS[data["development_execution"]["selected_builder"]]
    print(
        f"FXD control state validated: revision {data['revision']} / {gate['id']} / Issue #{gate['issue']} / "
        f"PR #{gate['pull_request']} {data['state']} offline only; selected builder {builder}; "
        "development API, paid dispatcher, and product-runtime requests all 0."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
