"""Native SVG figures for chapter 7 (economic growth). Standard-library-only.

Solow panels use f(k) = k^0.5 (Cobb-Douglas, alpha = 0.5).
Steady state: s*f(k) = (n+delta)*k  =>  k* = (s/(n+delta))^2.
Golden rule: f'(k) = n+delta  =>  k_gold = (0.5/(n+delta))^2, i.e. s_gold = 0.5.
"""
from generate_adas_figures import Panel, figure, linspace

f = lambda k: k ** 0.5


def kstar(s, nd):
    return (s / nd) ** 2


def main():
    ks = linspace(0, 30, 120)

    # ---------- 1. 储蓄率与人口增长对稳态的影响 ----------
    nd = 0.1
    k0, k1 = kstar(0.2, nd), kstar(0.3, nd)
    assert abs(0.2 * f(k0) - nd * k0) < 1e-9 and abs(0.3 * f(k1) - nd * k1) < 1e-9
    saving = Panel('储蓄率提高：s=0.2 → 0.3', (0, 14), (0, 1.6), 'k', 'y', (
        ('(n+δ)k', [(0, 0), (14, 1.4)], 'ochre', -30, -10),
        ('sf(k)', [(k, 0.2 * f(k)) for k in ks], 'green-old', 4, 12),
        ("s'f(k)", [(k, 0.3 * f(k)) for k in ks], 'green', 4, 4),
    ), points=((k0, 0.2 * f(k0), 'old-dot', 'E'), (k1, 0.3 * f(k1), 'ink-dot', "E'")),
        xticks=((k0, 'k₀'), (k1, "k'")))
    nd1 = 0.15
    k2 = kstar(0.3, nd1)
    assert abs(0.3 * f(k2) - nd1 * k2) < 1e-9
    pop = Panel('人口增长率提高：n → n′', (0, 14), (0, 1.6), 'k', 'y', (
        ('(n+δ)k', [(0, 0), (14, 1.4)], 'ochre-old', -10, 14),
        ("(n'+δ)k", [(0, 0), (10.5, 1.575)], 'ochre', -60, 4),
        ('sf(k)', [(k, 0.3 * f(k)) for k in ks], 'green', 4, 4),
    ), points=((k1, 0.3 * f(k1), 'old-dot', 'E'), (k2, 0.3 * f(k2), 'ink-dot', "E'")),
        xticks=((k2, "k'"), (k1, 'k₀')))
    desc1 = ('左：f(k)=√k，n+δ=0.1。储蓄率从 0.2 提高到 0.3，sf(k) 上移，稳态人均资本从 4 增至 9。'
             '右：人口增长率提高使 (n+δ)k 变陡（0.1→0.15），稳态人均资本从 9 降至 4。')
    figure('ch07-solow-steady', '新古典增长模型的稳态', desc1, (saving, pop), 2, 320, 270)
    figure('ch07-solow-steady-mobile', '新古典增长模型的稳态', desc1, (saving, pop), 1, 360, 270, True)

    # ---------- 2. 资本积累的黄金律 ----------
    kg = kstar(0.5, nd)                       # 25
    assert abs(0.5 * kg ** -0.5 - nd) < 1e-12
    tangent = lambda k: f(kg) + nd * (k - kg)
    gold = Panel('黄金律：f′(k*) = n+δ', (0, 60), (0, 8.5), 'k', 'y', (
        ('y=f(k)', [(k, f(k)) for k in linspace(0, 58, 160)], 'green', 4, 4),
        ('(n+δ)k', [(0, 0), (58, 5.8)], 'ochre', 4, 14),
        ('', [(kg - 14, tangent(kg - 14)), (kg + 14, tangent(kg + 14))], 'green-old', 4, 4),
    ), points=((kg, f(kg), 'ink-dot', 'M'), (kg, nd * kg, 'ink-dot', "M'"),
               (9, f(9), 'old-dot', 'T'), (49, f(49), 'old-dot', 'X')),
        xticks=((9, 'k⁻'), (kg, 'k*'), (49, 'k⁺')))
    for k in (9, 49):                          # consumption gap smaller away from k*
        assert f(k) - nd * k < f(kg) - nd * kg
    desc2 = ('f(k)=√k，n+δ=0.1。稳态人均消费等于 f(k) 与 (n+δ)k 的垂直距离；在 k*=25 处 f 的切线斜率等于 n+δ，'
             '距离 MM′=2.5 最大。k⁻=9 和 k⁺=49 处的消费都只有 2.1，对应储蓄率 0.3 和 0.7。')
    figure('ch07-golden-rule', '资本积累的黄金律', desc2, (gold,), 1, 520, 300)
    figure('ch07-golden-rule-mobile', '资本积累的黄金律', desc2, (gold,), 1, 360, 280, True)
    print('ok')


if __name__ == '__main__':
    main()
