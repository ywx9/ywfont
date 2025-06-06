import math
from scripts.transcoord import transcoord
from scripts.make_cap import make_cap
from scripts.fmt import fmt

# ベジエ補正係数
K = 0.55228475

# 90度の円弧を描くアウトラインを作成する関数
# 円弧の中心は(a[0], b[1])となる
def arc_to_path(a: tuple[float, float], b: tuple[float, float], width: float) -> str:
    a = transcoord(a) # 始点
    b = transcoord(b) # 終点
    r = width / 2     # アウトラインの幅の半分

    # アウトライン
    p0 = (a[0], a[0] + r)
    p1 = (a[0], a[0] - r)
    p2 = (b[0] + r, b[1])
    p3 = (b[0] - r, b[1])
    # アウトラインのパスを生成
    path = f"M {fmt(p0[0])} {fmt(p0[1])} "
    path += make_cap(p0, p1)
    path += f"C {fmt(p1[0] + (p2[0] - p1[0]) * K)} {fmt(p1[1])} {fmt(p2[0])} {fmt(p2[1] - (p2[1] - p1[1]) * K)} {fmt(p2[0])} {fmt(p2[1])} "
    path += make_cap(p2, p3)
    path += f"C {fmt(p3[0] + (p0[0] - p3[0]) * K)} {fmt(p3[1])} {fmt(p0[0])} {fmt(p0[1] - (p0[1] - p3[1]) * K)} {fmt(p0[0])} {fmt(p0[1])} "
    path += "Z"
    return path
