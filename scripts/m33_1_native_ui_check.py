"""Native Windows PySide6/VTK/OCP acceptance for the three M33.1 mode states.

This is intentionally separate from ordinary CI.  It uses synthetic geometry
and fake provider responses; the distinct live-provider acceptance script owns
the single paid request.
"""
from __future__ import annotations

import json
import argparse
from pathlib import Path
import sys
import tempfile
from time import monotonic

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fxd_geometry import (  # noqa: E402
    ExecutionMode, ai_response_from_proposal, execute_design_mode,
)
from fxd_qt_app import FxdWorkbenchWindow, create_application  # noqa: E402
from scripts.m33_1_self_check import synthetic_workflow  # noqa: E402


class MissingConfiguration:
    identity = "openai"
    engine_identifier = ""
    available = False
    request_count = 0


class SyntheticLiveProvider:
    identity = "openai"
    engine_identifier = "explicit-native-ui-proof-model"
    available = True

    def __init__(self, response):
        self.response = response
        self.request_count = 0
        self.last_usage = None

    def generate(self, request, *, timeout_seconds, cancellation):
        cancellation.raise_if_cancelled()
        self.request_count += 1
        return self.response


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screenshot", type=Path)
    args = parser.parse_args()
    app = create_application([])
    window = FxdWorkbenchWindow()
    try:
        _, document, workflow = synthetic_workflow(holed=True)
        window.document = document
        window.workflow = workflow
        window._set_process_setup(workflow.setup)
        window.viewport.load_document(document)
        window.show()
        window._refresh_all()
        app.processEvents()

        window.reconstruction_inspect.click()
        assert window.project.product_reconstruction.blocked
        assert "Confirm the manufacturing role" in window.classification_question.text()
        window.classification_answer.setCurrentIndex(window.classification_answer.findData("plate_sheet"))
        window.classification_apply.click()
        assert not window.project.product_reconstruction.blocked

        offline = execute_design_mode(
            document, window.workflow, ExecutionMode.DETERMINISTIC_OFFLINE,
            current_project=window.project,
        )
        window._replace_project(offline.project)
        window._refresh_all()
        app.processEvents()
        offline_label = window.ai_mode_banner.text()

        failed = execute_design_mode(
            document, offline.project.workflow, ExecutionMode.AI_DESIGN_LIVE,
            provider=MissingConfiguration(), current_project=offline.project,
        )
        window._replace_project(failed.project)
        window._refresh_all()
        app.processEvents()
        failed_label = window.ai_mode_banner.text()

        provider = SyntheticLiveProvider(ai_response_from_proposal(offline.proposal))
        window.ai_provider = provider
        window.proposal_execution_mode.setCurrentIndex(window.proposal_execution_mode.findData(ExecutionMode.AI_DESIGN_LIVE.value))
        window.proposal_generate.click()
        deadline = monotonic() + 30
        from PySide6.QtTest import QTest
        while window._proposal_tasks and monotonic() < deadline:
            app.processEvents()
            QTest.qWait(10)
        assert not window._proposal_tasks, "synthetic proposal UI execution timed out"
        assert window.project.ai_execution.request_count == 1
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "answered.fxd.json"
            window.save_project_path(path)
            window.load_project_path(path)
        assert window.classification_answer.currentData() == "plate_sheet"
        assert window.project.product.source_bytes == document.source_bytes
        window._refresh_all()
        app.processEvents()
        live_label = window.ai_mode_banner.text()
        diagnostics = window.viewport.diagnostics()

        assert offline_label == "DETERMINISTIC / OFFLINE — NO LIVE AI REQUEST"
        assert failed_label == "AI DESIGN — FAILED — NO FALLBACK USED"
        assert live_label == (
            "AI DESIGN — LIVE — openai / explicit-native-ui-proof-model"
        )
        assert provider.request_count == 1
        assert diagnostics is not None and diagnostics.native_rendering_active
        assert not diagnostics.fallback_active
        if args.screenshot is not None:
            window._navigate_stage("Proposal")
            app.processEvents()
            assert window.grab().save(str(args.screenshot))
        print(json.dumps({
            "schema": "fxd-m33-1-native-ui-check-v1",
            "offline_label": offline_label,
            "failed_label": failed_label,
            "live_label": live_label,
            "render_backend": diagnostics.backend,
            "native_rendering_active": diagnostics.native_rendering_active,
            "fallback_active": diagnostics.fallback_active,
            "actors": diagnostics.actor_count,
            "points": diagnostics.point_count,
            "source_sha256": document.source_sha256,
            "synthetic_provider_requests": provider.request_count,
            "classification_question_answer_execution_reload": "passed",
        }, sort_keys=True))
        return 0
    finally:
        window.close()
        app.processEvents()


if __name__ == "__main__":
    raise SystemExit(main())
