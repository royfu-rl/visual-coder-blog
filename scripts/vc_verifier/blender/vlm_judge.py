"""VLM judge 对照：同一批 22 个变异，两种看图条件
  single  参考 vs 候选，各一张「场景自带相机」的图（最常见的截图 + VLM 打分）
  multi   参考 vs 候选，各 4 个 verifier 视角（0° / 90° / 180° / 俯视）拼图
should 标签与 mutate.py 完全一致。判对率与程序化信号直接可比。

  python vlm_judge.py [重复次数，默认 1]
"""
import base64, io, json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests
from PIL import Image, ImageDraw
import mutate

HERE = Path(__file__).parent
RUNS = HERE / "runs/desk_lamp"
URL, KEY = "http://klink.internal/v1/chat/completions", "sk-klink-MJFlh5vNbu2Rnujem807KsvGhk7lhJ6O"
JUDGES = ["gpt-6-astra", "claude-opus-5-5", "gemini-3.8-flash", "doubao-seed-2.1-pro"]
VIEWS = [1, 3, 5, 9]

PROMPT = """你是 3D 场景复现任务的验收员。题干要求：
在空场景里搭一张 1.2×0.8 的木桌，桌面厚 0.05、四条圆腿，桌面边缘倒角；
桌上一盏金属台灯（底座+斜臂+锥形灯罩），灯罩里一颗暖色点光源 60 W；
桌上一个白陶瓷杯（杯身 + 把手环），杯身加一级细分；相机 50mm 对准桌面中心，加一盏日光；
灯臂第 1~40 帧绕 X 轴从 -20° 转到 15°；渲染 512×512、Cycles、32 采样。

算对：部件齐全、相对位置和大小一致、材质颜色一致、朝向一致。
不算错：网格细分密度、建模路径、相机机位、日光角度、未写死的微小参数、代码写法。
图中上半部分是参考解的渲染，下半部分是候选解的渲染。{extra}
只输出一行 JSON：{{"verdict": "pass" 或 "fail", "reason": "一句话"}}"""


def sheet(name, cond):
    idx = [0] if cond == "single" else VIEWS
    S = 320
    im = Image.new("RGB", (S * len(idx), 2 * S + 44), "white")
    d = ImageDraw.Draw(im)
    for row, who in enumerate(["ref", name]):
        for c, i in enumerate(idx):
            a = Image.open(RUNS / who / f"view_{i}.png").convert("RGBA").resize((S, S))
            bg = Image.new("RGB", (S, S), "white"); bg.paste(a, (0, 0), a.split()[3])
            im.paste(bg, (c * S, 22 + row * (S + 22)))
    d.text((4, 6), "REFERENCE", fill="black"); d.text((4, S + 28), "CANDIDATE", fill="black")
    buf = io.BytesIO(); im.save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()


def ask(model, img, cond):
    extra = ("每行四张分别是：正面、90°、180°、俯视。" if cond == "multi"
             else "每部分是同一个场景相机的一张图。")
    body = {"model": model, "max_tokens": 3000, "temperature": 0,
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": PROMPT.format(extra=extra)},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64," + img}}]}]}
    for k in range(4):
        try:
            r = requests.post(URL, json=body, headers={"Authorization": "Bearer " + KEY},
                              timeout=180, proxies={"http": None, "https": None})
            txt = r.json()["choices"][0]["message"]["content"] or ""
            m = re.search(r'"verdict"\s*:\s*"(pass|fail)"', txt)
            if m:
                return m.group(1), txt[-160:]
        except Exception as e:
            txt = repr(e)
        time.sleep(2 * (k + 1))
    return "err", str(txt)[:160]


def main(rep=1):
    cases = [(n, s) for n, _, _, s in mutate.MUTANTS + mutate.HOLDOUT]
    imgs = {(n, c): sheet(n, c) for n, _ in cases for c in ("single", "multi")}
    jobs = [(m, n, s, c, r) for m in JUDGES for n, s in cases for c in ("single", "multi") for r in range(rep)]
    t0 = time.time()
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(lambda j: (j, ask(j[0], imgs[(j[1], j[3])], j[3])), jobs))
    out = [dict(model=m, case=n, should=s, cond=c, rep=r, verdict=v, note=t) for (m, n, s, c, r), (v, t) in res]
    json.dump(out, open(RUNS / "vlm.json", "w"), indent=1, ensure_ascii=False)

    print(f"{len(jobs)} 次调用，{time.time()-t0:.0f}s")
    print(f"\n{'judge':22s} {'cond':7s} {'总判对':>7s} {'检出':>7s} {'保真':>7s} {'解析失败':>8s}")
    for m in JUDGES:
        for c in ("single", "multi"):
            g = [o for o in out if o["model"] == m and o["cond"] == c]
            nf = sum(o["should"] == "fail" for o in g)
            hit = sum(o["verdict"] == "fail" for o in g if o["should"] == "fail")
            keep = sum(o["verdict"] == "pass" for o in g if o["should"] == "pass")
            print(f"{m:22s} {c:7s} {hit+keep:3d}/{len(g):<3d} {hit:4d}/{nf:<3d} {keep:4d}/{len(g)-nf:<3d} "
                  f"{sum(o['verdict']=='err' for o in g):6d}")
    print(f"\n{'case':20s} {'should':6s} " + " ".join(f"{m.split('-')[0][:6]:>7s}" for m in JUDGES) * 1)
    for n, s in cases:
        line = []
        for c in ("single", "multi"):
            line.append(" ".join(f"{[o['verdict'] for o in out if o['model']==m and o['case']==n and o['cond']==c][0][:4]:>7s}" for m in JUDGES))
        print(f"{n:20s} {s:6s} S|{line[0]}  M|{line[1]}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1)

