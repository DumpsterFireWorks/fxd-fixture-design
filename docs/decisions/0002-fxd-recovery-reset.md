# Decision 0002 — FXD Practical Recovery Reset

- **Status:** Owner-approved direction for recovery
- **Date:** 2026-09-23
- **Authority:** Chris Hilton
- **Active recovery issue:** #87
- **Evidence basis:** `docs/FXD_REASSESSMENT_2026-09-22.md`
- **Preserved implementation:** PR #79

## Decision

FXD keeps its existing CAD/OCP/VTK/persistence foundation and changes the product-development sequence around one user promise:

> **Import the assembly → set it down → confirm welds and genuinely unknown job requirements → FXD designs a practical fixture → inspect/edit → validate/export.**

Internal engineering rigor remains. The normal user interface must not require Chris to translate shop-floor reasoning into academic fixture terminology.

## What this supersedes

This decision supersedes the old requirement that M33.1 must consume a live provider request before FXD has a strategy contract that can actually drive fixture geometry.

The explicit live/offline execution modes, fail-closed provider behavior, provenance, request budgets, and cost controls remain valuable and must be preserved.

**Profile E moves to the first recovery gate where a typed AI fixture strategy demonstrably controls OCP geometry.** A paid transport-only call before that point is not product acceptance.

M33/M32 history remains evidence. Issue #85 plus this decision define the recovery sequence.

## Product architecture

The accepted target remains:

```text
assembly geometry
+ confirmed manufacturing intent
+ useful fixture precedents
        ↓
typed AI fixture strategy
        ↓
restricted deterministic compiler
        ↓
real editable OCP fixture geometry
        ↓
deterministic physical validation
        ↓
human practicality review
```

AI owns strategy in AI Design mode. Deterministic systems own executable geometry and truth. Human engineering judgment owns practical acceptance and production authority.

## User-input rule

FXD asks a user question only when the answer:

1. cannot be reliably inferred from geometry, saved shop/job context, or deterministic checks; and
2. materially changes the fixture strategy or release evidence.

Otherwise FXD should infer, propose, batch-confirm, or hide the internal concept.

The normal UI should use shop language such as:
- “Which face sits on the fixture?”
- “These look like the welds. Keep/remove/add.”
- “This piece can still move.”
- “The torch hits here.”
- “The finished assembly cannot come out this way.”

## Weld-intent rule

Geometry-derived or AI-suggested welds are candidates only.

FXD must preserve a distinction between:
- candidate weld/joint evidence;
- AI-suggested weld intent;
- user-confirmed weld intent;
- user-rejected candidate intent.

Unconfirmed guesses never become manufacturing truth.

## Precedent rule

Retrieval must provide useful engineering substance, not only precedent IDs and ranking scores.

For the first supported family, a precedent should communicate:

```text
product feature / intent
→ fixture response
→ reason
→ parameters / constraints
→ access / load / release sequence
→ known failure / correction history
```

A mass fixture-library migration, training project, or universal rule system is not a prerequisite for the first useful fixture.

## Physical-truth rule

Before a live AI fixture result can be accepted, deterministic checks for the supported case must establish the physical conditions they claim, including:
- fixture/product interference;
- permitted touching versus penetration;
- physical contact validity;
- restraint of relevant loose bodies at the relevant operation stage;
- clamp reaction/support relationships;
- weld/torch access within the supported envelope model;
- loading and removal within the supported trajectory model;
- output coherence.

Mathematical rank, metadata labels, booleans, or prose alone do not prove those physical conditions.

## Builder policy

Review-Control owns product direction, scope, sequencing, and independent exact-head review.

A bounded gate may select either:
- **ChatGPT Codex Remote**, or
- **Claude Code**

as its implementation surface.

Exactly one builder is selected per active gate. The unselected builder must not modify the active branch. A builder cannot independently review or approve its own work.

Owner direction on September 23, 2026 sets **Claude Code as the default FXD implementation builder** and **Claude Opus 5.5 as the default development model** unless a later explicit owner/Review-Control decision changes the selected builder/model. This is development configuration only; it does not select Anthropic as an FXD product-runtime provider or authorize an Anthropic API route.

Claude/Anthropic is not an FXD product-runtime provider, independent review path, fallback, or tie-break route merely because Claude Code may be selected to implement a gate.

## Cost boundary

Development-agent subscription usage and FXD product-runtime API usage are different things.

- development API requests: 0 unless an owner-approved architecture explicitly changes this;
- repository paid development dispatchers: forbidden;
- product-runtime provider requests require separate gate authorization;
- unrelated legitimate APIs outside FXD are unaffected.

## Recovery order

1. **FXD-R0:** coherent baseline; preserve R1; fix control validation; native offline scene proof; merge the old foundation.
2. **FXD-R1:** simplified pose/job/weld-intent workflow.
3. **FXD-R2:** physical validation for the representative fixture family.
4. **FXD-R3:** precedent substance + typed strategy → actual OCP geometry; first meaningful bounded live strategy proof.
5. **FXD-R4:** one practical fixture, variations, native finishing, persistence, coherent outputs, Chris acceptance.

No later gate starts automatically.

## Acceptance standard

The product proof is not “all software checks pass.”

It is:

> **Would Chris actually build and use this fixture with only ordinary finishing edits?**

If Chris must replace the fundamental support, locating, clamping, or loading strategy, the proof failed.
