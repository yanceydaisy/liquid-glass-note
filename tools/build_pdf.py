from pathlib import Path
import math
import re

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader
from figure_math import radial_boundary, round_box, build_refraction_figures, validate_geometry


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


def draw_background_crop(c, x, y, w, h, crop=(0, 0, 370, 234)):
    """Crop the identical cover-scaled background without stretching it."""
    left, bottom, cw, ch = crop
    assert abs(w / h - cw / ch) < 1e-8
    image = ImageReader(str(ROOT / "assets" / "background-reference.jpeg"))
    iw, ih = image.getSize()
    cover = max(370 / iw, 234 / ih)
    dw, dh = iw * cover, ih * cover
    dx, dy = (370 - dw) / 2, (234 - dh) / 2
    scale = w / cw
    c.saveState()
    path = c.beginPath()
    path.rect(x, y, w, h)
    c.clipPath(path, fill=0, stroke=0)
    c.drawImage(image, x + (dx - left) * scale, y + (dy - bottom) * scale,
                width=dw * scale, height=dh * scale)
    c.restoreState()


def captured_material(c, x, y, w, material):
    """Place an unretouched crop of the supplied phone capture.

    The clipping is PDF layout only: no simulated optics, tint, or highlights
    are painted onto the captured pixels. Keep the full source JPEG in assets.
    """
    image = ImageReader(str(ROOT / "assets" / "material-browser-capture.jpeg"))
    iw, ih = image.getSize()
    left, top, right, bottom = (59, 137, 1119, 862) if material == "clear" else (59, 1010, 1119, 1735)
    scale = w / (right - left)
    h = (bottom - top) * scale
    c.saveState()
    clip_round(c, x, y, w, h, 12)
    c.drawImage(image, x - left * scale, y - (ih - bottom) * scale,
                width=iw * scale, height=ih * scale)
    c.restoreState()
    return h


validate_geometry()
build_refraction_figures(ROOT / "assets")
g = Guide(OUT)

# 1 / overview
g.begin("Overview")
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
y = g.title("裁出来的，必须是背景里的同一块。", 835, 33)
g.body("左图是铺满视口的背景，虚线框标出玻璃组件的位置。右图只把框内的原始纹理等比放大；此时还没有折射，也没有圆角遮罩。", M, y - 8, W - 2 * M, 11.5, 20)
g.label("1. VIEWPORT / COVER", M, 718)
draw_background_crop(g.c, M, 460, 370, 234)
crop = (190, 62, 130, 90)
rx, ry, rw, rh = M + crop[0], 460 + crop[1], crop[2], crop[3]
g.c.setStrokeColor(Color(0, 0, 0, .65))
g.c.setLineWidth(3)
g.c.rect(rx, ry, rw, rh, fill=0, stroke=1)
g.c.setStrokeColor(HexColor("#FFFFFF"))
g.c.setLineWidth(1.7)
g.c.setDash(5, 3)
g.c.rect(rx, ry, rw, rh, fill=0, stroke=1)
g.c.setDash()
g.label("2. LOCAL TEXTURE", 484, 675)
draw_background_crop(g.c, 484, 502, 188, 188 * 90 / 130, crop)
g.arrow(432, 567, 474, 567, BLUE, 1.4, 7)
g.body("同一纹理，等比放大", 484, 482, 188, 10, 17, INK)
g.body("虚线只标示采样范围，不会写入背景纹理。圆角形状由下一步 Shader 的遮罩决定。", M, 435, W - 2 * M, 10.1, 17, MUTED)
g.step(M, 306, 194, 1, "MEASURE", "读取组件的 rect：left、top、width、height。")
g.step(M + 215, 306, 194, 2, "CROP", "使用同一 cover 比例，按 rect 换算局部偏移。")
g.step(M + 430, 306, 194, 3, "UPLOAD", "将局部 Canvas 上传为该组件的背景纹理。")
g.code(M, 280, W - 2 * M, ["const rect = card.getBoundingClientRect();", "const scale = Math.max(vw / iw, vh / ih);", "const dx = (vw - iw * scale) / 2 - rect.left;", "const dy = (vh - ih * scale) / 2 - rect.top;", "ctx.drawImage(image, dx, dy, iw * scale, ih * scale);"], "local crop from the controlled background source", 14, 7.8)
g.body("这里重建的是受控背景源与主题蒙层，并非给整个页面截图。普通 DOM、视频和另一层玻璃不会自动进入纹理。", M, 86, W - 2 * M, 10, 17, MUTED)
g.end()


# 3 / geometry
g.begin("02 / Rounded geometry")
y = g.title("距离边界多远，与走到边界几成。", 835, 33)
g.body("SDF 给出到边界的有符号距离；径向归一化给出从中心走向该方向边界的比例。两者用途不同，不能当成同一个量。", M, y - 8, W - 2 * M, 11.5, 20)
g.panel(M, 460, 298, 248, Color(1, 1, 1, .60), 17)
g.label("A. SIGNED DISTANCE / PIXELS", M + 18, 681)
ax, ay, aw, ah, ar = 82, 535, 230, 110, 30
g.c.setFillColor(HexColor("#D7E0E4"))
g.c.setStrokeColor(NAVY)
g.c.setLineWidth(1.2)
g.c.roundRect(ax, ay, aw, ah, ar, fill=1, stroke=1)
for px, py, label, color, label_y in [(197, 590, "sd < 0", GREEN, 571), (312, 590, "sd = 0", NAVY, 571), (250, 659, "sd > 0", ROSE, 673)]:
    value = float(round_box(px - ax, py - ay, aw, ah, ar))
    assert (value < 0 if '<' in label else value > 0 if '>' in label else abs(value) < 1e-8)
    g.c.setFillColor(color)
    g.c.circle(px, py, 4, fill=1, stroke=0)
    g.c.setFont("Courier-Bold", 8)
    g.c.drawCentredString(px, label_y, label)
g.body("内部为负，边界为 0，外部为正。\n用于形状遮罩，以及按像素控制边缘厚度。", M + 18, 503, 262, 9.7, 17, MUTED)
g.panel(374, 460, 298, 248, Color(1, 1, 1, .60), 17)
g.label("B. RADIAL FRACTION / UNITLESS", 392, 681)
bx, by, bw, bh, br = 399, 535, 248, 110, 30
cx, cy = bx + bw / 2, by + bh / 2
g.c.setFillColor(HexColor("#DCE3E6"))
g.c.setStrokeColor(NAVY)
g.c.setLineWidth(1.1)
g.c.roundRect(bx, by, bw, bh, br, fill=1, stroke=1)
for angle in (-2.75, -2.0, -1.1, -.55, .32, 1.05, 2.0, 2.75):
    dx, dy = math.cos(angle), math.sin(angle)
    radius = float(radial_boundary(dx, dy, bw, bh, br))
    ex, ey = cx + dx * radius, cy + dy * radius
    assert abs(float(round_box(ex - bx, ey - by, bw, bh, br))) < 1e-8
    g.c.setStrokeColor(BLUE)
    g.c.setLineWidth(.8)
    g.c.line(cx, cy, ex, ey)
    g.c.setFillColor(NAVY)
    g.c.circle(ex, ey, 2.2, fill=1, stroke=0)
g.c.setStrokeColor(NAVY)
g.c.line(cx, cy, bx + bw, cy)
for px, label in [(cx, "0"), (cx + bw / 4, "0.5"), (bx + bw, "1")]:
    g.c.setFillColor(NAVY)
    g.c.circle(px, cy, 3.2, fill=1, stroke=0)
    g.c.setFont("Courier-Bold", 8)
    g.c.drawCentredString(px, cy - 18, label)
g.body("每条射线都止于真实边界。\n中心为 0，该方向的半程为 0.5，边界为 1。", 392, 503, 262, 9.7, 17, MUTED)
g.code(M, 426, 300, ["vec2 q = abs(point-u_res*.5)", "  -(u_res*.5-vec2(u_corner));", "float sd = length(max(q,0.))", "  + min(max(q.x,q.y),0.) - u_corner;"], "rounded rectangle SDF", 14, 7.4)
g.code(372, 426, 300, ["vec2 rel = px - u_res * .5;", "vec2 p = rel / radialBoundary(rel);", "float s = length(p);", "// static shape: center 0, boundary 1"], "normalized radial distance", 14, 7.4)
g.body("左图决定轮廓，右图组织整张玻璃的光学变化。", M, 260, W - 2 * M, 15, 24, INK)
g.body("例如同样向内 5 个像素，适合用 SDF 描述；从中心走到边界的一半，适合用径向比例描述。后者不是到最近边界的距离。", M, 225, W - 2 * M, 11, 19, MUTED)
g.panel(M, 84, W - 2 * M, 82, Color(1, 1, 1, .62), 15)
g.body("图示为静态几何。生产 Shader 在此基础上加入轻微的边界波动，再得到用于折射的 radius 与 rr；不能把图中的比例 s 直接等同于动画中的 rr。", M + 18, 135, W - 2 * M - 36, 10.3, 18, INK)
g.end()


# 4 / refraction
g.begin("03 / Refraction field")
y = g.title("折射，本质上是换一个位置读取背景。", 835, 35)
g.body("每个像素先得到归一化位置 p，再由整体透镜和低频波动计算位移 shift。最终不是给像素涂颜色，而是去背景纹理的邻近位置重新取色。", M, y - 8, W - 2 * M, 11.5, 20)
g.label("1. SOURCE GRID / ORIGINAL UV", M, 680)
g.label("2. SAME GRID / REFRACTED UV", 412, 680)
g.c.drawImage(str(ROOT / "assets" / "refraction-source.png"), M, 502, 260, 150)
g.c.drawImage(str(ROOT / "assets" / "refraction-sampling.png"), 412, 502, 260, 150)
g.arrow(324, 577, 394, 577, BLUE, 1.6, 8)
g.c.setFont("Courier-Bold", 8)
g.c.setFillColor(NAVY)
g.c.drawCentredString(359, 593, "SHIFT UV")
g.body("网格按生产位移公式重算，固定 t = 0，仅展示折射采样项；没有添加烟灰、色调或高光。完整材质的实机截图见下一页。", M, 479, W - 2 * M, 10, 17, MUTED)
flow = [("p", "归一化位置"), ("rr / ang", "半径与方向"), ("shift", "透镜与低频波动"), ("refrUv", "新的采样坐标")]
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
y = g.title("同一算法，两种玻璃。", 835, 35)
g.body("下面是手机浏览器的真实渲染截图。两块玻璃使用相同的背景、裁切和尺寸；图中已经包含折射、材质与边缘光学效果。", M, y - 8, W - 2 * M, 11.5, 20)
g.label("01 / CLEAR", M, 719, NAVY)
g.label("02 / SMOKED", 372, 719, NAVY)
captured_material(g.c, M, 496, 300, "clear")
captured_material(g.c, 372, 496, 300, "smoked")
g.body("透明：背景透射较亮。树枝和窗框在玻璃内弯曲，上层文字仍保持清晰。", M, 474, 300, 10.4, 18, INK)
g.body("烟灰：主体透射降低，仍能看见背景细节；内侧暗边与局部高光保留体积感。", 372, 474, 300, 10.4, 18, INK)
g.body("这是两套生产材质预设的对照。它们共用同一套光学算法，但烟灰预设还将折射强度乘以 1.06、高光强度乘以 0.92，并使用不同的色调与边缘参数。", M, 409, W - 2 * M, 10.5, 18, MUTED)
g.label("LUMINANCE ADAPTATION / SHADER EXCERPT", M, 335)
g.code(M, 315, W - 2 * M, ["float smokeLum = dot(color, vec3(0.2126, 0.7152, 0.0722));", "float smokeBright = smoothstep(0.42, 0.84, smokeLum);", "float smokeWidth = mix(7.2, 4.25, smokeBright);", "float smokeEdgeLoss = mix(0.27, 0.085, smokeBright);"], "sampled brightness controls the smoked edge", 15, 8.0)
g.body("边缘如何适应背景", M, 181, W - 2 * M, 13, 21, INK)
g.body("亮区：吸光边缘更窄、更轻；暗区：保留更多吸光厚度。判断依据是采样颜色的亮度，而不是日间或夜间标签。", M, 155, W - 2 * M, 10.5, 18, MUTED)
g.c.setStrokeColor(RULE)
g.c.line(M, 99, W - M, 99)
g.label("PHONE CAPTURE / 2026-11-05 / PRODUCTION SHADER V5", M, 79)
g.body("截图以静态图片嵌入，PDF 无需运行 WebGL。图像仅裁切排版，未重绘或添加玻璃效果。", M, 58, W - 2 * M, 9.1, 15, MUTED)
g.end()

# 6 / shared renderer
g.begin("05 / Shared renderer")
y = g.title("轮流借用渲染器，各自保存画面。", 835, 34)
g.body("每个组件有自己的背景纹理与输出 Canvas。它们依次借用同一个 WebGL 绘制表面：绘制 A 后立刻复制给 A，再处理 B。", M, y - 8, W - 2 * M, 11.5, 20)
g.label("PER-CARD INPUT", M, 706)
g.label("SHARED RENDERER", 258, 706)
g.label("PER-CARD OUTPUT", 482, 706)
g.panel(258, 452, 178, 226, CODE, 17, HexColor("#30363C"))
g.c.setFont("Courier-Bold", 8)
g.c.setFillColor(HexColor("#E8ECEE"))
g.c.drawString(274, 656, "1 WEBGL CONTEXT")
for idx, (name, yy) in enumerate([("A", 610), ("B", 550), ("C", 490)], 1):
    g.panel(M, yy - 25, 170, 50, Color(1, 1, 1, .64), 11)
    g.label("TEXTURE " + name, M + 13, yy + 7, NAVY)
    g.body("该组件裁取的背景", M + 13, yy - 12, 144, 9.2, 14, MUTED)
    g.arrow(225, yy, 251, yy, BLUE, 1.1, 5)
    g.c.setFont("Courier", 8.4)
    g.c.setFillColor(HexColor("#E8ECEE"))
    g.c.drawString(277, yy - 3, f"{idx}. draw {name}")
    g.arrow(443, yy, 475, yy, BLUE, 1.1, 5)
    g.panel(482, yy - 25, 190, 50, Color(1, 1, 1, .64), 11)
    g.label("2D CANVAS " + name, 495, yy + 7, NAVY)
    g.body("立即复制本次绘制的像素", 495, yy - 12, 164, 9.2, 14, MUTED)
g.body("三个编号表示先后顺序，不是三个并行的 GPU 渲染器。文字与交互仍位于输出 Canvas 上方的 DOM 中。", M, 425, W - 2 * M, 10.3, 17, INK)
g.code(M, 393, W - 2 * M, ["gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);", "// Copy this card before another card reuses the surface.", "output.clearRect(0, 0, width, height);", "output.drawImage(renderSurface, 0, 0);"], "draw, copy immediately, then process the next card", 15, 7.7)
g.label("OFFSCREEN / THREE DIFFERENT RESOURCES", M, 260)
g.panel(M, 126, W - 2 * M, 108, Color(1, 1, 1, .62), 15)
for x in [250, 460]:
    g.c.setStrokeColor(RULE)
    g.c.line(x, 144, x, 216)
g.label("GPU TEXTURE", M + 18, 208, ROSE)
g.body("删除纹理\n重新进入时重建", M + 18, 185, 170, 10.2, 19, INK)
g.label("BACKDROP CANVAS", 268, 208, ROSE)
g.body("采样画布尺寸归零\n释放这份像素缓冲", 268, 185, 174, 10.2, 19, INK)
g.label("OUTPUT 2D CANVAS", 478, 208, GREEN)
g.body("保留最近画面\nGPU 丢失时仍可显示", 478, 185, 176, 10.2, 19, INK)
g.body("“1 个 context”指单个文档中的一次玻璃引擎实例。独立 iframe 各有自己的实例，截图对照页因此使用两个。", M, 92, W - 2 * M, 9.8, 17, MUTED)
g.end()


# 7 / lifecycle
g.begin("06 / Lifecycle and reuse")
y = g.title("离屏会暂停，回来还能继续。", 835, 34)
g.body("可见性决定是否绘制；dirty 表示背景纹理需要重建；节点移除才销毁组件。这三件事不能画成一条单向流程。", M, y - 8, W - 2 * M, 11.3, 20)
g.panel(M, 655, W - 2 * M, 66, Color(.93, .89, .90, .66), 13)
g.label("DIRTY / INDEPENDENT FLAG", M + 17, 700, ROSE)
g.body("壁纸、主题、滚动或尺寸变化使背景纹理失效。下次绘制前重建；尺寸变化可能立即触发绘制。", M + 17, 679, W - 2 * M - 34, 10.1, 17, INK)
g.panel(M, 492, 238, 120, Color(1, 1, 1, .64), 15)
g.label("VISIBLE", M + 18, 585, NAVY)
g.body("观察区内：允许绘制\n页面隐藏时暂停\n减少动态效果时仅按需重绘", M + 18, 560, 202, 10.4, 19, INK)
g.panel(434, 492, 238, 120, Color(1, 1, 1, .64), 15)
g.label("OFFSCREEN", 452, 585, BLUE)
g.body("观察区外：暂停绘制\n释放纹理与背景缓冲\n保留自己的 2D 输出快照", 452, 560, 202, 10.4, 19, INK)
g.arrow(296, 567, 424, 567, BLUE, 1.2, 6)
g.body("离开观察区", 310, 580, 100, 9.4, 14, MUTED)
g.arrow(424, 526, 296, 526, BLUE, 1.2, 6)
g.body("重新进入", 318, 507, 94, 9.4, 14, MUTED)
g.c.setStrokeColor(RULE)
g.c.setLineWidth(1)
g.c.line(167, 492, 167, 453)
g.c.line(553, 492, 553, 453)
g.c.line(167, 453, 553, 453)
g.body("节点移除（任一状态）", 300, 467, 180, 9.2, 14, MUTED)
g.arrow(360, 453, 360, 440, RULE, 1, 5)
g.panel(M, 389, W - 2 * M, 51, Color(1, 1, 1, .64), 12)
g.label("DISPOSE", M + 17, 412, ROSE)
g.body("断开监听、释放纹理、移除输出画布，并从渲染集合中注销。", M + 125, 411, 480, 10, 17, INK)
g.code(M, 365, W - 2 * M, ["if (disposed || !visible || document.hidden || w < 5) return;", "if (reduced) { if (dirty || generationChanged) draw(0); return; }", "if (ms - last < 48) return;   // visible-card frame cap", "last = ms; draw(ms * .001);  // texture rebuilt only when dirty"], "frame policy, condensed", 14, 7.45)
g.label("CURRENT BUDGETS", M, 248)
budgets = [("DPR CAP", "1.5"), ("VISIBLE FPS", "~ 20"), ("IO MARGIN", "40 px"), ("HERO BLUR", "2.25 px"), ("FALLBACK", "CSS")]
for i, (name, value) in enumerate(budgets):
    x = M + i * 126
    g.panel(x, 175, 112, 56, Color(1, 1, 1, .58), 12)
    g.c.setFont("Courier-Bold", 10)
    g.c.setFillColor(INK)
    g.c.drawString(x + 12, 208, value)
    g.c.setFont("Courier", 6.5)
    g.c.setFillColor(MUTED)
    g.c.drawString(x + 12, 190, name)
g.c.setStrokeColor(RULE)
g.c.line(M, 145, W - M, 145)
g.label("PUBLIC SCOPE", M, 122)
g.body("只发布光学说明、选定的示例图与实现片段。完整应用、聊天后端与账户数据不在其中。上游来源与许可说明见仓库 CREDITS.md。", M, 99, W - 2 * M, 9.5, 16, MUTED)
g.body("PROJECT: github.com/yanceydaisy/liquid-glass-note", M, 51, W - 2 * M, 6.8, 11, BLUE, "Courier")
g.end()


g.save()
print(OUT)
