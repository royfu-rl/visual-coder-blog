# vc_verifier：visual coding 的可验证任务原型

四条技术线各一套最小 harness 加分层 verifier，外加自动造题与准入测试。
所有数字都能重跑，结论写在 `middle_processing/vc_data/90_local_experiments.md`。

机器：无 GPU，Chrome 148 无头加 SwiftShader 软渲染，约 48 核 CPU 配额。

## 目录

| 目录 | 技术线 | 判别力（带标签变异） |
|---|---|---|
| `proto/` | three.js | 三场景 47/47，其中第三个场景 18 个是阈值不动的留出 |
| `blender/` | Blender / bpy | 单场景 21/22 |
| `chart/` | 图表与 SVG | 单任务 16/16，噪声地板实测为 0 |
| `web/` | Web / DOM | 单参考页 22/22 |

## three.js 线怎么跑

```bash
cd proto
npm install                                   # puppeteer-core / three / pngjs
node harness.js <page.html> <outdir> [ref/probe.json]   # 探测：场景图 + 9 视角 + 体素
python3 compare.py tasks/snowman              # 一个任务下所有候选解的信号
python3 mutate.py car                         # 变异测试，打印每类信号判对多少
python3 blockiou.py                           # 分块 IoU 单独扫阈值
python3 gen_tasks.py tasks/desk/ref.html tasks/desk_gen 16   # 自动造题 + 准入测试
python3 solve.py tasks/desk_gen --conds none,page,multi,graph,oracle   # 让模型修，统计通过率
python3 vlm_judge.py                          # VLM judge 对照
python3 passk.py --k 8                        # 单模型 pass@8，量难度带留存
python3 analyze.py judge | python3 analyze.py solve          # 汇总
```

## 分层判据（three.js 线）

任一层挂即判挂，乘法门控。

| 层 | 查什么 | 为什么需要它 |
|---|---|---|
| L0 执行 | 页面报错、没渲染出 mesh、可见画布为空 | 把环境故障和模型失败分开 |
| L1 剪影 | 9 个视角的双面剪影与单面剪影，各取最差 | 单视角看不见的方位错误；单面通道能看见反面片 |
| L2 体素 | 按颜色的全局 IoU、6 的三次方分块最差块 | 形状对而颜色错；小部件的局部缺陷 |
| L2b 自洽 | 整体穿插比例、改变绘制顺序后的像素变化 | 共面重叠与绘制顺序闪烁 |
| L3 部件与拓扑 | 按颜色的体积比与连通块数、开放边界边数 | 细长部件缺失；不随尺寸衰减的破洞 |

渲染计数器（绘制调用、三角面、几何体与贴图实例）已采集，目前只作诊断，
因为还没有在带标签变异集上量过它的判别力。

## 取证的两条原则

- **不要求模型配合。** 场景通过 three.js 自身的 devtools 事件通道捕获，
  页面无论用 CDN、importmap 还是整个内联打包都能抓到。
  不要让模型把场景挂到约定好的全局变量上：它会学会「写这一行就行」，而且可以伪造。
- **只认用户真正看得到的那块画布。** 必须挂在文档里、有实际尺寸、未被隐藏。
  离屏渲染次数本身当蜜罐信号——正常解法不需要它。

## 踩过的坑

| 坑 | 症状 | 修法 |
|---|---|---|
| 钩子打在 prototype 上 | 捕获不到场景 | r160 的 render 挂在实例上，要在构造后包一层；后来换成 devtools 事件 |
| 开口曲面的体素填充 | 包围盒与参考逐位接近，按色体素 IoU 只有 0.017 | 按开放边界边数分流：闭合用射线奇偶，不闭合记录表面经过的体素 |
| 双面剪影填洞 | 顶部破洞四层信号全失明 | 加开放边界边数这个拓扑量，不随缺陷尺寸衰减 |
| 接缝处的正负零 | 闭合球面报出 70 条开放边 | 顶点坐标量化时把负零归一 |
| 按部件两两算穿插 | 参考解自己就是 1.0 | 48 的体素分辨率下薄部件被量化成一层，降级为诊断量 |
| 构建器把 iframe 内联成 srcdoc | demo 的图和数据 404 | 资源前缀运行时判断，不要写死相对路径 |

共性：**五个坑里有四个制造假阳性，也就是把正确产物判挂，在 RL 里是纯噪声，
而且调阈值一个也修不掉。** 所以变异集里「不该挂」的那一半比「该挂」的那一半更重要。

## 占盘与清理

整个目录约 1.6 GB，其中：

- `*/node_modules` 三份共约 210 MB，删了重跑 `npm install` 即可。
- `proto/runs` 约 320 MB，是探测产物。里面 `probe.json` 的体素数组很大，
  求解实验那两批已经删过候选渲染图并剥掉体素数组（信号都在 `results.jsonl` 与日志里）。
  带标签变异集的渲染图要留着，它们是判别力数字的证据。
- `alg/demos/` 下的 demo 资源是从 `runs/car_mut` 导出的，和这里相互独立，别一起删。

