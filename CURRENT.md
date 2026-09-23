# FXD Current Control State

## State

**FXD-R0 — RECOVERY BASELINE — OFFLINE ONLY — ISSUE #87 / PR #79**

Owner direction on September 23, 2026 resumes bounded FXD development under the practical-recovery reset.

The September 12 portfolio hold is lifted for this bounded offline gate. Product-runtime AI remains separately unauthorized.

Authoritative machine state: [docs/CONTROL_STATE.json](docs/CONTROL_STATE.json), revision 7.

## Why the direction changed

Read [the independent reassessment](docs/FXD_REASSESSMENT_2026-09-22.md) and [Decision 0002](docs/decisions/0002-fxd-recovery-reset.md).

FXD keeps the existing OCP/STEP/VTK/persistence foundation, but recovery is now organized around the actual product:

> **Import → set it down → confirm welds/job → get a practical fixture → inspect/edit → validate/export.**

The previous execution sequence asked too much from Chris, generated deterministic fixture concepts before AI, failed to pass enough useful reconstruction/precedent substance to the model, and lacked enough physical validation to prove practicality.

## Active assignment

- **Gate:** FXD-R0 — Recovery baseline and preserved R1 integration
- **Issue:** #87
- **Implementation PR:** #79 — existing draft, preserved
- **Branch:** `agent/m33-1-native-product-reconstruction`
- **Selected builder:** Claude Code
- **Work order:** [docs/FXD_RECOVERY_GATE_00.md](docs/FXD_RECOVERY_GATE_00.md)
- **Product-runtime requests:** 0
- **Development API requests:** 0

PR #79's previously reviewed R1 work at `de26501958045b5f1dd80eb40ce8f8f1f8d9cf5f` must be preserved:
- F05 classification decisions;
- F06 legacy proposal-bearing migration/history;
- F11 repository/cost preflight integration.

## FXD-R0 task

The builder must:

1. synchronize current main into PR #79 without losing reviewed R1 behavior;
2. repair the stale control validator/governance tests that still hard-code revision-4 history;
3. run focused and full offline CI, cost/firewall, OCP, persistence, and static evidence;
4. obtain native Windows visible-scene proof showing source and review/derived geometry;
5. stop `AWAITING_REVIEW`.

No live provider request, strategy compiler, weld-candidate UI, physical-validation repair, precedent migration, new dependency, or new product scope belongs in FXD-R0.

## Builder policy

FXD may use Codex or Claude Code as a subscription-backed implementation surface, but exactly one builder is selected per active gate.

Current selected builder: **Claude Code**.

Owner direction on September 23 selects Claude Code as the default FXD implementation builder. Codex remains an allowed fallback only when current GitHub authority explicitly selects it.

Claude Code is ready through `CLAUDE.md` but must not modify PR #79 unless Review-Control explicitly changes the selected builder in current GitHub authority.

The builder never independently approves its own work.

## Live-model sequencing

The explicit live/offline modes and fail-closed provider boundary remain protected.

The old requirement to spend Profile E before strategy could drive geometry is superseded.

The first meaningful live strategy proof is planned for **FXD-R3**, after:
- the simplified intent workflow exists;
- the physical judge can reject bad fixtures;
- manual and synthetic strategies demonstrably drive OCP geometry.

That later live request still requires separate authorization.

## Recovery roadmap

See [docs/FXD_RECOVERY_ROADMAP.md](docs/FXD_RECOVERY_ROADMAP.md):

- **R0:** clean recovery baseline and merge preserved foundation
- **R1:** simple pose/job/weld intent
- **R2:** physical truth
- **R3:** AI strategy actually drives CAD + first meaningful live proof
- **R4:** one practical fixture and native finishing

Only R0 is active.

## Next valid action

**CONTINUE**

Claude Code reads Issue #87, `CLAUDE.md`, and [the R0 work order](docs/FXD_RECOVERY_GATE_00.md), works only PR #79, uses subscription-backed development with zero product-runtime/API requests, and stops `AWAITING_REVIEW`.
