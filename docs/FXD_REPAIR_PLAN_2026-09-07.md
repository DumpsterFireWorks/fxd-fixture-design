# FXD repair plan — September 7, 2026

Authority: owner instruction recorded in Issue #83. Evidence: [full audit](FXD_FULL_AUDIT_2026-09-07.md). Current execution: [CONTROL_STATE](CONTROL_STATE.json), Issue #69 and [first Codex pass](CODEX_REPAIR_PASS_01.md).

## Decision

Repair and connect the existing system. FXD already has STEP import, a native CAD workspace, a real OCP geometry engine, fixture components, constraint algebra, access checks, persistence and exports. Their existence is not in question. The audit identifies where their inputs, integration, physical evidence or acceptance are insufficient.

No wholesale rewrite, replacement CAD engine, new provider stack, UI redesign or dependency upgrade is authorized. Preserve working modules and existing tests. Replace a local algorithm only when its assigned counterexample proves that a repair cannot meet the bounded contract.

Only **M33.1-R1** is executable now, on the existing PR #79. The remaining rows are a dependency-ordered queue for Review-Control, not concurrent tasks or standing Codex authorization. The accepted M33 architecture remains in force. Later gate scopes must incorporate the applicable validation prerequisites before activation; this plan does not silently extend Issue #69.

## Repair sequence

| Pass | Findings | Outcome | Dependency / authority |
| --- | --- | --- | --- |
| M33.1-R1 | F05, F06, F11 | Existing projects open safely; explicit classification answers survive execution; branch inherits current controls | **Authorized offline on #69 / #79** |
| R2 | F01, F02 | Authored geometry is checked against product and valid mating interfaces | Queued; first review R1, then record a separate bounded validation gate |
| R3 | F03, F04 | Physical contact evidence precedes locating rank; restraint is evaluated per operation/body group | Queued after R2; extend existing locating contracts for one assembly family |
| R4 | F08, selected F09 | Bounded load/release and weld access evidence; selected fabricated joints exist in actual outputs | Queued after R2/R3; use a synthetic representative assembly |
| R5 | F07, selected F10 | A typed strategy actually controls existing OCP authoring | Queued under future M33.2; deterministic judge and offline strategy replay must work before paid proof |
| R6 | F12, remaining output integration | Exact-head persistence/output/native evidence and qualified practical-fixture verdict | Queued; corresponds to final M33 proof, with separately authorized live requests only |

R2–R4 establish the checks needed to judge the synthesis experiment. They must not become universal mechanics, robot simulation or a general CAD rebuild. Review-Control may split a row if necessary for a reviewable change, but Codex must not choose or activate that split itself. Preserve the final live-provider and qualified-human acceptance requirements; a successful offline pass is not M33 completion.

## M33.1-R1 — reopen and carry trustworthy engineering intent

**Classification:** F05 and F06 are reproduced defects; F11 is reproduced CI/integration debt and a source-confirmed remote-identity mismatch.

**Violated invariant:** a valid historical source/project must not become unreadable solely because a derived proposal identity was partly migrated; an explicit, current engineer answer must not vanish when the operator starts design. The implementation branch must obey current main's cost boundary.

**Code boundary:** `fxd_geometry/project.py` legacy migration and project serialization; `product_reconstruction.py:reconstruct_product`; `ai_execution.py:execute_design_mode`; corresponding `fxd_qt_app.py` question/execute flow; `scripts/m33_1_live_acceptance.py` repository preflight only. Existing project/proposal, reconstruction, execution and Qt tests are the primary regression locations.

**Evidence:** actual main-generated v5 file with annotations and a proposal reloads on main, fails on PR with proposal-identity mismatch; removing the proposal changes the result to success. A holed plate with explicit plate/sheet classification becomes unknown during execution, before any fake provider call.

**Smallest repair:** carry source/context-bound classification decisions through UI, execution and reload; perform complete derived-artifact migration with visible staleness and preserved historical evidence. Reconcile current main before product edits. Correct canonical repository identity preflight without disabling it or executing the live harness.

**Regression/acceptance:** see the exact first work order. Demonstrate the old failure, positive repaired flow and negative stale/ambiguous/tampered cases. Full offline CI, pinned OCP and current-head synthetic-provider native interaction evidence are required. Linux success does not substitute for Windows acceptance.

**Rollback/failure:** keep original bytes untouched; save migrated work as a new file during acceptance. Unknown identities fail closed with actionable diagnostics. Old approval is never renewed by a migration hash update. No live request is required. R1 is reviewable before Profile E, but PR #79 is not merge-ready until all original gate requirements actually pass.

## R2 — physical collision and mating interfaces

**Classification:** F01/F02 reproduced validation defects.

**Invariant:** a claimed physical validation result must describe the actual authored geometry, source and revision. An interface name cannot exempt arbitrary penetration.

**Boundary:** `fabrication_workflow.py:validate_fixture_build_plan`, `author_fixture_build`; `validation.py:_intentional_interface`, `_kernel_findings`; `kernel.py` existing Boolean/intersection/clearance operations; `project.py:validation_for` and downstream evidence/export integration as needed.

**Evidence:** 120 × 80 × 8 mm synthetic plate produces ten authored fixture parts; three intersect the product while the build validator reports valid. A support cube fully inside a base cube with unrelated interface strings yields no kernel finding.

**Smallest repair:** retain plan/schema checks, add authored-solid validation, exact source/revision binding and explicit mating relationships. Distinguish touching from penetration using actual geometry. Permit only measured engagement within declared fit bounds, not role-wide exceptions. Carry the result to the displayed project/build and exported review evidence.

**Tests:** penetrating generated parts; deep nesting; different interface identities; too-large engagement; legitimate touching pad; valid fitted pin; separated parts; transformed product; geometry/kernel failure; edited geometry invalidating old results. At least one case must traverse project validation/output, not just a private helper.

**Acceptance:** real pinned OCP proves rejection and legitimate contacts remain usable. Stale or missing physical evidence is visibly unknown/blocked for physical-validity claims. Review exports may remain explicitly provisional; do not confuse them with production release. Full offline CI and exact-head independent review.

**Non-goals:** new kernel, full structural analysis, universal contact mechanics, changing all historical generators. **Rollback:** preserve geometry and evidence; failure blocks the corresponding validity claim and never creates approval.

## R3 — physical contacts and operation-specific restraint

**Classification:** F03/F04 reproduced capability gaps in the existing narrow locating abstraction, not evidence that its rank arithmetic is wrong.

**Invariant:** a mathematical constraint row counts as fixture evidence only when its referenced contact is physically supported. A pre-tack assembly cannot be certified located by six contacts on one member.

**Boundary:** `constraints.py:analyze_locating_strategy`, `placement.py`, `concepts.py`, exact OCP surface evidence and source-bound operation contracts. Retain the current rank calculation as a mathematical primitive.

**Evidence:** six off-part contacts give rank 6 and valid strategy; global analysis does not establish restraint of other component records. The current contract lacks stage-specific loose-body mechanics.

**Smallest repair:** verify point-on-trimmed-face, owning body, normal/side, units, frame and tolerance before accepting a contact. Represent loose bodies and explicitly justified rigid groups for loading/tacking/welding/release in the selected family; analyze each group at its relevant stage. Report mathematical rank separately from physical-contact validity and clamping/reaction adequacy.

**Tests:** off-part/off-trim contacts, wrong normal/frame/owner, valid transformed contact, all contacts on one member while another is loose, justified post-tack rigid group, intentional float, and a valid conventional locating arrangement. Use actual independent solids in the physical multi-member regression, not a metadata count alone.

**Acceptance:** counterexamples fail for the intended physical reason; valid locating arrangements pass the bounded contract. Unsupported mechanics remains unknown. Full offline CI and real OCP evidence. Qualified judgment of locating intent belongs to the representative-case review.

**Non-goals:** general multibody dynamics, clamp-force certification, replacing linear algebra. **Rollback:** retain source and manual contacts, invalidate physical acceptance and make the missing evidence explicit.

## R4 — usable access and manufactured joints

**Classification:** F08/F09 source-confirmed capability/integration gaps. Existing AABB envelope checks and manufacturing features remain reusable.

**Invariant:** a boolean or sequence sentence cannot establish removal clearance; declared joints must exist in authored solids and matching outputs.

**Boundary:** `access.py:evaluate_access`, `fabrication_workflow.py` requirements, `_shape_for`, `_dxf_for`, authoring; `component_geometry.py`, project validation and export/drawing integration.

**Smallest repair:** for one selected synthetic fabricated assembly, model a bounded straight-line loading/removal trajectory, opened/released clamp states and a declared torch envelope. Check against actual geometry with a documented conservative sweep or coverage/error bound; sparse point sampling alone must not claim a continuous clear path. Reuse existing tab/slot authoring only if the selected construction requires it. Otherwise mark unsupported joints unimplemented and prevent manufacturing-complete claims.

**Tests:** weld blocked despite clear overall bounds, trapped completed weldment, closed versus opened clamp, valid supported removal, missing envelope, thin obstruction between samples, matching joint and mismatched joint, actual STEP geometry versus DXF profile/BOM identity.

**Acceptance:** negative cases reject at the real failure layer; positive case is reviewable with documented assumptions. Native views make paths and interference understandable. No unmeasured thermal/robot claims. Full offline CI plus qualified process-intent judgment for the final case.

**Non-goals:** full robot programming, thermal solver, universal manufacturing catalog. **Rollback:** retain review geometry but mark access/joint evidence unresolved and block manufacturing-complete status.

## R5 — connect model strategy to existing authoring

**Classification:** F07 is the unimplemented later M33.2 capability; F10 contains existing heuristic ranking and disconnected precedent capabilities, not a blanket missing-library claim.

**Invariant:** in AI Design mode, the model's accepted typed decisions must determine construction; the software must not independently choose a template first and call the result AI-designed.

**Boundary:** `ai_fixture_engineer.py` request/schema/provider adapters, `ai_execution.py`, reconstruction contract, `concepts.py`, `fabrication_workflow.py`, and selected existing manufacturing builders/knowledge interfaces.

**Smallest slice:** one versioned typed strategy and restricted command vocabulary for the first family. Include measured geometry, referenced surfaces/frames, confirmed operation/weld intent, uncertainty, tooling and only explicitly approved precedent information. Specify datum/support/locator/float/clamp/reaction, construction and loading/release choices. First replay a manually specified and synthetic-provider strategy into existing OCP builders, then evaluate the configured live model under separately recorded authorization.

**Tests:** changing a strategy support/clamp choice changes the relevant authored geometry and identity; invalid source/face/unit/command/parameter rejects before construction; malformed/provider failures have no fallback; deterministic failures cannot be overridden; unsupported commands never execute arbitrary code. Synthetic-provider request capture proves intended evidence actually reaches the model boundary. Rank only after physical validation and label heuristic scores honestly.

**Acceptance:** exact evidence-to-strategy-to-geometry traceability, valid/invalid offline replay and then separately authorized live proof. Do not manufacture a success by replacing the model's core strategy downstream. Full offline CI and native review of the resulting geometry.

**Non-goals:** fine-tuning, universal precedent learning, broad private-library migration, new CAD stack, provider guessing, open-ended repair loops. **Rollback:** rejected strategy stays inspectable; no geometry is misrepresented as live AI output. Request ceilings cannot grow automatically.

## R6 — prove value and coherent deliverables

**Classification:** F12 acceptance gap; output/persistence risks must be verified rather than presumed defective everywhere.

**Case:** start with a synthetic multi-member fabricated assembly suitable for R2–R5; then use Chris's original rejected case if available and legally controlled. Its absence does not block current offline repairs. Record immutable source, constituent members, operation stage, critical dimensions, allowed contact areas, welds, load/release and process requirements. Do not infer missing manufacturing intent.

**Boundary:** project persistence/revisions, review UI, generated geometry, validation, STEP/DXF/BOM/setup/manifest output and exact-head native acceptance scripts. Installed-version identification and copied-project testing are evidence tasks, not an installer rebuild.

**Required evidence:** save/reload/edit preserves or explicitly invalidates each relevant identity; edits regenerate consistent geometry and outputs; quantities and features reconcile; source bytes remain identical. Include a meaningful geometry or tolerance variation and deliberately rejected fixtures. Record actual Windows build/head and live provider/model/request identities when those tests are authorized and run.

**Owner acceptance:** would Chris build and use the fixture with ordinary finishing edits? Replacing the fundamental datum, clamp, support or loading strategy is a failed proof. Record concrete reasons, not a confidence score. Software checks cannot substitute for this verdict.

**ROI/stop:** if the bounded proof cannot produce a useful fixture, preserve the evidence and reassess or hold. Do not justify broader spending with sunk cost or fill the queue with UI/platform work. Full M33 allows at most one separately governed repair; current M33.1 allows zero live repair requests. Missing live/Windows/human evidence stays missing, never waived by this plan.

## Operating and review rules

- One fresh ChatGPT Codex Remote session per bounded pass, same branch/PR until accepted. Read repository evidence rather than carrying a growing conversation transcript.
- Review-Control owns scope, issue coordination and exact-head review. Chris supplies real manufacturing decisions and practicality acceptance; he is not the routine message bus.
- No GitHub paid Codex dispatcher, development API key, automatic provider retry or live request authorized by an ordinary CONTINUE.
- A pass reports exact SHA, changed behavior, reproduction/regression results, full CI and remaining evidence. Builder confidence is not acceptance.
- Preserve frozen history. Future work stays queued until current authority is updated coherently. Do not create parallel implementation PRs from this list.
