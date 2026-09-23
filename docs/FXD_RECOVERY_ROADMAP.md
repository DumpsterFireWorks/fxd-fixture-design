# FXD Recovery Roadmap

Authority: Decision 0002 + Issue #85 + active gate in `docs/CONTROL_STATE.json`.

This is dependency order, not standing authorization for every gate.

## FXD-R0 — Recovery baseline

Purpose:
- preserve accepted PR #79 R1 work;
- synchronize current main;
- repair control-validator/test drift;
- prove native Windows visible-scene behavior offline;
- merge the preserved foundation after independent review.

Product-runtime requests: 0.

## FXD-R1 — Simple pose, job, and weld intent

Purpose:
- reduce normal interaction to shop language;
- make bottom-face orientation the default;
- make front direction conditional;
- persist candidate/suggested/confirmed/rejected weld intent;
- batch manufacturing classification questions so only consequential unknowns block;
- add saved job/shop profile behavior needed by the representative case.

Acceptance:
- representative assembly can reach fixture-generation readiness without the old large questionnaire;
- measured user-question count is recorded;
- save/reopen preserves pose, confirmed weld map, and job/profile state;
- no live provider required.

## FXD-R2 — Physical truth for the representative family

Purpose:
- authored fixture/product collision;
- legal touching versus penetration;
- point-on-surface/normal/frame contact proof;
- stage-specific restraint of loose bodies/rigid groups;
- clamp reaction/support evidence;
- bounded weld-access and load/removal checks;
- selected manufactured joint/output coherence.

Acceptance:
- deliberately bad fixtures fail at the physical layer;
- valid bounded cases pass;
- missing evidence cannot masquerade as a physical pass;
- no live provider required.

## FXD-R3 — AI strategy drives real CAD

Purpose:
- provide useful reconstruction, confirmed weld intent, critical requirements, and precedent substance to the model;
- implement one strict versioned strategy contract;
- compile only allowlisted commands;
- make support/locator/clamp/base/load decisions control actual OCP geometry;
- preserve traceability.

Order:
1. manual strategy replay;
2. synthetic-provider strategy replay;
3. exact-head offline validation;
4. only then one separately authorized live strategy request.

Acceptance:
- changing a supported strategy choice changes corresponding authored geometry;
- invalid identities/units/commands are rejected before authoring;
- deterministic failures remain authoritative;
- first meaningful Profile E live proof is recorded here, not earlier.

## FXD-R4 — One practical fixture

Purpose:
- one representative multi-member weld fixture end to end;
- geometry/tolerance variation;
- native finishing and undo/redo;
- persistence;
- coherent STEP/DXF/BOM/setup/review outputs;
- qualified practicality acceptance.

Final verdict:

> Would Chris actually build and use this with only ordinary finishing edits?

Fundamental redesign of support, locating, clamping, or loading means the proof failed.

## Deferred

Until R4 succeeds:
- multiple fixture families;
- broad integrated CAD;
- robot programming;
- universal learned rules;
- SaaS/accounts/billing;
- mass private-library ingestion;
- general-purpose CAD replacement.
