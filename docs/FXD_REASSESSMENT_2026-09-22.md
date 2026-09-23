# FXD — Independent Repository Reconstruction and Product Reset

Assessment date: September 22, 2026  
Disposition: Read-only reassessment. Implementation remains held.  
Repository: DumpsterFireWorks/fxd-fixture-design

## Executive conclusion

FXD is worth recovering. The CAD foundation does not need to be thrown away.

The central problem is that the product promise is not connected end to end:

1. FXD asks Chris for too much of the fixture-planning work.
2. FXD computes useful product/reconstruction information but does not deliver enough of that information to the model.
3. The AI proposal path does not yet own a complete fixture strategy that deterministically drives the authored fixture geometry.
4. Physical validation does not yet establish all of the real conditions needed to trust a weld fixture: actual contact, per-member restraint, interference, weld access, clamp state, loading, and removal.

The product should feel like:

> Import the assembly → set it down → confirm the welds and genuinely unknown job requirements → get a practical fixture → inspect/edit it → validate/export it.

The user should not need to understand datum hierarchies, constraint rank, contact normals, reference frames, or similar internal engineering terminology to operate FXD successfully.

## Verified repository snapshot

- Main inspected at 5810248a68229931a56d2f6ec4f8247e635ab75b.
- Current control revision is 5.
- product_implementation_held remains true.
- PR #79 remains open, draft, and unmerged.
- PR #79 preserved head is de26501958045b5f1dd80eb40ce8f8f1f8d9cf5f.
- R1 repairs for F05/F06/F11 previously passed bounded offline independent review.
- Full M33.1 is not accepted.
- Native visible-scene Windows acceptance remains incomplete.
- Live Profile E remains separately authorized work and is currently unspent.
- Current authorized FXD product-runtime requests: 0.
- This reassessment does not release the hold, authorize product work, merge anything, or authorize API spending.

## What should be kept

The following are valuable and should be preserved unless a reproduced defect proves otherwise:

- OCP STEP import and exact geometry foundation.
- Source-CAD immutability and source hashing.
- PySide/VTK desktop foundation.
- Project persistence and revision/state machinery.
- The accepted R1 classification and migration repairs.
- Existing fixture component/building blocks.
- Existing manufacturing/output machinery where it can be reconciled.
- Existing locating mathematics as a mathematical primitive.
- Existing explicit offline/live provider modes and fail-closed provenance.
- Existing tests and cost/API firewalls.

A whole-core rewrite is not justified by the inspected evidence.

## What went wrong

### 1. The workflow makes Chris do too much planning

The desktop exposes a large process form plus orientation, classification, annotation, tooling, proposal, manufacturing, and editing interactions.

The proposal path separately checks seven minimum-intent fields, including loading and unloading directions.

Those are not all bad pieces of information, but the product often asks for them at the wrong level.

FXD should propose geometry-dependent choices and ask Chris only when the answer genuinely cannot be inferred or safely suggested.

Missing software capability must not be disguised as a manufacturing question.

### 2. The orientation workflow is closer to the right language than the rest of the product

The existing guided UI already contains the useful prompt:

> Select the face that sits down on the fixture.

That is the correct direction.

For the normal weld-fixture workflow, setting the assembly down should usually establish the basic working pose. A separate “front” direction should be optional unless operator access, a table edge, automation, or another real restriction makes it important.

Internally FXD can still maintain a complete coordinate system.

### 3. Product classification is too limited

The automatic reconstruction classifier recognizes only a narrow set of manufacturing shapes confidently.

Holed plates, tube, formed parts, and other components can become classification questions.

The R1 bug that lost explicit answers was repaired and should not be redone.

The remaining problem is product behavior: an unknown manufacturing label should block only the decisions that truly depend on that label. Exact geometry should remain usable where appropriate.

### 4. Weld intent is not yet the guided experience the product needs

Geometry alone does not tell FXD which interfaces are supposed to be welded.

Current reconstruction can preserve explicit weld annotations, but it does not yet produce a useful candidate-weld review experience.

The future workflow should distinguish:

- geometry-derived candidate joints;
- AI-suggested weld intent;
- user-confirmed weld intent;
- user-rejected candidates.

A practical first version should let FXD highlight likely part-to-part seams and let Chris keep, remove, or add them.

The minimum useful weld information for fixture design is:

- which members are joined;
- where the relevant weld runs;
- which side/approach matters;
- whether the fixture must support tack-only or full welding;
- any job requirement that materially changes access or fit-up.

Do not invent critical weld size, tolerance, or process requirements when they are genuinely absent.

### 5. Useful evidence gets dropped before the model sees it

The current PR #79 request sends useful information such as component names, face identities, bounds, selected annotations, process setup, tooling metadata, existing placements, and already-generated fixture candidates.

However, the current request does not send the richer product-reconstruction package as the core design context, does not provide a proper member/joint seam graph, does not provide the useful precedent substance needed for fixture reasoning, and does not use the model as the owner of a complete fixture construction strategy.

The application can therefore ask Chris questions about reconstruction without fully giving that reconstruction to the model that is expected to reason about the fixture.

That is a direct integration failure.

## Fixture-library truth

The repository contains multiple different “knowledge” systems and they should not be conflated.

### Current local correction knowledge

fxd_geometry/knowledge.py stores attributable correction records and can produce a stripped training-style view.

That is not a trained fixture-design model.

### Superseded PR #54 public precedent system

PR #54 contained structured public fixture knowledge with engineering principles, fixture patterns, component applications, acceptance/rejection records, and deterministic local retrieval.

This was real structured precedent logic.

However, the old provider context reduced selected precedent to things such as record identity, score, matches/conflicts, assumptions, failure modes, and sources.

Many of the actual practical strategy fields — support strategy, locator strategy, clamp strategy, reaction strategy, base strategy, and load/unload guidance — were not passed through as the engineering substance the model needed.

In plain language:

> FXD found the useful page in the reference book, then often gave the model the page number and warnings instead of the useful instructions on the page.

### Extended fixture-library research

docs/research and data/research contain a much broader architecture for tooling, templates, shop standards, private benchmarks, context assets, and public engineering knowledge.

That package is explicitly research-only and current product code must not silently adopt it.

It is valuable architecture, but mass migration of the entire library should not be the prerequisite to proving one practical fixture.

### Recommended precedent repair

For the first supported weld-fixture family, create/use only a small set of approved structured precedents with the actual useful relationship:

product feature / manufacturing intent
→ fixture response
→ reason
→ parameters/constraints
→ weld and loading access
→ known failure/correction history.

Retrieve and provide that engineering substance to the strategy model.

Do not blindly copy an old fixture, and do not let precedent override project-specific deterministic validation.

## Current AI design path

The current broad path is:

STEP import
→ accepted manufacturing orientation
→ process/annotation/classification inputs
→ deterministic placements and fixture concepts
→ product reconstruction/checks
→ explicit offline or live mode
→ AI request containing already-generated candidates
→ recommendation-style AI response
→ proposal attached to the project
→ separate deterministic build generation
→ separate solid authoring/export.

That is not yet the intended architecture.

The intended architecture is:

assembly geometry
+ confirmed manufacturing intent
+ useful precedents
→ typed AI fixture strategy
→ restricted deterministic compiler
→ existing OCP fixture authoring
→ deterministic physical validation
→ human practicality review.

The key acceptance test is simple:

> If two valid typed strategies choose different support/clamp locations, the corresponding authored solids must actually change.

A different explanation with the same predetermined fixture is not AI-driven fixture synthesis.

## Physical-validation gaps that remain important

The September audit reported serious defects. Source inspection still supports the architectural basis of the important remaining ones:

- build geometry can be generated from fixed product-bound offsets rather than physical strategy;
- intended-interface metadata does not by itself prove that penetration is legitimate;
- locating rank does not by itself prove that a contact point lies on the referenced physical surface;
- a global six-degree-of-freedom result does not prove all loose members are restrained at the correct stage;
- ordinary project access checks do not yet prove a continuous real weld approach or finished-part removal path;
- declared tab/slot or poka-yoke information can exceed what the inspected authoring path actually creates;
- software success still does not prove fixture practicality.

The F05/F06/F11 R1 repairs should be preserved rather than repeated.

## Proposed Chris Input Budget

### Automatically infer or retrieve

- project name;
- assembly/component relationships;
- usable exact faces/holes/axes;
- duplicate volume category from production quantity;
- saved shop capabilities and standard tooling from a named profile;
- the basic manufacturing coordinate frame after the user sets the part down;
- deterministic collision/contact/access results.

### Suggest and confirm

- bottom/support face;
- likely weld seams;
- likely support regions;
- likely locator/stop strategy;
- clamp placement/direction;
- loading/removal sequence;
- base/construction method;
- fixture lifecycle when a saved preference exists.

### Ask Chris only when genuinely necessary

- which apparent joints are actually welded when it cannot be known;
- job-critical dimensions/tolerances that are absent from trusted records;
- unusual loading/handling restrictions;
- permission for a proposed product modification;
- actual shop/customer constraints FXD cannot know;
- private-data transmission and paid live-model permission.

### Remove from normal workflow

- engineering-academic terminology as required user vocabulary;
- arbitrary raw loading/unloading vectors when FXD can propose/check the sequence;
- blanket “reviewed” checkboxes standing in for actual access/removal proof;
- repeated questions already represented by a saved job/shop profile.

For the first supported case, a useful interaction target is:

1. Set/accept the pose.
2. Confirm the weld map.
3. Confirm one consolidated job/profile summary.
4. Review the generated fixture.

That is a target for the supported first family, not a promise that every future job requires exactly three clicks.

## Shop-language UI direction

Internal engineering terms can remain in the engine.

The normal interface should say things such as:

- “Set the assembly down.”
- “Which face sits on the fixture?”
- “These look like the welds. Keep/remove/add.”
- “This piece can still move.”
- “This piece can still twist.”
- “This clamp has nothing solid behind it.”
- “The torch hits here.”
- “The finished assembly cannot come out this way.”
- “I recommend locating from this hole.”
- “This design changed. Check it again.”

Do not require the user to understand the formal datum/constraint vocabulary to get a useful fixture.

## First convincing product proof

Do not prove FXD on a single plate.

Use one controlled, small multi-member weldment that includes:

- multiple loose members;
- at least one meaningful hole or locating feature;
- nontrivial weld locations;
- supports;
- locating;
- clamps;
- a weld-access conflict opportunity;
- a real removal requirement.

Freeze the job requirements first.

The fixture must survive negative tests such as:

- invalid contact away from the part;
- a support/clamp penetrating the product;
- an unrestrained loose member;
- blocked weld approach;
- trapped finished assembly.

Then make at least one meaningful geometry/tolerance variation and prove the design regenerates sensibly or clearly reports an unsupported condition.

The final product test remains:

> Would Chris actually build and use this fixture with only ordinary finishing edits?

If Chris must replace the fundamental support, locating, clamp, or loading strategy, the product proof failed even if unit tests passed.

## Recovery gates

This reassessment recommends the following dependency order. These are planning gates only; they do not release the current hold.

### Gate 0 — Coherent control baseline

Repair the current control-validator drift without weakening the legitimate held state or cost/API safeguards.

Preserve PR #79 and accepted R1 work.

### Gate 1 — Simple intent workflow

Use one representative case.

Simplify orientation, classification, weld confirmation, and process setup around the supported weld-fixture family.

Measure question count and remove questions created by software limitations.

### Gate 2 — Physical judge

Before trusting AI synthesis, repair authored-solid/product interference checks, physical contact evidence, stage/member restraint, weld approach, clamp states, and removal checks for the representative case.

### Gate 3 — AI strategy actually drives CAD

Create one strict, bounded fixture-strategy contract and restricted command/compiler path.

Supply useful reconstruction and precedent substance.

Prove offline first with manually authored and synthetic-provider strategies.

Changing a supported strategy decision must change the corresponding OCP geometry.

Only after that should a separately authorized live synthesis proof occur.

### Gate 4 — One practical fixture and normal finishing

Finish the representative fixture in the native Windows workflow.

Support ordinary edits/undo/save/reopen/revalidation.

Reconcile STEP, DXF, BOM, setup/review outputs.

Obtain Chris’s practicality verdict.

## Repository authority recommendation

Do not create another pile of competing directions.

The front door should clearly separate:

1. What FXD is supposed to be.
2. What the code actually does today.
3. What work is authorized right now.

Recommended authority surfaces:

- AGENTS.md — short agent routing and permanent boundaries.
- docs/CONTROL_STATE.json — machine-readable current permission/state.
- CURRENT.md — short projection of current state.
- docs/PRODUCT_DIRECTION.md — product promise and non-goals.
- docs/USER_WORKFLOW.md — normal user-facing workflow and input budget.
- docs/ARCHITECTURE_CURRENT.md — truthful current implementation map.
- docs/AI_DRIVEN_SYNTHESIS_ARCHITECTURE.md — target design architecture.
- one recovery roadmap — bounded dependency order.
- dated audits/reassessments — evidence/history, not standing execution authority.

This reassessment should remain a durable evidence document, not a new implementation authorization.

## Agent and cost direction

The repository currently prohibits Claude/Anthropic as a standard FXD implementation/audit/review route. This reassessment does not silently change that rule.

Under current authority, a clean use of both paid coding subscriptions is:

- Codex: bounded FXD implementation when explicitly authorized.
- Independent OpenAI review: exact-head FXD review.
- Claude Code: work an independent project/repository in parallel.

If Chris wants Claude Code to work directly on FXD later, change that repository policy explicitly rather than ignoring it.

Keep these cost routes separate:

1. subscription-backed coding-agent usage;
2. FXD product-runtime AI requests;
3. unrelated legitimate application APIs such as voice.

FXD development/test environments should not accidentally expose product-runtime provider credentials. Do not remove or break unrelated application APIs.

## Highest-value product changes

1. Make AI strategy decisions actually determine authored fixture geometry.
2. Give the model useful reconstructed geometry, confirmed weld intent, and real precedent substance.
3. Make physical checks reject interference, invalid contact, unrestrained members, and trapped assemblies.
4. Replace the questionnaire with a short visual workflow and saved job/shop profiles.
5. Add candidate/confirmed/rejected weld seams linked to actual members.
6. Stop treating every unknown manufacturing label as a global blocker.
7. Prove one representative fixture and meaningful variations before expanding scope.
8. Support normal native finishing edits, undo, save/reopen, and revalidation.
9. Derive coherent solids, flat profiles, BOM, and setup information from the same authored revision.
10. Consolidate active authority and enforce development/runtime cost separation.

## Final recommendation

Recover FXD through a bounded partial rebuild of its design integration and user workflow.

Keep the CAD foundation, source protections, useful builders, persistence, explicit AI modes, and accepted R1 repairs.

Do not begin with a new model swap, a mass fixture-library migration, a general CAD rewrite, or another giant implementation loop.

The standard for every accepted slice should be:

> Does this reduce what Chris must explain, make the design decision genuinely affect the fixture, or improve proof that the fixture can actually be built and used?

Current disposition remains unchanged:

- read-only reconstruction complete;
- implementation held;
- PR #79 preserved;
- live FXD spending unauthorized.

## Evidence anchors

- Current recovery plan: https://github.com/DumpsterFireWorks/fxd-fixture-design/issues/85
- Current continuation handoff: https://github.com/DumpsterFireWorks/fxd-fixture-design/issues/86
- Active preserved gate: https://github.com/DumpsterFireWorks/fxd-fixture-design/issues/69
- Preserved implementation PR: https://github.com/DumpsterFireWorks/fxd-fixture-design/pull/79
- Accepted AI-driven synthesis reset: https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/main/docs/decisions/0001-ai-driven-fixture-synthesis-reset.md
- Product direction: https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/main/docs/PRODUCT_DIRECTION.md
- September full audit: https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/main/docs/FXD_FULL_AUDIT_2026-09-07.md
- September repair plan: https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/main/docs/FXD_REPAIR_PLAN_2026-09-07.md

