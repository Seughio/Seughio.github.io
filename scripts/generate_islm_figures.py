"""Native SVG figures for chapter 3. Standard-library-only, no runtime scripts.

All line endpoints, equilibria and projections use the data-coordinate map.
Y and r have different units: x and y scales are explicit and independent.
"""
from dataclasses import dataclass
from html import escape
from math import isclose, sin, cos, pi
from pathlib import Path
import json

OUT = Path(__file__).resolve().parents[1] / 'docs/金融学/宏观经济学/figures'


@dataclass(frozen=True)
class Curve:
    name: str
    intercept: float
    slope: float
    style: str
    dy: int = 5


@dataclass(frozen=True)
class Scene:
    name: str
    title: str
    domain: tuple
    rates: tuple
    curves: tuple
    points: tuple  # income, rate, dot style


SCENES = (
    Scene('is', 'IS 曲线', (1600, 2400), (0, 40),
          (Curve('IS', 100, -.04, 'is'),),
          ((1800, 28, 'is-dot'), (2200, 12, 'is-dot'))),
    Scene('lm', 'LM 曲线', (1600, 2400), (0, 40),
          (Curve('LM', -60, .04, 'lm'),),
          ((1800, 12, 'lm-dot'), (2200, 28, 'lm-dot'))),
    Scene('equilibrium', 'IS 与 LM 的共同均衡', (1600, 2400), (0, 40),
          (Curve('IS', 100, -.04, 'is'), Curve('LM', -60, .04, 'lm')),
          ((2000, 20, 'ink-dot'),)),
    Scene('fiscal', '财政扩张', (1975, 2045), (18.2, 21.8),
          (Curve('IS₀', 100, -.04, 'is-old', -18),
           Curve('IS₁', 101.6, -.04, 'is'), Curve('LM', -60, .04, 'lm')),
          ((2000, 20, 'old-dot'), (2020, 20.8, 'is-dot'))),
    Scene('monetary', '货币扩张', (1975, 2045), (18.2, 21.8),
          (Curve('IS', 100, -.04, 'is', -18),
           Curve('LM₀', -60, .04, 'lm-old'), Curve('LM₁', -61.6, .04, 'lm')),
          ((2000, 20, 'old-dot'), (2020, 19.2, 'lm-dot'))),
    Scene('policy-mix', '收入提高而利率不变', (1975, 2045), (18.2, 21.8),
          (Curve('IS₀', 100, -.04, 'is-old', -18),
           Curve('LM₀', -60, .04, 'lm-old'),
           Curve('IS₁', 100.8, -.04, 'is'), Curve('LM₁', -60.8, .04, 'lm')),
          ((2000, 20, 'old-dot'), (2020, 20, 'ink-dot'))),
)


def fmt(v):
    return f'{v:.5f}'.rstrip('0').rstrip('.')


def render(scene, mobile=False):
    width, height, left, top, pw, ph = (400, 330, 52, 24, 276, 246) if mobile else (560, 362, 66, 26, 408, 276)
    right, bottom = left + pw, top + ph
    xmin, xmax = scene.domain
    rmin, rmax = scene.rates
    sx, sy = pw / (xmax - xmin), ph / (rmax - rmin)
    x = lambda y: left + (y - xmin) * sx
    y = lambda r: bottom - (r - rmin) * sy
    out = []

    def line(x1, y1, x2, y2, cls, **data):
        attrs = ''.join(f' data-{k}="{escape(str(v))}"' for k, v in data.items())
        out.append(f'<path class="{cls}" d="M{fmt(x1)} {fmt(y1)}L{fmt(x2)} {fmt(y2)}"{attrs}/>')

    def text(xx, yy, value, cls='label', anchor='start'):
        out.append(f'<text x="{fmt(xx)}" y="{fmt(yy)}" class="{cls}" text-anchor="{anchor}">{escape(value)}</text>')

    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">')
    out.append(f'<title id="title">{scene.title}</title>')
    desc = '；'.join(f'{c.name}: r={c.intercept:g}{c.slope:+g}Y' for c in scene.curves)
    desc += '；均衡或曲线上代表点：' + '、'.join(f'({a:g}, {b:g})' for a, b, _ in scene.points)
    out.append(f'<desc id="desc">{escape(desc)}。收入单位为亿元，利率按方程数值表示。</desc>')
    meta = dict(domain=scene.domain, rates=scene.rates, left=left, top=top,
                bottom=bottom, xScale=sx, rScale=sy,
                curves=[dict(name=c.name, a=c.intercept, b=c.slope) for c in scene.curves],
                points=scene.points)
    out.append('<metadata id="mapping">' + escape(json.dumps(meta, ensure_ascii=False)) + '</metadata>')
    out.append('''<style>
    :root {--paper:#fff;--ink:#46564c;--muted:#69766c;--green:#416f5d;
      --ochre:#ad7c51;--ochre-text:#96643e;--axis:#939f97;--guide:#e0e6e1;
      --old-is:#82998b;--old-lm:#a48d79;--old-point:#718078;
      --curve-width:1.8;--axis-width:.85;--guide-width:.75;
      --label-size:14px;--tick-size:12px;}
    text {font-family:'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',sans-serif;
      fill:var(--ink);font-size:var(--label-size);font-variant-numeric:tabular-nums;}
    path {fill:none;stroke-linecap:butt;}
    .axis {stroke:var(--axis);stroke-width:var(--axis-width);}
    .guide {stroke:var(--guide);stroke-width:var(--guide-width);stroke-dasharray:3 5;}
    .is {stroke:var(--green);stroke-width:var(--curve-width);}
    .lm {stroke:var(--ochre);stroke-width:var(--curve-width);}
    .is-old {stroke:var(--old-is);stroke-width:1.5;stroke-dasharray:4 4;}
    .lm-old {stroke:var(--old-lm);stroke-width:1.5;stroke-dasharray:4 4;}
    .is-label {fill:var(--green);}.lm-label {fill:var(--ochre-text);}
    .is-old-label,.lm-old-label {fill:var(--muted);}
    .tick {fill:var(--muted);font-size:var(--tick-size);}
    circle {stroke:var(--paper);stroke-width:1.1;}
    .is-dot {fill:var(--green);}.lm-dot {fill:var(--ochre);}
    .ink-dot {fill:var(--ink);}.old-dot {fill:var(--old-point);}
    </style>''')
    if mobile:
        out.append('<style>:root {--label-size:15px;--tick-size:13px;}</style>')
    out.append(f'<rect width="{width}" height="{height}" fill="var(--paper)"/>')
    # Shared rate projections are drawn once (not twice in the policy mix).
    projections = set()
    for yy, rr, _ in scene.points:
        for coords in [(left, y(rr), x(yy), y(rr)), (x(yy), y(rr), x(yy), bottom)]:
            if coords not in projections:
                line(*coords, 'guide')
                projections.add(coords)
    line(left, top, left, bottom, 'axis')
    line(left, bottom, right + 8, bottom, 'axis')
    for v in sorted(set([xmin] + [p[0] for p in scene.points])):
        text(x(v), bottom + 23, fmt(v), 'tick', 'middle')
    for v in sorted(set([rmin] + [p[1] for p in scene.points])):
        text(left - 12, y(v) + 4, fmt(v), 'tick', 'end')
    text(left - 10, top + 5, 'r', 'label', 'end')
    text(right + 21, bottom + 5, 'Y')
    for c in scene.curves:
        rlo, rhi = sorted(((rmin - c.intercept) / c.slope, (rmax - c.intercept) / c.slope))
        lo, hi = max(xmin, rlo), min(xmax, rhi)
        assert lo < hi
        e0, e1 = c.intercept + c.slope * lo, c.intercept + c.slope * hi
        line(x(lo), y(e0), x(hi), y(e1), c.style, name=c.name, a=c.intercept, b=c.slope)
        text(x(hi) + 10, y(e1) + c.dy, c.name, c.style + '-label')
    for yy, rr, style in scene.points:
        assert xmin <= yy <= xmax and rmin <= rr <= rmax
        assert any(isclose(c.intercept + c.slope * yy, rr) for c in scene.curves)
        out.append(f'<circle cx="{fmt(x(yy))}" cy="{fmt(y(rr))}" r="3.6" class="{style}"/>')
    out.append('</svg>')
    return '\n'.join(out) + '\n'


def render_extra(name, mobile=False):
    """Money-market equilibrium and a nonlinear, behavioral LM schematic."""
    import re
    width, height, left, top, pw, ph = (400, 330, 52, 24, 276, 246) if mobile else (560, 362, 66, 26, 408, 276)
    if mobile and name == 'money-market':
        top += 4
        ph -= 4
    bottom, right = top + ph, left + pw
    money = name == 'money-market'
    xmin, xmax = (200, 500) if money else (0, 1200)
    rmin, rmax = (0, 40) if money else (0, 26)
    sx, sy = pw/(xmax-xmin), ph/(rmax-rmin)
    x = lambda v: left+(v-xmin)*sx
    y = lambda v: bottom-(v-rmin)*sy
    title = '货币供求与均衡利率' if money else 'LM 的三个区域'
    desc = ('收入固定为2000，L=400-5r。实际货币供给由300增至350，均衡利率由20降至10。'
            if money else '行为特征示意：凯恩斯区域水平，中间区域逐渐变陡，古典区域垂直；不使用固定参数的线性LM。')
    styles = ''.join(re.findall(r'<style>.*?</style>', render(SCENES[0], mobile), re.S))
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
           f'<title id="title">{title}</title><desc id="desc">{desc}</desc>', styles,
           '<style>.region{font-size:13px;fill:var(--muted);}</style>',
           f'<metadata id="mapping">{escape(json.dumps(dict(domain=[xmin,xmax],rates=[rmin,rmax],left=left,top=top,bottom=bottom,xScale=sx,rScale=sy),ensure_ascii=False))}</metadata>',
           f'<rect width="{width}" height="{height}" fill="var(--paper)"/>']
    def line(x1,y1,x2,y2,cls):
        out.append(f'<path class="{cls}" d="M{fmt(x1)} {fmt(y1)}L{fmt(x2)} {fmt(y2)}"/>')
    def text(xx,yy,value,cls='label',anchor='start'):
        out.append(f'<text x="{fmt(xx)}" y="{fmt(yy)}" class="{cls}" text-anchor="{anchor}">{escape(value)}</text>')
    line(left,top,left,bottom,'axis');line(left,bottom,right+8,bottom,'axis')
    text(left-10,top+5,'r' if money else 'r','label','end')
    if money:
        for q,rr in [(300,20),(350,10)]:
            assert isclose(q,400-5*rr)
            line(left,y(rr),x(q),y(rr),'guide')
            text(x(q),bottom+23,str(q),'tick','middle')
            text(left-12,y(rr)+4,str(rr),'tick','end')
        text(x(200),bottom+23,'200','tick','middle')
        text(left-12,bottom+4,'0','tick','end')
        line(x(200),y(40),x(400),y(0),'is')
        text(x(400)+10,y(0)-12,'L','is-label')
        for q,cls,label in [(300,'lm-old','S₀'),(350,'lm','S₁')]:
            line(x(q),y(0),x(q),y(40),cls)
            text(x(q),y(40)-9,label,cls+'-label','middle')
        for q,rr,cls in [(300,20,'old-dot'),(350,10,'lm-dot')]:
            out.append(f'<circle cx="{fmt(x(q))}" cy="{fmt(y(rr))}" r="3.6" class="{cls}"/>')
        text(right+8,bottom+47,'M，L','label','end')
    else:
        text(right+21,bottom+5,'Y')
        text(left-12,bottom+4,'0','tick','end')
        text(left-12,y(2)+4,'r₀','tick','end')
        for q,rr,label in [(400,2,'Y₁'),(1000,20,'Y₂')]:
            line(x(q),y(0),x(q),y(rr),'guide')
            text(x(q),bottom+23,label,'tick','middle')
        points=[(0,2),(400,2)]
        for i in range(1,81):
            theta=(pi/2)*i/80
            yy,rr=400+600*sin(theta),2+18*(1-cos(theta))
            assert 400<=yy<=1000 and 2<=rr<=20
            points.append((yy,rr))
        points.append((1000,24))
        path='M'+'L'.join(f'{fmt(x(q))} {fmt(y(rr))}' for q,rr in points)
        out.append(f'<path class="lm" d="{path}"/>')
        text(x(1000)+10,y(24)+5,'LM','lm-label')
        for q,label in [(200,'凯恩斯区域'),(700,'中间区域')]:
            text(x(q),bottom+47,label,'region','middle')
        text(x(950),y(22),'古典区域','region','end')
    out.append('</svg>')
    return '\n'.join(out)+'\n'


def combined(title, width, height, content):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<style>:root{{--paper:#fff;--ink:#46564c;--muted:#69766c;--green:#416f5d;--ochre:#ad7c51;--ochre-text:#96643e;--axis:#939f97;--guide:#e0e6e1;--old-is:#82998b;--old-lm:#a48d79;--old-point:#718078;--curve-width:1.8;--axis-width:.85;--guide-width:.75;--label-size:15px;--tick-size:13px;}}
text{{font-family:'Microsoft YaHei','PingFang SC',sans-serif;fill:var(--ink);font-size:15px;font-variant-numeric:tabular-nums;}}path{{fill:none;}}.heading{{font-size:17px;}}.region{{fill:var(--muted);font-size:13px;}}</style>
<rect width="{width}" height="{height}" fill="white"/>{content}</svg>'''


def nest(svg, xx, yy, width, height, key):
    import re
    # Namespace embedded accessible IDs and retain native coordinate metadata.
    svg=re.sub(r'\bid="([^"]+)"', lambda m:f'id="{key}-{m[1]}"',svg)
    svg=svg.replace('aria-labelledby="title desc"',f'aria-labelledby="{key}-title {key}-desc"')
    return re.sub(r'<svg ',f'<svg x="{xx}" y="{yy}" ',svg,count=1).replace(
        re.search(r'width="[^"]+" height="[^"]+"',svg)[0],f'width="{width}" height="{height}"',1)


def mechanisms(mobile):
    width,height=(400,172) if mobile else (600,140)
    rows=[('IS', ['r↓','I↑','S↑','Y↑'],'其他条件不变'),
          ('LM', ['Y↑','L₁↑','r↑'],'M 固定')]
    out=[]
    for i,(name,nodes,condition) in enumerate(rows):
        baseline=43+i*(76 if mobile else 65)
        out.append(f'<text x="18" y="{baseline}" style="font-weight:600;fill:var(--{ "green" if i==0 else "ochre-text"})">{name}</text>')
        positions=([85,151,245,350] if mobile else [110,225,365,510]) if i==0 else ([85,216,350] if mobile else [110,310,510])
        for j,(xx,label) in enumerate(zip(positions,nodes)):
            out.append(f'<text x="{xx}" y="{baseline}" text-anchor="middle">{label}</text>')
            if j:
                arrow=(positions[j-1]+xx)/2
                # Leave the long labels clear of the connectors.
                if i==0 and j==2:arrow-=8
                if i==0 and j==3:arrow+=12
                out.append(f'<text x="{arrow}" y="{baseline}" text-anchor="middle" style="fill:var(--muted)">→</text>')
        out.append(f'<text x="{positions[0]}" y="{baseline+23}" style="font-size:12px;fill:var(--muted)">{condition}</text>')
    return combined('IS 与 LM 的沿线机制',width,height,''.join(out))


def money_regions(mobile):
    out=[]
    for i,(name,title) in enumerate([('money-market','货币市场'),('lm-regions','LM 三个区域')]):
        xx,yy=(0,i*365) if mobile else (i*450,0)
        out.append(f'<text x="{xx+52}" y="{yy+22}" class="heading">{title}</text>')
        out.append(nest(render_extra(name,True),xx,yy+38,400 if mobile else 450,330 if mobile else 371.25,name))
    return combined('货币市场与 LM 三个区域',400 if mobile else 900,738 if mobile else 412,''.join(out))


def equilibrium_regions(mobile):
    import re
    svg=render(SCENES[2],mobile)
    # Region labels replace projections: the axes still identify the equilibrium.
    svg=re.sub(r'<path class="guide"[^>]*/>', '', svg)
    left,top,pw,ph=(52,24,276,246) if mobile else (66,26,408,276)
    x=lambda v:left+(v-1600)*pw/800
    y=lambda v:top+ph-v*ph/40
    out=[]
    for name,yy,rr,goods,money in [('A',2000,34,'I < S','L < M'),('B',1750,20,'I > S','L < M'),('C',2000,6,'I > S','L > M'),('D',2250,20,'I < S','L > M')]:
        out.append(f'<text x="{x(yy)}" y="{y(rr)-10}" text-anchor="middle" style="font-size:15px;font-weight:600">{name}</text>')
        for dy,label in [(8,goods),(25,money)]:
            out.append(f'<text x="{x(yy)}" y="{y(rr)+dy}" text-anchor="middle" style="font-size:{12 if mobile else 13}px">{escape(label)}</text>')
    return svg.replace('</svg>',''.join(out)+'</svg>')


def policy_panel(scene, mobile):
    width,height,left,top,pw,ph=(400,266,63,48,268,165) if mobile else (320,310,56,55,204,199)
    xmin,xmax=scene.domain;rmin,rmax=scene.rates
    x=lambda v:left+(v-xmin)*pw/(xmax-xmin)
    y=lambda v:top+ph-(v-rmin)*ph/(rmax-rmin)
    out=[f'<text x="{width/2}" y="22" text-anchor="middle" style="font-size:{17 if mobile else 19}px">{scene.title if scene.name != "policy-mix" else "政策配合"}</text>']
    def line(x1,y1,x2,y2,style):out.append(f'<path d="M{fmt(x1)} {fmt(y1)}L{fmt(x2)} {fmt(y2)}" style="{style}"/>')
    def label(xx,yy,t,size=16,anchor='start',color='var(--ink)'):
        out.append(f'<text x="{fmt(xx)}" y="{fmt(yy)}" text-anchor="{anchor}" style="font-size:{size}px;fill:{color}">{escape(t)}</text>')
    line(left,top,left,top+ph,'stroke:var(--axis);stroke-width:.85')
    line(left,top+ph,left+pw+8,top+ph,'stroke:var(--axis);stroke-width:.85')
    label(left-8,top-13,'r',15,'end')
    label(left+pw+14,top+ph+29,'Y',16)
    for yy in [2000,2020]: label(x(yy),top+ph+25,str(yy),15,'middle','var(--muted)')
    for rr in sorted(set(p[1] for p in scene.points)):
        label(left-10,y(rr)+5,fmt(rr),15,'end','var(--muted)')
    for yy,rr,_ in scene.points:
        for coords in [(left,y(rr),x(yy),y(rr)),(x(yy),y(rr),x(yy),top+ph)]:
            line(*coords,'stroke:var(--guide);stroke-width:.75;stroke-dasharray:3 5')
    for c in scene.curves:
        rlo,rhi=sorted([(rmin-c.intercept)/c.slope,(rmax-c.intercept)/c.slope])
        lo,hi=max(xmin,rlo),min(xmax,rhi)
        color='var(--green)' if c.style.startswith('is') else 'var(--ochre-text)'
        old=c.style.endswith('old')
        stroke='stroke:'+color+';stroke-width:1.65'+(';stroke-dasharray:4 4;opacity:.6' if old else '')
        line(x(lo),y(c.intercept+c.slope*lo),x(hi),y(c.intercept+c.slope*hi),stroke)
        # Curve names sit outside the plotted domain, clear of all intersections.
        endpoint=y(c.intercept+c.slope*hi)
        label(x(hi)+12,endpoint+5,c.name,16,color=color)
    for yy,rr,style in scene.points:
        assert sum(isclose(c.intercept+c.slope*yy,rr) for c in scene.curves)>=2
        out.append(f'<circle cx="{fmt(x(yy))}" cy="{fmt(y(rr))}" r="3.4" fill="var(--ink)" stroke="white" stroke-width="1.1"/>')
    meta=dict(domain=scene.domain,rates=scene.rates,left=left,top=top,bottom=top+ph,xScale=pw/(xmax-xmin),rScale=ph/(rmax-rmin),curves=[dict(name=c.name,a=c.intercept,b=c.slope) for c in scene.curves],points=scene.points)
    out.append('<metadata>'+escape(json.dumps(meta))+'</metadata>')
    return f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">'+''.join(out)+'</svg>'


def policy_comparison(mobile):
    width,height=(400,810) if mobile else (960,320)
    out=[]
    for i,scene in enumerate(SCENES[3:]):
        panel=policy_panel(scene,mobile)
        xx,yy=(0,i*270) if mobile else (i*320,0)
        out.append(panel.replace('<svg ',f'<svg x="{xx}" y="{yy}" ',1))
    return combined('财政、货币扩张与政策配合同尺度对照',width,height,''.join(out))


if __name__ == '__main__':
    for name,draw in [('mechanisms',mechanisms),('money-and-regions',money_regions),('equilibrium-regions',equilibrium_regions),('policy-comparison',policy_comparison)]:
        for mobile in [False,True]:
            filename=f'ch03-{name}'+('-mobile' if mobile else '')+'.svg'
            (OUT/filename).write_text(draw(mobile),encoding='utf-8')
            print(filename)
