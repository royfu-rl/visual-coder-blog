"""参考解：桌面台灯。候选解就是和它同签名的一个 bpy 脚本（probe.py 负责 exec）。
需求（自然语言，给模型的题干）：
  在空场景里搭一张 1.2×0.8 的木桌，桌面厚 0.05、四条圆腿，桌面边缘倒角；
  桌上放一盏金属台灯（底座+斜臂+锥形灯罩），灯罩里一颗暖色点光源 60 W；
  桌上再放一个白陶瓷杯（杯身 + 把手环），杯身加一级细分；
  相机 50mm 对准桌面中心，加一盏日光；
  灯臂在第 1~40 帧绕 X 轴从 -20° 转到 15°；
  渲染 512×512、Cycles、32 采样。
"""
import bpy, math

# ---- 清空 ----------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
S = bpy.context.scene


def mat(name, color, rough, metal):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*color, 1.0)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    return m


def put(obj, name, coll, material=None, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
    obj.name = name
    obj.location, obj.rotation_euler, obj.scale = loc, rot, scale
    if material:
        obj.data.materials.append(material)
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    coll.objects.link(obj)
    return obj


def coll(name):
    c = bpy.data.collections.new(name)
    S.collection.children.link(c)
    return c


WOOD = mat("Wood", (0.35, 0.20, 0.09), 0.60, 0.0)
METAL = mat("Metal", (0.70, 0.72, 0.75), 0.25, 1.0)
CERAMIC = mat("Ceramic", (0.92, 0.92, 0.90), 0.10, 0.0)

C_DESK, C_LAMP, C_MUG = coll("Desk"), coll("Lamp"), coll("Mug")

# ---- 桌子 ----------------------------------------------------------------
bpy.ops.mesh.primitive_cube_add(size=1)
top = put(bpy.context.object, "Tabletop", C_DESK, WOOD, loc=(0, 0, 0.75), scale=(1.2, 0.8, 0.05))
bev = top.modifiers.new("Bevel", 'BEVEL')
bev.width, bev.segments = 0.01, 3

for i, (x, y) in enumerate([(0.55, 0.35), (-0.55, 0.35), (0.55, -0.35), (-0.55, -0.35)]):
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.04, depth=0.75)
    put(bpy.context.object, f"Leg_{i}", C_DESK, WOOD, loc=(x, y, 0.375))

# ---- 台灯 ----------------------------------------------------------------
bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.12, depth=0.04)
put(bpy.context.object, "LampBase", C_LAMP, METAL, loc=(-0.45, 0.0, 0.80))

bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.015, depth=0.50)
arm = put(bpy.context.object, "LampArm", C_LAMP, METAL, loc=(-0.45, 0.10, 1.05),
          rot=(math.radians(-20), 0, 0))

bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.11, radius2=0.03, depth=0.16)
shade = put(bpy.context.object, "LampShade", C_LAMP, METAL, loc=(-0.45, 0.28, 1.26),
            rot=(math.radians(125), 0, 0))

bulb = bpy.data.lights.new("Bulb", 'POINT')
bulb.energy, bulb.color, bulb.shadow_soft_size = 60.0, (1.0, 0.85, 0.65), 0.03
put(bpy.data.objects.new("Bulb", bulb), "Bulb", C_LAMP, loc=(-0.45, 0.30, 1.21))

# 灯臂动画：第 1 帧 -20°，第 40 帧 15°
arm.rotation_euler.x = math.radians(-20); arm.keyframe_insert("rotation_euler", index=0, frame=1)
arm.rotation_euler.x = math.radians(15);  arm.keyframe_insert("rotation_euler", index=0, frame=40)
arm.rotation_euler.x = math.radians(-20)

# ---- 杯子 ----------------------------------------------------------------
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.045, depth=0.11)
body = put(bpy.context.object, "MugBody", C_MUG, CERAMIC, loc=(0.35, -0.12, 0.83))


bpy.ops.mesh.primitive_torus_add(major_radius=0.030, minor_radius=0.006,
                                 major_segments=24, minor_segments=8)
put(bpy.context.object, "MugHandle", C_MUG, CERAMIC, loc=(0.405, -0.12, 0.84),
    rot=(math.radians(90), 0, 0))

# ---- 相机 / 日光 / 渲染设置 ----------------------------------------------
tgt = bpy.data.objects.new("Focus", None)
S.collection.objects.link(tgt)
tgt.location = (0, 0, 0.80)

cam = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
S.collection.objects.link(cam)
cam.data.lens = 50.0
cam.location = (2.2, -2.6, 1.9)
con = cam.constraints.new('TRACK_TO')
con.target, con.track_axis, con.up_axis = tgt, 'TRACK_NEGATIVE_Z', 'UP_Y'
S.camera = cam

sun = bpy.data.lights.new("Sun", 'SUN')
sun.energy, sun.angle = 3.0, math.radians(2)
put(bpy.data.objects.new("Sun", sun), "Sun", S.collection, loc=(3, -2, 5),
    rot=(math.radians(35), math.radians(12), math.radians(25)))

S.render.engine = 'CYCLES'
S.render.resolution_x = S.render.resolution_y = 512
S.cycles.samples = 32
S.frame_start, S.frame_end = 1, 40

