# FXD Development Orchestration

The autonomous Foreman and paid GitHub Codex dispatcher are retired.

FXD uses:

> **Review-Control → one selected subscription builder → AWAITING_REVIEW → exact-head Review-Control**

## Current gate

FXD-R0 / Issue #87 / PR #79 / offline only.

Selected builder: **ChatGPT Codex Remote**.

Claude Code is an allowed future implementation surface only when current CONTROL_STATE and the active issue select it.

## No paid development route

GitHub Actions must not:
- invoke paid Codex/provider development orchestration;
- receive provider API keys for implementation;
- turn CONTINUE into API spending.

FXD product-runtime API use is separately governed and currently unauthorized.

## Entry points

Codex reads:
- `AGENTS.md`
- `docs/CONTROL_STATE.json`
- `CURRENT.md`
- Issue #87
- `docs/FXD_RECOVERY_GATE_00.md`

Claude Code reads the same plus `CLAUDE.md`, and may modify only when `selected_builder=claude_code`.

## Current known failure

Main's control validator still expects the old revision-4/unheld M33.1 state.

Issue #27 records the failure.

FXD-R0 repairs that validator/tests without weakening cost or fail-closed controls.
