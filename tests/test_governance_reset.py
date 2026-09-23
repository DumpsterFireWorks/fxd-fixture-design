from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.validate_control_state import (
    CURRENT_DOCS, REQUIRED_AUTHORITY_FILES, _validate_workflow_cost_boundary, validate,
)


ROOT = Path(__file__).resolve().parents[1]


def _copy_governed_tree(root: Path) -> None:
    """Copy every file the control-state validator reads into an isolated tree."""
    paths = set(CURRENT_DOCS) | set(REQUIRED_AUTHORITY_FILES) | {
        "docs/CONTROL_STATE.json", "docs/MILESTONE_STATE.json", "scripts/fxd-backlog.mjs",
    }
    paths.update(str(path.relative_to(ROOT)) for path in (ROOT / ".github/workflows").glob("*"))
    for relative in paths:
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)


def _write_retired_dispatcher(workflows: Path) -> None:
    (workflows / "m33-1-codex-continue.yml").write_text(
        """name: RETIRED — M33.1 paid Codex dispatcher
on:\n  workflow_dispatch:\njobs:\n  retired:\n    permissions:\n      contents: read\n    steps:\n      - run: |\n          echo \"Use ChatGPT Codex Remote\"\n          exit 1\n""",
        encoding="utf-8",
    )


class GovernanceResetTests(unittest.TestCase):
    def test_recovery_authority_rejects_scope_spend_builder_and_state_drift(self) -> None:
        """Every unsafe or conflicting control-state edit must fail closed."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _copy_governed_tree(root)
            self.assertEqual([], validate(root))
            state_path = root / "docs/CONTROL_STATE.json"
            original = state_path.read_text(encoding="utf-8")
            mutations = (
                # product-runtime / development spend
                ("product_runtime_authorization", "authorized", True),
                ("product_runtime_authorization", "live_requests", 1),
                ("budgets", "development_api_requests", 1),
                ("budgets", "repository_paid_development_dispatchers", 1),
                ("budgets", "product_runtime_live_requests", 1),
                ("budgets", "automatic_provider_retries", 1),
                ("development_execution", "repository_api_key_for_development", True),
                ("development_execution", "github_paid_codex_dispatchers_allowed", True),
                ("development_execution", "product_runtime_api_requires_explicit_review_control_authorization", False),
                # builder selection
                ("development_execution", "selected_builder", "anthropic_api"),
                ("development_execution", "allowed_subscription_builders",
                 ["chatgpt_codex_remote", "claude_code", "openai_api"]),
                ("development_execution", "one_builder_per_gate", False),
                ("development_execution", "builder_cannot_independently_approve_own_work", False),
                ("implementation_authorization", "selected_builder", "chatgpt_codex_remote"),
                # scope / advancement
                ("implementation_authorization", "mode", "live"),
                ("implementation_authorization", "issue", 69),
                ("implementation_authorization", "pass_id", "FXD-R1"),
                ("implementation_authorization", "next_gate_authorized", True),
                ("implementation_authorization", "stop_state", "COMPLETE"),
                ("active_gate", "id", "FXD-R9"),
                ("active_gate", "issue", 69),
                ("active_gate", "pull_request", 54),
                ("active_gate", "branch", "main"),
                # held / stale state
                (None, "product_implementation_held", True),
                (None, "state", "ACTIVE"),
                (None, "revision", 4),
                (None, "authority_issue", 83),
                ("preserved_foundation", "reviewed_head", "0" * 40),
                ("preserved_foundation", "accepted_bounded_findings", ["F05", "F06"]),
                ("accepted_reset", "merge_commit", "0" * 40),
            )
            for section, key, value in mutations:
                with self.subTest(section=section, key=key, value=value):
                    state = json.loads(original)
                    target = state[section] if section else state
                    target[key] = value
                    state_path.write_text(json.dumps(state), encoding="utf-8")
                    self.assertTrue(validate(root))
            state_path.write_text(original, encoding="utf-8")
            self.assertEqual([], validate(root))

            # A re-held or pre-recovery CURRENT.md projection also fails closed.
            current_path = root / "CURRENT.md"
            current_text = current_path.read_text(encoding="utf-8")
            current_path.write_text(
                current_text.replace("OFFLINE ONLY", "HELD — COST CONTROL", 1), encoding="utf-8",
            )
            self.assertTrue(validate(root))
            current_path.write_text(current_text, encoding="utf-8")
            self.assertEqual([], validate(root))

    def test_projection_naming_the_unselected_builder_fails_closed(self) -> None:
        """Regression: main projected 'Selected builder: ChatGPT Codex Remote' after revision 8."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _copy_governed_tree(root)
            contract = root / "docs/MILESTONE_CONTRACT.md"
            contract.write_text(
                contract.read_text(encoding="utf-8").replace(
                    "- Selected builder: Claude Code", "- Selected builder: ChatGPT Codex Remote",
                ),
                encoding="utf-8",
            )
            errors = validate(root)
        self.assertTrue(any("conflicts with control state" in error for error in errors), errors)

    def test_missing_recovery_authority_document_fails_closed(self) -> None:
        for relative in REQUIRED_AUTHORITY_FILES:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                _copy_governed_tree(root)
                (root / relative).unlink()
                self.assertTrue(validate(root))

    def test_authoritative_control_state_validates(self) -> None:
        self.assertEqual([], validate(ROOT))

    def test_fxd_r0_is_the_active_offline_recovery_gate_on_existing_pr(self) -> None:
        state = json.loads((ROOT / "docs" / "CONTROL_STATE.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(state["revision"], 8)
        self.assertEqual(87, state["authority_issue"])
        self.assertEqual("REPAIR", state["state"])
        self.assertFalse(state["product_implementation_held"])
        self.assertEqual(87, state["hold"]["lifted_by_issue"])
        gate = state["active_gate"]
        self.assertEqual(
            ("product", "FXD-R0", 87, 79, "agent/m33-1-native-product-reconstruction",
             "open_draft_recovery_offline_only"),
            (gate["lane"], gate["id"], gate["issue"], gate["pull_request"], gate["branch"],
             gate["expected_pr_state"]),
        )
        authorization = state["implementation_authorization"]
        self.assertEqual("offline_only", authorization["mode"])
        self.assertEqual("FXD-R0", authorization["pass_id"])
        self.assertEqual("AWAITING_REVIEW", authorization["stop_state"])
        self.assertFalse(authorization["next_gate_authorized"])
        self.assertTrue(state["next_valid_action"].startswith("CONTINUE"))

    def test_exactly_one_bounded_subscription_builder_is_selected(self) -> None:
        state = json.loads((ROOT / "docs" / "CONTROL_STATE.json").read_text(encoding="utf-8"))
        execution = state["development_execution"]
        self.assertEqual(
            ["chatgpt_codex_remote", "claude_code"], sorted(execution["allowed_subscription_builders"]),
        )
        self.assertIn(execution["selected_builder"], execution["allowed_subscription_builders"])
        self.assertEqual(execution["selected_builder"], state["implementation_authorization"]["selected_builder"])
        self.assertTrue(execution["one_builder_per_gate"])
        self.assertFalse(execution["repository_api_key_for_development"])
        self.assertFalse(execution["github_paid_codex_dispatchers_allowed"])
        self.assertTrue(execution["builder_cannot_independently_approve_own_work"])

    def test_every_request_budget_is_zero_and_runtime_is_unauthorized(self) -> None:
        state = json.loads((ROOT / "docs" / "CONTROL_STATE.json").read_text(encoding="utf-8"))
        budgets = state["budgets"]
        for key in (
            "development_api_requests", "repository_paid_development_dispatchers",
            "product_runtime_live_requests", "automatic_provider_retries", "repair_requests",
        ):
            self.assertEqual(0, budgets[key], key)
        self.assertFalse(state["product_runtime_authorization"]["authorized"])
        self.assertEqual(0, state["product_runtime_authorization"]["live_requests"])

    def test_preserved_r1_foundation_is_recorded(self) -> None:
        state = json.loads((ROOT / "docs" / "CONTROL_STATE.json").read_text(encoding="utf-8"))
        preserved = state["preserved_foundation"]
        self.assertEqual(79, preserved["pull_request"])
        self.assertEqual("de26501958045b5f1dd80eb40ce8f8f1f8d9cf5f", preserved["reviewed_head"])
        self.assertEqual(["F05", "F06", "F11"], preserved["accepted_bounded_findings"])

    def test_current_state_projects_offline_recovery_and_cost_boundary(self) -> None:
        current = (ROOT / "CURRENT.md").read_text(encoding="utf-8")
        for token in (
            "FXD-R0", "ISSUE #87 / PR #79", "OFFLINE ONLY",
            "**Implementation PR:** #79", "**Selected builder:** Claude Code",
            "**Product-runtime requests:** 0", "**Development API requests:** 0",
            "**CONTINUE**",
        ):
            self.assertIn(token, current)
        for stale in ("Implementation PR:** none yet", "**HOLD**", "M33.1 / ISSUE #69"):
            self.assertNotIn(stale, current)

    def test_all_current_projections_name_active_gate_and_selected_builder(self) -> None:
        for relative in (
            "README.md", "AGENTS.md", "CLAUDE.md", "docs/FOREMAN_SETUP.md",
            "docs/MILESTONE_CONTRACT.md", "docs/OPERATOR_PROTOCOL.md", "docs/FXD_RECOVERY_GATE_00.md",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            for token in ("FXD-R0", "#87", "#79"):
                self.assertIn(token, text, relative)
        for relative in ("README.md", "AGENTS.md", "docs/FOREMAN_SETUP.md", "docs/MILESTONE_CONTRACT.md"):
            self.assertIn("Claude Code", (ROOT / relative).read_text(encoding="utf-8"), relative)

    def test_actual_github_workflows_have_no_paid_development_route(self) -> None:
        errors: list[str] = []
        _validate_workflow_cost_boundary(ROOT, errors)
        self.assertEqual([], errors)

    def test_cost_guard_detects_case_variant_codex_action(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            _write_retired_dispatcher(workflows)
            (workflows / "bad.yml").write_text(
                "jobs:\n  paid:\n    steps:\n      - uses: OpenAI/codex-action@v1\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            _validate_workflow_cost_boundary(root, errors)
        self.assertTrue(any("Codex action" in error for error in errors), errors)

    def test_cost_guard_detects_alternate_secret_forwarding(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            _write_retired_dispatcher(workflows)
            (workflows / "bad.yml").write_text(
                "jobs:\n  paid:\n    env:\n      OPENAI_API_KEY: ${{ secrets.DEVELOPMENT_OPENAI_KEY }}\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            _validate_workflow_cost_boundary(root, errors)
        self.assertTrue(any("API key forwarding" in error for error in errors), errors)

    def test_cost_guard_detects_direct_provider_endpoint_with_secret(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            _write_retired_dispatcher(workflows)
            (workflows / "bad.yml").write_text(
                "jobs:\n  paid:\n    steps:\n      - run: curl https://api.openai.com/v1/responses\n        env:\n          PROVIDER_KEY: ${{ secrets.PROVIDER_KEY }}\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            _validate_workflow_cost_boundary(root, errors)
        self.assertTrue(any("endpoint" in error for error in errors), errors)

    def test_retired_paid_dispatcher_is_inert_read_only_and_fail_closed(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "m33-1-codex-continue.yml").read_text(
            encoding="utf-8"
        )
        for token in (
            "RETIRED — M33.1 paid Codex dispatcher",
            "contents: read",
            "Use ChatGPT Codex Remote",
            "exit 1",
        ):
            self.assertIn(token, workflow)
        active_lines = "\n".join(
            line for line in workflow.splitlines()
            if not line.lstrip().startswith("#")
        ).casefold()
        for token in (
            "push:",
            "codex-action",
            "openai_api_key",
            "api.openai.com",
            "contents: write",
            "pull-requests: write",
            "issues: write",
            "gh pr create",
            "git push",
        ):
            self.assertNotIn(token, active_lines)

    def test_autonomous_foreman_workflow_is_retired_and_read_only(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "fxd-foreman.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("RETIRED BY ISSUE #66", workflow)
        self.assertIn("contents: read", workflow)
        self.assertIn("exit 1", workflow)
        for forbidden in (
            "openai/codex-action",
            "contents: write",
            "pull-requests: write",
            "issues: write",
            "gh pr create",
            "git push",
        ):
            self.assertNotIn(forbidden, workflow)

    def test_reset_merge_and_superseded_m32_remain_durable(self) -> None:
        state = json.loads((ROOT / "docs" / "CONTROL_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(66, state["accepted_reset"]["issue"])
        self.assertEqual(67, state["accepted_reset"]["pull_request"])
        self.assertEqual(
            "592876fefde118b5325bbb5b4949eeb1490cdf6c",
            state["accepted_reset"]["merge_commit"],
        )
        self.assertEqual("historical_foundation", state["accepted_reset"]["authority"])
        superseded = state["superseded_execution_authority"]
        m32 = next(item for item in superseded if item.get("issue") == 57)
        self.assertEqual(54, m32["pull_request"])
        self.assertEqual("closed_unmerged_selective_salvage_only", m32["disposition"])
        m33_1 = next(item for item in superseded if item.get("issue") == 69)
        self.assertEqual("historical_foundation_preserve_evidence", m33_1["disposition"])

    def test_real_repository_selector_fails_closed_under_review_control(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            context = Path(temp) / "selected.md"
            result = subprocess.run(
                ["node", "scripts/fxd-backlog.mjs", "select", "--context", str(context)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertFalse(context.exists())
        self.assertNotEqual(0, result.returncode)
        self.assertIn("automatic milestone selection is retired by Issue #66", result.stderr)

    def test_control_state_keeps_selector_retired_without_operator_protocol(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            scripts = root / "scripts"
            docs = root / "docs"
            scripts.mkdir()
            docs.mkdir()
            shutil.copy2(ROOT / "scripts" / "fxd-backlog.mjs", scripts / "fxd-backlog.mjs")
            (scripts / "validate_legacy_milestones.py").write_text(
                "raise SystemExit(0)\n", encoding="utf-8"
            )
            (docs / "CONTROL_STATE.json").write_text("{}\n", encoding="utf-8")
            (docs / "MILESTONE_STATE.json").write_text(
                json.dumps({
                    "product_lane": {"paused": False, "active_milestone": 32},
                    "milestones": [],
                }) + "\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                ["node", "scripts/fxd-backlog.mjs", "select"],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("automatic milestone selection is retired by Issue #66", result.stderr)

    def test_control_state_validator_pins_exact_historical_registry_path(self) -> None:
        validator = (ROOT / "scripts" / "validate_control_state.py").read_text(encoding="utf-8")
        self.assertIn('legacy.get("path") != "docs/MILESTONE_STATE.json"', validator)
        self.assertIn('(root / "docs/MILESTONE_STATE.json").read_bytes()', validator)

    def test_historical_validation_never_prints_m32_as_current_authority(self) -> None:
        result = subprocess.run(
            ["node", "scripts/fxd-backlog.mjs", "validate"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("immutable legacy FXD milestone records", result.stdout)
        self.assertIn("frozen historical projection only", result.stdout)
        self.assertNotIn("Active milestone 32", result.stdout)

    def test_operator_protocol_separates_builder_review_and_api_cost_boundary(self) -> None:
        protocol = (ROOT / "docs" / "OPERATOR_PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("Review-Control decides and reviews", protocol)
        self.assertIn("ChatGPT Codex Remote", protocol)
        self.assertIn("Claude Code", protocol)
        self.assertIn("Exactly one builder is selected for one active gate", protocol)
        self.assertIn("The unselected builder must not modify the active implementation branch", protocol)
        self.assertIn("It does not choose new scope, merge, advance, deploy, or approve its own work", protocol)
        self.assertIn("repository paid development dispatchers: forbidden", protocol)
        self.assertIn(
            "No coding-agent subscription session implicitly authorizes a product-runtime API call", protocol,
        )
        # Claude Code implementation authority never makes Anthropic a runtime/review path.
        claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("does not make Anthropic/Claude an FXD product-runtime provider", claude)


if __name__ == "__main__":
    unittest.main()
