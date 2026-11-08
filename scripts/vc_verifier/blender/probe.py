"""探针：在干净的 bpy 里执行一个候选 bpy 脚本，产出三类可比对的观测。

  .venv_bpy/bin/python probe.py <candidate.py> <outdir> [ref_probe.json]

  state.json   结构化状态（层级/变换/网格/修改器/材质节点/灯光相机/F-curve/约束/渲染设置）
  view_*.png   Workbench 多视角 RGBA（RGB=材质平光色，A=剪影）；view_0 用场景自己的相机
  points.npz   带颜色的表面采样点（世界坐标），给 Chamfer / F-score / 体素 IoU 用
  timing.json  各阶段耗时

给了 ref_probe.json 就复用参考解的相机和体素网格，保证同一坐标系下比对。
"""
import json, math, os, sys, time, traceback
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix

NVIEW, RES, NPTS = 9, 256, 60000


# ---------------------------------------------------------------- 状态读取
def xyz(v, n=4):
    return [round(float(x), n) for x in v]


def node_tree(nt):
    """材质节点树：节点类型表 + 连线（按类型命名，避开 Blender 自动改名）+ 关键 socket 默认值"""
    nodes = {n.name: n.bl_idname for n in nt.nodes}
    links = sorted(f"{nodes[l.from_node.name]}.{l.from_socket.name}->{nodes[l.to_node.name]}.{l.to_socket.name}"
                   for l in nt.links)
    defs = {}
    for n in nt.nodes:
        for s in n.inputs:
            if s.is_linked or not hasattr(s, "default_value"):
                continue
            v = s.default_value
            try:
                v = xyz(v) if hasattr(v, "__len__") else round(float(v), 4)
            except TypeError:
                continue
            defs[f"{n.bl_idname}.{s.name}"] = v
    return dict(nodes=sorted(nodes.values()), links=links, defaults=defs)


MOD_KEYS = ('width', 'segments', 'levels', 'render_levels', 'count',
            'relative_offset_displace', 'thickness', 'offset', 'angle_limit',
            'ratio', 'strength', 'factor', 'screw_offset', 'steps', 'deform_axis')


def mesh_stats(obj, dg):
    """基础网格 + 修改器求值后的网格两套统计。流形性/法线朝向只在求值后的网格上看"""
    out = {}
    for tag, o in (("base", obj), ("eval", obj.evaluated_get(dg))):
        me = o.to_mesh()
        me.calc_loop_triangles()
        bm = bmesh.new(); bm.from_mesh(me)
        out[tag] = dict(
            verts=len(me.vertices), edges=len(me.edges), faces=len(me.polygons),
            tris=len(me.loop_triangles),
            non_manifold_edges=sum(1 for e in bm.edges if not e.is_manifold),
            loose_verts=sum(1 for v in bm.verts if not v.link_edges),
            volume=round(bm.calc_volume(signed=True), 6),      # 负 = 法线整体朝内
            ngons=sum(1 for p in me.polygons if len(p.vertices) > 4),
            shade_smooth=bool(me.polygons and me.polygons[0].use_smooth),
        )
        bm.free(); o.to_mesh_clear()
    return out


def read_state():
    S = bpy.context.scene
    dg = bpy.context.evaluated_depsgraph_get()
    st = dict(objects={}, collections={}, render={}, world=None, materials={})

    for c in bpy.data.collections:
        st["collections"][c.name] = sorted(o.name for o in c.objects)
    st["collections"]["__scene_root__"] = sorted(o.name for o in S.collection.objects)

    for o in S.objects:
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box] or [o.matrix_world.translation]
        d = dict(
            type=o.type, parent=o.parent.name if o.parent else None,
            collections=sorted(c.name for c in o.users_collection),
            loc=xyz(o.matrix_world.translation),
            rot_deg=xyz([math.degrees(a) for a in o.matrix_world.to_euler()], 2),
            scale=xyz(o.matrix_world.to_scale()),
            bbox_min=xyz(np.min([xyz(b) for b in bb], axis=0)),
            bbox_max=xyz(np.max([xyz(b) for b in bb], axis=0)),
            materials=[m.name if m else None for m in o.data.materials] if getattr(o.data, "materials", None) else [],
            modifiers=[dict(name=m.name, type=m.type, show_render=m.show_render,
                            **{k: (xyz(getattr(m, k)) if hasattr(getattr(m, k), '__len__') else
                                   round(float(getattr(m, k)), 5) if isinstance(getattr(m, k), float) else getattr(m, k))
                               for k in MOD_KEYS if hasattr(m, k)})
                       for m in o.modifiers],
            constraints=[dict(type=c.type, target=getattr(getattr(c, 'target', None), 'name', None),
                              influence=round(c.influence, 3),
                              track_axis=getattr(c, 'track_axis', None), up_axis=getattr(c, 'up_axis', None))
                         for c in o.constraints],
            rigid_body=dict(type=o.rigid_body.type, mass=round(o.rigid_body.mass, 4),
                            shape=o.rigid_body.collision_shape) if o.rigid_body else None,
        )
        if o.type == 'MESH':
            d["mesh"] = mesh_stats(o, dg)
        if o.type == 'LIGHT':
            L = o.data
            d["light"] = dict(kind=L.type, energy=round(L.energy, 3), color=xyz(L.color, 3),
                              size=round(getattr(L, 'shadow_soft_size', getattr(L, 'angle', 0.0)), 4),
                              spot_size=round(math.degrees(L.spot_size), 2) if L.type == 'SPOT' else None)
        if o.type == 'CAMERA':
            C = o.data
            d["camera"] = dict(lens=round(C.lens, 3), type=C.type, sensor=round(C.sensor_width, 2),
                               clip=[round(C.clip_start, 4), round(C.clip_end, 2)],
                               dof=C.dof.use_dof, fstop=round(C.dof.aperture_fstop, 3),
                               is_active=(o is S.camera))
        if o.animation_data and o.animation_data.action:
            fc = {}
            for c in o.animation_data.action.fcurves:
                fc[f"{c.data_path}[{c.array_index}]"] = dict(
                    keys=[[round(k.co[0], 3), round(k.co[1], 5)] for k in c.keyframe_points],
                    interp=sorted({k.interpolation for k in c.keyframe_points}),
                    extrap=c.extrapolation)
            d["fcurves"] = fc
        st["objects"][o.name] = d

    for m in bpy.data.materials:
        st["materials"][m.name] = node_tree(m.node_tree) if m.use_nodes and m.node_tree else dict(nodes=[], links=[], defaults={})
    if S.world and S.world.use_nodes:
        st["world"] = node_tree(S.world.node_tree)

    R = S.render
    st["render"] = dict(engine=R.engine, res=[R.resolution_x, R.resolution_y, R.resolution_percentage],
                        fps=R.fps, frames=[S.frame_start, S.frame_end], film_transparent=R.film_transparent,
                        samples=getattr(S.cycles, 'samples', None) if R.engine == 'CYCLES'
                        else getattr(S.eevee, 'taa_render_samples', None),
                        view_transform=S.view_settings.view_transform, exposure=round(S.view_settings.exposure, 3))
    return st


# ------------------------------------------------------- 采样点（几何指标）
def hexcol(obj):
    ms = getattr(obj.data, "materials", None)
    if not ms or not ms[0] or not ms[0].use_nodes:
        return "808080"
    for n in ms[0].node_tree.nodes:
        s = n.inputs.get("Base Color") if n.inputs else None
        if s is not None and hasattr(s, "default_value"):
            return "".join(f"{int(round(min(max(c, 0), 1) ** (1 / 2.2) * 255)):02x}" for c in s.default_value[:3])
    return "808080"


def sample_points(n=NPTS):
    """按面积加权采样整场景表面点。每点带所属物体的材质基色，用于按色比对"""
    import trimesh
    np.random.seed(12345)                      # 采样要可复现，否则 IoU 自己抖
    dg = bpy.context.evaluated_depsgraph_get()
    parts, areas, cols = [], [], []
    for o in bpy.context.scene.objects:
        if o.type != 'MESH':
            continue
        ev = o.evaluated_get(dg)
        me = ev.to_mesh(); me.calc_loop_triangles()
        if not me.loop_triangles:
            ev.to_mesh_clear(); continue
        V = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", V)
        V = V.reshape(-1, 3)
        F = np.array([lt.vertices[:] for lt in me.loop_triangles], dtype=np.int64)
        M = np.array(ev.matrix_world)
        V = V @ M[:3, :3].T + M[:3, 3]
        tm = trimesh.Trimesh(vertices=V, faces=F, process=False)
        parts.append(tm); areas.append(float(tm.area)); cols.append(hexcol(o))
        ev.to_mesh_clear()
    if not parts:
        return np.zeros((0, 3)), np.array([])
    quota = np.maximum(1, (np.array(areas) / max(sum(areas), 1e-9) * n).astype(int))
    P, C = [], []
    for tm, q, c in zip(parts, quota, cols):
        p, _ = trimesh.sample.sample_surface(tm, int(q), seed=12345)
        P.append(p); C += [c] * len(p)
    return np.vstack(P), np.array(C)


# ---------------------------------------------------------------- 多视角渲染
def cameras(center, radius, n=NVIEW):
    out = []
    for i in range(n - 1):
        az, el = i * 2 * math.pi / (n - 1), math.radians(18)
        d = radius * 2.8
        out.append([center[0] + d * math.cos(el) * math.sin(az),
                    center[1] - d * math.cos(el) * math.cos(az),
                    center[2] + d * math.sin(el)])
    out.append([center[0] + 1e-3, center[1], center[2] + radius * 2.8])   # 俯视
    return out


def look_at(pos, target):
    f = (Vector(target) - Vector(pos)).normalized()
    up = Vector((0, 0, 1)) if abs(f.z) < 0.99 else Vector((0, 1, 0))
    r = f.cross(up).normalized(); u = r.cross(f)
    return Matrix([[r.x, u.x, -f.x], [r.y, u.y, -f.y], [r.z, u.z, -f.z]]).to_4x4()


def render_views(outdir, views):
    """Workbench 平光 + 透明底：RGB 给材质色，A 给剪影。view_0 用场景自己的相机"""
    S = bpy.context.scene
    keep = (S.render.engine, S.render.resolution_x, S.render.resolution_y,
            S.render.film_transparent, S.render.resolution_percentage, S.camera)
    S.render.engine = 'BLENDER_WORKBENCH'
    S.render.resolution_x = S.render.resolution_y = RES
    S.render.resolution_percentage = 100
    S.render.film_transparent = True
    S.render.image_settings.file_format, S.render.image_settings.color_mode = 'PNG', 'RGBA'
    sh = S.display.shading
    sh.light, sh.color_type, sh.show_shadows, sh.show_cavity = 'FLAT', 'MATERIAL', False, False
    for m in bpy.data.materials:        # Workbench 的 MATERIAL 取 viewport 色，这里从 Principled 基色同步过去
        if m.use_nodes and m.node_tree:
            for n in m.node_tree.nodes:
                s = n.inputs.get("Base Color") if n.inputs else None
                if s is not None and hasattr(s, "default_value"):
                    m.diffuse_color = tuple(s.default_value); break

    probe_cam = bpy.data.objects.new("__vc_cam", bpy.data.cameras.new("__vc_cam"))
    probe_cam.data.lens, probe_cam.data.sensor_width = 42.0, 36.0
    S.collection.objects.link(probe_cam)

    shots = []
    for i, v in enumerate([None] + views["pos"]):
        if v is None:
            if keep[5] is None:
                shots.append(None); continue
            S.camera = keep[5]
        else:
            S.camera = probe_cam
            probe_cam.matrix_world = Matrix.Translation(v) @ look_at(v, views["target"])
        S.render.filepath = os.path.join(outdir, f"view_{i}.png")
        bpy.ops.render.render(write_still=True)
        shots.append(S.render.filepath)

    bpy.data.objects.remove(probe_cam, do_unlink=True)
    (S.render.engine, S.render.resolution_x, S.render.resolution_y,
     S.render.film_transparent, S.render.resolution_percentage, S.camera) = keep
    return shots


# ---------------------------------------------------------------------- 主流程
def main(script, outdir, ref=None):
    os.makedirs(outdir, exist_ok=True)
    T, t0 = {}, time.time()
    err = None
    src = open(script).read()
    g = {"__name__": "__main__", "__file__": script}
    try:
        exec(compile(src, script, "exec"), g)
    except Exception:
        err = traceback.format_exc(limit=6)
    T["exec"] = round(time.time() - t0, 3)

    t = time.time(); state = read_state(); T["state"] = round(time.time() - t, 3)
    t = time.time(); P, C = sample_points(); T["sample"] = round(time.time() - t, 3)

    if ref:
        views, grid = ref["views"], np.array(ref["grid"])
    else:
        if len(P):
            lo, hi = P.min(0), P.max(0)
        else:
            lo, hi = np.zeros(3), np.ones(3)
        c, r = (lo + hi) / 2, float(np.linalg.norm(hi - lo) / 2) or 1.0
        views = dict(pos=cameras(c, r), target=[float(x) for x in c])
        grid = np.array([lo - 0.05 * r, hi + 0.05 * r])

    t = time.time(); render_views(outdir, views); T["render"] = round(time.time() - t, 3)
    T["total"] = round(time.time() - t0, 3)

    np.savez_compressed(os.path.join(outdir, "points.npz"), P=P.astype(np.float32), C=C)
    json.dump(dict(script=script, error=err, views=views, grid=grid.tolist(),
                   npoints=int(len(P)), colors=sorted(set(C.tolist())), timing=T, state=state),
              open(os.path.join(outdir, "state.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(T, open(os.path.join(outdir, "timing.json"), "w"))
    print(json.dumps(dict(out=outdir, err=bool(err), npoints=int(len(P)), timing=T)))


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("-")]
    if "--" in sys.argv:
        a = sys.argv[sys.argv.index("--") + 1:]
    main(a[0], a[1], json.load(open(a[2])) if len(a) > 2 else None)

