# FXD Operator Protocol

## Purpose

Keep FXD moving without making Chris the message bus and without letting agents invent scope.

> **Review-Control decides and reviews. GitHub remembers. One selected builder implements one bounded gate.**

## Roles

### Review-Control

Owns:
- current GitHub inspection;
- product direction and scope inside owner-approved direction;
- gate definition;
- current-state maintenance;
- exact-head independent review;
- routine merge/next-gate activation when authorized evidence passes;
- owner escalation only for real owner decisions.

### Selected implementation builder

Current control may select:
- ChatGPT Codex Remote; or
- Claude Code.

Exactly one builder is selected for one active gate.

The selected builder:
- implements/repairs only that gate;
- works on the one implementation PR;
- runs required evidence;
- pushes an exact head;
- stops `AWAITING_REVIEW`.

It does not choose new scope, merge, advance, deploy, or approve its own work.

The unselected builder must not modify the active implementation branch.

### Product-runtime AI

Product-runtime AI is separate from project implementation.

It may author typed fixture strategy only when an active gate explicitly authorizes a runtime provider/model request.

No coding-agent subscription session implicitly authorizes a product-runtime API call.

## Cost boundary

Permanent:
- development API requests: 0 unless a future owner-approved decision explicitly changes the architecture;
- repository paid development dispatchers: forbidden;
- provider API keys do not enter GitHub development automation;
- product-runtime calls require explicit provider/model/data/budget authorization;
- automatic retries are not invented.

## Current gate — FXD-R0

Issue #87 / PR #79 / offline only.

Read `docs/FXD_RECOVERY_GATE_00.md`.

The September 12 portfolio hold is lifted for this bounded gate. Live product-runtime authorization remains false.

R0 preserves accepted PR #79 R1 work, synchronizes current main, repairs control validator/test drift, proves offline/native behavior, and leaves the foundation merge-ready.

## Normal loop

```text
Review-Control → CONTINUE
Selected builder → AWAITING_REVIEW
Review-Control → CONTINUE | OWNER_DECISION | BLOCKED | COMPLETE
```

## What CONTINUE means

The selected builder must read current main authority before branch-local copies.

Then:

1. confirm current active gate/PR/selected builder;
2. stop if another builder is selected;
3. repair unresolved blocking findings inside scope;
4. repair required CI inside scope;
5. otherwise implement the smallest complete active-gate slice;
6. run required evidence;
7. push exact head;
8. stop AWAITING_REVIEW.

CONTINUE never authorizes:
- another gate;
- another implementation PR;
- backlog hunting;
- paid product-runtime calls;
- weakened validation;
- production release;
- destructive history rewriting.

## Exact-head review

Review-Control checks:
1. current authority;
2. scope;
3. actual diff;
4. deterministic evidence;
5. runtime/native evidence at the layer where it can fail;
6. cost/privacy/licensing/security;
7. product outcome;
8. human practicality boundary.

Any new commit invalidates prior exact-head acceptance.

## Merge and advancement

Review-Control may merge only when:
- exact head is unchanged;
- required evidence passes;
- no blocking finding remains;
- no owner-only boundary is crossed;
- current state can advance coherently.

No next gate starts automatically.
