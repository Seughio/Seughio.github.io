"""Native SVG figures for chapter 6 (business cycles). Standard-library-only.

Multiplier-accelerator paths are computed from
Y_t = G0 + beta*Y_{t-1} + v*beta*(Y_{t-1} - Y_{t-2}),  G0 = 1, Y_0 = 0, Y_1 = 1.
"""
from math import sin, pi

from generate_adas_figures import Panel, figure, linspace


def path(beta, v, n):
    ys = [0.0, 1.0]
    for _ in range(2, n + 1):
        ys.append(1 + beta * ys[-1] + v * beta * (ys[-1] - ys[-2]))
    return ys[1:]


def main():
    # ---------- 1. 经济周期的四个阶段 ----------
    N, A = 5, 3
    g = lambda t: N + A * sin(2 * pi * (t - 1) / 6)   # crosses trend upward at t=1
    pts = ((1, 'A'), (2.5, 'B'), (4, 'C'), (5.5, 'D'), (7, 'E'))
    for t, _ in pts:
        assert abs(g(t) - (N + A * {1: 0, 2.5: 1, 4: 0, 5.5: -1, 7: 0}[t])) < 1e-9
    phases = Panel('增长率围绕趋势线的波动', (0, 10), (0, 10), 't', 'g', (
        ('N', [(0.2, N), (9.6, N)], 'ochre-old', 6, 4),
        ('', [(t, g(t)) for t in linspace(0.2, 9.4, 120)], 'green', 0, 0),
    ), points=tuple((t, g(t), 'ink-dot' if lab in 'BD' else 'old-dot', lab) for t, lab in pts),
        xticks=((1.75, '繁荣'), (3.25, '衰退'), (4.75, '萧条'), (6.25, '复苏')),
        yticks=((N, 'N'),))
    desc1 = ('增长率曲线围绕长期趋势线 N 波动：A→B 为繁荣，B 为顶峰；B→C 为衰退；C→D 为萧条，D 为谷底；'
             'D→E 为复苏，E 之后进入下一个周期。')
    figure('ch06-cycle-phases', '经济周期的四个阶段', desc1, (phases,), 1, 560, 280)
    figure('ch06-cycle-phases-mobile', '经济周期的四个阶段', desc1, (phases,), 1, 360, 260, True)

    # ---------- 2. 乘数-加速数模型的四种路径 ----------
    n = 12
    ts = list(range(1, n + 1))
    a = path(.5, 0, n)
    b = path(.5, 2, n)
    c = path(.6, 2, n)
    d = path(.8, 4, 9)
    assert abs(a[-1] - 2) < 1e-3                        # converges to G0/(1-beta) = 2
    assert abs(b[7] - (-0.1172)) < 1e-4 and abs(b[8] - 0.2148) < 1e-4
    assert abs(c[8] - (-3.3603)) < 1e-4 and abs(d[3] - 56.2) < 1e-9
    left = Panel('β, v 较小：收敛或波动', (0, 13), (-5, 8), 't', 'Y', (
        ('β=0.5, v=0', list(zip(ts, a)), 'ochre', -78, 18),
        ('β=0.5, v=2', list(zip(ts, b)), 'green-old', 4, 4),
        ('β=0.6, v=2', list(zip(ts, c)), 'green', 4, 4),
    ), xticks=((1, '1'), (5, '5'), (9, '9')), yticks=((-4, '−4'), (0, '0'), (2, '2'), (6, '6')))
    right = Panel('β=0.8, v=4：单调爆炸', (0, 10), (0, 13000), 't', 'Y', (
        ('β=0.8, v=4', list(zip(range(1, 10), d)), 'green', -82, 0),
    ), xticks=((1, '1'), (5, '5'), (9, '9')), yticks=((d[-1], f'{d[-1]:.0f}'),))
    desc2 = ('左：β=0.5、v=0 时只有乘数，Y 单调收敛到 2；β=0.5、v=2 时等幅波动；β=0.6、v=2 时波动不断扩大。'
             '右：β=0.8、v=4 时 Y 单调爆炸式增长，第 9 期约 12168。')
    figure('ch06-multiplier-accelerator', '乘数-加速数模型的产出路径', desc2, (left, right), 2, 320, 270)
    figure('ch06-multiplier-accelerator-mobile', '乘数-加速数模型的产出路径', desc2, (left, right), 1, 360, 270, True)
    print('ok')


if __name__ == '__main__':
    main()
