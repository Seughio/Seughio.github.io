"""Native SVG figures for chapter 9 (macroeconomic policy). Standard-library-only.

Fiscal / monetary panels use 例 9.1 and 例 9.2:
IS: r = 300 - 0.02Y (IS' after G+100: r = 310 - 0.02Y);
LM: r = -440 + 0.06Y (LM' after M+100: r = -460 + 0.06Y).
Disinflation paths use pi_t = pi_{t-1} + h*(y_{t-1}-y*)/y*, h = 0.2 (例 9.4, 9.5).
"""
from generate_adas_figures import Panel, figure


def line(a, b, ys):
    return [(y, a + b * y) for y in ys]


def path(target, gap, start=10, n=10):
    pis, pi = [], start
    for _ in range(n):
        pi = max(target, pi + 0.2 * gap)
        pis.append(pi)
    return pis


def main():
    ys = (8900, 9950)
    assert abs((300 - 0.02 * 9250) - 115) < 1e-9 and abs((-440 + 0.06 * 9250) - 115) < 1e-9
    assert abs((310 - 0.02 * 9375) - 122.5) < 1e-9 and abs((-440 + 0.06 * 9375) - 122.5) < 1e-9
    assert abs((310 - 0.02 * 9750) - 115) < 1e-9
    assert abs((300 - 0.02 * 9500) - 110) < 1e-9 and abs((-460 + 0.06 * 9500) - 110) < 1e-9
    fiscal = Panel('财政政策：政府投资 +100', (8900, 10000), (95, 135), 'Y', 'r', (
        ('IS', line(300, -0.02, ys), 'green-old', 4, 4),
        ("IS'", line(310, -0.02, ys), 'green', 4, 4),
        ('LM', line(-440, 0.06, (9070, 9800)), 'ochre', 4, 4),
    ), points=((9250, 115, 'old-dot', 'E₀'), (9375, 122.5, 'ink-dot', 'E₁'), (9750, 115, 'old-dot', 'E₂')),
        xticks=((9250, 'Y₀'), (9375, 'Y₁'), (9750, 'Y₂')), yticks=((115, '115'), (122.5, '122.5')))
    money = Panel('货币政策：货币供给 +100', (8900, 10000), (95, 135), 'Y', 'r', (
        ('IS', line(300, -0.02, ys), 'green', 4, 4),
        ('LM', line(-440, 0.06, (9070, 9750)), 'ochre-old', -24, 4),
        ("LM'", line(-460, 0.06, (9250, 9900)), 'ochre', 4, 4),
    ), points=((9250, 115, 'old-dot', 'E₀'), (9500, 110, 'ink-dot', 'E₁')),
        xticks=((9250, '9250'), (9500, '9500')), yticks=((110, '110'), (115, '115')))
    desc1 = ('Y₀=9250，Y₁=9375，Y₂=9750。例 9.1：政府投资增加 100，IS 右移，均衡由 (9250, 115) 移到 (9375, 122.5)，产出效应 125；'
             '若利率不变产出可达 9750，挤出效应 375。例 9.2：货币供给增加 100，LM 右移，均衡移到 (9500, 110)，产出效应 250。')
    figure('ch09-policy-effects', '财政政策与货币政策的产出效应', desc1, (fiscal, money), 2, 330, 280)
    figure('ch09-policy-effects-mobile', '财政政策与货币政策的产出效应', desc1, (fiscal, money), 1, 360, 270, True)

    soft = path(2, -5)
    hard = path(2, -10)
    assert soft == [9, 8, 7, 6, 5, 4, 3, 2, 2, 2] and hard == [8, 6, 4, 2, 2, 2, 2, 2, 2, 2]
    ts = list(range(0, 11))
    land = Panel('通胀率从 10% 降到 2% 的两种路径', (0, 11), (0, 11), 't', 'π(%)', (
        ('软着陆', list(zip(ts, [10] + soft)), 'green', 6, -6),
        ('硬着陆', list(zip(ts, [10] + hard)), 'ochre', 6, 16),
    ), points=((8, 2, 'old-dot', ''), (4, 2, 'ink-dot', '')),
        xticks=((4, '4'), (8, '8'), (10, '10')), yticks=((2, '2'), (10, '10')))
    desc2 = ('h=0.2，充分就业产出 100。把产出压到 95（缺口 −5%）时通胀率每年降 1 个百分点，第 8 年降到 2%；'
             '压到 90（缺口 −10%）时每年降 2 个百分点，第 4 年就降到 2%，但产出损失更大。')
    figure('ch09-landing', '软着陆与硬着陆', desc2, (land,), 1, 520, 280)
    figure('ch09-landing-mobile', '软着陆与硬着陆', desc2, (land,), 1, 360, 270, True)
    print('ok')


if __name__ == '__main__':
    main()
