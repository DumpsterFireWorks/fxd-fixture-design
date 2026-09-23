# FXD Current Architecture — Recovery Baseline

This document describes what the inspected code does at the September 22/23, 2026 recovery baseline. It is not the target architecture.

## Valuable current foundation

FXD already has:
- real OCP STEP import and exact geometry evidence;
- immutable source bytes/SHA identity;
- PySide/VTK desktop foundation;
- product/project persistence and revisions;
- product reconstruction and explicit classification decisions;
- explicit offline/live execution modes and provider provenance;
- fixture primitives/builders and manufacturing outputs;
- locating mathematics;
- access/weld-rule proof layers;
- tests and cost/API firewalls.

PR #79 contains accepted bounded repairs for classification persistence, legacy proposal migration, and repository/cost integration. Preserve them.

## Current design path

Broadly:

```text
STEP
→ orientation/process/annotations
→ deterministic placement + fixture concepts
→ reconstruction/checks
→ AI request containing existing candidates
→ AI recommendations/proposal
→ separate deterministic build generation
→ authored solids/outputs
```

This is not yet the desired synthesis path.

## Current user-input problem

The desktop exposes a large process form plus orientation, classification, annotation, tooling, proposal, manufacturing, and editing surfaces.

The proposal path also requires multiple “minimum intent” values, including explicit loading/unloading vectors.

The recovery direction moves many of these from mandatory user inputs to inference, saved profiles, or proposed choices.

## Current weld-intent problem

Confirmed weld annotations can be persisted, but the reconstructed weld-candidate collection is not yet a useful automatic candidate-weld workflow.

A future supported path must distinguish candidate, suggested, confirmed, and rejected weld intent.

## Current model-context problem

The current request carries useful IDs, bounds, annotations, setup information, tooling metadata, existing placements, deterministic findings, and already-generated fixture candidates.

It does not yet make the richer product reconstruction and useful precedent engineering substance the core strategy context.

## Current precedent problem

There are multiple knowledge layers:
- local correction records;
- superseded PR #54 structured public precedent retrieval;
- broader research-only library schemas/data.

The old precedent path could select relevant records, but the compact context exposed mostly retrieval metadata rather than all of the useful strategy substance stored in those records.

The recovery path should start with a small useful precedent adapter, not a mass library rewrite.

## Current authoring problem

The AI proposal is not yet a complete typed construction strategy that controls the fixture build.

Some existing build geometry is derived through fixed product-bound offsets and deterministic templates.

Recovery must prove that changing an allowed strategy decision changes the corresponding authored OCP geometry.

## Current physical-validation gaps

The recovery audit identified these important boundaries:
- interface labels do not by themselves prove penetration is legal;
- locating rank does not prove a contact point is physically on the referenced surface;
- a global rank result does not prove all loose members are restrained at the correct stage;
- normal access validation does not yet prove a continuous weld approach/removal path;
- declared manufacturing relationships can exceed what an authoring path actually creates.

These are bounded repair targets, not justification for replacing OCP or the whole CAD foundation.

## Current governance state

The September 12 hold is superseded by the September 23 owner recovery authorization once CONTROL_STATE revision 6 lands.

Issue #87 is the first bounded recovery gate.

PR #79 remains the sole implementation PR for FXD-R0 so accepted R1 work is not discarded.

The current main control validator is known to be stale and is intentionally the first code/test repair in FXD-R0.
