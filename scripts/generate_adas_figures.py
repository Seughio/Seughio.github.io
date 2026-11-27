"""Native SVG figures for chapter 4 (AD-AS). Standard-library-only.

Quantitative panels (AD derivation) use the data of 例 4.2:
IS: Y = 1250 - 30r;  LM: 0.2Y - 4r = 150/P;  AD: Y = 500 + 450/P.
The remaining panels are qualitative shape sketches; their curves are
generated from simple formulas so that every intersection is exact.
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'docs/金融学/宏观经济学/figures'

STYLE = '''<style>
    :root {--paper:#fff;--ink:#46564c;--muted:#69766c;--green:#416f5d;
      --ochre:#ad7c51;--ochre-text:#96643e;--axis:#939f97;--guide:#e0e6e1;
      --old-green:#82998b;--old-ochre:#a48d79;--old-point:#718078;
      --curve-width:1.8;--axis-width:.85;--guide-width:.75;
      --label-size:14px;--tick-size:12px;}
    text {font-family:'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',sans-serif;
      fill:var(--ink);font-size:var(--label-size);font-variant-numeric:tabular-nums;}
    path {fill:none;stroke-linecap:butt;stroke-linejoin:round;}
    .axis {stroke:var(--axis);stroke-width:var(--axis-width);}
    .guide {stroke:var(--guide);stroke-width:var(--guide-width);stroke-dasharray:3 5;}
    .green {stroke:var(--green);stroke-width:var(--curve-width);}
    .ochre {stroke:var(--ochre);stroke-width:var(--curve-width);}
    .green-old {stroke:var(--old-green);stroke-width:1.5;stroke-dasharray:4 4;}
    .ochre-old {stroke:var(--old-ochre);stroke-width:1.5;stroke-dasharray:4 4;}
    .green-label {fill:var(--green);}.ochre-label {fill:var(--ochre-text);}
    .green-old-label,.ochre-old-label {fill:var(--muted);}
    .tick {fill:var(--muted);font-size:var(--tick-size);}
    .title {font-size:var(--label-size);font-weight:600;}
    .arrow {stroke:var(--muted);stroke-width:1.2;}
    .arrow-head {fill:var(--muted);stroke:none;}
    circle {stroke:var(--paper);stroke-width:1.1;}
    .green-dot {fill:var(--green);}.ochre-dot {fill:var(--ochre);}
    .ink-dot {fill:var(--ink);}.old-dot {fill:var(--old-point);}
    </style>'''


def fmt(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def linspace(a, b, n=60):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


class Panel:
    """A panel in data coordinates. curves: (name, [(x, y)...], style, label_dx, label_dy)."""

    def __init__(self, title, xr, yr, xlab, ylab, curves, points=(), xticks=(), yticks=(),
                 arrows=()):
        self.title, self.xr, self.yr = title, xr, yr
        self.xlab, self.ylab = xlab, ylab
        self.curves, self.points = curves, points
        self.xticks, self.yticks, self.arrows = xticks, yticks, arrows


def draw_panel(out, p, ox, oy, pw, ph):
    left, top = ox + 46, oy + 40
    w, h = pw - 46 - 58, ph - 40 - 34
    right, bottom = left + w, top + h
    (x0, x1), (y0, y1) = p.xr, p.yr
    X = lambda v: left + (v - x0) / (x1 - x0) * w
    Y = lambda v: bottom - (v - y0) / (y1 - y0) * h

    def path(pts, cls):
        d = 'M' + 'L'.join(f'{fmt(X(a))} {fmt(Y(b))}' for a, b in pts)
        out.append(f'<path class="{cls}" d="{d}"/>')

    def text(xx, yy, s, cls='label', anchor='start'):
        out.append(f'<text x="{fmt(xx)}" y="{fmt(yy)}" class="{cls}" text-anchor="{anchor}">{escape(s)}</text>')

    text(ox + pw / 2, oy + 16, p.title, 'title', 'middle')
    for px, py, _, _ in p.points:
        path([(x0, py), (px, py)], 'guide')
        path([(px, py), (px, y0)], 'guide')
    path([(x0, y1), (x0, y0)], 'axis')
    out.append(f'<path class="axis" d="M{fmt(left)} {fmt(bottom)}L{fmt(right + 8)} {fmt(bottom)}"/>')
    text(left - 8, top + 4, p.ylab, 'label', 'end')
    text(right + 14, bottom + 5, p.xlab)
    text(left - 8, bottom + 16, 'O', 'tick', 'end')
    for v, s in p.xticks:
        text(X(v), bottom + 19, s, 'tick', 'middle')
    for v, s in p.yticks:
        text(left - 8, Y(v) + 4, s, 'tick', 'end')
    for name, pts, cls, dx, dy in p.curves:
        dense = [pts[0]]
        for (a, b), (c, d) in zip(pts, pts[1:]):  # densify so clipping keeps in-range parts
            dense += [(a + (c - a) * t, b + (d - b) * t) for t in linspace(0, 1, 200)[1:]]
        pts = [(a, b) for a, b in dense if x0 <= a <= x1 and y0 <= b <= y1]
        if len(pts) > 3:  # drop redundant collinear samples
            pts = [pts[0]] + [q for i, q in enumerate(pts[1:-1], 1) if i % 8 == 0] + [pts[-1]]
        path(pts, cls)
        ex, ey = pts[-1]
        text(X(ex) + dx, Y(ey) + dy, name, cls + '-label')
    for (ax, ay), (bx, by) in p.arrows:
        sx, sy, tx, ty = X(ax), Y(ay), X(bx), Y(by)
        out.append(f'<path class="arrow" d="M{fmt(sx)} {fmt(sy)}L{fmt(tx)} {fmt(ty)}"/>')
        import math
        ang = math.atan2(ty - sy, tx - sx)
        p1 = (tx - 7 * math.cos(ang - .45), ty - 7 * math.sin(ang - .45))
        p2 = (tx - 7 * math.cos(ang + .45), ty - 7 * math.sin(ang + .45))
        out.append(f'<path class="arrow-head" d="M{fmt(tx)} {fmt(ty)}L{fmt(p1[0])} {fmt(p1[1])}L{fmt(p2[0])} {fmt(p2[1])}Z"/>')
    for px, py, cls, lab in p.points:
        out.append(f'<circle cx="{fmt(X(px))}" cy="{fmt(Y(py))}" r="4" class="{cls}"/>')
        if lab and cls == 'old-dot':
            text(X(px) - 8, Y(py) + 4, lab, 'label', 'end')
        elif lab:
            text(X(px) + 8, Y(py) - 7, lab, 'label')


def figure(name, title, desc, panels, cols, pw=300, ph=260, mobile=False):
    rows = -(-len(panels) // cols)
    width, height = cols * pw, rows * ph
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
           f'<title id="title">{escape(title)}</title>', f'<desc id="desc">{escape(desc)}</desc>', STYLE]
    if mobile:
        out.append('<style>:root {--label-size:15px;--tick-size:13px;}</style>')
    out.append(f'<rect width="{width}" height="{height}" fill="var(--paper)"/>')
    for i, p in enumerate(panels):
        draw_panel(out, p, (i % cols) * pw, (i // cols) * ph, pw, ph)
    out.append('</svg>')
    (OUT / f'{name}.svg').write_text('\n'.join(out) + '\n', encoding='utf-8')


YF = 10


def sas(shift=0.0):
    """Keynesian flat segment, rising segment, vertical at Yf+shift."""
    yf = YF + shift
    pts = [(2 + shift, 2), (4 + shift, 2)]
    pts += [(4 + shift + (yf - 4 - shift) * (1 - (1 - t) ** 2), 2 + 4 * t ** 2.2) for t in linspace(0, 1, 40)[1:]]
    pts += [(yf, 9.5)]
    return pts


def adline(c):
    return [(c - 6, 9.5), (c + 2.5, 9.5 - 8.5 * 8.9 / 9.5)]  # on the line through (c-6, 9.5), slope -8.9/9.5


def inter_ad_sas(c, shift=0.0):
    """Find intersection of AD (through (c-6, 9.5)) with sas(shift) by scanning the polyline."""
    pts = sas(shift)
    f = lambda x, y: y - (9.5 - (x - (c - 6)) * 8.9 / 9.5)
    for (a, b), (d, e) in zip(pts, pts[1:]):
        if f(a, b) * f(d, e) <= 0:
            t = f(a, b) / (f(a, b) - f(d, e))
            return a + t * (d - a), b + t * (e - b)
    raise ValueError('no intersection')


def shift_panel(title, ad0, ad1, s0, s1):
    curves = []
    e0, e1 = inter_ad_sas(ad0, s0), inter_ad_sas(ad1, s1)
    if s0 == s1:
        curves.append(('AS', sas(s0), 'ochre', 6, 10))
        curves.append(('AD₀', adline(ad0), 'green-old', -30 if ad0 < ad1 else 4, 12))
        curves.append(('AD₁', adline(ad1), 'green', -30 if ad1 < ad0 else 4, 12))
    else:
        curves.append(('AS₀', sas(s0), 'ochre-old', -26 if s0 < s1 else 6, 10))
        curves.append(('AS₁', sas(s1), 'ochre', -26 if s1 < s0 else 6, 10))
        curves.append(('AD', adline(ad0), 'green', 4, 4))
    return Panel(title, (0, 15), (0, 10), 'Y', 'P', curves,
                 points=((e0[0], e0[1], 'old-dot', 'E₀'), (e1[0], e1[1], 'ink-dot', 'E₁')))


def main():
    # ---------- 1. AD 推导（例 4.2 数据） ----------
    is_ = lambda r: 1250 - 30 * r
    lm = lambda P: (lambda r: 750 / P + 20 * r)
    ad = lambda P: 500 + 450 / P
    assert abs(is_(10) - 950) < 1e-9 and abs(lm(1)(10) - 950) < 1e-9
    assert abs(is_(15) - 800) < 1e-9 and abs(lm(1.5)(15) - 800) < 1e-9
    assert abs(ad(1) - 950) < 1e-9 and abs(ad(1.5) - 800) < 1e-9
    rs = linspace(0, 25, 2)
    rl = linspace(0, 21, 2)
    islm = Panel('IS-LM：P 上升，LM 左移', (600, 1200), (0, 25), 'Y', 'r', (
        ('IS', [(is_(r), r) for r in rs], 'green', 6, 4),
        ('LM(P=1)', [(lm(1)(r), r) for r in rl], 'ochre', -40, -8),
        ('LM(P=1.5)', [(lm(1.5)(r), r) for r in rl], 'ochre-old', -40, -8),
    ), points=((950, 10, 'ink-dot', 'E₁'), (800, 15, 'old-dot', 'E₂')),
        xticks=((800, '800'), (950, '950')), yticks=((10, '10'), (15, '15')))
    Ps = linspace(.8, 2.0)
    adp = Panel('AD：Y = 500 + 450/P', (600, 1200), (.6, 2.0), 'Y', 'P', (
        ('AD', [(ad(P), P) for P in reversed(Ps)], 'green', 6, 4),
    ), points=((950, 1, 'ink-dot', 'D₁'), (800, 1.5, 'old-dot', 'D₂')),
        xticks=((800, '800'), (950, '950')), yticks=((1, '1'), (1.5, '1.5')))
    desc1 = ('例 4.2：IS 为 Y=1250−30r；P=1 时 LM 为 Y=750+20r，均衡 (950, 10)；'
             'P=1.5 时 LM 为 Y=500+20r，均衡 (800, 15)。对应 AD 曲线 Y=500+450/P 上的点 (950, 1)、(800, 1.5)。')
    figure('ch04-ad-derivation', 'AD 曲线的推导', desc1, (islm, adp), 2, 320, 270)
    figure('ch04-ad-derivation-mobile', 'AD 曲线的推导', desc1, (islm, adp), 1, 360, 270, True)

    # ---------- 2. AS 曲线形状 ----------
    short = Panel('短期 AS：工资刚性', (0, 13), (0, 10), 'Y', 'P', (
        ('SAS', sas(), 'ochre', 6, 10),
    ), xticks=((YF, 'Yf'),), yticks=())
    long = Panel('长期 AS：工资完全伸缩', (0, 13), (0, 10), 'Y', 'P', (
        ('LAS', [(YF, 1), (YF, 9.5)], 'ochre', 6, 10),
    ), xticks=((YF, 'Yf'),))
    desc2 = '左：短期 AS 由近乎水平段、向右上倾斜段和在 Yf 处的垂直段组成；右：长期 AS 在充分就业产出 Yf 处垂直。'
    figure('ch04-as-shapes', 'AS 曲线的形状', desc2, (short, long), 2, 300, 250)
    figure('ch04-as-shapes-mobile', 'AS 曲线的形状', desc2, (short, long), 1, 340, 250, True)

    # ---------- 3. 宏观均衡的四种变动 ----------
    p_adr = shift_panel('AD 右移：增长与通胀', 8.5, 10.5, 0, 0)
    p_adl = shift_panel('AD 左移：衰退与通缩', 10.5, 8.5, 0, 0)
    p_asr = shift_panel('AS 右移：技术进步', 11, 11, 0, 2)
    p_asl = shift_panel('AS 左移：滞胀', 11, 11, 2, 0)
    desc3 = ('四个图共用同一形状的短期 AS。AD 右移：产出与价格同升；AD 左移：产出与价格同降；'
             'AS 右移：产出上升、价格下降；AS 左移：产出下降、价格上升（滞胀）。')
    panels = (p_adr, p_adl, p_asr, p_asl)
    figure('ch04-equilibrium-shifts', '宏观均衡的四种变动', desc3, panels, 4, 240, 240)
    figure('ch04-equilibrium-shifts-mobile', '宏观均衡的四种变动', desc3, panels, 2, 200, 230, True)

    # sanity: direction checks for each panel
    for p, dy_sign, dp_sign in ((p_adr, 1, 1), (p_adl, -1, -1), (p_asr, 1, -1), (p_asl, -1, 1)):
        (a, b, *_), (c, d, *_) = p.points
        assert (c - a) * dy_sign > 0 and (d - b) * dp_sign > 0, p.title
    print('ok')


if __name__ == '__main__':
    main()
