"""Generate real v5 evidence using only pinned pre-M33 application code.

Run with Python 3.12 from a checkout with full Git history and pinned OCP.
No provider requests; all geometry is a synthetic plate.
"""
import io
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

BASELINE = "801aad49f4c5e5fac4626fe18576717d71d19580"
ROOT = Path(__file__).resolve().parents[2]

GENERATOR = r'''
from pathlib import Path
import sys
from fxd_geometry import *
from fxd_geometry.ai_fixture_engineer import UnavailableAiProvider
from fxd_geometry.project import FxdProject
kernel = OcpKernel()
source = kernel.export_step(kernel.make_box((0,0,0),(120,80,8)))
document = load_step_for_workbench(source, source_name="synthetic-legacy-v5.step")
product = product_from_workbench_document(document)
component = product.components[0]
faces = document.assembly.components[0].faces
bottom = next(f for f in faces if abs(f.normal[2]) > .9)
front = next(f for f in faces if abs(f.normal[1]) > .9)
def reference(face):
    return GeometryReference(component.identity, component.bodies[0].identity, face.reference)
orientation = orientation_from_faces(document, reference(bottom), reference(front), accepted=True)
setup = ProcessSetup("legacy-v5", fixture_type="Full weld fixture",
    manufacturing_process="MIG welding", operation_mode="Manual",
    production_quantity=10, volume_category="Low", fixture_lifecycle="Store and reuse",
    manufacturing_orientation=orientation, manufacturing_build_direction=Vec3(0,0,1),
    manufacturing_loading_direction=Vec3(1,0,0), manufacturing_unloading_direction=Vec3(-1,0,0))
workflow = InteractiveWorkflow(document.source_sha256, setup, geometry_annotations=(
    face_annotation(document, reference(front), AnnotationRole.WELD_JOINT, notes="Synthetic weld"),))
outcome = generate_fixture_proposal(document, workflow, provider=UnavailableAiProvider())
project = outcome.project.decide_fixture_proposal("rejected", "Synthetic historical review")
project = project.edit_parameter("base_thickness", 14, "Synthetic retained edit")
requirements = FixtureBuildRequirements(product.source_sha256, FixturePurpose.FULL_WELD,
    ConstructionMethod.LASER_CUT_FABRICATED, FixtureLifecycle.STORE_AND_REUSE,
    'A', 'A', 10, 'repeat', 'MIG', ('machining',), True, True, True, AdjustmentState.LOCKED)
project = project.with_fixture_build(generate_fixture_build_plan(product, project.active, requirements))
path = project.save(Path(sys.argv[1]))
assert project.to_dict()["format"] == "fxd-neutral-project-v5"
assert FxdProject.load(path).product.source_bytes == source
'''

if __name__ == "__main__":
    archive = subprocess.check_output(
        ["git", "archive", BASELINE, "fxd_geometry"], cwd=ROOT,
    )
    with tempfile.TemporaryDirectory(prefix="fxd-legacy-generator-") as directory:
        with tarfile.open(fileobj=io.BytesIO(archive)) as source:
            source.extractall(directory, filter="data")
        script = Path(directory) / "generate.py"
        script.write_text(GENERATOR, encoding="utf-8")
        subprocess.run([sys.executable, str(script), str(
            Path(__file__).with_name("m33_genuine_v5.fxd.json")
        )], cwd=directory, check=True)
