# Blender 无头多视角渲染实测。用法:
#   blender -b --factory-startup --python bench_blender.py -- ENGINE N_VIEWS RES SAMPLES THREADS
# ENGINE: BLENDER_WORKBENCH | CYCLES | BLENDER_EEVEE
import bpy, sys, math, time, json, os
a = sys.argv[sys.argv.index('--') + 1:]
eng, nv, res, spp, thr = a[0], int(a[1]), int(a[2]), int(a[3]), int(a[4])
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'blender')
os.makedirs(OUT, exist_ok=True)
t0 = time.time()
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
# 同 three.js 的桌子场景
bpy.ops.mesh.primitive_plane_add(size=20); bpy.context.object.name = 'floor'
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1)); top = bpy.context.object; top.name = 'table_top'; top.scale = (1.5, .8, .075)
for x, y in [(-1.35, -.65), (1.35, -.65), (-1.35, .65), (1.35, .65)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=.06, depth=1, location=(x, y, .5)); bpy.context.object.name = 'leg'
bpy.ops.mesh.primitive_torus_add(location=(0, 0, 1.45), major_radius=.25, minor_radius=.08); bpy.context.object.name = 'red_knot'
bpy.ops.object.shade_smooth()
mat = bpy.data.materials.new('red'); mat.use_nodes = True
mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (1, .1, .2, 1)
bpy.context.object.data.materials.append(mat)
bpy.ops.object.light_add(type='SUN', location=(5, 3, 8)); bpy.context.object.data.energy = 3
world = bpy.data.worlds.new('w'); sc.world = world; world.color = (.1, .12, .15)
bpy.ops.object.empty_add(location=(0, 0, 1)); tgt = bpy.context.object
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
sc.render.engine = eng
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = res, int(res * .75), 100
sc.render.image_settings.file_format = 'PNG'
if eng == 'CYCLES':
    sc.cycles.device = 'CPU'; sc.cycles.samples = spp; sc.cycles.use_denoising = False
    sc.render.threads_mode = 'FIXED'; sc.render.threads = thr
elif eng == 'BLENDER_EEVEE':
    sc.eevee.taa_render_samples = spp
setup = time.time() - t0
times = []
for i in range(nv):
    az = 2 * math.pi * i / nv; el = math.radians(25); r = 6
    cam.location = (r * math.cos(el) * math.sin(az), -r * math.cos(el) * math.cos(az), 1 + r * math.sin(el))
    sc.render.filepath = os.path.join(OUT, f'{eng}_{i}.png')
    t = time.time(); bpy.ops.render.render(write_still=True); times.append(round(time.time() - t, 3))
# scene graph 读取
t = time.time()
graph = [{'name': o.name, 'type': o.type, 'loc': [round(v, 3) for v in o.location], 'dims': [round(v, 3) for v in o.dimensions],
          'mats': [m.name for m in getattr(o.data, 'materials', []) if m]} for o in sc.objects]
gms = round((time.time() - t) * 1000, 2)
print('VCJSON ' + json.dumps({'engine': eng, 'res': f'{res}x{int(res*.75)}', 'spp': spp, 'threads': thr, 'setup_s': round(setup, 3),
      'per_view_s': times, 'total_render_s': round(sum(times), 2), 'scene_graph_ms': gms, 'n_objects': len(graph)}))

