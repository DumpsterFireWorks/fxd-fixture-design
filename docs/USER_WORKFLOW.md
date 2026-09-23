# FXD User Workflow

## Product promise

The normal weld-fixture workflow should feel like:

```text
Import assembly
→ Set it down
→ Confirm welds + job summary
→ Generate fixture
→ Inspect / edit
→ Validate / export
```

The engineering engine may use datums, constraint rank, normals, frames, and typed contacts internally. The user should not need that vocabulary to operate FXD.

## Step 1 — Import assembly

FXD imports immutable STEP geometry and reconstructs the component/body/face evidence it can prove.

The user should not answer manufacturing-classification questions unless the unknown classification materially changes a fixture decision.

## Step 2 — Set it down

Primary normal interaction:

> **Select the face that sits down on the fixture.**

FXD may recommend a likely stable support face. The user can accept it or pick another.

A separate “front” face is optional unless operator access, table orientation, automation, or another real constraint requires it.

## Step 3 — Confirm welds and job summary

FXD finds candidate part-to-part joints/seams and highlights likely weld locations.

The user can:
- keep;
- reject;
- add.

Candidate or AI-suggested welds are never silently confirmed.

Show one consolidated job summary rather than a large engineering form. Prefer saved profiles for:
- welding/process family;
- manual/cobot/robot handling;
- shop capabilities;
- standard tooling;
- preferred construction methods;
- normal clearance preferences.

Ask only missing job facts that materially change the fixture.

## Step 4 — Generate fixture

FXD:
1. retrieves a small number of useful approved precedents;
2. provides the model with trustworthy product reconstruction, confirmed weld intent, critical requirements, and precedent substance;
3. receives a strict typed fixture strategy;
4. compiles that strategy through allowlisted deterministic commands into OCP geometry;
5. validates the authored result.

The model does not directly mutate CAD objects.

## Step 5 — Inspect and edit

The user sees actual fixture geometry, not only proposal prose.

Normal finishing actions should include supported:
- move;
- resize;
- replace;
- suppress/restore;
- holes/slots/reliefs/markings as later supported by the active scope;
- undo/redo;
- regenerate and revalidate.

## Step 6 — Validate and export

Show failures in shop language:
- “This support goes through the part.”
- “This piece can still move.”
- “This piece can still twist.”
- “The clamp is pushing without a solid reaction.”
- “The torch hits here.”
- “The finished assembly cannot come out this way.”
- “The design changed; check it again.”

Outputs must correspond to the same authored revision.

## Owner input budget

### Infer automatically
- source identity and component relationships;
- exact measurable geometry;
- stable planar/cylindrical feature evidence;
- duplicate volume category from quantity;
- previously saved shop/tooling profile;
- deterministic physical-check results.

### Suggest and confirm
- bottom/support face;
- likely weld seams;
- support/locator regions;
- clamp strategy;
- loading/removal sequence;
- base/construction approach;
- lifecycle when a saved preference exists.

### Ask only when genuinely required
- which ambiguous interfaces are actually welded;
- job-critical dimensions/tolerances absent from trusted records;
- unusual handling/loading restrictions;
- permission for a proposed product modification;
- private-data transmission;
- paid live-model execution.

### Remove from the normal path
- raw datum terminology as required vocabulary;
- raw loading/unloading vectors when FXD can propose and check a sequence;
- blanket “reviewed” checkboxes as proof;
- repeated questions already answered by a saved profile.

## First-family interaction target

For the representative supported case, target:

1. set/accept pose;
2. confirm weld map;
3. confirm one consolidated job/profile summary;
4. review the fixture.

This is a product target, not a claim that every future fixture requires exactly four interactions.
