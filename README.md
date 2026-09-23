# FXD — Intelligent Industrial Fixture Design

FXD is practical AI-assisted industrial fixture-design software.

## Product promise

> **Import the assembly → set it down → confirm welds and genuinely unknown job requirements → FXD designs a practical fixture → inspect/edit → validate/export.**

FXD begins with weld fixtures for fabricated assemblies. It is not trying to replace general-purpose CAD.

## Current state

**FXD-R0 — OFFLINE RECOVERY BASELINE — Issue #87 / PR #79**

Owner direction on September 23, 2026 resumed bounded offline development using the recovery direction in:

- [Independent reassessment](docs/FXD_REASSESSMENT_2026-09-22.md)
- [Decision 0002](docs/decisions/0002-fxd-recovery-reset.md)
- [User workflow](docs/USER_WORKFLOW.md)
- [Current architecture](docs/ARCHITECTURE_CURRENT.md)
- [Recovery roadmap](docs/FXD_RECOVERY_ROADMAP.md)

Current machine authority is [docs/CONTROL_STATE.json](docs/CONTROL_STATE.json).

## Current work

PR #79 contains previously reviewed foundation repairs that must be preserved.

FXD-R0 does not add new fixture behavior. It:
- synchronizes current main into PR #79;
- repairs stale control-state validator/tests;
- refreshes offline CI/OCP/persistence/cost evidence;
- proves native Windows source + derived/review geometry are visibly rendered;
- leaves PR #79 merge-ready after independent review.

Product-runtime requests authorized now: **0**.

## Architecture

Target:

```text
assembly geometry
+ confirmed manufacturing intent
+ useful fixture precedents
        ↓
typed AI fixture strategy
        ↓
restricted deterministic compiler
        ↓
real OCP fixture geometry
        ↓
deterministic physical validation
        ↓
human practicality review
```

AI owns strategy in AI Design mode. Deterministic systems own geometry and engineering truth. Human engineering judgment owns practical acceptance and production authority.

## Recovery order

- R0 — clean baseline and preserved foundation
- R1 — simple pose/job/weld intent
- R2 — physical truth
- R3 — AI strategy drives CAD + first meaningful bounded live strategy proof
- R4 — one practical fixture + native finishing

Only R0 is active.

## Builders

FXD can use ChatGPT Codex Remote or Claude Code as subscription-backed implementation surfaces, but exactly one is selected per active gate.

Current selected builder: **ChatGPT Codex Remote**.

See [AGENTS.md](AGENTS.md) and [CLAUDE.md](CLAUDE.md).

## Health

Repository health command:

```text
bash scripts/ci.sh
```

Current main is known to fail the stale control-state validator recorded in Issue #27. Repairing that mismatch is intentionally part of FXD-R0.

Passing software checks does not prove fixture practicality.

## Rights

No open-source license is granted. Copyright © 2026 Christopher Hilton. All rights reserved. See `NOTICE.md`.
