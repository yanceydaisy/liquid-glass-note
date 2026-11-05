from pathlib import Path
import math
import re

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "liquid-glass-technical-guide-v4.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 720, 960
M = 48

PAPER = HexColor("#F4F4F1")
INK = HexColor("#171A1D")
NAVY = HexColor("#183248")
MUTED = HexColor("#697178")
RULE = HexColor("#C8CDD0")
PALE = HexColor("#E8EBEC")
BLUE = HexColor("#718DA7")
ROSE = HexColor("#A9848C")
CODE = HexColor("#171B20")
GREEN = HexColor("#738C82")

pdfmetrics.registerFont(TTFont("NotoSerifSC", str(ROOT / "assets" / "noto-serif-sc.ttf")))


def sw(text, font, size):
    return pdfmetrics.stringWidth(text, font, size)


def wrap(text, font, size, width):
    result = []
    for paragraph in text.split("\n"):
        if not paragraph:
            result.append("")
            continue
        units = re.findall(r"[A-Za-z0-9_./+*<>=()-]+|\s+|.", paragraph)
        current = ""
        for unit in units:
            trial = current + unit
            if current and sw(trial, font, size) > width:
                if unit in "，。；：！？、）》”’":
                    current += unit
                    continue
                result.append(current.rstrip())
                current = unit.lstrip()
            else:
                current = trial
        if current:
            result.append(current.rstrip())
    return result


class Guide:
    def __init__(self, path):
        self.c = canvas.Canvas(str(path), pagesize=(W, H), pageCompression=1)
        self.c.setTitle("Liquid Glass Technical Guide v4")
        self.c.setAuthor("@whereyanlands")
        self.c.setSubject("A public technical guide to a layered liquid-glass renderer")
        self.c.setKeywords("liquid glass, WebGL, SDF, refraction, Canvas, UI")
        self.page = 0

    def begin(self, section):
        self.page += 1
        c = self.c
        c.setFillColor(PAPER)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.55)
        c.line(M, H - 54, W - M, H - 54)
        c.setFont("Courier", 7.5)
        c.setFillColor(HexColor("#91999F"))
        c.drawString(M, H - 38, f"{self.page:02d} / 07")
        c.setFillColor(NAVY)
        c.drawRightString(W - M, H - 38, "LIQUID GLASS / V4")
        c.setFont("Courier-Bold", 7.5)
        c.drawString(M, H - 79, section.upper())

    def end(self):
        c = self.c
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.line(M, 28, W - M, 28)
        c.setFont("Courier", 6.5)
        c.setFillColor(HexColor("#929AA0"))
        c.drawString(M, 15, "TECHNICAL GUIDE / PUBLIC EDITION")
        c.setFillColor(BLUE)
        c.drawCentredString(W / 2, 15, "@whereyanlands")
        c.setFillColor(HexColor("#929AA0"))
        c.drawRightString(W - M, 15, f"{self.page:02d}")
        c.showPage()

    def title(self, text, y, size=34, width=None):
        width = width or W - 2 * M
        self.c.setFillColor(INK)
        self.c.setFont("NotoSerifSC", size)
        for line in wrap(text, "NotoSerifSC", size, width):
            self.c.drawString(M, y, line)
            y -= size * 1.22
        return y

    def body(self, text, x, y, width, size=11.2, leading=19, color=MUTED, font="NotoSerifSC"):
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        for line in wrap(text, font, size, width):
            self.c.drawString(x, y, line)
            y -= leading
        return y

    def label(self, text, x, y, color=BLUE):
        self.c.setFont("Courier-Bold", 7.5)
        self.c.setFillColor(color)
        self.c.drawString(x, y, text.upper())

    def panel(self, x, y, w, h, fill=Color(1, 1, 1, 0.56), radius=16, stroke=RULE):
        self.c.setFillColor(fill)
        self.c.setStrokeColor(stroke)
        self.c.setLineWidth(0.65)
        self.c.roundRect(x, y, w, h, radius, fill=1, stroke=1)

    def code(self, x, y, w, items, title=None, line_h=14, font_size=8.0):
        h = 28 + len(items) * line_h + (13 if title else 0)
        c = self.c
        c.setFillColor(CODE)
        c.roundRect(x, y - h, w, h, 15, fill=1, stroke=0)
        yy = y - 18
        if title:
            c.setFont("Courier-Bold", 6.6)
            c.setFillColor(HexColor("#8FA5B6"))
            c.drawString(x + 18, yy, title.upper())
            yy -= 18
        for number, line in enumerate(items, 1):
            c.setFont("Courier", 6.3)
            c.setFillColor(HexColor("#66717B"))
            c.drawString(x + 16, yy, f"{number:02d}")
            c.setFont("Courier", font_size)
            c.setFillColor(HexColor("#E4E8EA"))
            c.drawString(x + 44, yy, line)
            yy -= line_h
        return y - h

    def arrow(self, x1, y1, x2, y2, color=BLUE, width=1.3, head=7):
        c = self.c
        c.setStrokeColor(color)
        c.setFillColor(color)
        c.setLineWidth(width)
        c.line(x1, y1, x2, y2)
        angle = math.atan2(y2 - y1, x2 - x1)
        left = (x2 - head * math.cos(angle - 0.55), y2 - head * math.sin(angle - 0.55))
        right = (x2 - head * math.cos(angle + 0.55), y2 - head * math.sin(angle + 0.55))
        path = c.beginPath()
        path.moveTo(x2, y2)
        path.lineTo(*left)
        path.lineTo(*right)
        path.close()
        c.drawPath(path, fill=1, stroke=0)

    def step(self, x, y, w, number, title, description, fill=Color(1, 1, 1, 0.62)):
        self.panel(x, y, w, 82, fill, 14)
        self.c.setFillColor(NAVY)
        self.c.circle(x + 23, y + 58, 12, fill=1, stroke=0)
        self.c.setFont("Courier-Bold", 8)
        self.c.setFillColor(PAPER)
        self.c.drawCentredString(x + 23, y + 55, str(number))
        self.c.setFont("Courier-Bold", 8)
        self.c.setFillColor(INK)
        self.c.drawString(x + 44, y + 57, title.upper())
        self.body(description, x + 16, y + 30, w - 32, 9.2, 14, MUTED)

    def save(self):
        self.c.save()


def clip_round(c, x, y, w, h, radius):
    path = c.beginPath()
    path.roundRect(x, y, w, h, radius)
    c.clipPath(path, stroke=0, fill=0)


def scene_crop(c, x, y, w, h, crop=(0, 0, 1, 1), radius=18, smoked=False):
    """Draw the same synthetic wallpaper through an arbitrary normalized crop."""
    cx, cy, cw, ch = crop

    def px(u):
        return x + (u - cx) / cw * w

    def py(v):
        return y + (v - cy) / ch * h

    c.saveState()
    clip_round(c, x, y, w, h, radius)
    c.setFillColor(HexColor("#DCE2E5"))
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setStrokeColor(Color(0.17, 0.25, 0.31, 0.16))
    c.setLineWidth(0.55)
    for i in range(11):
        u = i / 10
        c.line(px(u), py(0), px(u), py(1))
        c.line(px(0), py(u), px(1), py(u))
    c.setFillColor(Color(0.60, 0.40, 0.45, 0.78))
    c.circle(px(0.22), py(0.72), w * 0.22 / cw, fill=1, stroke=0)
    c.setFillColor(Color(0.34, 0.49, 0.66, 0.78))
    c.circle(px(0.72), py(0.24), w * 0.27 / cw, fill=1, stroke=0)
    c.setFillColor(Color(0.08, 0.13, 0.19, 0.90))
    c.roundRect(px(0.58), py(0.48), w * 0.30 / cw, h * 0.38 / ch, 10, fill=1, stroke=0)
    c.setStrokeColor(Color(1, 1, 1, 0.58))
    c.setLineWidth(1.2)
    c.line(px(0.05), py(0.12), px(0.92), py(0.88))
    c.line(px(0.02), py(0.28), px(0.76), py(0.93))
    if smoked:
        c.setFillColor(Color(0.05, 0.06, 0.08, 0.42))
        c.rect(x, y, w, h, fill=1, stroke=0)
    c.restoreState()
    c.setStrokeColor(HexColor("#AEB7BC"))
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, radius, fill=0, stroke=1)


def draw_glass_card(c, x, y, w, h, smoked=False, label=None):
    # Both materials start from the exact same crop. The smoked variant adds
    # separate body attenuation, an inward dark bevel, and a narrow clear rim.
    scene_crop(c, x, y, w, h, crop=(0.26, 0.17, 0.55, 0.54), radius=23, smoked=False)
    c.saveState()
    clip_round(c, x, y, w, h, 23)
    if smoked:
        c.setFillColor(Color(0.035, 0.045, 0.060, 0.38))
        c.rect(x, y, w, h, fill=1, stroke=0)
        # The production shader's smokeOuter / edgeLoss are represented here
        # as a broad bevel that fades toward the card interior.
        for i in range(12):
            inset = 2.5 + i * 1.15
            alpha = 0.115 * (1 - i / 12) ** 1.35
            c.setStrokeColor(Color(0.025, 0.032, 0.043, alpha))
            c.setLineWidth(2.6)
            c.roundRect(x + inset, y + inset, w - inset * 2, h - inset * 2,
                        max(7, 23 - inset), fill=0, stroke=1)
        # A narrow refractive band survives at the edge instead of becoming a
        # uniform white outline.
        c.setStrokeColor(Color(0.78, 0.87, 0.94, 0.55))
        c.setLineWidth(4.6)
        c.arc(x + 3, y + 3, x + w - 3, y + h - 3, 112, 52)
        c.arc(x + 3, y + 3, x + w - 3, y + h - 3, 292, 34)
        c.setStrokeColor(Color(1, 1, 1, 0.62))
        c.setLineWidth(1.0)
        c.arc(x + 5, y + 5, x + w - 5, y + h - 5, 116, 42)
    else:
        c.setFillColor(Color(0.86, 0.91, 0.96, 0.055))
        c.rect(x, y, w, h, fill=1, stroke=0)
        c.setStrokeColor(Color(1, 1, 1, 0.80))
        c.setLineWidth(1.35)
        c.arc(x + 4, y + 3, x + w - 4, y + h - 3, 105, 72)
        c.setStrokeColor(Color(0.10, 0.14, 0.18, 0.24))
        c.arc(x + 5, y + 4, x + w - 5, y + h - 4, 285, 55)
    c.restoreState()
    if label:
        c.setFont("Courier-Bold", 8)
        c.setFillColor(HexColor("#F1F3F4") if smoked else NAVY)
        c.drawString(x + 16, y + h - 24, label)


def material_marker(c, x, y, number, smoked=False):
    c.setFillColor(HexColor("#F2F4F5") if smoked else NAVY)
    c.circle(x, y, 8.5, fill=1, stroke=0)
    c.setFont("Courier-Bold", 7)
    c.setFillColor(NAVY if smoked else PAPER)
    c.drawCentredString(x, y - 2.5, str(number))


def material_key(c, x, y, number, text_value):
    c.setFillColor(NAVY)
    c.circle(x + 7, y + 3, 7, fill=1, stroke=0)
    c.setFont("Courier-Bold", 6.5)
    c.setFillColor(PAPER)
    c.drawCentredString(x + 7, y + 0.7, str(number))
    c.setFont("NotoSerifSC", 9.2)
    c.setFillColor(INK)
    c.drawString(x + 21, y, text_value)


g = Guide(OUT)

# 1 / overview
g.begin("Overview / 总览")
y = g.title("液态玻璃，是一条可以顺着读懂的渲染链。", 835, 34)
g.body("它由五步组成：先确定背景，再裁出组件所在区域，建立圆角光学场，计算折射与材质，最后把结果保存为稳定画面。文字和交互始终留在普通 DOM 上层。", M, y - 10, W - 2 * M, 11.5, 20)
steps = [("SCENE", "壁纸、底色和主题蒙层"), ("CROP", "按卡片在视口中的位置裁取"), ("FIELD", "把圆角矩形变成统一坐标"), ("OPTICS", "折射、烟灰、暗边和高光"), ("SNAPSHOT", "复制到 2D Canvas，DOM 盖在上面")]
start_y = 585
for i, (name, desc) in enumerate(steps, 1):
    yy = start_y - (i - 1) * 91
    g.panel(M + 78, yy, W - 2 * M - 156, 66, Color(1, 1, 1, 0.64), 15)
    g.c.setFillColor(NAVY if i in (1, 3, 5) else HexColor("#39434B"))
    g.c.circle(M + 103, yy + 33, 15, fill=1, stroke=0)
    g.c.setFont("Courier-Bold", 8)
    g.c.setFillColor(PAPER)
    g.c.drawCentredString(M + 103, yy + 30, f"{i:02d}")
    g.c.setFont("Courier-Bold", 9)
    g.c.setFillColor(INK)
    g.c.drawString(M + 138, yy + 40, name)
    g.body(desc, M + 138, yy + 20, W - 2 * M - 235, 9.6, 14, MUTED)
    if i < len(steps):
        g.arrow(W / 2, yy - 4, W / 2, yy - 21, RULE, 1.0, 5)
g.panel(M, 82, W - 2 * M, 82, Color(1, 1, 1, 0.60), 16)
g.label("READING RULE", M + 20, 138)
g.body("从背景到快照是一条数据链；从 Canvas 到文字是一层合成关系。", M + 20, 109, W - 2 * M - 40, 13, 21, INK)
g.end()

# 2 / background sampling
g.begin("01 / Background sampling")
y = g.title("先找准卡片在背景里的位置。", 835, 35)
g.body("同一张背景先铺满视口。每块玻璃读取自己的矩形位置，再从背景中裁出完全对应的那一块；这样折射后的纹理才不会错位。", M, y - 8, W - 2 * M, 11.5, 20)
g.label("1. FULL VIEWPORT", M, 686)
scene_crop(g.c, M, 420, 390, 238, radius=18)
card_crop = (0.48, 0.34, 0.32, 0.30)
rx = M + card_crop[0] * 390
ry = 420 + card_crop[1] * 238
rw = card_crop[2] * 390
rh = card_crop[3] * 238
g.c.setStrokeColor(HexColor("#F4F6F6"))
g.c.setLineWidth(2.1)
g.c.roundRect(rx, ry, rw, rh, 16, fill=0, stroke=1)
g.c.setFillColor(Color(1, 1, 1, 0.90))
g.c.roundRect(rx + 10, ry + rh - 28, 90, 20, 8, fill=1, stroke=0)
g.c.setFont("Courier-Bold", 7)
g.c.setFillColor(NAVY)
g.c.drawString(rx + 20, ry + rh - 22, "CARD RECT")
g.label("2. LOCAL TEXTURE", 500, 686)
scene_crop(g.c, 500, 486, 172, 132, crop=card_crop, radius=19)
g.arrow(452, 539, 489, 539, BLUE, 1.4, 8)
g.body("同一位置\n同一纹理", 514, 455, 150, 10.2, 17, INK)
g.step(M, 306, 194, 1, "MEASURE", "读取卡片的 rect：left、top、width、height。")
g.step(M + 215, 306, 194, 2, "CROP", "按 cover 后的背景比例换算局部偏移。")
g.step(M + 430, 306, 194, 3, "UPLOAD", "把局部 Canvas 上传为当前卡片纹理。")
g.code(M, 280, W - 2 * M, ["const rect = card.getBoundingClientRect();", "const scale = Math.max(vw / iw, vh / ih);", "const dx = (vw - iw * scale) / 2 - rect.left;", "const dy = (vh - ih * scale) / 2 - rect.top;", "ctx.drawImage(image, dx, dy, iw * scale, ih * scale);"], "local crop from the controlled background source", 14, 7.8)
g.body("边界：这里重建的是受控背景源（默认渐变或本地压缩后的壁纸 data URL）与主题蒙层。普通 DOM、视频和另一层玻璃不会自动进入纹理。", M, 86, W - 2 * M, 9.7, 16, MUTED)
g.end()

# 3 / geometry
g.begin("02 / Rounded geometry")
y = g.title("光学场必须知道真实圆角在哪里。", 835, 35)
g.body("两个量解决两件事：roundBox() 判断像素离圆角边界有多远；radialBoundary() 把不同方向的边界都归一为 1。", M, y - 8, W - 2 * M, 11.5, 20)
g.panel(M, 460, 298, 224, Color(1, 1, 1, 0.60), 17)
g.label("A. SIGNED DISTANCE", M + 18, 650)
g.c.setFillColor(HexColor("#D7E0E4"))
g.c.roundRect(M + 54, 505, 190, 108, 31, fill=1, stroke=0)
g.c.setStrokeColor(NAVY)
g.c.setLineWidth(1.4)
g.c.roundRect(M + 54, 505, 190, 108, 31, fill=0, stroke=1)
for px, py, value, color in [(M + 148, 555, "-18  inside", GREEN), (M + 244, 559, "0  edge", NAVY), (M + 271, 625, "+24  outside", ROSE)]:
    g.c.setFillColor(color)
    g.c.circle(px, py, 4, fill=1, stroke=0)
    g.c.setFont("Courier-Bold", 7.2)
    g.c.drawString(px - 25, py - 18, value)
g.body("负值在内部，0 是边界，正值在外部。它负责裁出真正的圆角轮廓。", M + 18, 484, 262, 9.4, 15, MUTED)
g.panel(374, 460, 298, 224, Color(1, 1, 1, 0.60), 17)
g.label("B. NORMALIZED FIELD", 392, 650)
g.c.setFillColor(HexColor("#DCE3E6"))
g.c.roundRect(408, 505, 230, 108, 31, fill=1, stroke=0)
cx, cy = 523, 559
for angle in (-2.55, -1.75, -0.95, -0.35, 0.35, 1.0, 1.8, 2.55):
    ex = cx + math.cos(angle) * 108
    ey = cy + math.sin(angle) * 50
    g.c.setStrokeColor(Color(0.39, 0.52, 0.62, 0.72))
    g.c.setLineWidth(0.8)
    g.c.line(cx, cy, ex, ey)
g.c.setFillColor(NAVY)
for px, label in [(cx, "0"), (cx + 54, "0.5"), (cx + 108, "1.0")]:
    g.c.circle(px, cy, 3.5, fill=1, stroke=0)
    g.c.setFont("Courier-Bold", 7)
    g.c.drawCentredString(px, cy - 18, label)
g.body("无论射线撞到直边还是圆角，边界都变成 1；宽卡片不会被当成长圆镜片。", 392, 484, 262, 9.4, 15, MUTED)
g.code(M, 420, 300, ["vec2 q = abs(point-u_res*.5)", "  -(u_res*.5-vec2(u_corner));", "float sd = length(max(q,0.))", "  + min(max(q.x,q.y),0.) - u_corner;"], "rounded rectangle SDF", 14, 7.4)
g.code(372, 420, 300, ["vec2 rel = px - u_res * .5;", "vec2 p = rel / radialBoundary(rel);", "float rr = clamp(length(p), 0., 1.);", "// center = 0, exact boundary = 1"], "field coordinates", 14, 7.4)
g.panel(M, 84, W - 2 * M, 76, Color(1, 1, 1, 0.62), 15)
g.body("先用 SDF 得到形状，再用归一化场描述“离边缘还有多远”。后面的折射、暗边和高光都复用这两个结果。", M + 18, 126, W - 2 * M - 36, 10.6, 18, INK)
g.end()

# 4 / refraction
g.begin("03 / Refraction field")
y = g.title("折射，本质上是换一个位置读取背景。", 835, 35)
g.body("每个像素先得到归一化位置 p，再由整体透镜和低频波动计算位移 shift。最终不是给像素涂颜色，而是去背景纹理的邻近位置重新取色。", M, y - 8, W - 2 * M, 11.5, 20)
g.label("BEFORE", M, 680)
scene_crop(g.c, M, 500, 260, 150, crop=(0.18, 0.18, 0.64, 0.58), radius=20)
g.label("AFTER / REFRACTED", 412, 680)
scene_crop(g.c, 412, 500, 260, 150, crop=(0.205, 0.16, 0.60, 0.61), radius=20)
g.c.setStrokeColor(Color(1, 1, 1, 0.82))
g.c.setLineWidth(1.2)
g.c.arc(417, 505, 667, 645, 105, 72)
g.arrow(322, 575, 390, 575, BLUE, 1.6, 9)
g.c.setFont("Courier-Bold", 8)
g.c.setFillColor(NAVY)
g.c.drawCentredString(356, 590, "SHIFT UV")
flow = [("p", "归一化位置"), ("rr", "中心到边缘"), ("sh + wave", "透镜与波动"), ("refrUv", "新的采样坐标")]
for i, (name, desc) in enumerate(flow):
    x = M + i * 158
    g.panel(x, 390, 139, 72, Color(1, 1, 1, 0.64), 13)
    g.c.setFont("Courier-Bold", 9)
    g.c.setFillColor(NAVY)
    g.c.drawString(x + 14, 438, name)
    g.body(desc, x + 14, 414, 111, 8.8, 13, MUTED)
    if i < len(flow) - 1:
        g.arrow(x + 139, 426, x + 153, 426, RULE, 1.0, 5)
g.code(M, 356, W - 2 * M, ["float edgeGain = smoothstep(0.05, 0.97, rr);", "float strength = (0.052 + 0.12 * edgeGain)", "  * u_refract * u_lDistort;", "vec2 shift = p * sh + interiorWave * strength;", "vec2 refrUv = v_uv + vec2(shift.x/u_res.x, -shift.y/u_res.y);", "vec3 refr = backdrop(refrUv, u_blur * u_lBlur);"], "condensed from the production shader", 14, 7.55)
g.label("CURRENT TUNING", M, 210)
values = [("REFRACT", "26"), ("TINT", "0"), ("BLUR", "0"), ("EDGE", "25"), ("SHINE", "13"), ("WOBBLE", "15")]
for i, (name, value) in enumerate(values):
    x = M + i * 104
    g.c.setFillColor(NAVY if name in ("REFRACT", "EDGE") else HexColor("#3C444A"))
    g.c.circle(x + 8, 170, 7, fill=1, stroke=0)
    g.c.setFont("Courier-Bold", 13)
    g.c.setFillColor(INK)
    g.c.drawString(x, 143, value)
    g.c.setFont("Courier", 6.6)
    g.c.setFillColor(MUTED)
    g.c.drawString(x, 126, name)
g.body("这些是 Shader 调节刻度，不是物理单位。", M, 87, W - 2 * M, 9.6, 16, MUTED)
g.end()

# 5 / material and light
g.begin("04 / Material and light")
y = g.title("光学相同，透射方式可以完全不同。", 835, 35)
g.body("透明与烟灰材质共用同一套折射坐标。区别在于背景透过多少、边缘吸收多少光，以及亮背景下要不要压低整圈白边。", M, y - 8, W - 2 * M, 11.5, 20)
g.c.setFont("Courier-Bold", 7.5)
g.c.setFillColor(MUTED)
g.c.drawCentredString(W / 2, 681, "SAME SOURCE TEXTURE  /  同一背景纹理")
draw_glass_card(g.c, M, 508, 286, 146, smoked=False, label="CLEAR")
material_marker(g.c, M + 183, 566, 1)
material_marker(g.c, M + 40, 632, 2)
material_key(g.c, M + 10, 480, 1, "背景细节保持清晰")
material_key(g.c, M + 10, 457, 2, "只保留方向性高光")
draw_glass_card(g.c, 386, 508, 286, 146, smoked=True, label="SMOKED")
material_marker(g.c, 386 + 180, 566, 1, True)
material_marker(g.c, 386 + 260, 580, 2, True)
material_marker(g.c, 386 + 40, 632, 3, True)
material_key(g.c, 396, 480, 1, "主体透射降低")
material_key(g.c, 396, 457, 2, "内侧暗边吸光")
material_key(g.c, 396, 434, 3, "边缘留下清透折射带")
g.label("LUMINANCE ADAPTATION", M, 418)
g.panel(M, 290, W - 2 * M, 104, Color(1, 1, 1, 0.62), 15)
g.c.setFillColor(HexColor("#ECEDE9"))
g.c.roundRect(M + 18, 312, 254, 58, 16, fill=1, stroke=0)
g.c.setFillColor(HexColor("#252A30"))
g.c.roundRect(400, 312, 254, 58, 16, fill=1, stroke=0)
g.c.setFont("Courier-Bold", 8)
g.c.setFillColor(NAVY)
g.c.drawString(M + 34, 348, "BRIGHT BACKDROP")
g.c.setFillColor(HexColor("#EEF1F2"))
g.c.drawString(416, 348, "DARK BACKDROP")
g.body("暗边更窄，均匀白环被压低", M + 34, 326, 220, 9.2, 14, INK)
g.body("保留更多吸光厚度与局部高光", 416, 326, 220, 9.2, 14, HexColor("#EEF1F2"))
g.code(M, 270, W - 2 * M, ["float lum = dot(color, vec3(0.2126, 0.7152, 0.0722));", "float bright = smoothstep(0.42, 0.84, lum);", "float smokeWidth = mix(7.2, 4.25, bright);", "float edgeLoss = mix(0.27, 0.085, bright);", "float hairline = exp(-pow((signedBorder + .46) / .43, 2.));"], "adaptive smoke and directional rim", 14, 7.45)
g.panel(M, 82, W - 2 * M, 68, Color(1, 1, 1, 0.62), 15)
g.body("判断依据是实际采样到的背景亮度，不是日间/夜间标签。这样同一张壁纸里的亮区和暗区也能分别得到合适边缘。", M + 18, 121, W - 2 * M - 36, 10.2, 17, INK)
g.end()

# 6 / shared renderer
g.begin("05 / Shared renderer")
y = g.title("一个 WebGL 渲染器，许多独立快照。", 835, 35)
g.body("玻璃引擎只创建一个 WebGL context。可见组件依次借用这块共享表面完成绘制，然后立即把像素复制到自己的 2D Canvas。", M, y - 8, W - 2 * M, 11.5, 20)
g.label("ONE SHARED GPU SURFACE", M, 690)
g.panel(M, 455, 188, 205, Color(0.08, 0.10, 0.13, 1), 20, HexColor("#30363C"))
g.c.setFont("Courier-Bold", 9)
g.c.setFillColor(HexColor("#E8ECEE"))
g.c.drawString(M + 20, 620, "WEBGL")
g.c.setFont("Courier", 8)
g.c.setFillColor(HexColor("#BFC8CE"))
for i, item in enumerate(("1 context", "1 program", "1 buffer", "1 drawing surface")):
    g.c.drawString(M + 20, 585 - i * 30, item)
rows = [("CARD A", 594), ("CHAT B", 525), ("DOCK C", 456)]
for index, (name, yy) in enumerate(rows, 1):
    g.arrow(245, yy + 20, 288, yy + 20, BLUE, 1.3, 7)
    g.panel(298, yy - 5, 374, 50, Color(1, 1, 1, 0.64), 12)
    g.c.setFillColor(NAVY)
    g.c.circle(320, yy + 20, 10, fill=1, stroke=0)
    g.c.setFont("Courier-Bold", 7)
    g.c.setFillColor(PAPER)
    g.c.drawCentredString(320, yy + 17, str(index))
    g.c.setFont("Courier-Bold", 8)
    g.c.setFillColor(INK)
    g.c.drawString(342, yy + 25, name)
    g.c.setFont("Courier", 7)
    g.c.setFillColor(MUTED)
    g.c.drawString(342, yy + 8, "texture + backdrop canvas + stable output canvas")
g.code(M, 414, W - 2 * M, ["gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);", "// Copy before the shared drawing buffer is discarded.", "output.clearRect(0, 0, width, height);", "output.drawImage(renderSurface, 0, 0);", "// Normal DOM text remains above the output canvas."], "render once, keep a component-owned snapshot", 14, 7.7)
g.label("WHEN A CARD LEAVES THE VIEWPORT", M, 250)
g.panel(M, 135, W - 2 * M, 91, Color(1, 1, 1, 0.62), 15)
g.c.setFont("Courier-Bold", 8)
g.c.setFillColor(ROSE)
g.c.drawString(M + 20, 194, "GPU TEXTURE")
g.c.setFont("NotoSerifSC", 10.2)
g.c.setFillColor(INK)
g.c.drawString(M + 20, 169, "释放")
g.arrow(M + 155, 181, M + 250, 181, RULE, 1.2, 6)
g.c.setFont("Courier-Bold", 8)
g.c.setFillColor(GREEN)
g.c.drawString(M + 278, 194, "2D SNAPSHOT")
g.c.setFont("NotoSerifSC", 10.2)
g.c.setFillColor(INK)
g.c.drawString(M + 278, 169, "继续显示；context 丢失时旧画面仍在")
g.body("这里的“1 个 context”只指液态玻璃引擎。", M, 92, W - 2 * M, 9.6, 16, MUTED)
g.end()

# 7 / lifecycle
g.begin("06 / Lifecycle and reuse")
y = g.title("动画一直存在，昂贵工作只在必要时发生。", 835, 34)
g.body("背景纹理更新和材质动画分开管理。滚动、尺寸、主题或壁纸变化只把组件标为 dirty；可见组件按帧率上限绘制，离屏后保留快照并释放 GPU 纹理。", M, y - 8, W - 2 * M, 11.3, 20)
g.label("STATE FLOW", M, 680)
states = [("DIRTY", "背景或尺寸变化", ROSE), ("VISIBLE", "约 20 fps 绘制", NAVY), ("OFFSCREEN", "暂停并释放纹理", BLUE), ("DISPOSE", "断开 observer", HexColor("#454B50"))]
xs = [M, 208, 368, 528]
for i, ((name, desc, color), x) in enumerate(zip(states, xs)):
    g.panel(x, 548, 134, 92, Color(1, 1, 1, 0.64), 14)
    g.c.setFillColor(color)
    g.c.circle(x + 20, 614, 8, fill=1, stroke=0)
    g.c.setFont("Courier-Bold", 8)
    g.c.setFillColor(INK)
    g.c.drawString(x + 36, 611, name)
    g.body(desc, x + 14, 579, 106, 8.9, 14, MUTED)
    if i < 3:
        g.arrow(x + 134, 594, xs[i + 1] - 8, 594, RULE, 1.0, 5)
g.c.setFont("Courier", 6.7)
g.c.setFillColor(MUTED)
g.c.drawString(M + 10, 525, "theme / wallpaper / resize / scroll")
g.arrow(M + 214, 530, M + 214, 548, ROSE, 1.0, 5)
g.c.drawString(389, 525, "IntersectionObserver")
g.arrow(454, 530, 454, 548, BLUE, 1.0, 5)
g.code(M, 488, W - 2 * M, ["if (disposed || !visible || document.hidden || w < 5) return;", "if (reduced) { if (dirty || generationChanged) draw(0); return; }", "if (ms - last < 48) return;        // max about 20 fps", "last = ms;", "draw(ms * 0.001);                  // redraws texture only if dirty"], "actual frame policy, condensed", 14, 7.45)
g.label("CURRENT BUDGETS", M, 285)
budgets = [("DPR", "<= 1.5"), ("VISIBLE FPS", "~ 20"), ("GL CONTEXT", "1 engine"), ("HERO BLUR", "2.25 px"), ("FALLBACK", "CSS blur")]
for i, (name, value) in enumerate(budgets):
    x = M + i * 126
    g.panel(x, 205, 112, 58, Color(1, 1, 1, 0.58), 12)
    g.c.setFont("Courier-Bold", 10)
    g.c.setFillColor(INK)
    g.c.drawString(x + 12, 238, value)
    g.c.setFont("Courier", 6.3)
    g.c.setFillColor(MUTED)
    g.c.drawString(x + 12, 220, name)
g.c.setStrokeColor(RULE)
g.c.line(M, 177, W - M, 177)
g.label("PUBLIC SCOPE", M, 151)
g.body("公开内容只包含光学思路、技术图与经过压缩的实现片段。真实应用、私人背景、聊天逻辑和个人数据不在其中。", M, 126, W - 2 * M, 9.5, 16, MUTED)
g.body("UPSTREAM: VII-Cae/hyalite--liquid-glass (MIT) / everett745/liquid-glass (NO LICENCE DECLARED)", M, 70, W - 2 * M, 6.8, 11, MUTED, "Courier")
g.body("PROJECT: github.com/yanceydaisy/liquid-glass-note", M, 55, W - 2 * M, 6.8, 11, BLUE, "Courier")
g.end()

g.save()
print(OUT)
