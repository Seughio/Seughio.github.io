"""Native SVG figures for chapter 8 (open economy). Standard-library-only.

Mundell-Fleming panels (indirect quotation: e up = home currency appreciates):
IS*: e = c - Y (c = 10 before, 12 after a demand expansion); LM*: vertical at Y = 5 or 7.
"""
from generate_adas_figures import Panel, figure


def is_line(c, name, style, dx=4, dy=4):
    lo, hi = max(0.6, c - 9.5), min(9.6, c - 0.6)
    return (name, [(lo, c - lo), (hi, c - hi)], style, dx, dy)


def lm_line(y, name, style, dx=-10, dy=-6):
    return (name, [(y, 0.5), (y, 9.5)], style, dx, dy)


def mf(title, curves, points, xticks, yticks):
    return Panel(title, (0, 11), (0, 10), 'Y', 'e', curves, points=points, xticks=xticks, yticks=yticks)


def main():
    E = 'e*'
    fixed_fiscal = mf('固定汇率：扩张性财政政策', (
        is_line(10, 'IS*₁', 'green-old'), is_line(12, 'IS*₂', 'green'),
        lm_line(5, 'LM*₁', 'ochre-old'), lm_line(7, 'LM*₂', 'ochre'),
    ), ((5, 5, 'old-dot', 'E₁'), (5, 7, 'old-dot', ''), (7, 5, 'ink-dot', 'E₂')),
        ((5, 'Y₁'), (7, 'Y₂')), ((5, E),))
    fixed_money = mf('固定汇率：扩张性货币政策', (
        is_line(10, 'IS*', 'green'),
        lm_line(7, 'LM*₂', 'ochre-old'), lm_line(5, 'LM*₁', 'ochre'),
    ), ((7, 3, 'old-dot', ''), (5, 5, 'ink-dot', 'E₁')),
        ((5, 'Y₁'), (7, 'Y′')), ((5, E),))
    float_fiscal = mf('浮动汇率：扩张性财政政策', (
        is_line(10, 'IS*₁', 'green-old'), is_line(12, 'IS*₂', 'green'),
        lm_line(5, 'LM*', 'ochre'),
    ), ((5, 5, 'old-dot', 'E₁'), (5, 7, 'ink-dot', 'E₂')),
        ((5, 'Y*'),), ((5, 'e₁'), (7, 'e₂')))
    float_money = mf('浮动汇率：扩张性货币政策', (
        is_line(10, 'IS*', 'green'),
        lm_line(5, 'LM*₁', 'ochre-old'), lm_line(7, 'LM*₂', 'ochre'),
    ), ((5, 5, 'old-dot', 'E₁'), (7, 3, 'ink-dot', 'E₂')),
        ((5, 'Y₁'), (7, 'Y₂')), ((3, 'e₂'), (5, 'e₁')))
    for p in (fixed_fiscal, fixed_money, float_fiscal, float_money):   # every dot sits on a drawn line
        for x, y, *_ in p.points:
            assert any(abs(y - (c - x)) < 1e-9 for c in (10, 12)) or x in (5, 7)
    desc1 = ('间接标价法下 e 上升表示本币升值。固定汇率：财政扩张使 IS* 右移，汇率面临上升压力，央行增加货币供给使 LM* 右移，'
             '汇率保持 e*，收入由 Y₁ 增至 Y₂；货币扩张使 LM* 右移、汇率下降，央行抛售外汇收回本币，LM* 回到原位，收入不变。'
             '浮动汇率：财政扩张使 IS* 右移，汇率由 e₁ 升至 e₂，收入不变；货币扩张使 LM* 右移，汇率由 e₁ 降至 e₂，收入由 Y₁ 增至 Y₂。')
    panels = (fixed_fiscal, fixed_money, float_fiscal, float_money)
    figure('ch08-mundell-fleming', '蒙代尔-弗莱明模型中的政策效果', desc1, panels, 2, 320, 270)
    figure('ch08-mundell-fleming-mobile', '蒙代尔-弗莱明模型中的政策效果', desc1, panels, 1, 360, 260, True)

    # ---------- BP 曲线的三种形状 ----------
    rw = 5
    full = Panel('资本完全流动：BP 水平', (0, 10), (0, 10), 'Y', 'r', (
        ('BP=0', [(0.5, rw), (9, rw)], 'ochre', -30, -10),
    ), xticks=(), yticks=((rw, 'rw'),))
    none = Panel('资本完全不流动：BP 垂直', (0, 10), (0, 10), 'Y', 'r', (
        ('BP=0', [(5, 0.5), (5, 9.5)], 'ochre', 6, 12),
    ))
    part = Panel('资本不完全流动：向右上倾斜', (0, 10), (0, 10), 'Y', 'r', (
        ('BP=0', [(1, 1.5), (8.5, 8.5)], 'ochre', -40, -8),
    ))
    desc2 = ('BP 曲线斜率为 γ/σ。资本完全流动（σ→∞）时 BP 在世界利率处水平；资本完全不流动（σ=0）时 BP 垂直；'
             '资本不完全流动时 BP 向右上倾斜。各图中 BP 左上方为国际收支顺差（BP>0），右下方为逆差（BP<0）。')
    figure('ch08-bp-slopes', 'BP 曲线的三种形状', desc2, (full, none, part), 3, 230, 230)
    figure('ch08-bp-slopes-mobile', 'BP 曲线的三种形状', desc2, (full, none, part), 1, 340, 230, True)
    print('ok')


if __name__ == '__main__':
    main()
