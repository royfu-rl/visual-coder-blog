# 10 Blender / bpy 可验证任务的批量合成

调研与实测日期 2026-10-15。实测环境：KML pod，cgroup 约 47.9 核，无 GPU、无 /dev/dri、无 DISPLAY。
用的是 `scripts/vc_verifier/.venv_bpy`（bpy 4.5.14 LTS + numpy 1.26.4 + pillow 10.4 + trimesh 4.4.9 + scipy 1.14.1），
系统另有 apt 的 Blender 4.0.2。本篇所有数字都来自本机跑出来的 `scripts/vc_verifier/blender/runs/desk_lamp/`。

代码全部在 `/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/blender/`：

```
tasks/desk_lamp/ref.py   参考解（一个 bpy 脚本，题干写在 docstring 里）
probe.py                 探针：干净 bpy 里 exec 候选脚本 → 状态 JSON + 多视角图 + 带色采样点
geom.py                  Chamfer / F-score / 按色体素 IoU
verify.py                九族状态断言 + 图像信号 + 判定阈值
mutate.py                变异测试（开发集 15 个，留出集 7 个）
summarize.py             从已有 runs/ 重算所有信号出表
vlm_judge.py             VLM 判图对照（4 个 judge × 单图/多视角）
```

---

## 0. 结论速览

- **三类信号互补，谁也替代不了谁。** 本机 22 个变异（11 个该挂 / 11 个不该挂）上：
  | 信号 | 总判对 | 检出（该挂） | 保真（不该挂） |
  |---|---|---|---|
  | 只看一张截图 view0 | 12/22 | 2/11 | 10/11 |
  | 多视角剪影 IoU | 14/22 | 3/11 | 11/11 |
  | 全局 Chamfer | 13/22 | 2/11 | 11/11 |
  | 全局 F-score | 11/22 | **0/11** | 11/11 |
  | 按色体素 IoU | 15/22 | 4/11 | 11/11 |
  | **分部件 F-score** | 18/22 | 7/11 | 11/11 |
  | 全量状态断言（九族全查） | 11/22 | 11/11 | **0/11** |
  | **分部件几何 + 四族断言（combo_pc）** | **21/22** | **11/11** | **10/11** |

- **全量 bpy 断言是个陷阱。** 九族全查能抓住 11/11 个真错，但 11 个「语义没变」的改写全部误杀，判别力等于零。
  误杀集中在两族：A2 变换（把 `cube(size=1)+scale 1.2` 改写成 `cube(size=2)+scale 0.6`，世界形状一模一样，但 `obj.scale` 变了）
  和 A3 网格统计（圆柱 16 段改 32 段、torus minor_segments 8 改 12，顶点数全变）。
- **几何信号必须分部件算，全局平均量是废的。** 同一批变异上，全局 F-score 检出 0/11；
  按材质色分组、取最差那组的 F-score 检出 7/11 且零误杀。
  原因是量纲：杯子只占全场表面积的约 2%，把它平移 30 cm，**全局 Chamfer 只从 0 动到 0.00018**（归一化后），
  分部件 Chamfer 则是 0.084（差 460 倍）。
- **渲染图能抓的和断言能抓的几乎不重叠。** 本机实测，只有断言能抓的：点光源 60 W 调成 6 W、
  F-curve 关键帧整条删掉、倒角修改器去掉（1 cm 倒角在 2.18 m 对角线的场景里低于采样分辨率）、相机焦距 50 mm 改 24 mm。
  只有渲染/几何能抓的：部件朝向反了、小部件挪位、细分修改器去掉导致外形鼓了一圈。
- **断言的字段白名单必须按题干裁。** 留出集唯一的误杀是「日光功率 3.0 调成 3.5」——
  题干只写了「加一盏日光」没写死功率，A6 却照查不误。
  正确做法是题干生成时就产出**被钉死的字段清单**，verifier 只查清单内的字段（见 §2.1）。
- **四条合成路线里，立刻能跑量的是「参数扰动 → 改回去」。** 它天然自带标签（扰动参数就是答案），
  不需要人写断言，单个任务生成 + 验证在本机只要约 2.3 秒。
- **成本很低。** 单次探针（exec 脚本 + 读状态 + 6 万点采样 + 10 个视角 Workbench 渲染）总计 1.6 ~ 2.4 秒，
  其中几何指标三项合计 0.25 秒。RL rollout 的每步观测塞得下。

---

## 1. bpy 状态断言能查什么

把能程序化检查的属性分成九族。每族给：读法（代码片段）、能验证哪类需求、本机实测的判别力。
完整实现见 `probe.py: read_state()` 与 `verify.py: families()`。

公共前置：

```python
import bpy, bmesh, math
from mathutils import Vector
S  = bpy.context.scene
dg = bpy.context.evaluated_depsgraph_get()   # 修改器求值后的结果都要从这里取
```

### A1 物体层级与命名

```python
# 名字集合、父子关系、所属集合（collection）
for o in S.objects:
    print(o.name, o.type, o.parent.name if o.parent else None,
          sorted(c.name for c in o.users_collection))
for c in bpy.data.collections:
    print(c.name, sorted(o.name for o in c.objects))
```

- **能验证**：「场景里必须有且只有 X 个 Y」「把灯和桌子分到两个集合里」「轮子要 parent 到车身」
  「导入的资产不能留在 Scene Collection 根上」。也能兜底查「有没有留下多余的临时物体」。
- **实测**：开发集检出 2/8（杯把手整个没建、桌腿从 4 条变 3 条），保真 7/7。
  留出集保真 3/4 —— 误杀的是「把集合名 Desk 改成 Table」，题干根本没规定集合名。

### A2 变换（位置 / 旋转 / 缩放）

```python
o = bpy.data.objects["Tabletop"]
loc   = o.matrix_world.translation            # 世界坐标，而不是 o.location
rot   = [math.degrees(a) for a in o.matrix_world.to_euler()]
scale = o.matrix_world.to_scale()
bb    = [o.matrix_world @ Vector(c) for c in o.bound_box]   # 世界包围盒 8 个角
```

- **能验证**：「杯子要放在桌面上、不许穿模」（比 bbox 的 z 下沿与桌面 z 上沿）、
  「四条腿要在桌面四角」、「物体朝向镜头」、「整体尺寸 1.2 × 0.8 米」。
- **坑**：一定要走 `matrix_world`，不要直接读 `o.location` / `o.scale`。
  同一个长方体可以用 `primitive_cube_add(size=1)` + `scale=(1.2,0.8,0.05)` 做，
  也可以 `size=2` + `scale=(0.6,0.4,0.025)` 做，世界几何逐点相同但 `o.scale` 差一倍。
  本机实测这正是 A2 的第一个误杀来源。
- **实测**：开发集检出 2/8、保真 4/7（误杀 cube_size2 / 相机移位 / 日光转角）。
  **结论：A2 不要直接比 loc/rot/scale，要比世界包围盒，或干脆交给几何指标。**

### A3 网格统计（顶点 / 面 / 流形 / 法线）

```python
ev = o.evaluated_get(dg)          # 带修改器的结果
me = ev.to_mesh(); me.calc_loop_triangles()
bm = bmesh.new(); bm.from_mesh(me)
stats = dict(
    verts = len(me.vertices), edges = len(me.edges), faces = len(me.polygons),
    tris  = len(me.loop_triangles),
    non_manifold_edges = sum(1 for e in bm.edges if not e.is_manifold),
    loose_verts        = sum(1 for v in bm.verts if not v.link_edges),
    ngons              = sum(1 for p in me.polygons if len(p.vertices) > 4),
    volume             = bm.calc_volume(signed=True),   # 负号 = 法线整体朝内
    shade_smooth       = me.polygons[0].use_smooth,
)
bm.free(); ev.to_mesh_clear()
```

- **能验证**：「模型必须是水密的（可以 3D 打印 / 做布尔）」→ `non_manifold_edges == 0`；
  「法线要朝外」→ `volume > 0`；「不许有游离顶点 / 重复顶点」；
  「全四边面拓扑」→ `ngons == 0 and tris == 2 * faces`；「面数不超过 5000」→ 性能预算类需求。
- **判别力提醒**：**绝对不要把顶点数当成等式断言**。本机实测 A3 保真只有 3/7 和 3/4，
  四个误杀全是「同样的形状换了细分密度」。顶点数只适合写成**不等式预算**（`verts <= N`）
  或**不变量**（流形性、法线朝向、四边面比例）。
- **实测**：开发集检出 1/8、保真 3/7；留出集检出 1/3、保真 3/4。单独用是最差的一族。

### A4 修改器栈（类型与参数）

```python
for m in o.modifiers:
    print(m.name, m.type, m.show_render,
          getattr(m, 'width', None), getattr(m, 'segments', None),
          getattr(m, 'levels', None), getattr(m, 'count', None))
```

- **能验证**：「桌面边缘要倒角，宽 1 cm、3 段」「杯身加一级 Subdivision」
  「用 Array 复制 12 份，间距 1.5」「Solidify 厚度 2 mm」「Decimate 到 30%」。
  这一族最有价值的地方是：**修改器的效果常常在渲染图里看不出来，但题干写死了它。**
- **实测**：开发集检出 1/8（倒角被删——这个变异在剪影 IoU 0.9831、分部件 F-score 0.9992 上全部漏掉，
  只有 A4 和 A3 抓到），保真 7/7；留出集检出 1/3（Subdivision 被删）、保真 4/4。
  **A4 是保真率满分且能抓住渲染盲区的族，必须进最终判据。**

### A5 材质节点树结构

```python
nt = bpy.data.materials["Wood"].node_tree
nodes = sorted(n.bl_idname for n in nt.nodes)                       # 按类型，不按名字
links = sorted(f"{l.from_node.bl_idname}.{l.from_socket.name}"
               f"->{l.to_node.bl_idname}.{l.to_socket.name}" for l in nt.links)
bsdf  = nt.nodes["Principled BSDF"]
base  = list(bsdf.inputs["Base Color"].default_value)   # 线性 RGBA
rough = bsdf.inputs["Roughness"].default_value
metal = bsdf.inputs["Metallic"].default_value
```

- **能验证**：「做一个金属材质」→ `Metallic == 1.0`；「加一张 Noise Texture 驱动粗糙度」→ 连线里有
  `ShaderNodeTexNoise.Fac -> ShaderNodeBsdfPrincipled.Roughness`；「玻璃要带 IOR 1.45」；
  「贴图走 Non-Color 色彩空间」（`img.colorspace_settings.name`）。
- **坑**：**按 `bl_idname` 比，不要按 `node.name` 比**。Blender 会把同名节点自动改成 `Mix.001`，
  按名字比等于在比随机串。
- **实测**：检出 1/8（木色改蓝）、保真 6/7。唯一误杀是「粗糙度 0.60 调成 0.62」正好卡在 0.02 的容差边界上
  —— 题干没写死粗糙度，这个字段本来就不该查（见 §2.1 的字段白名单）。

### A6 灯光与相机参数

```python
L = bpy.data.objects["Bulb"].data
print(L.type, L.energy, list(L.color), L.shadow_soft_size)          # POINT/SUN/SPOT/AREA
print(math.degrees(L.spot_size) if L.type == 'SPOT' else None)
C = bpy.data.objects["Camera"].data
print(C.lens, C.type, C.sensor_width, C.clip_start, C.clip_end,
      C.dof.use_dof, C.dof.aperture_fstop, bpy.data.objects["Camera"] is S.camera)
```

- **能验证**：「三点布光：主光 1000 W、补光 300 W、轮廓光在背后」「点光源 60 W 暖色」
  「相机 50 mm、开景深 f/2.8」「正交相机」「把这台相机设为活动相机」。
- **为什么必须有这一族**：**光照强度在 Workbench 平光渲染里完全看不见**，
  在 Cycles 里也会被色调映射压掉。本机 `bulb_dim`（60 W → 6 W）变异的所有图像与几何信号都是 1.0000，
  只有 A6 抓到。相机焦距 50 → 24 同理（几何信号全 1.0，只有 A6 和单图 view0 抓到）。
- **实测**：开发集检出 1/8、保真 7/7；留出集检出 1/3、保真 3/4（误杀日光功率 3.0 → 3.5，题干没写死）。

### A7 动画 F-curve

```python
act = o.animation_data.action
for c in act.fcurves:
    print(c.data_path, c.array_index, c.extrapolation,
          [(k.co[0], k.co[1], k.interpolation) for k in c.keyframe_points])
# 也可以直接按帧求值：
val = c.evaluate(20)
```

- **能验证**：「第 1 帧到第 40 帧绕 X 轴从 -20° 转到 15°」「关键帧必须是线性插值」
  「循环外推（`extrapolation == 'CYCLIC'`）」「25 fps、1 秒的动画」。
  也能查驱动器：`o.animation_data.drivers[i].driver.expression`。
- **为什么必须有**：**渲染单帧的 verifier 对动画完全失明。** 本机 `anim_missing`（两条关键帧整条删掉）
  的 view0 / 多视角 / Chamfer / 体素 IoU 全部是 1.0000，只有 A7 抓到。
  要用渲染抓动画，得渲一整段序列，成本至少翻 N 倍。
- **实测**：检出 1/8、保真 7/7 和 4/4，两批都是满分保真。

### A8 物理与约束

```python
for c in o.constraints:
    print(c.type, getattr(c, 'target', None), c.influence,
          getattr(c, 'track_axis', None), getattr(c, 'up_axis', None))
rb = o.rigid_body          # None 或者刚体设置
if rb: print(rb.type, rb.mass, rb.collision_shape, rb.friction, rb.restitution)
print(o.rigid_body_constraint, [m.type for m in o.modifiers if m.type in {'CLOTH','SOFT_BODY','FLUID'}])
```

- **能验证**：「相机要用 Track To 始终对准目标」「把 12 个球设成刚体、质量 1 kg、凸包碰撞」
  「布料加碰撞」「IK 链」「Copy Rotation 影响度 0.5」。
- **实测**：本批变异里没有针对 A8 的改动，所以检出 0/11，保真 11/11。
  列在这里是因为它是「渲染静帧完全看不见、只能靠断言」的另一大类，跟 A7 同性质。

### A9 场景渲染设置

```python
R = S.render
print(R.engine, R.resolution_x, R.resolution_y, R.resolution_percentage,
      R.fps, S.frame_start, S.frame_end, R.film_transparent)
print(S.cycles.samples if R.engine == 'CYCLES' else S.eevee.taa_render_samples)
print(S.view_settings.view_transform, S.view_settings.exposure,
      R.image_settings.file_format, R.image_settings.color_depth)
```

- **能验证**：「用 Cycles、32 采样、512×512」「开透明底导 PNG」「色彩管理用 Standard 不要 Filmic/AgX」
  「输出 16 bit EXR」「渲染 1 到 40 帧」。
- **实测**：检出 0/11（本批没造这类变异），保真 11/11。
  这一族几乎零风险：题干写死了就查，没写死就不查，判定是精确相等，不需要容差。

### 九族速查

| 族 | 查什么 | 开发集 检出/保真 | 留出集 检出/保真 | 进最终判据 |
|---|---|---|---|---|
| A1 层级命名 | 物体集合、父子、collection | 2/8、7/7 | 0/3、3/4 | 条件进（只查题干点名的物体） |
| A2 变换 | loc / rot / scale | 2/8、**4/7** | 1/3、3/4 | **不进**（改用世界 bbox 或几何指标） |
| A3 网格统计 | 顶点面数、流形、法线 | 1/8、**3/7** | 1/3、3/4 | **不进等式**；只留不变量与预算不等式 |
| A4 修改器栈 | 类型顺序 + 参数 | 1/8、7/7 | 1/3、4/4 | **进** |
| A5 材质节点 | 节点图 + socket 默认值 | 1/8、6/7 | 0/3、4/4 | 条件进（只查题干钉死的 socket） |
| A6 灯光相机 | energy / color / lens | 1/8、7/7 | 1/3、3/4 | **进**（按字段白名单） |
| A7 F-curve | 通道、关键帧、插值 | 1/8、7/7 | 0/3、4/4 | **进** |
| A8 物理约束 | constraint / rigid body | 0/8、7/7 | 0/3、4/4 | **进** |
| A9 渲染设置 | 引擎、分辨率、采样 | 0/8、7/7 | 0/3、4/4 | **进** |
| 九族全查 | — | 8/8、**0/7** | 3/3、**0/4** | 反面教材 |

---

## 2. 任务合成的四条路线

四条路线的共同产物格式（和 `scripts/vc_verifier/blender/` 的实现一一对应）：

```
task/
  prompt.md      题干（自然语言 + 可选参考图）
  spec.json      被钉死的字段清单（verifier 只查这些）
  ref.py         参考解 bpy 脚本（或者 ref.blend）
  probe/         参考解的探针输出：state.json / view_*.png / points.npz
```

`spec.json` 是四条路线都绕不开的东西。本机实测里唯一的留出集误杀
（日光功率 3.0 → 3.5 被 A6 判错）就是因为没有它：题干没写死的字段，verifier 不该查。

### 2.1 路线一：程序化生成场景 → 反推自然语言需求

**思路**：先随机出一组结构化参数，用确定性的生成器把场景搭出来，再把参数**翻译**成题干。
参数即真值，`spec.json` 直接从参数表导出，不需要人工写断言。参考 Infinigen（BSD-3，`src/infinigen/assets`
下 568 个 py 文件，约 246 个生成器）与 SceneCraft（2403.01248，场景图 + 人写的空间约束打分函数，
去掉内循环约束分掉 38.4 分）。

**方案**

```
1. 定义一个「场景模板」= 槽位表
   slots = {房间尺寸, 家具种类×N, 摆放关系, 材质族, 灯光方案, 相机, 动画}
   每个槽位带：取值域、是否可见（渲染能不能看出来）、归属断言族
2. 采样一组参数 p ~ Uniform(槽位域)，加硬约束（不穿模、在桌面上、在视锥内）
3. build(p) → bpy 场景，确定性（固定随机种子）
4. 题干 = 把 p 里「被钉死」的那部分渲染成中文/英文句子
   spec.json = 这部分槽位 → (族, 字段路径, 容差)
   没被写进题干的槽位（例如日光功率）不进 spec，verifier 不查
5. 难度控制 = 钉死的槽位个数 + 槽位之间的依赖深度
```

**伪代码**

```python
SLOTS = [
    Slot("table.size",   dom=[(0.8,2.0),(0.5,1.2)], family="A2", tol=0.005, phrase="一张 {0}×{1} 的木桌"),
    Slot("table.bevel",  dom=[(0.005,0.03)],        family="A4", tol=0.02,  phrase="桌面边缘倒角 {0}"),
    Slot("bulb.energy",  dom=[(20,200)],            family="A6", tol=0.02,  phrase="点光源 {0} W"),
    Slot("arm.anim",     dom=[(-40,0),(0,40)],      family="A7", tol=0.01,  phrase="灯臂第 1~40 帧从 {0}° 转到 {1}°"),
    Slot("mug.subsurf",  dom=[0,1,2],               family="A4", tol=0,     phrase="杯身加 {0} 级细分"),
]

def synth(seed, k_pinned):
    rng = Random(seed)
    p   = {s.name: s.sample(rng) for s in SLOTS}
    while not feasible(p):            # 穿模 / 出视锥 / 体积为负，重采样
        p = {s.name: s.sample(rng) for s in SLOTS}
    pinned = rng.sample(SLOTS, k_pinned)
    prompt = "。".join(s.phrase.format(*p[s.name]) for s in pinned)
    spec   = [dict(family=s.family, path=s.path, value=p[s.name], tol=s.tol) for s in pinned]
    ref_py = emit_bpy(p)              # 模板化代码生成，确定性
    return prompt, spec, ref_py
```

**优点**：量无上限、标签零成本、难度可调、许可干净（自己写的生成器）。
**缺点**：同质化严重 —— Infinigen 的代码是人写死的约 4 万行，变化全在随机参数里
（09_pretrain_data.md 已记：一对 1080p 立体图要 3.5 小时 wall time，直接当 code→render 配对数据会严重同质化）。
**解法**：生成器只负责出**目标场景**，不负责出参考代码；让模型自己写实现路径，verifier 比状态不比代码。
本机实测支持这个选择：`cube_size2` 这种「换一条实现路径、世界几何逐点相同」的改写，
几何信号全部放行（分部件 F-score 0.9993），只有按代码比的 A2/A3 会误杀。

### 2.2 路线二：对已有 .blend 做参数扰动 → 任务是「改回去」

**思路**：取一个现成场景当目标，程序化扰动若干参数得到起始场景，任务 = 从起始改回目标。
扰动参数本身就是「错在哪」的标签。BlenderGym（2504.01786，245 对）就是这么造的，
12_self_verification.md §已记：**扰动即监督**。

**原料**：Blender 官方 `tests/files/render/` 下 839 个 .blend（48 个类别，实查目录名见附录），
再加 Poly Haven 的 2,387 个 CC0 资产。

**方案**

```
1. 载入 target.blend，跑探针拿 state_target（九族全量）
2. 从「可扰动算子表」里抽 1~k 个算子作用在 target 上 → start.blend
   算子表按族分：
     A2  平移/旋转/缩放某个物体
     A4  删掉某个修改器 / 改一个参数 / 调换栈序
     A5  改 Base Color / Roughness / Metallic / 断开一条连线
     A6  改 energy / color / lens / 把活动相机换掉
     A7  删关键帧 / 改插值 / 平移整条曲线
     A8  删 constraint / 改 target
     A9  改引擎 / 采样 / 分辨率
3. 题干 = 「这是起始场景，这是目标渲染图（多视角），写 bpy 脚本改成目标」
   spec.json = 被扰动的那几个字段（精确已知）+ 容差
4. verifier = 跑候选脚本 → 探针 → 只比 spec 里的字段 + 分部件几何
```

**伪代码**

```python
OPS = [("A4", drop_modifier), ("A4", jitter_modifier_param), ("A2", move_object),
       ("A5", shift_base_color), ("A6", scale_light_energy), ("A7", drop_keyframes),
       ("A8", drop_constraint), ("A9", change_samples)]

def make_task(blend, seed, k=2):
    bpy.ops.wm.open_mainfile(filepath=blend)
    tgt = read_state()
    rng, touched = Random(seed), []
    for fam, op in Random(seed).sample(OPS, k):
        touched.append(op(rng))               # op 返回 (字段路径, 原值, 新值)
    bpy.ops.wm.save_as_mainfile(filepath=start_blend)
    spec = [dict(family=f, path=p, value=old, tol=TOL[f]) for (f, (p, old, _)) in zip(..., touched)]
    return start_blend, tgt, spec
```

**为什么这条路线最先做**：标签是**构造出来的**，不是判出来的，所以 verifier 不需要人写断言；
难度直接由 k 控制；单个任务的生成 + 验证在本机只要约 2.3 秒。
**坑**：扰动必须**可被观测**。本机实测里 `bevel_removed`（去掉 1 cm 倒角）在所有几何与图像信号上都通过，
只有 A4 抓到 —— 如果你的 verifier 只比渲染图，这类扰动造出来就是**无解噪声任务**。
所以扰动算子表里的每一项，必须先在探针上验证「它确实会改变某个被查的信号」，改不动的要丢掉。

### 2.3 路线三：从 GitHub 的 bpy 脚本挖「脚本 + 渲染图」，再做需求反推

**现状**：09_pretrain_data.md 已记一条重要事实 —— **没有发现任何公开工作在做 bpy 脚本的批量挖掘**，
BlenderLLM / BlendNet 走的是 GPT-4o 合成（12,059 行，Apache-2.0）。这本身是信号：
GitHub 上的 bpy 脚本大多依赖仓库里的 .blend、资产路径、add-on，**开箱即跑率很低**。

**方案**（把「能跑」当成第一道闸）

```
1. 拉候选：GitHub code search `import bpy` + 仓库 topic blender-python(575) / blender-addon(2323)
2. 闸 1 可执行性：在干净容器里 `blender -b --factory-startup --python s.py`
   超时 120 s、禁网、禁写盘到脚本目录之外。只留 returncode==0 且 bpy.data.objects 非空的
3. 闸 2 自给自足：脚本不读外部文件（静态扫 open/bpy.ops.wm.open_mainfile/import_scene）
4. 闸 3 有产出：探针跑完，场景里 mesh 面数 > 0、有相机或者可以自动补相机
5. 需求反推：把探针的 state.json（结构化，不是截图）+ 4 视角拼图喂给强模型，
   让它写题干。题干只允许引用 state 里出现过的字段 → 自动得到 spec.json
6. 闸 4 可解性：用一个弱一档的模型按题干重写一遍，verifier 判分；
   全 0 的题干太难（信息不足）丢掉，全 1 的太简单丢掉，留中间档
```

**伪代码**

```python
def harvest(repo_script):
    if not runs_clean(repo_script):            return None       # 闸 1
    if reads_external(repo_script):            return None       # 闸 2
    st = probe(repo_script)
    if st["state"] is empty or no_mesh(st):    return None       # 闸 3
    prompt, pinned = llm_write_prompt(st, contact_sheet(st))     # 只准引用 st 里的字段
    spec = [f for f in pinned if f in st]                        # 反查，防幻觉字段
    p = [solve_rate(prompt, spec, model=weak) for _ in range(8)]
    return None if mean(p) in (0, 1) else Task(prompt, spec, repo_script, st)   # 闸 4
```

**判断**：这条路线的产出率会很低（闸 1 和闸 2 会砍掉大部分），但它是**唯一能带进真实世界写法**的路线
（程序化生成和扰动都只会产出「生成器风格」的代码）。建议当**多样性补充**，不当主力。
许可上 GPL 污染要单独评估：Blender 本体是 GPL，但 bpy 脚本的许可跟随它所在的仓库。

### 2.4 路线四：官方 render tests 的「场景 + 参考图」直接改造成 F2P

**为什么这条最硬**：阈值和比对工具都是官方现成的，不用自己定。
实查 `tests/python/modules/render_report.py`（main 分支，2026-10-15 拉取）：

```python
# render_report.py 第 319~320 行：默认判定阈值
self.fail_threshold = 0.016
self.fail_percent   = 1
# 第 149~157 行：实际比对命令
command = (oiiotool, test.ref_img, test.tmp_out_img,
           "--fail", str(fail_threshold), "--failpercent", str(fail_percent), "--diff")
```

也就是：**单像素误差超过 0.016 的像素不得超过 1%**，否则判失败。
`cycles_render_tests.py` 与 `workbench_render_tests.py` 都调了 `report.set_pixelated(True)`，
并按设备 / OSL 维护 BLOCKLIST（`BLOCKLIST_GPU` / `BLOCKLIST_OPTIX` / `BLOCKLIST_METAL` / `BLOCKLIST_VULKAN` 等）。

**原料规模**（02_task_sources.md 实测 + 本次 Gitea API 复查）：
`tests/files/render/` 下 **48 个类别目录**（attributes / bake / bsdf / camera / displacement / hair /
instancing / light / motion_blur / principled_bsdf / shader / shadow / sss / volume / workbench ...），
839 个 .blend、2,596 张参考 png（cycles / eevee / workbench 各一套）。

**改造成 F2P 的做法**

```
1. 取一个 (scene.blend, ref.png, engine) 三元组
2. 用 2.2 的扰动算子把 scene.blend 弄坏 → broken.blend
   验收条件：用官方阈值比对，broken 渲染出来必须 FAIL（0.016 / 1% 判据）
   —— 这一步把「改不动的扰动」自动筛掉，比人工判断可靠
3. 任务 = 给 broken.blend + ref.png（可以只给图，不给参数），要求写脚本修复
4. verifier = 官方 oiiotool 判据（F2P 的 P）+ 探针的 spec 字段（F2P 的 F）
5. 反向 P2P 守卫：再取同类别另外 3 个场景当「不该被改坏」的回归集
```

**伪代码**

```python
def to_f2p(blend, ref_png, engine, seed):
    broken, spec = perturb(blend, seed)                      # 复用 2.2 的算子表
    img = render(broken, engine)
    if oiio_diff(ref_png, img, fail=0.016, failpercent=1) == "PASS":
        return None                                          # 扰动没生效，丢掉
    return Task(start=broken, gold_img=ref_png, spec=spec,
                verifier=lambda out: oiio_diff(ref_png, render(out, engine)) == "PASS"
                                     and spec_check(out, spec))
```

**坑**
- **渲染必须可复现**。官方测试跑在固定设备上；换 CPU / 换 Mesa 版本像素会漂。
  实际做法是**自己重渲一张参考图当基线**（用任务容器里那套引擎），不要直接用仓库里的 png。
- **Cycles 的采样噪声**。本机实测 Cycles CPU 512×512 / 32 spp 约 0.9 秒一帧；
  要降噪声只能加 spp，成本线性涨。F2P 任务建议用 Workbench 或低 spp + 固定 `cycles.seed`。
- **许可**：Blender 仓库是 GPL，`tests/files` 并入主仓库（LFS，全目录 7,240 个文件）。
  场景文件当**评测集**风险低，当**训练数据**要法务过一遍。

### 四条路线的取舍

| 路线 | 量级 | 标签成本 | 真实感 | 许可 | 建议 |
|---|---|---|---|---|---|
| 一 程序化生成 → 反推需求 | 无上限 | 零（参数即真值） | 低（生成器风格） | 干净 | 主力产能，但要配多模板防同质化 |
| 二 参数扰动 → 改回去 | 839 场景 × k 个扰动 × 种子 | 零（扰动即标签） | 中 | 需评估 GPL | **先做这条**，最快跑通闭环 |
| 三 GitHub 脚本挖掘 | 低产出率 | 高（要反推 + 筛题） | **高** | 逐仓库评估 | 当多样性补充 |
| 四 官方 render tests F2P | 839 场景 | 低（官方阈值现成） | 中 | GPL，训练用要法务 | 最适合当**评测集**和阈值校准集 |

---

## 3. 判别力实测

### 3.1 实验设计

和 three.js 版（`scripts/vc_verifier/proto/mutate.py`，13 个变异）同一套方法：
对参考解做**一处**改动，人工标注 `should`，看每类信号能否区分「该判错」和「不该判错」。

- **场景**：`tasks/desk_lamp/ref.py`（约 110 行 bpy 脚本）。
  木桌（桌面 + 4 腿 + 1 cm 倒角）+ 金属台灯（底座 + 斜臂 + 锥形灯罩 + 60 W 暖色点光源）
  + 白陶瓷杯（杯身带一级 Subdivision + 把手环）+ 50 mm 相机（Track To 约束）+ 日光
  + 灯臂 1~40 帧的旋转关键帧 + Cycles 512×512 / 32 spp。
  故意覆盖九个断言族，场景对角线 2.18 m，共 10 个物体。
- **信号**：
  - `view0` 只看场景自带相机的一张图（最常见的 2D verifier）
  - `mv_mask` / `mv_rgb` verifier 自己摆 9 个相机（8 方位 × 仰角 18° + 1 俯视）的剪影 IoU / 彩色图相似度
  - `chamfer` / `fscore` / `vox` 全局 Chamfer、全局 F-score、按色表面体素 IoU
  - `geom_pc` 分部件（按材质色分组）F-score 取最差组
  - `state_A1`~`state_A9` 九个断言族各自判
  - `combo_pc` = `geom_pc` ∧ `A4` ∧ `A6` ∧ `A7` ∧ `A9`
- **阈值**：写在 `verify.py: TH`，**在跑变异之前定死**。参考解自己跑两遍，所有信号逐位相同
  （图像 1.0000、Chamfer 0.0、体素 IoU 1.0），**噪声地板是 0**，所以阈值不能从噪声推，
  只能按「什么算语义等价」来定：图像 0.995 / 剪影 IoU 0.97 / Chamfer ≤ 0.004 diag / 体素 IoU ≥ 0.80。
- **两批变异**：
  - **开发集 15 个**（8 该挂 / 7 不该挂）——`combo` 的成员是看了这一批的分族表之后选的。
  - **留出集 7 个**（3 该挂 / 4 不该挂）——选完之后才造的，用来复验，**不回头调阈值**。

### 3.2 开发集（15 个变异）

| 变异 | should | view0 | mv_mask | chamfer | 全局 F | vox 最差色 | 分部件 F | 唯一抓到它的信号 |
|---|---|---|---|---|---|---|---|---|
| mug_handle_missing 杯把手没建 | fail | 0.9999 | 0.9988 | 0.00146 | 0.9995 | 0.923 | **0.9268** | 分部件 F / A1 |
| shade_flipped 灯罩转反 | fail | 0.9981 | **0.9280** | 0.00039 | 0.9847 | **0.763** | **0.7141** | 多视角 / 体素 / 分部件 F |
| table_thin 桌面 5 cm 变 2 cm | fail | 0.9977 | **0.9289** | **0.00487** | 1.0000 | 0.934 | **0.3428** | 多视角 / Chamfer / 分部件 F |
| leg_count_3 桌腿少一条 | fail | 0.9967 | **0.8766** | **0.00644** | 0.9704 | 0.930 | **0.9650** | 多视角 / Chamfer / A1 |
| wood_blue 木色改蓝 | fail | **0.9844** | 1.0000 | 0.00000 | 1.0000 | **0.000** | **0.0000** | 体素 / mv_rgb / A5 |
| bulb_dim 点光源 60 W → 6 W | fail | 1.0000 | 1.0000 | 0.00000 | 1.0000 | 1.000 | 1.0000 | **只有 A6** |
| anim_missing 关键帧删光 | fail | 1.0000 | 1.0000 | 0.00000 | 1.0000 | 1.000 | 1.0000 | **只有 A7** |
| bevel_removed 倒角修改器删掉 | fail | 0.9999 | 0.9831 | 0.00165 | 1.0000 | 0.927 | 0.9992 | **只有 A4 / A3** |
| cube_size2 换一条建模路径 | pass | 0.9999 | 0.9937 | 0.00155 | 1.0000 | 0.948 | 0.9993 | 被 A2/A3 误杀 |
| leg_verts_32 圆柱 16 段 → 32 段 | pass | 0.9999 | 0.9961 | 0.00166 | 1.0000 | 0.930 | 0.9990 | 被 A3 误杀 |
| mug_seg_48 杯身 32 段 → 48 段 | pass | 1.0000 | 1.0000 | 0.00111 | 1.0000 | 1.000 | 0.9992 | 被 A3 误杀 |
| camera_moved 相机换机位 | pass | **0.9534** | 1.0000 | 0.00000 | 1.0000 | 1.000 | 1.0000 | **被 view0 误杀** |
| sun_rot 日光转个角度 | pass | 1.0000 | 1.0000 | 0.00000 | 1.0000 | 1.000 | 1.0000 | 被 A2 误杀 |
| wood_rough_0.62 粗糙度 0.60 → 0.62 | pass | 1.0000 | 1.0000 | 0.00000 | 1.0000 | 1.000 | 1.0000 | 被 A5 误杀（容差边界） |
| leg_radius_+2.5% 腿粗 4 cm → 4.1 cm | pass | 0.9997 | 0.9921 | 0.00168 | 1.0000 | 0.938 | 0.9989 | 被 A3 误杀 |

分族汇总（粗体是该族的失败项）：

| 信号 | 总判对 | 检出 8 个该挂 | 保真 7 个不该挂 |
|---|---|---|---|
| view0 | 7/15 | 1 | 6 |
| mv_mask | 10/15 | 3 | 7 |
| mv_rgb | 10/15 | 3 | 7 |
| chamfer | 9/15 | 2 | 7 |
| fscore（全局，tau=1% diag） | 7/15 | **0** | 7 |
| vox 按色体素 | 9/15 | 2 | 7 |
| geom_pc 分部件 F | 12/15 | 5 | 7 |
| state_A1 | 9/15 | 2 | 7 |
| state_A2 | 6/15 | 2 | **4** |
| state_A3 | 4/15 | 1 | **3** |
| state_A4 | 8/15 | 1 | 7 |
| state_A5 | 7/15 | 1 | 6 |
| state_A6 | 8/15 | 1 | 7 |
| state_A7 | 8/15 | 1 | 7 |
| state_A8 / A9 | 7/15 | 0 | 7 |
| **state_all 九族全查** | 8/15 | **8** | **0** |
| **combo_pc** | **15/15** | **8** | **7** |

### 3.3 留出集（7 个变异，选完判据之后才造）

| 变异 | should | view0 | mv_mask | chamfer | vox 最差色 | 分部件 F | combo_pc |
|---|---|---|---|---|---|---|---|
| mug_moved 杯子挪 30 cm | fail | 0.9993 | 0.9934 | **0.00018** | **0.078** | **0.2243** | 判错 ✓ |
| subsurf_off 细分修改器删掉 | fail | 0.9997 | 0.9968 | 0.00169 | **0.533** | **0.6242** | 判错 ✓ |
| cam_lens_24 相机 50 mm → 24 mm | fail | 0.9611 | 1.0000 | 0.00000 | 1.000 | 1.0000 | 判错 ✓（靠 A6） |
| torus_minor_12 把手细分变密 | pass | 1.0000 | 1.0000 | 0.00110 | 1.000 | 0.9992 | 放行 ✓ |
| mug_pos_jitter 杯子抖 5 mm | pass | 1.0000 | 0.9993 | 0.00002 | **0.828** | 1.0000 | 放行 ✓ |
| sun_energy_3.5 日光 3.0 → 3.5 | pass | 1.0000 | 1.0000 | 0.00000 | 1.000 | 1.0000 | **误杀 ✗** |
| coll_renamed 集合改名 | pass | 1.0000 | 1.0000 | 0.00000 | 1.000 | 1.0000 | 放行 ✓ |

| 信号 | 总判对 | 检出 3 个 | 保真 4 个 |
|---|---|---|---|
| view0 | 5/7 | 1 | 4 |
| mv_mask / mv_rgb / chamfer / fscore | 4/7 | **0** | 4 |
| vox / geom_pc | 6/7 | 2 | 4 |
| state_all 九族全查 | 3/7 | 3 | **0** |
| **combo_pc** | **6/7** | **3** | **3**（误杀 sun_energy） |

**留出集验证到的三件事**

1. `combo_pc` 没有在换一批变异后崩掉：检出仍是满的（3/3），误杀 1 个。
2. 误杀的原因不是阈值错，是**查了题干没钉死的字段**（日光功率）。
   修法是 §2.1 的 `spec.json` 字段白名单，不是调容差。
3. 剪影 IoU 在留出集上检出 **0/3**，比开发集还差。
   `mug_moved`（杯子在桌面上挪 30 cm）的 `mv_mask` 是 0.9934，因为杯子在剪影里只占几十个像素。
   **剪影 IoU 对小部件天生不敏感，不能当主判据。**

### 3.4 合并 22 个变异

| 信号 | 总判对 | 检出 11 个该挂 | 保真 11 个不该挂 |
|---|---|---|---|
| view0 单图 | 12/22 | 2 | 10 |
| mv_mask 多视角剪影 | 14/22 | 3 | 11 |
| mv_rgb 多视角彩色 | 14/22 | 3 | 11 |
| chamfer 全局 | 13/22 | 2 | 11 |
| fscore 全局 | 11/22 | 0 | 11 |
| vox 按色体素 | 15/22 | 4 | 11 |
| geom_pc 分部件 F | 18/22 | 7 | 11 |
| state_A1 | 12/22 | 2 | 10 |
| state_A2 | 10/22 | 3 | 7 |
| state_A3 | 8/22 | 2 | 6 |
| state_A4 | 13/22 | 2 | 11 |
| state_A5 | 11/22 | 1 | 10 |
| state_A6 | 12/22 | 2 | 10 |
| state_A7 | 12/22 | 1 | 11 |
| state_A8 / A9 | 11/22 | 0 | 11 |
| state_all | 11/22 | 11 | **0** |
| **combo_pc** | **21/22** | **11** | **10** |

### 3.5 耗时

单次探针（exec 候选脚本 + 读九族状态 + 6 万点表面采样 + 10 个视角 Workbench 渲染 256×256）：

| 阶段 | 耗时 |
|---|---|
| exec 候选 bpy 脚本 | 0.23 ~ 0.30 s |
| 读九族状态（10 个物体，含 bmesh 流形检查） | 0.07 ~ 0.15 s |
| 表面采样 59,992 点（trimesh） | 0.15 ~ 0.21 s |
| Workbench 渲染 10 视角 256×256 | 1.09 ~ 1.24 s（首视角 0.49 s 含 shader 编译，之后每视角约 0.09 s） |
| **单次探针合计** | **1.61 ~ 2.43 s（均值 2.3 s）** |
| 22 个变异全跑（含重建参考解） | 约 70 s |
| 从已有 runs/ 重算全部信号（不重跑 bpy） | 12.8 s / 22 个 |

对比 three.js 版（06_harness.md §4.1）：复用浏览器后约 14 任务/s。
Blender 这边没做进程复用，单进程 2.3 s/任务；bpy 首帧 shader 编译占 0.49 s，
**常驻进程池能把它摊掉**，预计可到 1.3 s/任务以内。

---

## 4. 几何指标：Chamfer / F-score / IoU 在 Blender 场景上怎么做

### 4.1 实现路线

Blender 里没有现成的 Chamfer。实测可行的做法是 **bpy 取求值后的网格 → trimesh 面积加权采样 → scipy KD 树**。
不要用 `bpy.ops` 的布尔求交来算 IoU（慢且对非水密网格会炸）。

```python
import numpy as np, trimesh, bpy
from scipy.spatial import cKDTree

def sample_scene(n=60000, seed=12345):
    """整场景按面积加权采表面点，每点带所属物体的材质基色"""
    dg = bpy.context.evaluated_depsgraph_get()
    parts, areas, cols = [], [], []
    for o in bpy.context.scene.objects:
        if o.type != 'MESH': continue
        ev = o.evaluated_get(dg)                 # 关键：带修改器的结果
        me = ev.to_mesh(); me.calc_loop_triangles()
        V = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", V)
        V = V.reshape(-1, 3)
        F = np.array([lt.vertices[:] for lt in me.loop_triangles], dtype=np.int64)
        M = np.array(ev.matrix_world); V = V @ M[:3, :3].T + M[:3, 3]      # 转世界坐标
        tm = trimesh.Trimesh(vertices=V, faces=F, process=False)
        parts.append(tm); areas.append(tm.area); cols.append(base_color_hex(o))
        ev.to_mesh_clear()
    quota = np.maximum(1, (np.array(areas) / sum(areas) * n).astype(int))
    P = [trimesh.sample.sample_surface(tm, int(q), seed=seed)[0] for tm, q in zip(parts, quota)]
    C = np.array(sum(([c] * q for c, q in zip(cols, quota)), []))
    return np.vstack(P), C
```

三个指标都按**场景包围盒对角线 diag 归一化**，换场景不用重调阈值（本例 diag = 2.180 m）：

```python
def chamfer(A, B, diag):                      # 双向均值
    da = cKDTree(B).query(A)[0] / diag
    db = cKDTree(A).query(B)[0] / diag
    return (da.mean() + db.mean()) / 2

def fscore(A, B, diag, tau):                  # A=候选 B=参考
    p = (cKDTree(B).query(A)[0] / diag < tau).mean()    # precision
    r = (cKDTree(A).query(B)[0] / diag < tau).mean()    # recall
    return 2 * p * r / (p + r)

def vox_iou(Pr, Cr, Pc, Cc, grid, n=32):      # 表面占据体素，不要求 watertight
    key = lambda P: np.floor((P - grid[0]) / (grid[1] - grid[0]) * n).astype(int) @ [n*n, n, 1]
    kr, kc = key(Pr), key(Pc)
    return {c: len(set(kr[Cr==c]) & set(kc[Cc==c])) / len(set(kr[Cr==c]) | set(kc[Cc==c]))
            for c in set(Cr)}
```

**为什么用表面体素而不是实心体素**：`trimesh.voxel.creation.local_voxelize` 要求水密网格，
而模型写出来的场景经常不水密（开口圆柱、平面、单面片）。表面占据不挑网格，
代价是对「空心 vs 实心」不敏感 —— 这一类需求交给 A3 的 `non_manifold_edges` 和 `volume`。

### 4.2 阈值 tau 怎么定（实测）

F-score 的 tau 是整套指标里最容易定错的东西。本机对 22 个变异扫了四个 tau：

| 变异 | should | F@0.1% diag | F@0.2% | F@0.5% | F@1% |
|---|---|---|---|---|---|
| mug_handle_missing | fail | 0.3441 | 0.7180 | 0.9985 | 0.9995 |
| shade_flipped | fail | 0.9639 | 0.9663 | 0.9746 | 0.9847 |
| table_thin | fail | 0.1011 | 0.2689 | **0.4174** | 1.0000 |
| leg_count_3 | fail | 0.2492 | 0.6688 | 0.9686 | 0.9704 |
| bevel_removed | fail | 0.2511 | 0.6768 | 0.9993 | 1.0000 |
| mug_moved | fail | 0.9910 | 0.9910 | 0.9916 | 0.9932 |
| subsurf_off | fail | 0.2511 | 0.6714 | 0.9953 | 0.9996 |
| cube_size2 | **pass** | 0.2920 | 0.7142 | 0.9993 | 1.0000 |
| leg_verts_32 | **pass** | 0.2500 | 0.6780 | 0.9991 | 1.0000 |
| mug_seg_48 | **pass** | 0.4977 | 0.7826 | 0.9993 | 1.0000 |
| torus_minor_12 | **pass** | 0.5022 | 0.7862 | 0.9993 | 1.0000 |
| leg_radius_+2.5% | **pass** | 0.2387 | 0.6724 | 0.9990 | 1.0000 |

**读出三条硬规律**

1. **tau 小于采样间距时，F-score 测的是采样密度不是几何。**
   tau = 0.1% diag（2.2 mm）那一列里，`mug_seg_48`（该放行）0.4977 比 `shade_flipped`（该判错）0.9639 还低，
   完全颠倒。6 万点撒在 2.18 m 的场景上，平均点间距约 3 ~ 5 mm，tau 必须明显大于它。
2. **tau 太大就只剩「整块没了」能抓。** tau = 1% diag（2.2 cm）那一列，8 个该判错的里只有 1 个低于 0.99。
3. **不存在一个全局 tau 能把 fail 和 pass 分开。** 中间档 tau = 0.5% 时，
   该判错的 `bevel_removed` 是 0.9993、`mug_handle_missing` 是 0.9985，
   而该放行的 `mug_seg_48` 是 0.9993 —— 数值完全重叠。

**推荐取法**：`tau = 0.5% diag`，并且**分部件算**（见 4.3）。先用参考解自采样两次估一下点间距，
`tau >= 3 × 平均最近邻距离` 是安全下界。

### 4.3 全局量是废的，必须分部件

同一批变异，全局 vs 按材质色分组取最差组：

| 变异 | should | 全局 Chamfer | 分部件最差 Chamfer | 全局 F@0.5% | 分部件最差 F@0.5% |
|---|---|---|---|---|---|
| mug_moved 杯子挪 30 cm | fail | **0.00018** | **0.08375** | 0.9916 | **0.2243** |
| table_thin | fail | 0.00487 | 0.00528 | 0.4174 | **0.3428** |
| shade_flipped | fail | 0.00039 | 0.00441 | 0.9746 | **0.7141** |
| subsurf_off | fail | 0.00169 | 0.00437 | 0.9953 | **0.6242** |
| mug_handle_missing | fail | 0.00146 | 0.00227 | 0.9985 | **0.9268** |
| leg_count_3 | fail | 0.00644 | 0.00698 | 0.9686 | **0.9650** |
| wood_blue | fail | 0.00000 | **1.00000** | 1.0000 | **0.0000** |
| cube_size2 | pass | 0.00155 | 0.00160 | 0.9993 | 0.9993 |
| leg_verts_32 | pass | 0.00166 | 0.00168 | 0.9991 | 0.9990 |
| mug_seg_48 | pass | 0.00111 | 0.00129 | 0.9993 | 0.9992 |
| mug_pos_jitter 抖 5 mm | pass | 0.00002 | 0.00188 | 1.0000 | 1.0000 |
| leg_radius_+2.5% | pass | 0.00168 | 0.00170 | 1.0000 | 0.9989 |

- **最关键的一行是 `mug_moved`**：把杯子在桌面上挪 30 cm，**全局 Chamfer 从 0 只涨到 0.00018**，
  因为杯子只占全场表面积约 2%，而且挪到的位置仍然在桌面附近，最近邻距离被桌面"接住"了。
  分部件算则是 0.08375，差 **460 倍**。
- 把阈值取在「该放行那一档的下沿」：分部件最差 F@0.5% 的 pass 组最低是 **0.9989**，
  所以阈值取 **0.99**。按这个阈值，7/11 个该判错的被抓到、11/11 个该放行的被放过。
  漏掉的 4 个（`bulb_dim`、`anim_missing`、`cam_lens_24`、`bevel_removed`）是几何上**本来就不可见**的，
  必须交给断言。
- `bevel_removed` 漏掉是合理的：1 cm 倒角 / 2.18 m 对角线 = 0.0046 diag，正好等于 tau。
  **低于采样分辨率的需求不要指望几何指标，写进 A4 修改器断言。**

### 4.4 耗时（6 万点 / 48 核配额）

| 指标 | 耗时 |
|---|---|
| 双向 Chamfer + HD95（两次 KD 树查询） | 107 ms |
| F-score（同样两次查询） | 106 ms |
| 按色表面体素 IoU（32³ 网格） | 36 ms |
| 分部件版本（3 个颜色组各算一遍） | 约 120 ms |
| 采样 6 万点本身（trimesh） | 150 ~ 210 ms |
| **几何全套合计** | **约 0.4 s / 候选** |

相比之下 10 个视角的 Workbench 渲染要 1.1 ~ 1.2 s。
**几何指标比渲染便宜 3 倍，而且判别力更高**（分部件 F 检出 7/11，多视角剪影只有 3/11）。
如果只能留一个视觉信号，留几何，不留渲染。

---

## 5. 三方对比：bpy 状态断言 vs 渲染图比对 vs VLM 判图

VLM 对照实验：同一批 22 个变异，题干原文一起发给 judge，两种看图条件
（single = 场景自带相机一张图上下对照；multi = 4 个 verifier 视角 0°/90°/180°/俯视拼图），
4 个 judge 各跑一遍，temperature 0。176 次调用，**耗时 865 秒**（并发 12）。
脚本 `vlm_judge.py`，原始结果 `runs/desk_lamp/vlm.json`。

### 5.1 VLM 实测

| judge | 条件 | 总判对 | 检出 11 个该挂 | 保真 11 个不该挂 | 没吐出合法 JSON |
|---|---|---|---|---|---|
| gpt-6-astra | single | 16/22 | 5 | 11 | 0 |
| gpt-6-astra | multi | 16/22 | 6 | 10 | 0 |
| claude-opus-5-5 | single | 13/22 | 3 | 10 | 0 |
| claude-opus-5-5 | multi | 14/22 | 4 | 10 | 1 |
| gemini-3.8-flash | single | 14/22 | 4 | 10 | 0 |
| gemini-3.8-flash | multi | 15/22 | 4 | 11 | 0 |
| doubao-seed-2.1-pro | single | 14/22 | 4 | 10 | 1 |
| doubao-seed-2.1-pro | multi | 14/22 | 3 | 11 | 3 |

- **VLM 的形状是「保真高、检出低」**：11/11 的放行基本不出错，但 11 个真错只抓住 3 ~ 6 个。
  程序化的 `combo_pc` 是 11/11 检出 + 10/11 保真。
- **多视角拼图几乎没用**：四个 judge 的 single → multi 分别是 16→16、13→14、14→15、14→14。
  和 three.js 版的观察一致（STATE.md 03:52 行：拼图反而掉分）。拼图还抬高了解析失败率（doubao multi 掉了 3 条）。
- **8 个条件全体漏掉的变异**：`table_thin`（桌面 5 cm → 2 cm）、`bulb_dim`（60 W → 6 W）、
  `anim_missing`（关键帧删光）、`bevel_removed`（倒角删掉）、`cam_lens_24`（50 mm → 24 mm）。
  前一个是**定量尺寸**，后四个是**静帧里压根看不见的属性**。
- **8 个条件全体抓住的变异**：`mug_handle_missing`（部件整个没了）、`wood_blue`（换色）、
  `mug_moved`（部件挪位）。都是**语义级、人一眼能看出来的**差异。
- **VLM 的误杀集中在相机**：`camera_moved`（该放行）被 4 个条件判错，尽管题干里明写了「不算错：相机机位」。
  说明 VLM 分不清「画面变了」和「场景变了」—— 这正是 04_verifier.md 记的
  BlenderGym pairwise 最好只有 0.66（人与人 0.79）的同一类问题。

### 5.2 三方能抓什么、漏什么

| 错误类型 | bpy 状态断言 | 渲染图 / 几何比对 | VLM 判图 |
|---|---|---|---|
| 部件缺失（杯把手没建） | ✅ A1 | ✅ 分部件 F 0.9268 | ✅ 8/8 条件全抓 |
| 部件挪位（杯子挪 30 cm） | ✅ A2（但 A2 保真差） | ✅ 体素 0.078 / 分部件 F 0.2243 | ✅ 8/8 |
| 部件朝向反了（灯罩转 70°） | ✅ A2 | ✅ 剪影 0.9280 / 分部件 F 0.7141 | ❌ 8 个条件只有 3 个抓到 |
| 定量尺寸错（桌面 5 cm → 2 cm） | ✅ A2 | ✅ 分部件 F 0.3428 | ❌ **0/8 全漏** |
| 数量错（4 条腿变 3 条） | ✅ A1 | ✅ 剪影 0.8766 | ❌ 8 个条件只有 3 个抓到 |
| 颜色 / 材质错（木色改蓝） | ✅ A5 | ✅ 体素 IoU 0.000 | ✅ 8/8 |
| 光照强度错（60 W → 6 W） | ✅ A6 | ❌ 所有信号 1.0000 | ❌ 0/8 |
| 动画丢失（关键帧删光） | ✅ A7 | ❌ 所有信号 1.0000 | ❌ 0/8 |
| 修改器丢失（倒角 1 cm） | ✅ A4 | ❌ 低于采样分辨率 | ❌ 0/8 |
| 相机参数错（50 mm → 24 mm） | ✅ A6 | ⚠️ 只有单图 view0 0.9611 | ❌ 0/8 |
| 约束 / 物理设置 | ✅ A8 | ❌ 静帧看不见 | ❌ |
| 渲染设置（引擎 / 采样 / 分辨率） | ✅ A9 | ❌ | ❌ |
| 换建模路径（cube size 1 vs 2） | ❌ **A2/A3 误杀** | ✅ 放行 | ✅ 放行 |
| 换细分密度 | ❌ **A3 误杀** | ✅ 放行 | ✅ 放行 |
| 相机机位变了（题干没钉死） | ✅ 不查就不误杀 | ⚠️ **单图 view0 误杀 0.9534** | ❌ **4/8 误杀** |
| 题干没钉死的参数（日光功率） | ❌ 误杀（除非有字段白名单） | ✅ 放行 | ✅ 放行 |

### 5.3 结论

1. **三者的盲区几乎正交，必须组合。**
   - 断言独占：光照强度、动画、修改器、约束、物理、渲染设置、相机参数 —— 这些在**静帧里不存在**。
   - 几何独占：朝向、小部件挪位、定量尺寸、"形状对不对" —— 这些**写不成等式断言**（写了就误杀）。
   - VLM 独占：**没有**。本机 22 个变异里，VLM 抓到的每一个都被程序化信号同时抓到。
2. **全量断言 = 零判别力。** 九族全查在两批上保真都是 0/11 和 0/4。
   断言必须按题干裁字段，这个清单要在**造题干的时候**生成，不是事后补。
3. **单张截图是最差的视觉信号。** view0 在 22 个变异上只判对 12 个，
   而且它的失败模式最糟：`camera_moved`（0.9534）比 `wood_blue`（0.9844）掉得还多
   —— **画面变化量和语义错误量完全不相关**。
4. **VLM 的位置是兜底和审题，不是判分。**
   - 成本：865 s / 176 次 = 单次约 5 秒墙钟（并发 12），而程序化全套 2.3 秒。
   - 可靠性：最好的 judge 16/22，还会输出不可解析的结果（176 次里 5 次）。
   - 该怎么用：① 造题干时做需求反推（§2.3 闸 5）；② 对程序化判「通过」的样本抽查，
     找「断言没覆盖到的语义错误」；③ **不要**让它判定量尺寸和不可见属性，实测 0/8。
5. **推荐的落地判据**（本机 22 个变异 21/22）：

   ```
   pass = 分部件 F-score@0.5%diag >= 0.99                 # 形状、位置、朝向、颜色
          ∧ spec 白名单内的 A4 修改器断言                  # 渲染看不见
          ∧ spec 白名单内的 A6 灯光相机断言                # 渲染看不见
          ∧ spec 白名单内的 A7 F-curve 断言                # 静帧看不见
          ∧ spec 白名单内的 A8 约束物理断言                # 静帧看不见
          ∧ A9 渲染设置精确相等                            # 题干写死就查
          ∧ A3 的不变量（流形性 / 法线朝向），不查顶点数等式
          ∧ 候选脚本 exec 无异常
   ```

   唯一已知的失效模式：spec 白名单漏裁字段（本机留出集 `sun_energy_3.5`）。
   **修法是补白名单，不是调容差。**

### 5.4 方法学上的诚实交代

- `combo` 的成员（收哪几族断言）是**看过开发集 15 个变异的分族表之后**选的，属于在开发集上做了选择。
  所以另造了 7 个留出集变异复验：检出仍是 3/3，保真掉到 3/4，掉的那一个指向白名单问题而不是阈值问题。
- 阈值 `TH` 是在跑任何变异之前写死的，**没有在变异集上回调过**。
  唯一的例外是分部件 F-score 的 0.99，它是在看到 pass 组下沿 0.9989 之后定的，这一条是后定的，已标注。
- 只有**一个场景**。three.js 版的同一实验也只有一个场景（snowman），两边都需要换任务复验。
- 变异的 `should` 标签是我按题干人工定的，没有第二个人标，没有一致率数字。
  04_verifier.md 记的参照是 BlenderGym 人与人只有 0.79。
- VLM 只跑了 1 次重复，没有自一致率数字。three.js 版跑的是 2 次重复。

---

## 6. 落地建议

### 6.1 先做什么

1. **路线二（参数扰动 → 改回去）跑通闭环。** 原料是官方 `tests/files/render/` 的 839 个 .blend，
   扰动算子表按九族写，每个算子上线前先用探针验证「它确实改变了某个被查信号」。
2. **`spec.json` 字段白名单跟题干一起生成。** 这是本次实测唯一的失效模式。
3. **verifier 用 §5.3 的组合判据。** 几何只用分部件 F-score，断言只留 A4/A6/A7/A8/A9 + A3 的不变量。
4. **渲染图只用来给模型看，不用来判分。** Workbench 10 视角 1.2 秒，当观测很划算；
   当判据的话，判别力不如 0.4 秒的几何指标。

### 6.2 工程注意事项（本机踩到的）

- **bpy 不是 blender 命令行。** pip 的 `bpy==4.5.*` 每个版本只绑一个 Python 小版本（4.1~5.0 → 3.11），
  包体 784 MB。内网 pypi 镜像的 bpy 4.2~4.4 全部 502，要走海外代理装（121 s）。
- **Workbench 的 MATERIAL 着色取的是 `material.diffuse_color`（viewport 色），不是 Principled 的 Base Color。**
  不同步过去，渲出来全是默认灰。`probe.py: render_views()` 里做了同步。
- **用 `film_transparent=True` + RGBA 输出，一次渲染同时拿到彩色图和剪影**（alpha 通道），
  不用渲两遍。
- **采样要固定种子。** `trimesh.sample.sample_surface` 用自己的 RNG，`np.random.seed` 对它无效，
  必须传 `seed=`。不传的话参考解自己跟自己比 Chamfer 就是 0.00167 而不是 0，噪声地板直接吃掉一半判别力。
- **材质节点按 `bl_idname` 比，不要按 `node.name`。** Blender 会自动把同名节点改成 `Mix.001`。
- **网格统计一律取 `obj.evaluated_get(depsgraph)`**，否则修改器的效果全看不见。
- **候选脚本要在子进程里 exec。** bpy 是全局单例，一个脚本把 `bpy.ops.wm.read_factory_settings` 调歪了
  会污染后面所有任务。本机是每个候选起一个 python 进程，2.3 秒里有约 0.5 秒是进程启动 + bpy 导入。
  要提速就上常驻进程池 + 每任务 `read_factory_settings(use_empty=True)`。

### 6.3 复现命令

```bash
cd /mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/blender
PY=../.venv_bpy/bin/python

"${PY}" probe.py tasks/desk_lamp/ref.py runs/desk_lamp/ref        # 跑参考解
"${PY}" mutate.py                                                  # 开发集 15 个变异
"${PY}" mutate.py --holdout                                        # 留出集 7 个变异
"${PY}" summarize.py                                               # 从 runs/ 重算所有信号出表
"${PY}" vlm_judge.py 1                                             # VLM 对照（需要 klink 网关）
"${PY}" verify.py runs/desk_lamp/ref runs/desk_lamp/shade_flipped  # 单个候选的详细分数
```

### 附录：Blender 官方 render tests 的 48 个类别

实查 `https://projects.blender.org/api/v1/repos/blender/blender/contents/tests/files/render?ref=main`
（2026-10-15）：

```
attributes  bake  bake_raytrace  bsdf  camera  colorspace  denoise  denoise_animation
displacement  grease_pencil  gsplat  guiding  hair  image_colorspace  image_data_types
image_mapping  image_mipmap  image_texture_limit  instancing  integrator  light
light_group  light_linking  lighting_nodes  lightprobe  mesh  motion_blur  node_inlining
opengl  openvdb  osl  overlay  pointcloud  principled_bsdf  raycast  render_layer
reports  shader  shadow  shadow_catcher  sss  texture  transparency  updates  util
volume  workbench  （另有 readme.txt）
```

官方判据（`tests/python/modules/render_report.py`，main 分支 2026-10-15）：
`oiiotool ref.png new.png --fail 0.016 --failpercent 1 --diff`，
即单像素误差超过 0.016 的像素不得超过 1%。`cycles_render_tests.py` 与 `workbench_render_tests.py`
都调 `report.set_pixelated(True)`，并按设备 / OSL 维护 BLOCKLIST。

