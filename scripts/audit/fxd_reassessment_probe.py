import sys, json, argparse
from pathlib import Path
from dataclasses import replace
parser = argparse.ArgumentParser(description='Offline FXD audit observations, not a pass/fail acceptance test')
parser.add_argument('--phase', choices=('main', 'held'), required=True)
parser.add_argument('--artifact-dir', type=Path, required=True)
args = parser.parse_args()
args.artifact_dir.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(Path.cwd()))
from fxd_geometry import *
from fxd_geometry.project import FxdProject
from fxd_geometry.validation import _kernel_findings
from fxd_geometry.manufacturing import ManufacturingGeometry, ManufacturingSolid
from fxd_geometry.ai_fixture_engineer import UnavailableAiProvider

def emit(name, value):
    print('AUDIT_RESULT ' + json.dumps({'case': name, 'result': value}, sort_keys=True))

kernel = OcpKernel()
source = kernel.export_step(kernel.make_box((0,0,0),(120,80,8)))
doc = load_step_for_workbench(source, source_name='audit-synthetic-plate.step')
product = product_from_workbench_document(doc)
component = product.components[0]
body = component.bodies[0]
ref = GeometryReference(component.identity, body.identity)
contacts = tuple(LocatorContact(name, role, ref, Vec3(x+10000,y+10000,z+10000), Vec3(*normal))
    for name,role,x,y,z,normal in [
      ('a','rest',0,0,0,(0,0,1)),('b','rest',20,0,0,(0,0,1)),
      ('c','rest',0,20,0,(0,0,1)),('d','stop',0,0,0,(1,0,0)),
      ('e','stop',0,20,0,(1,0,0)),('f','diamond_pin',0,0,0,(0,1,0))])
analysis = analyze_locating_strategy(product, LocatingStrategy(contacts, datum_assumptions=('audit synthetic datum',)))
emit('off_part_contacts', {'rank': analysis.rank, 'strategy_valid': analysis.strategy_valid,
    'findings':[x.code for x in analysis.findings], 'contact_minimum_mm':10000, 'part_maximum_mm':120})

multi = import_step(Path('tests/fixtures/synthetic_assembly.step'))
multiref = GeometryReference('BRACKET_A','BRACKET_BODY')
multicontacts = tuple(replace(x, reference=multiref) for x in contacts)
multianalysis = analyze_locating_strategy(multi,LocatingStrategy(multicontacts,datum_assumptions=('audit',)))
emit('unlocated_other_components', {'component_count':len(multi.components),'contacted_components':['BRACKET_A'],
    'rank':multianalysis.rank,'strategy_valid':multianalysis.strategy_valid})

annotations = EngineeringAnnotations.for_product(product, build_orientation=Vec3(0,0,1),loading_direction=Vec3(1,0,0),process_type='MIG',production_quantity=20)
concept = generate_fixture_concepts(product, annotations).concepts[0]
requirements = FixtureBuildRequirements(product.source_sha256, FixturePurpose.FULL_WELD,
    ConstructionMethod.LASER_CUT_FABRICATED, FixtureLifecycle.STORE_AND_REUSE,'A','A',20,'repeat','MIG',
    ('machining',),True,True,True,AdjustmentState.LOCKED)
plan = generate_fixture_build_plan(product,concept,requirements)
validation = validate_fixture_build_plan(product,plan)
authored = author_fixture_build(plan,product,kernel)
overlaps=[]
for item in authored.components:
    if kernel.intersects(doc.shape,item.shape):
        overlaps.append(item.component.identity)
emit('m30_build_collision', {'status':validation.status,'findings':[x.message for x in validation.findings],
    'overlapping_authored_components':overlaps,'authored_count':len(authored.components)})

box1=kernel.make_box((0,0,0),(10,10,10)); box2=kernel.make_box((2,2,2),(8,8,8))
solids=tuple(ManufacturingSolid(i,k,'machined','steel',1,'fit',0.5,0,interface,(),shape)
    for i,k,interface,shape in [('base','baseplate','unrelated-A',box1),('pad','support_pad','unrelated-B',box2)])
geometry=ManufacturingGeometry('audit',product.source_sha256,'mm',('base','pad'),solids,kernel.compound((box1,box2)),source,b'0\nSECTION\n0\nENDSEC\n0\nEOF\n')
emit('interface_overlap', {'kernel_overlap':kernel.intersects(box1,box2),'clearance_mm':kernel.clearance(box1,box2),
    'findings':[x.code for x in _kernel_findings(geometry,kernel,0.5)]})

def workflow_for(document):
    comp=document.assembly.components[0]
    a=next(f for f in comp.faces if f.is_planar and abs(f.normal[2])>0.9)
    b=next(f for f in comp.faces if f.is_planar and abs(f.normal[1])>0.9)
    prod=product_from_workbench_document(document)
    def ref_for(face):
        owner=next(b for b in prod.components[0].bodies if any(f.identity==face.reference for f in b.faces))
        return GeometryReference(prod.components[0].identity,owner.identity,face.reference)
    orient=orientation_from_faces(document,ref_for(a),ref_for(b),accepted=True)
    setup=ProcessSetup('audit',fixture_type='Full weld fixture',manufacturing_process='MIG welding',operation_mode='Manual',
        production_quantity=20,fixture_lifecycle='Store and reuse',manufacturing_orientation=orient,
        manufacturing_build_direction=Vec3(0,0,1),manufacturing_loading_direction=Vec3(1,0,0),manufacturing_unloading_direction=Vec3(-1,0,0))
    return InteractiveWorkflow(document.source_sha256,setup,geometry_annotations=(face_annotation(document,ref_for(b),AnnotationRole.WELD_JOINT,notes='synthetic'),))

workflow=workflow_for(doc)
offline=generate_fixture_proposal(doc,workflow,provider=UnavailableAiProvider())
request=build_ai_request(offline.project)
emit('provider_context', {'keys':sorted(request.context.keys()) if hasattr(request,'context') else sorted(request.to_dict().keys()),
    'contains_reconstruction': 'reconstruction' in json.dumps(request.to_dict()),
    'contains_images':'input_image' in json.dumps(request.to_dict())})
if args.phase == 'main':
    offline.project.save(str(args.artifact_dir / 'audit-genuine-v5.fxd.json'))
    own_reload=FxdProject.load(str(args.artifact_dir / 'audit-genuine-v5.fxd.json'))
    replace(offline.project,fixture_proposal=None).save(str(args.artifact_dir / 'audit-genuine-v5-no-proposal.fxd.json'))
    emit('genuine_v5_saved', {'format':offline.project.to_dict()['format'],'source_sha256':product.source_sha256,'main_reload_succeeded':True})
else:
    try:
        restored=FxdProject.load(str(args.artifact_dir / 'audit-genuine-v5.fxd.json'))
        emit('genuine_v5_load',{'format':restored.to_dict()['format'],'source_sha256':restored.product.source_sha256,
             'annotations':len(restored.workflow.geometry_annotations)})
    except Exception as exc:
        emit('genuine_v5_load',{'error_type':type(exc).__name__,'error':str(exc)})
    try:
        no_proposal=FxdProject.load(str(args.artifact_dir / 'audit-genuine-v5-no-proposal.fxd.json'))
        emit('genuine_v5_without_proposal_load',{'succeeded':True})
    except Exception as exc:
        emit('genuine_v5_without_proposal_load',{'error':str(exc)})
    hole_shape=kernel.cut(kernel.make_box((0,0,0),(120,80,8)),kernel.make_cylinder((60,40,-1),5,10))
    holedoc=load_step_for_workbench(kernel.export_step(hole_shape),source_name='audit-holed-plate.step')
    holeworkflow=workflow_for(holedoc)
    holeoff=execute_design_mode(holedoc,holeworkflow,ExecutionMode.DETERMINISTIC_OFFLINE)
    resolved=reconstruct_product(holedoc,holeoff.project.product,holeoff.project.workflow,
        classification_overrides={holeoff.project.product.components[0].identity:ManufacturingClassification.PLATE_SHEET})
    class FakeProvider:
        identity='openai'; engine_identifier='audit-fake'; available=True; request_count=0
        def generate(self,*args,**kwargs):
            self.request_count+=1
            raise RuntimeError('No network allowed in audit')
    fake=FakeProvider()
    outcome=execute_design_mode(holedoc,holeworkflow,ExecutionMode.AI_DESIGN_LIVE,provider=fake,
        current_project=holeoff.project.with_product_reconstruction(resolved))
    emit('classification_override_lost',{'resolved_before_execution':not resolved.blocked,
        'classification_after_execution':outcome.project.product_reconstruction.components[0].manufacturing_classification.value,
        'failure':outcome.provenance.failure_category.value,'fake_provider_calls':fake.request_count})
