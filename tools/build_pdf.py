from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color
import math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/liquid-glass-technical-guide-v4.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
W,H=720,960
M=48
PAPER=HexColor('#F3F4F2'); INK=HexColor('#15181C'); NAVY=HexColor('#173149')
MUTED=HexColor('#737B83'); RULE=HexColor('#C9CDD0'); PALE=HexColor('#E8EBEC')
BLUE=HexColor('#647F99'); ROSE=HexColor('#A9878C'); CODE=HexColor('#171B20')
pdfmetrics.registerFont(TTFont('NotoSerifSC',str(ROOT/'assets/noto-serif-sc.ttf')))
pdfmetrics.registerFont(TTFont('Mono','/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
pdfmetrics.registerFont(TTFont('Sans','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))

def sw(text,font,size): return pdfmetrics.stringWidth(text,font,size)
def lines(text,font,size,width):
    out=[]
    for paragraph in text.split('\n'):
        if not paragraph: out.append(''); continue
        cur=''
        for ch in paragraph:
            trial=cur+ch
            if cur and sw(trial,font,size)>width:
                out.append(cur);cur=ch
            else:cur=trial
        if cur:out.append(cur)
    return out

class Guide:
    def __init__(self,path):
        self.c=canvas.Canvas(str(path),pagesize=(W,H),pageCompression=1)
        self.c.setTitle('Liquid Glass Technical Guide v4')
        self.c.setAuthor('@whereyanlands')
        self.c.setSubject('A public implementation guide for the layered liquid-glass rendering system')
        self.c.setKeywords('liquid glass, WebGL, SDF, refraction, Canvas, UI')
        self.page=0
    def begin(self,section):
        self.page+=1;c=self.c;c.setFillColor(PAPER);c.rect(0,0,W,H,fill=1,stroke=0)
        c.setStrokeColor(RULE);c.setLineWidth(.55);c.line(M,H-54,W-M,H-54)
        c.setFont('Mono',7);c.setFillColor(HexColor('#9AA1A7'));c.drawString(M,H-38,f'{self.page:02d} / 07')
        c.setFillColor(NAVY);c.drawRightString(W-M,H-38,'LIQUID GLASS / V4')
        c.setFont('Mono',7);c.drawString(M,H-78,section.upper())
    def end(self):
        c=self.c;c.setStrokeColor(RULE);c.line(M,28,W-M,28)
        c.setFont('Mono',6.5);c.setFillColor(HexColor('#98A0A6'));c.drawString(M,15,'TECHNICAL GUIDE · PUBLIC EDITION')
        c.setFillColor(BLUE);c.drawCentredString(W/2,15,'@whereyanlands')
        c.setFillColor(HexColor('#98A0A6'));c.drawRightString(W-M,15,f'{self.page:02d}')
        c.showPage()
    def title(self,text,y,size=36,width=None):
        width=width or W-2*M;c=self.c;c.setFillColor(INK);c.setFont('NotoSerifSC',size)
        for line in lines(text,'NotoSerifSC',size,width):
            c.drawString(M,y,line);y-=size*1.22
        return y
    def body(self,text,x,y,width,size=11,leading=19,color=MUTED,font='NotoSerifSC'):
        c=self.c;c.setFont(font,size);c.setFillColor(color)
        for line in lines(text,font,size,width):c.drawString(x,y,line);y-=leading
        return y
    def label(self,text,x,y):
        c=self.c;c.setFont('Mono',7);c.setFillColor(BLUE);c.drawString(x,y,text.upper())
    def panel(self,x,y,w,h,fill=Color(1,1,1,.46),radius=18,stroke=RULE):
        c=self.c;c.setFillColor(fill);c.setStrokeColor(stroke);c.setLineWidth(.65);c.roundRect(x,y,w,h,radius,fill=1,stroke=1)
    def code(self,x,y,w,items,title=None,line_h=13,font_size=7.3):
        h=30+len(items)*line_h+(10 if title else 0);c=self.c
        c.setFillColor(CODE);c.roundRect(x,y-h,w,h,16,fill=1,stroke=0)
        yy=y-18
        if title:c.setFont('Mono',6.2);c.setFillColor(HexColor('#91A5B6'));c.drawString(x+18,yy,title.upper());yy-=18
        for i,line in enumerate(items,1):
            c.setFont('Mono',5.8);c.setFillColor(HexColor('#68737D'));c.drawString(x+16,yy,f'{i:02d}')
            c.setFont('Mono',font_size);c.setFillColor(HexColor('#E4E8EA'));c.drawString(x+42,yy,line);yy-=line_h
        return y-h
    def save(self):self.c.save()

g=Guide(OUT)

# 1
g.begin('Overview / 总览')
y=g.title('液态玻璃，是一条光学渲染链。',840,40)
y=g.body('它不等于给 div 加 blur。CSS 定义外壳，Canvas 重建局部背景，WebGL 重新计算折射与光，生命周期让玻璃在滚动、换肤和长聊天里保持正确。',M,y-12,620,12,21,HexColor('#626A71'))
g.c.setStrokeColor(RULE);g.c.line(M,y-28,W-M,y-28)
cols=[('01','SCENE','背景 / 主题 / 页面状态'),('02','SAMPLE','同一坐标系里的局部背景'),('03','OPTICS','纹理 / uniforms / 材质'),('04','UI','文字与交互独立叠加')]
py=y-168;cw=145
for i,(n,en,zh) in enumerate(cols):
    x=M+i*(cw+15);g.panel(x,py,cw,112)
    g.c.setFillColor(NAVY);g.c.setFont('Times-Roman',20);g.c.drawString(x+18,py+78,n)
    g.c.setFont('Mono',7);g.c.drawString(x+18,py+52,en)
    g.body(zh,x+18,py+31,cw-36,9,14,MUTED)
g.label('Render chain',M,py-46)
chain=[('SCENE','壁纸与页面底色'),('CROP','按组件位置采样'),('FIELD','圆角折射场'),('MATERIAL','透明 / 烟灰'),('SNAPSHOT','二维稳定输出')]
cy=py-115
for i,(a,b) in enumerate(chain):
    x=M+i*126;g.c.setFillColor(NAVY if i in (0,2,4) else HexColor('#343A40'));g.c.circle(x+11,cy+14,9,fill=1,stroke=0)
    if i<4:g.c.setStrokeColor(RULE);g.c.line(x+25,cy+14,x+113,cy+14)
    g.c.setFont('Mono',7);g.c.setFillColor(INK);g.c.drawString(x,cy-13,a)
    g.body(b,x,cy-31,105,8,12,MUTED)
g.panel(M,86,W-2*M,94,Color(1,1,1,.5),16)
g.label('一句话定点',M+20,151);g.body('玻璃先看见背景，再把它折射；文字始终留在上层。',M+20,122,W-2*M-40,16,24,INK)
g.end()

# 2
g.begin('01 / Background sampling')
y=g.title('先对齐背景，玻璃才不会穿帮。',835,34)
y=g.body('每个组件都从同一张全屏背景里，按自己在视口中的位置切出对应区域。我们重建壁纸、页面底色与主题蒙层；不会实时截图任意 DOM。',M,y-8,620,11,19)
g.label('Same source · local crop',M,662)
# sampling diagram
g.c.setFillColor(HexColor('#1B2531'));g.c.roundRect(M,390,360,240,16,fill=1,stroke=0)
g.c.setFillColor(Color(.67,.43,.48,.65));g.c.circle(M+80,555,120,fill=1,stroke=0)
g.c.setFillColor(Color(.35,.52,.72,.58));g.c.circle(M+310,430,150,fill=1,stroke=0)
g.c.setStrokeColor(HexColor('#ECF0F2'));g.c.setLineWidth(1.2);g.c.roundRect(M+190,458,118,92,22,fill=0,stroke=1)
g.c.setFont('Mono',7);g.c.setFillColor(HexColor('#ECF0F2'));g.c.drawString(M+206,442,'card rect')
g.c.setStrokeColor(BLUE);g.c.setLineWidth(1);g.c.line(420,510,456,510);g.c.line(449,516,456,510);g.c.line(449,504,456,510)
g.c.setFillColor(HexColor('#263847'));g.c.roundRect(470,430,202,160,25,fill=1,stroke=0)
g.c.setFillColor(Color(.35,.52,.72,.55));g.c.circle(630,430,110,fill=1,stroke=0)
g.c.setStrokeColor(HexColor('#EAF0F2'));g.c.roundRect(470,430,202,160,25,fill=0,stroke=1)
g.c.setFillColor(NAVY);g.c.setFont('Mono',7);g.c.drawString(470,405,'same background · local coordinates')
code=['const rect = card.getBoundingClientRect();','const scale = Math.max(vw / iw, vh / ih);','const dx = (vw - iw*scale)/2 - rect.left;','const dy = (vh - ih*scale)/2 - rect.top;','ctx.drawImage(image, dx, dy, iw*scale, ih*scale);','gl.texImage2D(..., backdrop);']
g.code(M,350,W-2*M,code,'actual sampling',13,7.6)
g.body('关键限制：普通文字、视频与叠在玻璃后的任意 DOM 不会自动进入纹理；多层玻璃也不是递归折射。公开 demo 使用同一张自托管背景来保证坐标一致。',M,114,W-2*M,9.5,16,MUTED)
g.end()

# 3
g.begin('02 / Rounded geometry')
y=g.title('形状不是裁出来的，光也要认识圆角。',835,34)
y=g.body('CSS 的尺寸与圆角会作为 uniforms 传进 Shader。roundBox() 给出真实圆角矩形的有符号距离；radialBoundary() 则让任意长宽比都拥有从中心到边缘的统一光学坐标。',M,y-8,620,11,19)
# two geometry panels
for x,title in [(M,'SIGNED DISTANCE'),(374,'NORMALIZED FIELD')]:
    g.panel(x,455,298,220)
    g.label(title,x+18,646)
g.c.setFillColor(HexColor('#D7E0E4'));g.c.roundRect(90,495,206,112,34,fill=1,stroke=0)
for i in range(5):
    g.c.setStrokeColor(Color(.10,.23,.32,.18+.11*i));g.c.setLineWidth(.6);g.c.roundRect(82-i*7,487-i*7,222+i*14,128+i*14,41+i*7,fill=0,stroke=1)
g.c.setFillColor(NAVY);g.c.circle(193,551,3,fill=1,stroke=0);g.c.setFont('Mono',7);g.c.drawString(110,472,'sd < 0 inside · sd = 0 boundary')
cx,cy=523,551
g.c.setFillColor(HexColor('#DCE3E6'));g.c.roundRect(414,495,218,112,34,fill=1,stroke=0)
for ang in [-2.6,-2,-1.25,-.55,0,.6,1.25,2,2.6]:
    ex=cx+math.cos(ang)*104;ey=cy+math.sin(ang)*52;g.c.setStrokeColor(BLUE);g.c.line(cx,cy,ex,ey)
g.c.setFillColor(NAVY);g.c.circle(cx,cy,4,fill=1,stroke=0);g.c.setFont('Mono',7);g.c.drawString(430,472,'p = relative / boundary(relative)')
code1=['float roundBox(vec2 point) {','  vec2 q = abs(point-u_res*.5)','    -(u_res*.5-vec2(u_corner));','  return length(max(q,0.))','    +min(max(q.x,q.y),0.)-u_corner;','}']
code2=['vec2 rel = px - u_res*.5;','vec2 p = rel / radialBoundary(rel);','float rr = clamp(length(p), 0., 1.);','','// center ≈ 0 · edge ≈ 1']
g.code(M,416,298,code1,'rounded-rect sdf',12,6.7)
g.code(374,416,298,code2,'field coordinates',12,6.7)
g.panel(M,92,W-2*M,84,Color(1,1,1,.5),16);g.body('这一步解决了“宽卡片被当成拉长的圆形透镜”的问题。后面的折射、暗边和高光都共享同一组几何坐标。',M+20,142,W-2*M-40,11,19,INK)
g.end()

# 4
g.begin('03 / Refraction field')
y=g.title('折射覆盖整块表面，而不是一圈边框。',835,34)
y=g.body('径向透镜负责整体的厚度变化，低频双轴波动提供轻微流动。两者相加后转换成 UV 偏移，再从背景纹理的另一个位置取色。',M,y-8,620,11,19)
g.label('Field composition',M,660)
items=[('p','归一化位置'),('rr','中心到边缘'),('wave','双轴低频扰动'),('shift','透镜 + 波动'),('refrUv','重新采样背景')]
for i,(a,b) in enumerate(items):
    x=M+i*126;g.panel(x,536,112,90,Color(1,1,1,.45),14)
    g.c.setFont('Mono',10);g.c.setFillColor(NAVY);g.c.drawString(x+13,590,a)
    g.body(b,x+13,563,88,8,12,MUTED)
    if i<4:g.c.setStrokeColor(BLUE);g.c.line(x+112,581,x+126,581)
code=['float edgeGain = smoothstep(0.05, 0.97, rr);','float strength = (0.052 + 0.12*edgeGain)','  * u_refract * u_lDistort;','vec2 wave = vec2(','  sin(p.y*3.1+p.x*1.4+u_time*.18)*cos(p.x*2.2),','  cos(p.x*3.4-p.y*1.3-u_time*.15)*sin(p.y*2.1+.8)',');','vec2 shift = p*lensShift + wave*strength;','vec2 refrUv = v_uv + vec2(shift.x/u_res.x,','                              -shift.y/u_res.y);','vec3 refr = texture2D(u_bg, clamp(refrUv,.001,.999)).rgb;']
g.code(M,500,W-2*M,code,'continuous interior lens',13,7.0)
g.label('Tuning baseline',M,250)
vals=[('refract','26'),('tint','0'),('blur','0'),('edge','25'),('shine','13'),('wobble','15')]
for i,(a,b) in enumerate(vals):
    x=M+i*104;g.c.setFillColor(NAVY if i in (0,3) else HexColor('#353B40'));g.c.circle(x+10,205,10,fill=1,stroke=0)
    g.c.setFont('Times-Roman',16);g.c.setFillColor(INK);g.c.drawString(x,173,b);g.c.setFont('Mono',6.5);g.c.setFillColor(MUTED);g.c.drawString(x,155,a)
g.body('参数是这套 Shader 的调节刻度，并非物理单位。位移太强会像水波，过度集中在边缘则会重新退化成“玻璃边框”。',M,112,W-2*M,9.5,16,MUTED)
g.end()

# 5
g.begin('04 / Material & light')
y=g.title('同一套光学，两种透射性格。',835,36)
y=g.body('透明与烟灰材质共用 Shader。区别来自透射衰减、内侧吸光、清透折射带，以及随背景亮度变化的边缘配方。',M,y-8,620,11,19)
# material cards
for x,name,fill in [(M,'CLEAR',Color(.82,.88,.94,.42)),(374,'SMOKED',Color(.17,.20,.24,.82))]:
    g.c.setFillColor(HexColor('#BAC7D2'));g.c.roundRect(x,515,298,150,34,fill=1,stroke=0)
    g.c.setFillColor(fill);g.c.roundRect(x+18,535,262,110,28,fill=1,stroke=0)
    g.c.setStrokeColor(Color(1,1,1,.7));g.c.arc(x+18,535,x+280,645,110,52)
    g.c.setFont('Mono',8);g.c.setFillColor(HexColor('#F0F2F3') if name=='SMOKED' else NAVY);g.c.drawString(x+34,610,name)
    g.body('保留背景细节' if name=='CLEAR' else '衰减透射 + 内侧暗部',x+34,579,225,10,16,HexColor('#F0F2F3') if name=='SMOKED' else INK)
g.label('Luminance adaptation',M,478)
g.body('lum = dot(color, vec3(0.2126, 0.7152, 0.0722))',M,451,620,10,16,NAVY,'Mono')
g.body('亮场：暗边更窄、更轻，均匀白环被抑制。  深场：保留更多吸光厚度与局部高光。',M,425,620,10,17,MUTED)
code=['float bright = smoothstep(0.42, 0.84, lum);','float smokeWidth = mix(7.2, 4.25, bright);','float edgeLoss  = mix(0.27, 0.085, bright);','','float hairline  = exp(-pow((sd + .46)/.43, 2.));','float upperLeft = exp(-pow((ang + 2.38)/.60, 2.));','float lowerRight= exp(-pow((ang - .76)/.62, 2.));','float glint = hairline*(upperLeft*.66 + lowerRight*.48);']
g.code(M,390,W-2*M,code,'adaptive smoke + directional glint',13,7.2)
g.panel(M,92,W-2*M,70,Color(1,1,1,.5),15);g.body('方向性高光比整圈白描边更重要。浅色背景尤其需要收掉全周 Fresnel，否则玻璃会变成发亮的塑料按钮。',M+18,133,W-2*M-36,10.5,18,INK)
g.end()

# 6
g.begin('05 / Shared renderer')
y=g.title('一套 WebGL，许多稳定的玻璃快照。',835,34)
y=g.body('长聊天不能为每个气泡申请一个 WebGL 上下文。当前版本由整页共享 program 与 buffer；每个组件只保存自己的背景纹理和二维输出 Canvas。',M,y-8,620,11,19)
g.label('Shared GPU · independent outputs',M,654)
# renderer diagram
g.panel(M,442,160,170,Color(.09,.11,.14,1),22,HexColor('#30363C'))
g.c.setFont('Mono',8);g.c.setFillColor(HexColor('#E8ECEE'));g.c.drawString(M+20,574,'WEBGL SURFACE')
g.body('program\nbuffer\nshader',M+20,540,120,10,20,HexColor('#BFC8CE'),'Mono')
g.c.setStrokeColor(BLUE);g.c.setLineWidth(1.2)
for yy in (568,523,478):g.c.line(208,yy,270,yy);g.c.line(263,yy+5,270,yy);g.c.line(263,yy-5,270,yy)
for i,(name,y0) in enumerate([('CARD A',532),('CHAT B',487),('DOCK C',442)]):
    g.panel(282,y0,390,34,Color(1,1,1,.5),10);g.c.setFont('Mono',7);g.c.setFillColor(NAVY);g.c.drawString(296,y0+13,name)
    g.c.setFillColor(HexColor('#738B9D'));g.c.rect(382,y0+8,88,18,fill=1,stroke=0);g.c.setFillColor(HexColor('#D6DDE1'));g.c.rect(485,y0+8,165,18,fill=1,stroke=0)
g.c.setFont('Mono',6.5);g.c.setFillColor(MUTED);g.c.drawString(382,420,'texture');g.c.drawString(485,420,'stable 2D snapshot')
code=['gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);','','// Copy before the shared drawing buffer is discarded.','output.clearRect(0, 0, width, height);','output.drawImage(renderSurface, 0, 0);','','// Text remains normal DOM above the canvas.']
g.code(M,382,W-2*M,code,'render then snapshot',13,7.3)
g.label('Why it matters',M,212)
g.body('屏幕外的气泡可以释放 GPU 纹理，却保留已经渲染好的二维画面；WebGL context 暂时丢失时，旧内容也不会全部变空。',M,183,620,11,19,INK)
g.body('这是 v4 相比旧方案最关键的工程变化：从“每块玻璃一个上下文”，转为“一个渲染器，多份稳定输出”。',M,120,620,9.5,16,MUTED)
g.end()

# 7
g.begin('06 / Lifecycle & reuse')
y=g.title('玻璃一直活着，但只在必要时工作。',835,34)
y=g.body('背景更新与材质动画分开。滚动、尺寸、主题和壁纸变化只标记 dirty；可见组件按上限频率绘制，离屏后释放纹理并保留二维快照。',M,y-8,620,11,19)
g.label('Lifecycle',M,666)
events=[('RESIZE','重读尺寸与圆角'),('SCROLL','重算局部采样位置'),('THEME / BG','重建背景纹理'),('OFFSCREEN','暂停并释放 texture'),('DISPOSE','清理 observer 与资源')]
for i,(a,b) in enumerate(events):
    yy=626-i*55;g.c.setFillColor(NAVY if i in (0,3) else HexColor('#3C4248'));g.c.circle(M+10,yy+6,8,fill=1,stroke=0)
    g.c.setFont('Mono',7);g.c.setFillColor(INK);g.c.drawString(M+32,yy+3,a);g.body(b,M+148,yy+3,430,9.5,15,MUTED)
g.code(M,340,W-2*M,['if (!visible || document.hidden) return;','if (!reduced && ms-last < 48) return;','last = ms;','','if (dirty) redrawTexture();','draw(reduced ? 0 : ms * 0.001);'],'frame budget',13,7.5)
g.label('Current budgets',M,226)
budgets=[('DPR','≤ 1.5'),('VISIBLE FPS','≈ 20'),('WEBGL CONTEXT','1'),('HERO BLUR','2.25 px'),('FALLBACK','CSS blur')]
for i,(a,b) in enumerate(budgets):
    x=M+i*126;g.c.setFont('Times-Roman',17);g.c.setFillColor(INK);g.c.drawString(x,188,b);g.c.setFont('Mono',6);g.c.setFillColor(MUTED);g.c.drawString(x,169,a)
g.c.setStrokeColor(RULE);g.c.line(M,142,W-M,142)
g.label('Public scope',M,119)
g.body('公开仓库只提供光学思路、最小 demo 与技术册。真实 Home、私人背景、聊天逻辑和个人数据不在其中。',M,94,W-2*M,9.2,15,MUTED)
g.body('UPSTREAM: VII-Cae/hyalite--liquid-glass (MIT) · everett745/liquid-glass (NO LICENCE DECLARED)',M,57,W-2*M,6.8,11,MUTED,'Mono')
g.body('PROJECT: github.com/yanceydaisy/liquid-glass-note',M,44,W-2*M,6.8,11,BLUE,'Mono')
g.end();g.save()
print(OUT)
