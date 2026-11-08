"""变异测试：对参考解做一处改动，看每类信号能否区分「该判错」和「不该判错」。
  should=fail  语义变了（部件缺失、朝向反了、尺寸超规格、换色、灯灭、动画没了、倒角没做）
  should=pass  语义没变（建模路径、细分密度、相机机位、日光角度、未指定的微小参数）
判别力 = 该挂的挂了多少（检出）+ 不该挂的放过多少（保真）。

  python mutate.py            # 跑全部变异并出表
阈值写在 verify.TH，在跑变异之前就定死，不回头调。
"""
import json, subprocess, sys, time
from pathlib import Path
import verify

HERE = Path(__file__).parent
TASK = HERE / "tasks/desk_lamp"
PY = str(HERE.parent / ".venv_bpy/bin/python")

TORUS = """bpy.ops.mesh.primitive_torus_add(major_radius=0.030, minor_radius=0.006,
                                 major_segments=24, minor_segments=8)
put(bpy.context.object, "MugHandle", C_MUG, CERAMIC, loc=(0.405, -0.12, 0.84),
    rot=(math.radians(90), 0, 0))"""
ANIM = """arm.rotation_euler.x = math.radians(-20); arm.keyframe_insert("rotation_euler", index=0, frame=1)
arm.rotation_euler.x = math.radians(15);  arm.keyframe_insert("rotation_euler", index=0, frame=40)
arm.rotation_euler.x = math.radians(-20)"""
BEVEL = """bev = top.modifiers.new("Bevel", 'BEVEL')
bev.width, bev.segments = 0.01, 3"""
CUBE = """bpy.ops.mesh.primitive_cube_add(size=1)
top = put(bpy.context.object, "Tabletop", C_DESK, WOOD, loc=(0, 0, 0.75), scale=(1.2, 0.8, 0.05))"""

MUTANTS = [
    # 该判错
    ("mug_handle_missing", TORUS, "", "fail"),
    ("shade_flipped",      "rot=(math.radians(125), 0, 0))", "rot=(math.radians(55), 0, 0))", "fail"),
    ("table_thin",         "scale=(1.2, 0.8, 0.05))", "scale=(1.2, 0.8, 0.02))", "fail"),
    ("leg_count_3",        "[(0.55, 0.35), (-0.55, 0.35), (0.55, -0.35), (-0.55, -0.35)]",
                           "[(0.55, 0.35), (-0.55, 0.35), (0.55, -0.35)]", "fail"),
    ("wood_blue",          'mat("Wood", (0.35, 0.20, 0.09), 0.60, 0.0)',
                           'mat("Wood", (0.10, 0.18, 0.45), 0.60, 0.0)', "fail"),
    ("bulb_dim",           "60.0, (1.0, 0.85, 0.65), 0.03", "6.0, (1.0, 0.85, 0.65), 0.03", "fail"),
    ("anim_missing",       ANIM, "arm.rotation_euler.x = math.radians(-20)", "fail"),
    ("bevel_removed",      BEVEL, "", "fail"),
    # 不该判错
    ("cube_size2",         CUBE, 'bpy.ops.mesh.primitive_cube_add(size=2)\n'
                                 'top = put(bpy.context.object, "Tabletop", C_DESK, WOOD, '
                                 'loc=(0, 0, 0.75), scale=(0.6, 0.4, 0.025))', "pass"),
    ("leg_verts_32",       "vertices=16, radius=0.04, depth=0.75", "vertices=32, radius=0.04, depth=0.75", "pass"),
    ("mug_seg_48",         "vertices=32, radius=0.045, depth=0.11", "vertices=48, radius=0.045, depth=0.11", "pass"),
    ("camera_moved",       "cam.location = (2.2, -2.6, 1.9)", "cam.location = (-2.4, -2.2, 2.1)", "pass"),
    ("sun_rot",            "rot=(math.radians(35), math.radians(12), math.radians(25))",
                           "rot=(math.radians(42), math.radians(5), math.radians(18))", "pass"),
    ("wood_rough_0.62",    'mat("Wood", (0.35, 0.20, 0.09), 0.60, 0.0)',
                           'mat("Wood", (0.35, 0.20, 0.09), 0.62, 0.0)', "pass"),
    ("leg_radius_+2.5%",   "vertices=16, radius=0.04, depth=0.75", "vertices=16, radius=0.041, depth=0.75", "pass"),
]

# 留出集：combo 的成员（收哪几族断言）是看过上面这批的分族表之后定的，所以必须换一批复验。
# 这批里刻意放了两个「题干没写死、但断言族照样会查」的改动，用来暴露断言白名单必须按题干裁剪。
HOLDOUT = [
    ("mug_moved",        "loc=(0.35, -0.12, 0.83)", "loc=(0.05, 0.22, 0.83)", "fail"),
    ("subsurf_off",      'sub = body.modifiers.new("Subdivision", \'SUBSURF\')\nsub.levels = sub.render_levels = 1', "", "fail"),
    ("cam_lens_24",      "cam.data.lens = 50.0", "cam.data.lens = 24.0", "fail"),
    ("torus_minor_12",   "major_segments=24, minor_segments=8", "major_segments=24, minor_segments=12", "pass"),
    ("mug_pos_jitter",   "loc=(0.35, -0.12, 0.83)", "loc=(0.355, -0.125, 0.83)", "pass"),
    ("sun_energy_3.5",   "sun.energy, sun.angle = 3.0", "sun.energy, sun.angle = 3.5", "pass"),
    ("coll_renamed",     'coll("Desk"), coll("Lamp"), coll("Mug")', 'coll("Table"), coll("Lamp"), coll("Mug")', "pass"),
]

SIGNALS = ["combo", "combo+A5", "view0", "mv_mask", "mv_rgb", "chamfer", "fscore", "vox", "geom_all", "mv+vox",
           "state_A1", "state_A2", "state_A3", "state_A4", "state_A5", "state_A6",
           "state_A7", "state_A8", "state_A9", "state_all"]


def probe(script, out, ref=None):
    t = time.time()
    cmd = [PY, str(HERE / "probe.py"), str(script), str(out)] + ([str(ref)] if ref else [])
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if r.returncode:
        print(r.stderr[-2000:]); raise RuntimeError(script)
    return round(time.time() - t, 2)


def main(MUTANTS, tag="mutation"):
    mdir = TASK / "mut"; mdir.mkdir(exist_ok=True)
    src = (TASK / "ref.py").read_text()
    for name, a, b, _ in MUTANTS:
        assert a in src, f"pattern not found: {name}"
        (mdir / f"{name}.py").write_text(src.replace(a, b, 1))

    runs = HERE / "runs/desk_lamp"
    t_ref = probe(TASK / "ref.py", runs / "ref")
    rows, times = [], []
    for name, _, _, should in MUTANTS:
        times.append(probe(mdir / f"{name}.py", runs / name, runs / "ref/state.json"))
        s = verify.score(runs / "ref", runs / name)
        v = verify.verdicts(s)
        rows.append(dict(name=name, should=should, raw=s,
                         verdict={k: ("pass" if v[k] else "fail") for k in SIGNALS}))
        print(f"{name:20s} {should:4s} " + " ".join(k for k in SIGNALS if not v[k])[:110])

    print(f"\nprobe 单次耗时 ref={t_ref}s 变异 {min(times)}~{max(times)}s 均值 {sum(times)/len(times):.2f}s")
    nf = sum(r["should"] == "fail" for r in rows)
    print(f"\n{'信号':12s} {'总判对':>7s} {'检出(该挂)':>12s} {'保真(不该挂)':>14s}")
    for k in SIGNALS:
        hit = sum(r["verdict"][k] == "fail" for r in rows if r["should"] == "fail")
        keep = sum(r["verdict"][k] == "pass" for r in rows if r["should"] == "pass")
        print(f"{k:12s} {hit+keep:3d}/{len(rows):<3d} {hit:6d}/{nf:<5d} {keep:8d}/{len(rows)-nf:<5d}")
    json.dump(rows, open(runs / f"{tag}.json", "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    if "--holdout" in sys.argv:
        main(HOLDOUT, "holdout")
    else:
        main(MUTANTS, "mutation")

