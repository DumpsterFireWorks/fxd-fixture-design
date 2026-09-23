# Claude Code Instructions for FXD

GitHub is authoritative.

## Current selection

**Claude Code is the selected FXD implementation builder.**

**Owner-selected development model: Claude Opus 5.5.**

This is a development-model selection only. Do not invent an Anthropic API model identifier and do not switch to an API billing route to satisfy it.

Current expected gate:
- FXD-R0
- Issue #87
- PR #79
- branch `agent/m33-1-native-product-reconstruction`
- offline only

Before modifying anything, read current main:
1. `AGENTS.md`
2. `docs/CONTROL_STATE.json`
3. `CURRENT.md`
4. Issue #87
5. `docs/FXD_RECOVERY_GATE_00.md`
6. `docs/decisions/0002-fxd-recovery-reset.md`
7. `docs/FXD_REASSESSMENT_2026-09-22.md`
8. PR #79 exact head/comments/review
9. required tests/evidence

If current CONTROL_STATE does not select `claude_code`, do not modify the active branch.

## Development route

Use the user's subscription-backed Claude Code session on Claude Opus 5.5.

Do not intentionally use:
- `ANTHROPIC_API_KEY`;
- an Anthropic API development route;
- a paid GitHub/provider development dispatcher;
- any FXD product-runtime provider credential.

If the available execution route is not the selected subscription-backed Claude Code surface, stop `BLOCKED` rather than silently changing billing/auth routes.

FXD-R0 development API requests authorized: **0**.  
FXD-R0 product-runtime requests authorized: **0**.

## Scope

Implement exactly `docs/FXD_RECOVERY_GATE_00.md`.

For R0:
- preserve the reviewed F05/F06/F11 PR #79 behavior;
- synchronize current main non-destructively;
- repair the stale revision-4/M33.1 control validator/governance tests for current revision-8/FXD-R0 authority;
- run the full offline evidence;
- obtain native Windows visible-scene evidence;
- push one exact head;
- stop `AWAITING_REVIEW`.

Do not implement R1/R2/R3/R4 early.

## Permanent boundaries

- one active gate;
- one implementation PR;
- one selected builder;
- source CAD immutable;
- deterministic validation remains authoritative;
- no provider/API spending unless separately authorized;
- do not choose new scope;
- do not merge;
- do not advance;
- do not independently review/approve your own work;
- do not use Codex as a second implementation writer on the active branch.

Claude Code implementation authority does not make Anthropic/Claude an FXD product-runtime provider, independent review path, audit fallback, or tie-break route.

## Stop format

```text
AWAITING_REVIEW
Gate: FXD-R0 / Issue #87
PR: #79
Head: <full SHA>
CI: green | failing | running
Work: recovery baseline/control reconciliation + native scene evidence
Blocker: none | <one sentence>
```

or:

```text
BLOCKED
Gate: FXD-R0 / Issue #87
Reason: <one sentence>
```
