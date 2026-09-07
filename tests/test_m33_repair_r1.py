"""R1 failure-layer regressions; no real provider or opt-in harness execution."""
import hashlib
import json
from dataclasses import replace
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from fxd_geometry import (
    ExecutionMode, FailureCategory, ManufacturingClassification as Role, OcpKernel,
    ProviderState, ai_response_from_proposal, execute_design_mode, load_step_for_workbench,
)
from fxd_geometry.project import FxdProject, ProjectFormatError
from scripts import m33_1_live_acceptance as acceptance
from scripts.m33_1_self_check import synthetic_workflow
from tests.test_m33_ai_execution import _LiveProvider

LEGACY = Path(__file__).parent / "fixtures" / "m33_genuine_v5.fxd.json"


def classified_case(kind="holed-plate"):
    from fxd_geometry import (AnnotationRole, GeometryReference, InteractiveWorkflow,
        face_annotation, orientation_from_faces, product_from_workbench_document)
    kernel = OcpKernel()
    if kind == "holed-plate":
        shape = kernel.cut(kernel.make_box((0, 0, 0), (120, 80, 8)),
                           kernel.make_cylinder((60, 40, -1), 5, 10))
    elif kind == "tube":
        shape = kernel.cut(kernel.make_box((0, 0, 0), (100, 40, 20)),
                           kernel.make_box((-1, 3, 3), (101, 37, 17)))
    else:
        shape = kernel.cut(kernel.make_box((0, 0, 0), (100, 40, 20)),
                           kernel.make_box((-1, 3, 3), (101, 37, 21)))
    document = load_step_for_workbench(kernel.export_step(shape), source_name=kind + ".step")
    product = product_from_workbench_document(document)
    component = product.components[0]
    faces = document.assembly.components[0].faces
    down = next(f for f in faces if f.is_planar and abs(f.normal[2]) > .9)
    front = next(f for f in faces if f.is_planar and abs(f.normal[1]) > .9)
    def ref(face):
        return GeometryReference(component.identity, component.bodies[0].identity, face.reference)
    _, _, prototype = synthetic_workflow()
    workflow = InteractiveWorkflow(document.source_sha256, replace(prototype.setup,
        manufacturing_orientation=orientation_from_faces(document, ref(down), ref(front), accepted=True)),
        geometry_annotations=(face_annotation(document, ref(front), AnnotationRole.WELD_JOINT, notes="Synthetic"),))
    return document, workflow


class LegacyMigrationTests(unittest.TestCase):
    def test_absent_proposal_field_is_not_geometry_migration(self):
        from fxd_geometry.project import _migrate_legacy_geometry_references
        from fxd_geometry import product_from_workbench_document
        project = FxdProject.load(LEGACY)
        raw = project.to_dict()
        raw.pop("fixture_proposal")
        raw.pop("legacy_evidence")
        document = load_step_for_workbench(project.product.source_bytes, source_name=project.product.source_name)
        migrated = _migrate_legacy_geometry_references(raw, document, product_from_workbench_document(document))
        self.assertNotIn("legacy_evidence", migrated)
        self.assertEqual(migrated["validations"], raw["validations"])

    def test_real_v5_proposal_history_edits_and_source_survive_reload(self):
        before = LEGACY.read_bytes()
        original = json.loads(before)
        self.assertEqual(original["format"], "fxd-neutral-project-v5")
        migrated = FxdProject.load(LEGACY)
        historical = json.loads(migrated.legacy_evidence["payload"])
        for key in ("fixture_proposal", "revisions", "decisions", "approved_revision"):
            self.assertEqual(historical[key], original[key])
        self.assertEqual(migrated.edit_log[0].value, 14)
        self.assertIsNotNone(migrated.fixture_build)
        self.assertEqual(len(migrated.fixture_build.components), len(original["fixture_build"]["components"]))
        self.assertEqual(migrated.fixture_proposal.proposal_decision, "pending")
        self.assertTrue(any(issue.rule_id == "proposal_stale" for issue in migrated.fixture_proposal.guided_issues))
        self.assertIsNone(migrated.approved_revision)
        with self.assertRaisesRegex(ProjectFormatError, "stale fixture proposal"):
            migrated.decide("approve_for_review")
        self.assertEqual(hashlib.sha256(migrated.product.source_bytes).hexdigest(), original["source_sha256"])
        self.assertNotEqual(migrated.workflow.geometry_annotations[0].reference.component_identity,
                            original["interactive_workflow"]["geometry_annotations"][0]["reference"]["component_identity"])
        with tempfile.TemporaryDirectory() as directory:
            restored = FxdProject.load(migrated.save(Path(directory) / "migrated.fxd.json"))
            self.assertEqual(restored.revision_id, migrated.revision_id)
            self.assertEqual(restored.legacy_evidence, migrated.legacy_evidence)
            self.assertEqual(restored.fixture_proposal.to_dict(), migrated.fixture_proposal.to_dict())
            self.assertEqual(restored.product.source_bytes, migrated.product.source_bytes)
        self.assertEqual(LEGACY.read_bytes(), before)

    def test_legacy_without_proposal_and_old_approval_is_invalidated(self):
        raw = json.loads(LEGACY.read_bytes())
        raw["fixture_proposal"] = None
        raw["approved_revision"] = raw["revisions"][-1]["revision_id"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "no-proposal.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            project = FxdProject.load(path)
            self.assertIsNone(project.fixture_proposal)
            self.assertIsNone(project.approved_revision)
            self.assertEqual(json.loads(project.legacy_evidence["payload"])["approved_revision"], raw["approved_revision"])
            FxdProject.load(project.save(Path(directory) / "reload.json"))

    def test_tampered_original_proposal_is_rejected_before_migration(self):
        raw = json.loads(LEGACY.read_bytes())
        raw["fixture_proposal"]["concept_name"] = "tampered"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaisesRegex(ProjectFormatError, "proposal identity"):
                FxdProject.load(path)

    def test_tampered_saved_history_is_rejected(self):
        raw = FxdProject.load(LEGACY).to_dict()
        raw["legacy_evidence"]["payload"] += " "
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaisesRegex(ProjectFormatError, "legacy history identity"):
                FxdProject.load(path)

    def test_unknown_proposal_reference_and_ambiguous_alias_fail_closed(self):
        from fxd_geometry.ai_fixture_engineer import FixtureProposal, proposal_identity
        from fxd_geometry.project import _migrate_legacy_geometry_references
        from fxd_geometry import product_from_workbench_document
        raw = json.loads(LEGACY.read_bytes())
        proposal = FixtureProposal.from_dict(raw["fixture_proposal"])
        index = next(i for i, item in enumerate(proposal.recommendations) if item.geometry_reference)
        recommendations = list(proposal.recommendations)
        recommendations[index] = replace(recommendations[index], geometry_reference=replace(
            recommendations[index].geometry_reference, component_identity="unknown-component"))
        proposal = replace(proposal, proposal_identity="", recommendations=tuple(recommendations))
        raw["fixture_proposal"] = replace(proposal, proposal_identity=proposal_identity(proposal)).to_dict()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unknown-reference.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaisesRegex(ProjectFormatError, "unknown component reference"):
                FxdProject.load(path)
        project = FxdProject.load(LEGACY)
        document = load_step_for_workbench(project.product.source_bytes, source_name=project.product.source_name)
        ambiguous = replace(document, assembly=replace(document.assembly,
            components=document.assembly.components * 2))
        with self.assertRaisesRegex(ProjectFormatError, "alias is ambiguous"):
            _migrate_legacy_geometry_references(json.loads(LEGACY.read_bytes()), ambiguous, product_from_workbench_document(document))


class ClassificationFlowTests(unittest.TestCase):
    def test_explicit_roles_reach_provider_once_after_save_reload(self):
        for name, role in (("holed-plate", Role.PLATE_SHEET), ("tube", Role.TUBE_STRUCTURAL), ("formed", Role.FORMED)):
            with self.subTest(name=name):
                document, workflow = classified_case(name)
                offline = execute_design_mode(document, workflow, ExecutionMode.DETERMINISTIC_OFFLINE)
                project = offline.project
                self.assertTrue(project.product_reconstruction.blocked)
                provider = _LiveProvider(ai_response_from_proposal(offline.proposal))
                blocked = execute_design_mode(document, project.workflow, ExecutionMode.AI_DESIGN_LIVE,
                                              provider=provider, current_project=project)
                self.assertEqual(blocked.provenance.failure_category, FailureCategory.RECONSTRUCTION_BLOCKED)
                self.assertEqual(provider.request_count, 0)
                answered = project.with_classification_answer(document, project.product.components[0].identity, role)
                with tempfile.TemporaryDirectory() as directory:
                    restored = FxdProject.load(answered.save(Path(directory) / "answered.json"))
                outcome = execute_design_mode(document, restored.workflow, ExecutionMode.AI_DESIGN_LIVE,
                                              provider=provider, current_project=restored)
                self.assertEqual(provider.request_count, 1)
                self.assertEqual(outcome.provider_state, ProviderState.SUCCESS)
                self.assertEqual(outcome.project.product_reconstruction.components[0].manufacturing_classification, role)
                self.assertEqual(outcome.project.classification_decisions, answered.classification_decisions)
                cleared = outcome.project.with_classification_answer(document, project.product.components[0].identity, Role.UNKNOWN)
                self.assertTrue(cleared.product_reconstruction.blocked)
                self.assertIsNone(cleared.ai_execution)
                self.assertIsNone(cleared.fixture_proposal)
                again = _LiveProvider(provider.response)
                execute_design_mode(document, cleared.workflow, ExecutionMode.AI_DESIGN_LIVE, provider=again, current_project=cleared)
                self.assertEqual(again.request_count, 0)

    def test_context_change_clears_answers_and_source_or_component_mismatch_fails(self):
        document, workflow = classified_case()
        offline = execute_design_mode(document, workflow, ExecutionMode.DETERMINISTIC_OFFLINE)
        project = offline.project.with_classification_answer(document, offline.project.product.components[0].identity, Role.PLATE_SHEET)
        changed = replace(project.workflow, setup=replace(project.workflow.setup, manufacturing_process="TIG welding"))
        current = project.with_workflow(changed)
        self.assertFalse(current.classification_decisions)
        provider = _LiveProvider(failure=AssertionError("must not call"))
        outcome = execute_design_mode(document, changed, ExecutionMode.AI_DESIGN_LIVE, provider=provider, current_project=project)
        self.assertEqual(provider.request_count, 0)
        self.assertTrue(outcome.project.product_reconstruction.blocked)
        answer = project.classification_decisions[0]
        for changed_answer in (replace(answer, source_sha256="0" * 64), replace(answer, component_identity="different")):
            with self.assertRaisesRegex(ProjectFormatError, "stale or references unknown"):
                replace(project, classification_decisions=(changed_answer,))


class RepositoryPreflightTests(unittest.TestCase):
    def _run(self, remote, metadata=None, branch=None, dirty=""):
        responses = {("remote", "get-url", "origin"): remote,
                     ("branch", "--show-current"): branch or acceptance.EXPECTED_BRANCH,
                     ("rev-parse", "HEAD"): "a" * 40, ("status", "--porcelain"): dirty}
        if metadata is None:
            metadata = {"id": acceptance.EXPECTED_REPOSITORY_ID, "full_name": acceptance.EXPECTED_REPOSITORY}
        with patch.object(acceptance, "_git", side_effect=lambda *args: responses[args]), patch.object(
            acceptance.subprocess, "check_output", return_value=json.dumps(metadata)
        ), patch.object(acceptance, "OpenAiResponsesProvider", side_effect=AssertionError("no provider")):
            return acceptance.repository_preflight()

    def test_canonical_and_verified_former_alias(self):
        for remote in ("https://github.com/DumpsterFireWorks/fxd-fixture-design.git",
                       "git@github.com:DumpsterFireWorks/fxd-fixture-design.git",
                       "https://github.com/kool1160/fxd-fixture-design.git"):
            self.assertEqual(self._run(remote)[1], "a" * 40)

    def test_lookalikes_wrong_repository_branch_and_dirty_head_fail(self):
        canonical = "https://github.com/DumpsterFireWorks/fxd-fixture-design.git"
        for remote in (canonical + "-fake", canonical.replace("github.com", "github.com.evil"), canonical.replace("DumpsterFireWorks", "other")):
            with self.assertRaises(ValueError):
                self._run(remote)
        for kwargs in ({"metadata": {"id": 1, "full_name": acceptance.EXPECTED_REPOSITORY}},
                       {"branch": "main"}, {"dirty": " M changed.py"}):
            with self.assertRaises(ValueError):
                self._run(canonical, **kwargs)

    def test_unavailable_metadata_fails_without_provider_access(self):
        with patch.object(acceptance, "_git", return_value="https://github.com/kool1160/fxd-fixture-design.git"), patch.object(
            acceptance.subprocess, "check_output", side_effect=subprocess.CalledProcessError(1, "gh")
        ):
            with self.assertRaises(subprocess.CalledProcessError):
                acceptance.repository_preflight()

    def test_former_alias_must_still_resolve_to_same_repository(self):
        good = {"id": acceptance.EXPECTED_REPOSITORY_ID, "full_name": acceptance.EXPECTED_REPOSITORY}
        wrong = {"id": 1234, "full_name": "kool1160/fxd-fixture-design"}
        with patch.object(acceptance, "_git", return_value="https://github.com/kool1160/fxd-fixture-design.git"), patch.object(
            acceptance.subprocess, "check_output", side_effect=[json.dumps(good), json.dumps(wrong)]
        ):
            with self.assertRaisesRegex(ValueError, "alias no longer resolves"):
                acceptance.repository_preflight()
