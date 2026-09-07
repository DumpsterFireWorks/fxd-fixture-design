# FXD repository and product reassessment

Audit requested September 7, 2026 · Product source inspected without modification · Baseline evidence pinned below

## Decision

**Keep the CAD foundation, but do not resume the existing plan as though a model upgrade is the remaining task. FXD needs a bounded reassessment of its synthesis and validation path before another product build. A complete rewrite is not justified by the evidence.**

The repository contains functioning geometry, desktop, persistence, and governance infrastructure. It does not yet demonstrate an AI-designed, practically acceptable fixture. Several existing checks validate metadata or mathematical abstractions without establishing the corresponding physical condition. New, independently reproduced failures show that this distinction is material.

Chris reports that Opus 5 and what he recalls as ChatGPT 5.5 both failed to produce a useful fixture, which is why he stopped the project. That is the owner’s current account of the product failure. GitHub’s formal hold records cost control. Both belong in the reassessment; the cost record must not be used to dismiss the engineering rejection. This audit did not reproduce those historical model sessions and cannot apportion their failures between model capability, instructions, input evidence, and application behavior.

**Current disposition:** Owner direction on September 7 authorizes Review-Control to prepare Codex repairs. Governance Issue #83 records the bounded offline resumption. Read `docs/CONTROL_STATE.json`, `CURRENT.md`, and `docs/CODEX_REPAIR_PASS_01.md` for execution authority; this audit never authorizes work by itself. No product code or live-provider use was required to obtain these findings.

## Scope and evidence

GitHub resolved the originally supplied `kool1160/fxd-fixture-design` repository to `DumpsterFireWorks/fxd-fixture-design`.

| Inspected surface | Exact identity | Disposition |
| --- | --- | --- |
| Current main | `801aad49f4c5e5fac4626fe18576717d71d19580` | Authoritative baseline |
| Active issue | [#69](https://github.com/DumpsterFireWorks/fxd-fixture-design/issues/69) | M33.1, held |
| Preserved implementation | [PR #79](https://github.com/DumpsterFireWorks/fxd-fixture-design/pull/79), `686486b0cfd6e1f062a3074b8d1319a0e84549b4` | Open draft, unaccepted |
| Earlier PR product evidence | `3397c96ad011aedc185e8cb46484662bd87a272e` | Historical successful hosted run, not current-head acceptance |
| Superseded implementation | [PR #54](https://github.com/DumpsterFireWorks/fxd-fixture-design/pull/54), `52524b14ca5adc46735f69b1b198bb6909a93d8c` | Closed unmerged; selected source inspection for salvage only |

Read the authority stack, current issue and comments, active PR and reviews, hosted checks, architecture and engineering contracts. Traced source import, product reconstruction, AI context and response parsing, deterministic concepts, build authoring, locating, access, weld checks, placement, persistence, export gates, desktop integration, dependency records, and fixture-library boundaries. Ran complete offline repository commands against main and the held head, plus independent synthetic probes. Historical PR #54 was not executed or accepted.

This is a broad repository and product audit, not a claim that every line or every possible failure was exhaustively verified. The installed Windows application, its revision, Chris’s original assembly, original outputs, native Windows interaction, live-provider behavior, and physical fixture practicality remain untested here. Linux Qt tests do not establish native Windows rendering or usability. No access to Chris’s computer was available.

## Test results

| Check | Observed result |
| --- | --- |
| Main `bash scripts/ci.sh` | PASS: 480 tests run, 6 skipped; pinned OCP proof and governance checks pass |
| Held-head `bash scripts/ci.sh` | FAIL: 487 tests run, 1 failure, 6 skipped |
| Held-head failing test | `test_operator_protocol_separates_builder_and_review_control`; obsolete literal assertion expects `Codex implements one bounded gate` while protocol says `ChatGPT Codex Remote implements one bounded gate` |
| Held-head standalone kernel proof | PASS: real OCP import, assembly, topology, Boolean, clearance/contact semantics, tessellation, transformed edges, sectioning, STEP/DXF proof |
| Held-head standalone M33.1 self-check | PASS: synthetic single plate; 1 body, 6 faces, 6 planes, 1 confirmed weld annotation; offline request count 0; persistence passes |
| Hosted main check | Successful [Pinned OCP acceptance](https://github.com/DumpsterFireWorks/fxd-fixture-design/actions/runs/31435350294/job/93608130218) |
| Hosted held-head check-runs | No check runs returned for `686486b…` |
| Earlier hosted PR evidence | [Run 31392285357](https://github.com/DumpsterFireWorks/fxd-fixture-design/actions/runs/31392285357) succeeded on `3397c96…` |
| Product-runtime API requests in audit | 0; classification failure probe used a fake provider and made 0 fake calls |
| Tracked source changes | None in main or held worktree |

Environment: Python 3.12; pinned `cadquery-ocp==7.9.3.1.1`, `PySide6==6.8.3`, `vtk==9.6.2`. The first attempts encountered shallow Git history and missing Linux `libEGL.so.1`. Full history was fetched and a local Ubuntu library supplied before the final runs above. Those initial environment failures are not product findings. Test counts are total tests run, including skips, not all-pass counts.

## Findings

Priorities describe impact on a credible restart, not production incidents. “Reproduced defect” means the specific behavior below was exercised. “Capability gap” means current behavior is too limited for the product goal; it does not automatically imply a violation of an older, narrower proof contract.

### F01 · High · Reproduced validation defect: generated manufacturing parts can intersect the product while the build is valid

**Boundary:** main and held `fxd_geometry/fabrication_workflow.py`, `generate_fixture_build_plan()`, `validate_fixture_build_plan()`, `author_fixture_build()`.

**Reproduction:** Import an actual OCP 120 × 80 × 8 mm solid plate. Generate the existing laser-cut fabricated plan with explicit full-weld/access/unload input flags and locked adjustment state. The build validator returns `valid` with no findings. OCP authors 10 components. Independent volumetric intersection checks find that `m30-clamp-plate`, `m30-gusset`, and `m30-riser` penetrate the product.

**Cause:** Fixed offsets from overall product bounds choose the geometry. The build validator checks references, declared roles, parent AABB connectivity, and metadata, but does not compare authored solids against the immutable product. Authoring returns the earlier validation rather than a fresh physical result.

**Consequence:** A build-level `valid` state is insufficient fixture evidence. Other project/export checks may still block the complete project; this probe does not establish a production-release bypass.

**Bounded correction:** Validate authored fixture/product and fixture/fixture geometry, explicitly model intended contacts, and bind the result to the authored revision. Add a regression for this generated plate case and one legitimate touching support. Do not simply exempt component roles from collision checks.

### F02 · High · Reproduced validation defect: interface labels exempt deep penetration

**Boundary:** main and held `fxd_geometry/validation.py`, `_intentional_interface()` and `_kernel_findings()`.

**Reproduction:** Put a 6 mm cube completely inside a 10 mm cube. Label them `support_pad` and `baseplate`, assign two different nonempty interface strings, and supply the real OCP kernel. Volumetric overlap is true and clearance is 0, but `_kernel_findings()` returns no finding.

**Cause:** A recognized role pair plus nonempty interface metadata permits the pair. Minimum distance cannot distinguish contact from penetration; the exception checks an excessive gap but not excessive overlap or interface compatibility.

**Bounded correction:** Require compatible explicit mating identities and a permitted contact/engagement geometry. Distinguish zero-gap touching from volumetric interference and check engagement bounds. Retain tests for legitimate fits.

### F03 · High · Reproduced capability gap: locating validity is not physical contact validity

**Boundary:** main and held `fxd_geometry/constraints.py`, `analyze_locating_strategy()`; callers in `placement.py` and `concepts.py`.

**Reproduction:** Six mathematically independent contacts at coordinates of at least 10,000 mm reference a 120 mm plate. The solver returns rank 6, `strategy_valid=True`, and no findings.

**Interpretation:** The rigid-body rank calculation is useful and behaves consistently with its supplied-contact abstraction. It validates identity membership, not whether points and normals lie on the referenced surface. The source contract already says full rank is insufficient. The gap is allowing this abstraction to stand in for physical fixture validation without an enforced geometry-aware contact stage.

**Bounded correction:** Establish point-on-trimmed-face, normal, contact-side, units/frame, and tolerance evidence before accepting contact rows. Qualify the output explicitly as mathematical restraint until physical evidence exists. Add off-face, wrong-normal, wrong-frame, and valid-contact adversaries.

### F04 · High · Reproduced capability gap: one six-DOF result cannot establish loose-assembly restraint

**Boundary:** same solver and stage-independent locating contracts.

**Reproduction:** The repository’s synthetic assembly contains four component records. Supply all six contacts on `BRACKET_A` only. The solver still reports a valid rank-6 strategy. Other component freedom is not part of this calculation.

**Interpretation:** A single rigid-body check can be appropriate for an already joined rigid weldment. It is not proof that all loose members are located before tacking. This audit did not verify a complete multi-body mechanical solver elsewhere.

**Bounded correction:** For the chosen proof family, model which components are loose, supported, clamped, tacked, or rigidly joined at each operation. Check each independent body or explicitly justified rigid group. Do not sum unrelated contacts into one global success claim.

### F05 · High · Reproduced PR defect: resolving manufacturing classification is lost at execution

**Boundary:** held `product_reconstruction.py:reconstruct_product()`, `ai_execution.py:execute_design_mode()`, and the native UI.

**Reproduction:** A rectangular plate with a through-hole is classified `unknown`. An explicit `PLATE_SHEET` override creates an unblocked reconstruction. Attach it to the current project and select live execution with a fake available provider. Execution reconstructs without the override, resets classification to `unknown`, and returns `reconstruction_blocked`; the fake provider is never called.

**Cause:** The classifier intentionally recognizes only a very restricted rectangular solid. The override exists in a library function, but execution does not carry it forward. No classification-override caller or question-answer integration was found in the UI.

**Bounded correction:** Persist source-bound engineer classification decisions, expose the unresolved component and focused answer in the UI, and consume those decisions during execution/reload. Keep unsupported automatic classifications unknown. Test a holed plate, tube, and formed part with and without an explicit answer.

### F06 · High · Reproduced PR defect: genuine v5 projects with fixture proposals fail migration

**Boundary:** held `project.py:_migrate_legacy_geometry_references()` and `FxdProject.load()`; `ai_fixture_engineer.py:FixtureProposal` identity validation.

**Reproduction:** Main generates and saves an actual v5 project with a deterministic fixture proposal and geometry annotations. It reloads successfully on main. The held branch rejects the same bytes with `invalid FXD project: proposal identity does not match proposal evidence`. An otherwise equivalent main-generated project without its proposal loads on the held branch.

**Cause:** Recursive migration rewrites proposal geometry references without coherently migrating the proposal’s content-bound identity and related evidence. Existing migration coverage exercises annotations and workflow references but does not reproduce this complete historical proposal-bearing artifact.

**Bounded correction:** Preserve the original snapshot and proposal history. Define explicit migration/staleness behavior for proposal identity, context, citations, decisions, and approvals. Load the source/project while requiring renewed validation when old proposal authority cannot be preserved. Never silently rehash edited evidence as though the old approval still applies.

**Acceptance:** Main-generated legacy fixtures containing proposals, annotations, build plans, and edits load safely, preserve source bytes, and either retain valid history or visibly require revalidation. Unknown mappings continue to fail closed. This finding is relevant to reopening Chris’s installed project, but its actual format remains unknown.

### F07 · High · Confirmed capability gap: the accepted AI-driven synthesis path remains unimplemented

**Boundary:** `ai_fixture_engineer.py:prepare_proposal_project()`, `build_ai_request()`, response schema, and `generate_fixture_proposal()`; `concepts.py`; `fabrication_workflow.py`.

The current flow prepares deterministic concepts before asking for a proposal. The request includes existing fixture candidates. The response contains recommendations, reasons, and editable parameters, not a complete construction strategy that compiles into fixture geometry. Request inspection confirms no product-reconstruction package or images are included. Only selected annotations carry surface measurements; face identity lists and bounds do not provide complete manufacturing meaning.

This is consistent with M33.1 being a foundation gate, not the promised M33.2 synthesis gate. It explains why passing this PR could not demonstrate the product. It does not invalidate Chris’s report that stronger models failed his practical task.

**Bounded direction:** Test a supported strategy contract against exact geometry evidence, readable views, confirmed intent, and a small tooling vocabulary. Model decisions must determine the build. Keep the existing provider failure handling and deterministic authority. Do not treat adding pictures alone as a solution.

### F08 · High · Confirmed capability gap: load/weld/unload evidence is mostly declared rather than physically verified

**Boundary:** `access.py:evaluate_access()`, `project.py:validation_for()`, and `fabrication_workflow.py` requirements/sequences.

Access checks conservatively intersect supplied AABB envelopes with fixture features and explicitly say they are not B-Rep or motion validation. The normal project validation call supplies no weld requests or unload envelopes, so it produces missing-evidence warnings. Build validation relies on booleans such as `unload_clearance_evaluated` and on nonempty sequence text. These cannot demonstrate a removable finished weldment or an accessible torch path.

**Bounded correction:** Define one supported load/unload trajectory family and a torch/clamp envelope for the proof case. Check motion against actual geometry, including clamp-open and fixture-release states. Preserve unknown status when motion or process inputs are absent. Full robot simulation and thermal analysis are not prerequisites for this bounded check.

### F09 · Medium · Confirmed manufacturing gap: tab/slot and poka-yoke declarations exceed this authoring path

**Boundary:** `fabrication_workflow.py:generate_fixture_build_plan()`, `_shape_for()`, `_dxf_for()`, `author_fixture_build()`.

The default fabricated plan declares a riser-to-base tab/slot and asymmetric poka-yoke evidence. This authoring path builds boxes, pins, tubes, and holes; it does not consume the plan’s tab-slot or poka-yoke geometry definitions. Its DXF path emits XY rectangles and circles. Those records therefore do not establish that the declared keyed assembly aid exists in the produced parts. Other component-geometry modules have separate manufacturing capabilities; their existence does not wire them into this path.

**Bounded correction:** Compile selected joints into actual mating geometry and matching profiles, or label them unimplemented and block manufacturing-complete claims. Verify shape changes, insertion/engagement, and STEP/DXF agreement. Prefer one shared authoring route over parallel proof representations.

### F10 · Medium · Confirmed capability gap: design ranking and precedent learning are not established product intelligence

`concepts.py` gives alternatives fixed objective scores and one or two clamp mounts. `compare_fixture_build_plans()` uses a construction-method weight table. These are disclosed heuristics, not measured labor, access, cost, or repeatability predictions.

`knowledge.py` stores attributable corrections, while the extended fixture library in `docs/research` explicitly forbids runtime adoption without a later gate. The inspected active provider request does not retrieve that structured precedent system. Superseded PR #54 has additional knowledge/quality modules, but its full flow remains rejected and must not be restored wholesale.

**Bounded direction:** Use a few approved, private feature-to-fixture precedents with reasons and rejection examples. Rank only after physical checks, with explicit measurable criteria for the chosen fixture family. Do not begin fine-tuning, universal rule learning, or a large library migration before one fixture succeeds.

### F11 · Medium · Reproduced integration debt: preserved head lacks current acceptance and carries stale branch governance

The held head fails the protocol-literal test described above. Its branch also predates main’s cost-control state and workflow retirement even though selected instruction files were synchronized. Current-main precedence prevents branch-local documents from legally authorizing work. The earlier green head cannot approve the current one.

The live acceptance script hardcodes the former repository URL, so a checkout using today’s canonical owner fails its repository comparison. This was established by source inspection, without executing the opt-in live harness.

**Bounded correction after resume:** Reconcile the same PR with current main, preserve the retired development dispatcher and zero development API budget, correct stale test assertions and repository-identity handling, then obtain fresh exact-head CI and review. Do not weaken identity checks or change remotes merely to make the live harness run.

### F12 · High · Acceptance gap: software evidence has not established product value

Main’s complete suite passes while the independent probes above expose important physical gaps. The M33 self-check is a single box with a weld annotation; mocked-provider tests prove contracts and failure handling, not design competence. The archived M32 rejection specifically describes generic stations, excess empty rail span, weak clamp/support relationships, and inadequate loading/release rhythm.

**Bounded correction:** Keep software tests and add a product acceptance case with immutable source, operation requirements, expected physical checks, and an independent fixture-engineer verdict. Include rejected designs and variations that break a template. Never reinterpret a valid solid, accepted JSON, or a successful API response as fixture success.

## What is worth keeping

| Area | Assessment | Recovery treatment |
| --- | --- | --- |
| OCP/OCCT and CAD-neutral boundary | Real geometry operations and deterministic proof pass | Keep; strengthen how physical evidence reaches validators |
| Source identity and save infrastructure | Source hashes, embedded bytes, atomic save, revision controls are useful | Keep; fix complete-project migration before touching old user projects |
| Native desktop and VTK infrastructure | Substantial functioning base; Linux tests pass on main | Keep; separately verify installed Windows revision and real fixture interaction |
| Typed data, explicit provider mode, provenance | Sound direction, incomplete held integration | Repair on preserved PR if resumed |
| Constraint algebra and metadata checks | Useful narrow components | Retain with precise evidence labels and physical prerequisites |
| Manufacturing components/export machinery | Real solids and useful bounded operations | Consolidate selected paths; prove contacts, joints, and output correspondence |
| Fixed fixture generators | Useful offline fixtures and regression baselines | Do not use as the authority for AI fixture strategy |
| Broad research/library schemas | Useful reference work, not shipped intelligence | Keep deferred; adopt only what the first proof consumes |
| Superseded M32 improvements | Some contact/quality/knowledge work may be salvageable | Review individual components against new regressions; never restore the rejected full flow |
| Governance | Preserves owner control and explicit spending | Keep the boundaries; correct stale projections during an authorized transition |

No dependency-stack replacement is justified by the failures found. Runtime pins and third-party records exist. Installer redistribution remains a separate documented review; this audit does not provide legal clearance. No installed binary or dependency-vulnerability assessment was performed.

## Reassessment options

| Option | Assessment |
| --- | --- |
| Change model and continue unchanged | Reject: leaves construction authority and validation gaps intact |
| Rewrite FXD from scratch | Not supported: discards functioning infrastructure without addressing the core proof |
| Repair every historical issue before testing value | Reject: spends effort before resolving the central capability question |
| Recover a narrow synthesis/validation path and test one representative fixture | Recommended, subject to explicit owner resume and bounded scope |

Astra is a candidate to evaluate, not a verified solution. This repository audit makes no model-benchmark or pricing claim. A successful live strategy and a useful fixture must be demonstrated on the supported case.

## Proposed recovery sequence — decision proposal, not an active work order

1. **Recover the actual failed case without altering it.** Identify installed revision and project format; preserve the original project and source. Record why the fixture was rejected in engineering terms. Use a rights-approved private case or a synthetic equivalent. No update should overwrite the installed project as part of diagnosis.
2. **Close only the foundation blockers needed to run the experiment.** On the existing PR after an explicit resume, reconcile main, repair proposal-bearing migration and the classification answer path, and refresh deterministic/native evidence. Keep provider spending separately authorized. A foundation pass still does not count as fixture success.
3. **Establish a trustworthy judge for the selected case.** Require actual contacts, per-stage loose-component restraint, fixture/product interference checks, clamp reaction evidence, and a bounded removal/access check. The F01–F04 and F08 counterexamples become negative acceptance cases. Checks not implemented remain visibly unknown.
4. **Give Astra one properly specified design challenge.** Supply source-bound measured features, labeled views, confirmed weld/operation intent, a restricted construction vocabulary, and approved precedents. Ask for explicit supports, datums, locator/float decisions, clamp directions/reactions, component loading, weld access, and release. Compile its typed choices into the existing geometry engine. Record exact provider/model and input/output identities.
5. **Apply the existing bounded feedback principle.** The accepted full M33 direction allows at most one repair, but M33.1 allows zero; any experiment must have its own explicitly recorded gate and spend ceiling. No unlimited agent loop, retries, or automatic budget extension. A different interaction budget is an owner decision, not an implementation convenience.
6. **Decide based on the fixture.** Pass only if the checks hold and Chris would build/use it with ordinary finishing edits. Replacing the fundamental datum, locator, clamp, or loading strategy is a failed product proof. If it fails, retain the evidence and reassess or stop; do not add more UI or infrastructure to justify continuing.

After a first pass, require at least one meaningful geometry or tolerance variation before making broader capability claims. A single successful example supports a narrow proof, not universal fixture design.

The owner’s work should be limited to providing/identifying the case, resolving real manufacturing intent or privacy/spend decisions, and judging practicality. Routine test repair, evidence collection, and repository coordination should remain with Review-Control and Codex.

## Remaining unknowns

- Exact installed commit, project format, assembly, original rejected geometry, and historical model settings.
- Whether Chris’s failure came through the M32 installed path, an earlier build, external model assistance, or a combination.
- Native Windows behavior and usability of the held changes.
- Live Astra compatibility, latency, output quality, and actual request cost under an explicitly chosen configuration.
- Contact, tolerance, loading, weld-access, force, distortion, and practicality results on the original case.
- Which superseded M32 components survive independent review without importing rejected design authority.

## Source map

All source references below are pinned snapshots. This audit is evidence, not a replacement for GitHub’s current control state.

- [Main authority](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/801aad49f4c5e5fac4626fe18576717d71d19580/docs/CONTROL_STATE.json), [accepted reset](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/801aad49f4c5e5fac4626fe18576717d71d19580/docs/decisions/0001-ai-driven-fixture-synthesis-reset.md)
- [Build generation/validation/authoring](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/801aad49f4c5e5fac4626fe18576717d71d19580/fxd_geometry/fabrication_workflow.py): F01, F08, F09
- [Validation](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/801aad49f4c5e5fac4626fe18576717d71d19580/fxd_geometry/validation.py): F02
- [Constraint solver](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/801aad49f4c5e5fac4626fe18576717d71d19580/fxd_geometry/constraints.py): F03, F04
- [Held execution](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/686486b0cfd6e1f062a3074b8d1319a0e84549b4/fxd_geometry/ai_execution.py), [reconstruction](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/686486b0cfd6e1f062a3074b8d1319a0e84549b4/fxd_geometry/product_reconstruction.py): F05
- [Held project migration](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/686486b0cfd6e1f062a3074b8d1319a0e84549b4/fxd_geometry/project.py), [proposal contract](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/686486b0cfd6e1f062a3074b8d1319a0e84549b4/fxd_geometry/ai_fixture_engineer.py): F06, F07
- [Access](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/801aad49f4c5e5fac4626fe18576717d71d19580/fxd_geometry/access.py), [concepts](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/801aad49f4c5e5fac4626fe18576717d71d19580/fxd_geometry/concepts.py), [knowledge](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/801aad49f4c5e5fac4626fe18576717d71d19580/fxd_geometry/knowledge.py): F08, F10
- [Held live harness](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/686486b0cfd6e1f062a3074b8d1319a0e84549b4/scripts/m33_1_live_acceptance.py), [held governance test](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/686486b0cfd6e1f062a3074b8d1319a0e84549b4/tests/test_governance_reset.py): F11
- [Historical M32 rejection](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/52524b14ca5adc46735f69b1b198bb6909a93d8c/docs/engineering-reviews/M32_VISUAL_ENGINEERING_REJECTION_001.md), [held self-check](https://github.com/DumpsterFireWorks/fxd-fixture-design/blob/686486b0cfd6e1f062a3074b8d1319a0e84549b4/scripts/m33_1_self_check.py): F12

## Independent probe evidence

The following compact records are captured from the executed probes. They describe synthetic API-level cases, not Chris’s installed project or production release.

```json
[
  {
    "case": "off_part_contacts",
    "result": {
      "contact_minimum_mm": 10000,
      "findings": [],
      "part_maximum_mm": 120,
      "rank": 6,
      "strategy_valid": true
    },
    "checkout": "main"
  },
  {
    "case": "unlocated_other_components",
    "result": {
      "component_count": 4,
      "contacted_components": [
        "BRACKET_A"
      ],
      "rank": 6,
      "strategy_valid": true
    },
    "checkout": "main"
  },
  {
    "case": "m30_build_collision",
    "result": {
      "authored_count": 10,
      "findings": [],
      "overlapping_authored_components": [
        "m30-clamp-plate",
        "m30-gusset",
        "m30-riser"
      ],
      "status": "valid"
    },
    "checkout": "main"
  },
  {
    "case": "interface_overlap",
    "result": {
      "clearance_mm": 0.0,
      "findings": [],
      "kernel_overlap": true
    },
    "checkout": "main"
  },
  {
    "case": "provider_context",
    "result": {
      "contains_images": false,
      "contains_reconstruction": false,
      "keys": [
        "alternatives",
        "annotations",
        "components",
        "customer_tooling",
        "deterministic_findings",
        "fixture_candidates",
        "intent",
        "manufacturing_orientation",
        "placements",
        "source"
      ]
    },
    "checkout": "main"
  },
  {
    "case": "genuine_v5_saved",
    "result": {
      "format": "fxd-neutral-project-v5",
      "main_reload_succeeded": true,
      "source_sha256": "cd99d4908ac35d061e0847a6e05a6b04aaa1d05b717dbcbd19f6e659d2337cfa"
    },
    "checkout": "main"
  },
  {
    "case": "off_part_contacts",
    "result": {
      "contact_minimum_mm": 10000,
      "findings": [],
      "part_maximum_mm": 120,
      "rank": 6,
      "strategy_valid": true
    },
    "checkout": "held"
  },
  {
    "case": "unlocated_other_components",
    "result": {
      "component_count": 4,
      "contacted_components": [
        "BRACKET_A"
      ],
      "rank": 6,
      "strategy_valid": true
    },
    "checkout": "held"
  },
  {
    "case": "m30_build_collision",
    "result": {
      "authored_count": 10,
      "findings": [],
      "overlapping_authored_components": [
        "m30-clamp-plate",
        "m30-gusset",
        "m30-riser"
      ],
      "status": "valid"
    },
    "checkout": "held"
  },
  {
    "case": "interface_overlap",
    "result": {
      "clearance_mm": 0.0,
      "findings": [],
      "kernel_overlap": true
    },
    "checkout": "held"
  },
  {
    "case": "provider_context",
    "result": {
      "contains_images": false,
      "contains_reconstruction": false,
      "keys": [
        "alternatives",
        "annotations",
        "components",
        "customer_tooling",
        "deterministic_findings",
        "fixture_candidates",
        "intent",
        "manufacturing_orientation",
        "placements",
        "source"
      ]
    },
    "checkout": "held"
  },
  {
    "case": "genuine_v5_load",
    "result": {
      "error": "invalid FXD project: proposal identity does not match proposal evidence",
      "error_type": "ProjectFormatError"
    },
    "checkout": "held"
  },
  {
    "case": "genuine_v5_without_proposal_load",
    "result": {
      "succeeded": true
    },
    "checkout": "held"
  },
  {
    "case": "classification_override_lost",
    "result": {
      "classification_after_execution": "unknown",
      "failure": "reconstruction_blocked",
      "fake_provider_calls": 0,
      "resolved_before_execution": true
    },
    "checkout": "held"
  }
]
```

## Reproduction files and refresh

The independent probes were repeated against the same main and PR heads during repair setup; all fourteen result records reproduced. See `docs/audit-evidence/2026-09-07/probe-results.json` and `scripts/audit/fxd_reassessment_probe.py`. The script emits diagnostic observations; a zero exit code does **not** mean the product passes. Convert the relevant cases into regression assertions in the assigned repair pass.

Run from each pinned checkout with the pinned OCP runtime. Use the same temporary artifact directory for both runs, baseline first. The probe script can be supplied by absolute path from the governance checkout:

```sh
python /path/to/governance/scripts/audit/fxd_reassessment_probe.py --phase main --artifact-dir /tmp/fxd-audit
python /path/to/governance/scripts/audit/fxd_reassessment_probe.py --phase held --artifact-dir /tmp/fxd-audit
```

The first command runs in baseline main; the second runs in the PR checkout. All source CAD is synthetic. No provider credentials or live acceptance commands are needed. The classification probe injects a fake provider; it never performs a network request. Original probe source is retained with portable paths and explicit phase selection.

## Coverage and limits

| Surface | Evidence and disposition |
| --- | --- |
| Import, assembly transforms, OCP topology/Booleans, native CAD | Inspected and exercised by real kernel proof; retain. STEP import and CAD engine already exist. |
| Fixture generation, components, constraints, access, weld intent | Existing functionality traced; F01–F04 and F08–F10 identify limitations and defects, not absence of all these features. |
| AI request construction, parsing and execution | Existing provider, schema and failure tests retained; F05 and F07 distinguish integration defect from later unimplemented strategy contract. |
| Save/reload, revisions, review and outputs | Main/held suites and genuine v5 differential probe; F06 plus output consistency work. Export explicitly permits provisional engineering-review artifacts and sets production approval false. No production-release bypass reproduced. |
| Desktop, launcher and native interaction | Source and Linux tests inspected. Historical Windows evidence does not establish current-head Windows acceptance; installed build remains unavailable. |
| Repository automation and cost controls | Current workflows and firewall validators inspected; paid dispatcher inert. Controls are repository guardrails, not an OpenAI billing-account spending cap. |
| Dependencies and distribution | Runtime pins and notice/third-party records inspected; no stack replacement indicated. No installed-binary inspection, external vulnerability scan, or commercial redistribution clearance claimed. |
| Private knowledge and model payload | Request construction and knowledge boundaries inspected; no private owner CAD was available or uploaded. No exhaustive penetration test claimed. |
| Historical and future work | PR #54 is selective salvage only; research contracts are not asserted as working runtime features. |

Current main’s validator is deliberately hard-pinned to revision 3 and HELD. Resuming requires a narrow governance validator/test update, not merely changing a status string. The standing prompt also names the former repository owner. Issue #83 fixes these control projections and permits only current-main synchronization on PR #79 before its product edits. This is setup work, not a new CAD-engine defect.
