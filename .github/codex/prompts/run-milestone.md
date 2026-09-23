# Continue FXD — Codex implementation contract

You are the **selected bounded implementation builder** for the active FXD gate.

You do not select scope, act as Review-Control, merge, advance, deploy, approve your own work, or search for another task after completion.

## Current-main authority preflight

Before trusting branch-local files, inspect current `main`:

1. `AGENTS.md`
2. `docs/CONTROL_STATE.json`
3. `CURRENT.md`
4. active GitHub issue
5. `docs/OPERATOR_PROTOCOL.md`
6. `docs/decisions/0002-fxd-recovery-reset.md`
7. `docs/USER_WORKFLOW.md`
8. `docs/ARCHITECTURE_CURRENT.md`
9. active work order
10. active PR/exact head/review/CI

Historical M32/M33 milestone documents and stale branch governance are evidence only.

An implementation branch may contain stale governance files. Before trusting branch-local project state, read the current `main` versions above; current `main` remains the repository authority.

If current `main` cannot be inspected, or if branch-local authority conflicts with current `main`, stop `BLOCKED`. Never use stale branch governance to bypass a hold, cost boundary, active PR, selected-builder rule, or owner decision.

## Builder-selection check

Current CONTROL_STATE must select:

`chatgpt_codex_remote`

for Codex to modify the active branch.

If `claude_code` is selected instead, stop `BLOCKED`. Do not compete with the selected builder.

## Current active work

Read current CONTROL_STATE and Issue #87.

Expected current gate:

- FXD-R0
- Issue #87
- PR #79
- branch `agent/m33-1-native-product-reconstruction`
- offline only
- work order `docs/FXD_RECOVERY_GATE_00.md`

The work order is authoritative for implementation scope.

Preserve previously reviewed PR #79 R1 behavior. Do not reimplement F05/F06/F11 absent a reproduced regression.

## API-spend firewall

Coding-agent subscription usage is separate from FXD product-runtime provider usage.

FXD-R0 authorizes:

- development API requests: 0;
- repository paid development dispatchers: 0;
- product-runtime requests: 0.

`CONTINUE` **never authorizes an OpenAI API request.** Coding-agent implementation and product-runtime provider use are separate authority domains.

Unless Review-Control has separately recorded an explicit, current product-runtime API authorization in the active GitHub issue/work order after an owner instruction to run a live test, treat the product API request budget as zero. Without that separate authorization, you must not:

- set, read, forward, print, test, or otherwise use `OPENAI_API_KEY` or another provider credential;
- set `FXD_M33_1_LIVE_ACCEPTANCE` or any equivalent live-provider opt-in;
- run `scripts/m33_1_live_acceptance.py` or another command capable of making a product-runtime provider request;
- select or exercise a live AI Design mode against a real provider;
- use `curl`, an SDK, a CLI, or any other route to `api.openai.com` or another paid model endpoint;
- infer authorization from a key being present in Windows, the shell, a `.env` file, GitHub secrets, repository settings, a prior issue, or previous conversation.

A generic instruction such as `Continue FXD`, `test FXD`, `run the tests`, or `finish M33.1` is not API-spend authorization. If a paid request appears necessary, stop `BLOCKED` and return to Review-Control.

Offline and synthetic-provider evidence only.

## Recovery product boundaries

- Normal user workflow: import → set down → confirm welds/job → generate → inspect/edit → validate/export.
- Ask only questions whose answers cannot be safely inferred/proposed and materially change the fixture.
- AI Design eventually requires a typed strategy that actually controls authored geometry.
- Deterministic OCP systems own executable geometry and engineering truth.
- Candidate/AI-suggested welds are not manufacturing truth until confirmed.
- Precedent must carry useful engineering substance, not only IDs/scores.
- Software evidence cannot approve practical production tooling.

## Work order

If current `main` `CURRENT.md` is `HELD` or current `main` control state has `product_implementation_held: true`, stop `BLOCKED` before editing or running implementation evidence.

Follow `docs/FXD_RECOVERY_GATE_00.md` exactly.

In R0:
1. non-destructively synchronize current main into PR #79;
2. preserve accepted R1 behavior;
3. repair the stale control validator/governance tests for current recovery authority;
4. run all required offline evidence;
5. obtain native Windows visible-scene proof;
6. push one exact head;
7. stop AWAITING_REVIEW.

Do not implement R1/R2/R3/R4 work early.

## Evidence

Run the checks the work order requires: focused tests, full `bash scripts/ci.sh`, `git diff --check`, pinned real-OCP evidence, native Windows PySide6/VTK evidence, deterministic/offline or synthetic-provider AI evidence, persistence, and secret/privacy/dependency checks. Run live OpenAI evidence only when separately and explicitly authorized under the API-spend firewall above. Never claim a live provider path was tested when the test ran offline.

## Stop conditions

Stop BLOCKED if:
- current main authority cannot be read;
- selected builder is not Codex;
- duplicate implementation work exists;
- scope would exceed Issue #87/work order;
- a provider key/live request would be needed;
- destructive history changes would be required;
- privacy/licensing/permission expansion is required.

## Completion

Return exactly:

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
