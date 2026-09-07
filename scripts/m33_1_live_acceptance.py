"""Opt-in exactly-one-request M33.1 OpenAI acceptance proof.

The script prints only bounded provenance.  It never prints credentials,
prompt content, unrestricted provider output, or source STEP bytes.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fxd_geometry import (  # noqa: E402
    ExecutionMode, OpenAiResponsesProvider, ProviderState, execute_design_mode,
)
from scripts.m33_1_self_check import synthetic_workflow  # noqa: E402


EXPECTED_REPOSITORY = "DumpsterFireWorks/fxd-fixture-design"
EXPECTED_REPOSITORY_ID = 1299678045
ACCEPTED_REPOSITORY_NAMES = (EXPECTED_REPOSITORY, "kool1160/fxd-fixture-design")
EXPECTED_BRANCH = "agent/m33-1-native-product-reconstruction"


def _git(*arguments: str) -> str:
    return subprocess.check_output(
        ("git", *arguments), cwd=ROOT, text=True, stderr=subprocess.DEVNULL,
    ).strip()


def _refuse(reason: str) -> int:
    print(json.dumps({
        "schema": "fxd-m33-1-live-acceptance-v1",
        "status": "refused",
        "reason": reason,
    }, sort_keys=True))
    return 2


def repository_preflight() -> tuple[str, str]:
    """Read Git/GitHub identity only; independently testable without runtime opt-in."""
    remote = _git("remote", "get-url", "origin")
    accepted_urls = {
        prefix + name + suffix
        for name in ACCEPTED_REPOSITORY_NAMES
        for prefix in ("https://github.com/", "git@github.com:", "ssh://git@github.com/")
        for suffix in ("", ".git")
    }
    if remote.rstrip("/") not in accepted_urls:
        raise ValueError("repository identity does not match the M33.1 work order")
    metadata = json.loads(subprocess.check_output(
        ("gh", "api", "repos/" + EXPECTED_REPOSITORY,
         "--jq", "{id: .id, full_name: .full_name}"),
        cwd=ROOT, text=True, stderr=subprocess.DEVNULL,
    ))
    # Resolve the supplied alias too: an accepted spelling alone is not identity.
    supplied = next(name for name in ACCEPTED_REPOSITORY_NAMES if name in remote)
    if supplied != EXPECTED_REPOSITORY:
        alias = json.loads(subprocess.check_output(
            ("gh", "api", "repos/" + supplied,
             "--jq", "{id: .id, full_name: .full_name}"),
            cwd=ROOT, text=True, stderr=subprocess.DEVNULL,
        ))
        if alias != metadata:
            raise ValueError("former repository alias no longer resolves to the canonical identity")
    if metadata != {"id": EXPECTED_REPOSITORY_ID, "full_name": EXPECTED_REPOSITORY}:
        raise ValueError("canonical GitHub repository identity does not match")
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    if branch != EXPECTED_BRANCH:
        raise ValueError("branch does not match the sole M33.1 implementation branch")
    if _git("status", "--porcelain"):
        raise ValueError("worktree must be clean so evidence binds to one exact head")
    return branch, head


def main() -> int:
    if os.environ.get("FXD_M33_1_LIVE_ACCEPTANCE") != "1":
        return _refuse("explicit opt-in is required")
    try:
        branch, head = repository_preflight()
    except (OSError, subprocess.CalledProcessError):
        return _refuse("expected Git repository is unavailable")
    except (ValueError, TypeError):
        return _refuse("repository, branch or clean-head identity preflight failed")
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    model = os.environ.get("FXD_OPENAI_MODEL", "").strip()
    if not api_key or not model:
        return _refuse("explicit OpenAI key and model configuration are required")

    source, document, workflow = synthetic_workflow()
    provider = OpenAiResponsesProvider(api_key, model)
    outcome = execute_design_mode(
        document, workflow, ExecutionMode.AI_DESIGN_LIVE,
        provider=provider, timeout_seconds=60.0,
    )
    evidence = outcome.provenance.to_dict()
    safe = {
        "schema": "fxd-m33-1-live-acceptance-v1",
        "repository": EXPECTED_REPOSITORY,
        "branch": branch,
        "head": head,
        "source_sha256": document.source_sha256,
        "source_unchanged": document.source_bytes == source,
        "reconstruction_identity": evidence["reconstruction_identity"],
        "mode": evidence["mode"],
        "provider_identity": evidence["provider_identity"],
        "model_identity": evidence["model_identity"],
        "request_attempted": evidence["request_attempted"],
        "request_count": evidence["request_count"],
        "request_status": evidence["request_status"],
        "failure_category": evidence["failure_category"],
        "fallback_used": evidence["fallback_used"],
        "automatic_retries": evidence["automatic_retries"],
        "timeout_seconds": evidence["timeout_seconds"],
        "prompt_contract_version": evidence["prompt_contract_version"],
        "response_contract_version": evidence["response_contract_version"],
        "result_identity": evidence["result_identity"],
        "usage_status": evidence["usage_status"],
        "input_tokens": evidence["input_tokens"],
        "output_tokens": evidence["output_tokens"],
        "total_tokens": evidence["total_tokens"],
        "cost_usd": evidence["cost_usd"],
    }
    print(json.dumps(safe, sort_keys=True))
    if outcome.provider_state != ProviderState.SUCCESS:
        return 1
    if provider.request_count != 1 or evidence["request_count"] != 1:
        return 1
    if evidence["fallback_used"] or evidence["automatic_retries"] != 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
