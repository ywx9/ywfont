import math

from scripts.fmt import fmt

# ベジエ補正係数
K = 0.55228475

# 点Aが現在地として、点Bに向かう反時計回りの半円弧を描くSVGパス
def make_cap(a: tuple[float, float], b: tuple[float, float]) -> str:
    # AB間の距離
    d = math.hypot(b[0] - a[0], b[1] - a[1])
    r = d / 2
    # 単位ベクトル(点Aにおける円弧の接ベクトル)
    u = ((b[1] - a[1]) / d, -(a[0] - b[0]) / d)
    ru = (u[0] * r, u[1] * r)
    kru = (ru[0] * K, ru[1] * K)
    # 半円弧の頂点をCとする
    c = ((a[0] + b[0]) / 2 + ru[0], (a[1] + b[1]) / 2 - ru[1])
    # 結果
    path = ""
    # A -> C のベジエ曲線
    path += f"C {fmt(a[0] + kru[0])} {fmt(a[1] - kru[1])} {fmt(c[0] - kru[1])} {fmt(c[1] - kru[0])} {fmt(c[0])} {fmt(c[1])} "
    # C -> B のベジエ曲線
    path += f"C {fmt(c[0] + kru[1])} {fmt(c[1] + kru[0])} {fmt(b[0] + kru[0])} {fmt(b[1] - kru[1])} {fmt(b[0])} {fmt(b[1])} "
    return path
