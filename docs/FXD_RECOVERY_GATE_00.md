# FXD-R0 Work Order — Recovery Baseline

Active issue: #87  
Implementation PR: #79  
Branch: `agent/m33-1-native-product-reconstruction`  
Selected builder: Claude Code  
Development model: Claude Opus 5.5  
Mode: OFFLINE ONLY  
Product-runtime requests authorized: 0

## Builder/auth boundary

Use Claude Code through the user's Claude subscription, with the owner-selected **Claude Opus 5.5** development model. Do not intentionally route FXD development through an Anthropic API key or any paid API development dispatcher. The model label is development configuration only; do not invent or require an Anthropic API model ID. Product-runtime provider requests remain zero. If the available Claude session cannot be verified as the selected subscription-backed implementation surface, stop `BLOCKED` rather than silently switching routes.

Codex is not the active implementation builder for this gate and must not modify PR #79 while `selected_builder=claude_code`.

## Read first

1. current main `AGENTS.md`
2. `docs/CONTROL_STATE.json`
3. `CURRENT.md`
4. Issue #87
5. `docs/decisions/0002-fxd-recovery-reset.md`
6. `docs/FXD_REASSESSMENT_2026-09-22.md`
7. `docs/USER_WORKFLOW.md`
8. `docs/ARCHITECTURE_CURRENT.md`
9. this work order
10. PR #79 exact head/comments/review
11. prior R1 evidence

## Objective

Produce one exact PR #79 head that:
- preserves all previously accepted R1 behavior;
- contains current main recovery authority;
- makes the repository control validator/tests agree with current authority without weakening cost safeguards;
- passes full offline CI;
- proves native Windows source + review/derived geometry are visibly rendered.

## Required steps

### 1. Synchronize current main

Integrate current main into the existing PR #79 branch non-destructively.

Preserve:
- F05 classification-decision repair;
- F06 migration/history repair;
- F11 repository/cost preflight repair;
- explicit offline/live mode provenance;
- retired paid dispatcher and API firewall.

Do not force-push reviewed history away.

### 2. Repair current-state validation

The known failure is Issue #27: `scripts/validate_control_state.py` still hard-codes revision-4/unheld/M33.1-R1 assumptions.

Update the validator and governance tests to validate the **meaning** of current recovery authority:
- revision 8/current schema;
- `product_implementation_held=false`;
- active issue #87 / gate FXD-R0 / PR #79;
- selected builder matches current control;
- allowed builder surfaces remain bounded;
- product-runtime authorization is false / zero requests;
- development API requests remain zero;
- paid repository development dispatcher remains forbidden;
- stale/conflicting/held states still fail closed;
- historical registry remains historical.

Do not “fix” CI by deleting safeguards or making the validator accept arbitrary states.

### 3. Refresh offline evidence

Run:
- focused governance/control tests;
- F05/F06 regression coverage;
- API/cost firewall tests;
- pinned OCP proof;
- full `bash scripts/ci.sh`;
- compile/static checks required by the repo;
- `git diff --check`.

No real provider calls.

### 4. Native Windows visible-scene proof

On the exact head, prove:
- native PySide/VTK/OCP path;
- source assembly visibly renders;
- review/derived fixture geometry visibly renders;
- controls needed for the preserved M33.1 foundation can be operated;
- save/reopen still works;
- offline/live banners remain truthful.

A black VTK capture is not sufficient visual evidence.

This is visual/software evidence only; it is not fixture-practicality acceptance.

## Out of scope

Do not implement:
- simplified workflow;
- weld candidates;
- physical-validation repairs;
- fixture strategy schema/compiler;
- precedent migration;
- live provider proof;
- M33.2;
- new dependencies.

## Stop

Push one exact head to PR #79 and stop:

```text
AWAITING_REVIEW
Gate: FXD-R0 / Issue #87
PR: #79
Head: <full SHA>
CI: green | failing | running
Work: recovery baseline/control reconciliation + native scene evidence
Blocker: none | <one sentence>
```

Builder confidence is not acceptance. Review-Control decides merge/readiness.
