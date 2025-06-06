import math
from scripts.transcoord import transcoord
from scripts.make_cap import make_cap
from scripts.fmt import fmt

# 3次ベジエ曲線をアウトラインに変換
def bezier_to_path(a: tuple[float, float], b: tuple[float, float],
                c: tuple[float, float], d: tuple[float, float], width: float) -> str:
    a = transcoord(a) # 始点
    b = transcoord(b) # 終点
    c = transcoord(c) # 制御点1
    d = transcoord(d) # 制御点2
    r = width / 2     # アウトラインの幅の半分
    # 各点の差分ベクトル
    v_ab = (b[0] - a[0], b[1] - a[1])
    v_ac = (c[0] - a[0], c[1] - a[1])
    v_bd = (d[0] - b[0], d[1] - b[1])
    # 各点の距離
    l_ab = math.hypot(v_ab[0], v_ab[1])
    l_ac = math.hypot(v_ac[0], v_ac[1])
    l_bd = math.hypot(v_bd[0], v_bd[1])
    # 単位ベクトル
    t_ac = (v_ac[0] / l_ac, v_ac[1] / l_ac)
    t_bd = (v_bd[0] / l_bd, v_bd[1] / l_bd)
    print(t_ac)
    print(t_bd)
    rt_ac = (r * t_ac[0], r * t_ac[1])
    rt_bd = (r * t_bd[0], r * t_bd[1])
    # アウトラインのa->b側
    a0 = (a[0] - rt_ac[1], a[1] + rt_ac[0])
    b0 = (b[0] + rt_bd[1], b[1] - rt_bd[0])
    v_ab0 = (b0[0] - a0[0], b0[1] - a0[1])
    c0 = (a0[0] + v_ac[0] * v_ab0[0] / v_ab[0], a0[1] + v_ac[1] * v_ab0[1] / v_ab[1])
    d0 = (b0[0] + v_bd[0] * v_ab0[0] / v_ab[0], b0[1] + v_bd[1] * v_ab0[1] / v_ab[1])
    # アウトラインのb->a側
    a1 = (a[0] + rt_ac[1], a[1] - rt_ac[0])
    b1 = (b[0] - rt_bd[1], b[1] + rt_bd[0])
    v_ab1 = (b1[0] - a1[0], b1[1] - a1[1])
    c1 = (a1[0] + v_ac[0] * v_ab1[0] / v_ab[0], a1[1] + v_ac[1] * v_ab1[1] / v_ab[1])
    d1 = (b1[0] + v_bd[0] * v_ab1[0] / v_ab[0], b1[1] + v_bd[1] * v_ab1[1] / v_ab[1])
    # 初期位置はA0
    path = f"M {fmt(a0[0])} {fmt(a0[1])} "
    # A0 -> A1はキャップ
    path += make_cap(a0, a1)
    # A1 -> B1はベジエ曲線
    path += f"C {fmt(c1[0])} {fmt(c1[1])} {fmt(d1[0])} {fmt(d1[1])} {fmt(b1[0])} {fmt(b1[1])} "
    # B1 -> B0はキャップ
    path += make_cap(b1, b0)
    # B0 -> A0はベジエ曲線
    path += f"C {fmt(d0[0])} {fmt(d0[1])} {fmt(c0[0])} {fmt(c0[1])} {fmt(a0[0])} {fmt(a0[1])} "
    # 不要だがZで閉じる
    path += "Z"
    return path
