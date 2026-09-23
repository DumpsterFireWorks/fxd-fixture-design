# FXD Agent Instructions

## Mission

Build FXD into practical intelligent fixture-design software.

The normal user promise is:

> **Import the assembly → set it down → confirm welds and genuinely unknown job requirements → FXD designs a practical fixture → inspect/edit → validate/export.**

The user should not need academic fixture-engineering vocabulary to operate the product.

## Authority order

1. Explicit current owner instruction
2. `docs/CONTROL_STATE.json`
3. `CURRENT.md`
4. active GitHub issue
5. `docs/decisions/0002-fxd-recovery-reset.md`
6. `docs/PRODUCT_DIRECTION.md`
7. `docs/USER_WORKFLOW.md`
8. `docs/ARCHITECTURE_CURRENT.md`
9. `docs/OPERATOR_PROTOCOL.md`
10. `docs/ENGINEERING_CONSTITUTION.md`
11. `docs/AI_DRIVEN_SYNTHESIS_ARCHITECTURE.md`
12. active PR, exact review findings, and CI
13. recovery roadmap and historical evidence

Lower authority cannot silently override higher authority.

Historical M32/M33 milestone documents and superseded issues are evidence/salvage, not current work selectors.

## Operating model

> **Review-Control decides and independently reviews. GitHub remembers. One selected subscription builder implements one bounded gate.**

- One repository.
- One active gate.
- One implementation PR.
- Exactly one implementation builder per gate.
- Allowed builder surfaces: ChatGPT Codex Remote or Claude Code.
- Current selected builder is recorded in CONTROL_STATE and the active issue.
- Owner default for FXD implementation is Claude Code unless a later explicit decision selects another allowed builder.
- The unselected builder must not modify the active branch.
- The builder stops `AWAITING_REVIEW`.
- Review-Control checks the exact pushed head and decides merge/next action.
- A builder cannot approve its own work.

Claude Code implementation authority never makes Claude/Anthropic an FXD product-runtime provider, independent reviewer, audit fallback, or tie-break path.

## Current gate

- **FXD-R0**
- **Issue #87**
- **PR #79**
- **Branch:** `agent/m33-1-native-product-reconstruction`
- **Selected builder:** Claude Code
- **Development model:** Claude Opus 5.5
- **Mode:** OFFLINE ONLY
- **Work order:** `docs/FXD_RECOVERY_GATE_00.md`

Preserve previously reviewed PR #79 R1 behavior. Do not redo F05/F06/F11 without a reproduced regression.

## Permanent cost/API boundary

- development API requests: 0;
- paid repository development dispatchers: forbidden;
- GitHub Actions must not receive provider API keys for development;
- product-runtime provider calls require separate explicit gate authorization;
- an ordinary `CONTINUE`, test request, or builder session never authorizes product-runtime spending.

FXD-R0 authorizes **zero** product-runtime calls and may not read provider credentials.

## Product rules

### User questions are expensive

Ask only when missing information cannot be safely inferred/proposed and materially changes fixture strategy or release evidence.

Prefer:
- infer;
- recommend;
- batch confirm;
- use saved profiles.

### AI authors strategy, not prose after a template

In AI Design mode, an accepted typed strategy must drive downstream fixture geometry.

Changing a supported strategy support/locator/clamp/base decision must change corresponding authored geometry.

### Deterministic systems own truth

OCP and deterministic logic own executable geometry, units, identities, contacts, collision, restraint, access/removal, persistence, and output gates.

AI cannot override a deterministic failure.

### Weld guesses are not manufacturing truth

Keep candidate/suggested/confirmed/rejected weld intent distinct.

### Precedent must carry substance

Useful precedent is feature/intent → response → reason → parameters/constraints → sequence/access → failure/correction history.

### Human practicality remains final

A fixture that passes software but requires fundamental support/locating/clamping/loading redesign fails the product proof.

## Current builder stop format

```text
AWAITING_REVIEW
Gate: FXD-R0 / Issue #87
PR: #79
Head: <full SHA>
CI: green | failing | running
Work: <one sentence>
Blocker: none | <one sentence>
```

or:

```text
BLOCKED
Gate: FXD-R0 / Issue #87
Reason: <one sentence>
```
