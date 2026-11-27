"""Native SVG figures for chapter 5 (unemployment and inflation). Standard-library-only.

Reuses the panel renderer and the short-run AS shape of chapter 4.
Phillips curves use pi = pi_e + 6 * (u_star / u - 1): at u = u_star, pi = pi_e,
so each short-run curve crosses the long-run (vertical) curve at its expected rate.
"""
from generate_adas_figures import Panel, figure, linspace, sas, adline, inter_ad_sas

U_STAR = 5


def pc(pi_e):
    return lambda u: pi_e + 6 * (U_STAR / u - 1)


def main():
    # ---------- 1. 需求拉上与成本推动 ----------
    ads = (7, 9.5, 12)
    pts = [inter_ad_sas(c) for c in ads]
    names = ('AD₁', 'AD₂', 'AD₃')
    curves = [('AS', sas(), 'ochre', 6, 10)]
    curves += [(n, adline(c)[::-1], 'green' if i == 2 else 'green-old', -10, -6)  # label at top end
               for i, (n, c) in enumerate(zip(names, ads))]
    demand = Panel('需求拉上：AD 右移', (0, 15), (0, 10), 'Y', 'P', curves,
                   points=tuple((x, y, 'ink-dot' if i == 2 else 'old-dot', f'E{"₁₂₃"[i]}')
                                for i, (x, y) in enumerate(pts)))
    shifts = (0, -2, -4)
    cpts = [inter_ad_sas(11, s) for s in shifts]
    curves = [(f'AS{"₁₂₃"[i]}', sas(s), 'ochre' if i == 2 else 'ochre-old', -10, -6)
              for i, s in enumerate(shifts)]
    curves.append(('AD', adline(11), 'green', 4, 4))
    cost = Panel('成本推动：AS 左移', (0, 15), (0, 10), 'Y', 'P', curves,
                 points=tuple((x, y, 'ink-dot' if i == 2 else 'old-dot', f'E{"₁₂₃"[i]}')
                              for i, (x, y) in enumerate(cpts)))
    for (a, b), (c, d) in zip(pts, pts[1:]):
        assert c > a and d > b            # demand-pull: Y up, P up
    for (a, b), (c, d) in zip(cpts, cpts[1:]):
        assert c < a and d > b            # cost-push: Y down, P up
    desc1 = ('左：AS 不变，AD 由 AD₁ 右移至 AD₃，价格持续上升；越接近充分就业产出，产出增加越少、价格上升越多。'
             '右：AD 不变，AS 由 AS₁ 左移至 AS₃，价格上升而产出下降。')
    figure('ch05-inflation-causes', '需求拉上型与成本推动型通货膨胀', desc1, (demand, cost), 2, 300, 250)
    figure('ch05-inflation-causes-mobile', '需求拉上型与成本推动型通货膨胀', desc1, (demand, cost), 1, 340, 250, True)

    # ---------- 2. 菲利普斯曲线 ----------
    short = pc(2)
    assert abs(short(4) - 3.5) < 1e-9 and abs(short(6) - 1) < 1e-9
    p1 = Panel('短期：失业与通胀交替', (0, 10), (-1, 8), 'u(%)', 'π(%)', (
        ('PC', [(u, short(u)) for u in linspace(2.6, 9.5, 80)], 'green', -8, -12),
    ), points=((4, 3.5, 'ink-dot', 'A'), (6, 1, 'old-dot', 'B')),
        xticks=((4, '4'), (6, '6')), yticks=((1, '1'), (3.5, '3.5')))
    u1 = U_STAR / 1.5                      # on PC(πe=3%) where π = 6%
    assert abs(pc(3)(u1) - 6) < 1e-9 and abs(pc(3)(U_STAR) - 3) < 1e-9 and abs(pc(6)(U_STAR) - 6) < 1e-9
    p2 = Panel('长期：预期调整，LPC 垂直', (0, 10), (-1, 11), 'u(%)', 'π(%)', (
        ('PC(πᵉ=3%)', [(u, pc(3)(u)) for u in linspace(2.3, 7.5, 80)], 'green-old', 4, 5),
        ('PC(πᵉ=6%)', [(u, pc(6)(u)) for u in linspace(2.9, 9.5, 80)], 'green', -70, -8),
        ('LPC', [(U_STAR, -0.5), (U_STAR, 10.5)], 'ochre', 6, 12),
    ), points=((U_STAR, 3, 'old-dot', 'A'), (u1, 6, 'ink-dot', 'C'), (U_STAR, 6, 'ink-dot', 'B')),
        xticks=((u1, 'u₁'), (U_STAR, 'u*')), yticks=((3, '3'), (6, '6')))
    desc2 = ('左：短期菲利普斯曲线向右下方倾斜，失业率 4% 对应通胀 3.5%，失业率 6% 对应通胀 1%。'
             '右：预期通胀 3% 时经济在 A（u=u*）；扩张使经济沿 PC(πᵉ=3%) 移到 C，失业率暂时降到 u₁、通胀升到 6%；'
             '预期调整到 6% 后短期曲线上移，经济回到 B，失业率回到 u*。长期菲利普斯曲线 LPC 在 u* 处垂直。')
    figure('ch05-phillips', '菲利普斯曲线', desc2, (p1, p2), 2, 300, 260)
    figure('ch05-phillips-mobile', '菲利普斯曲线', desc2, (p1, p2), 1, 340, 260, True)
    print('ok')


if __name__ == '__main__':
    main()
