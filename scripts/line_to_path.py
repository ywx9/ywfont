import math
from scripts.make_cap import make_cap
from scripts.transcoord import transcoord
from scripts.fmt import fmt

# 直線ストロークをアウトラインに変換
def line_to_path(a: tuple[float, float], b: tuple[float, float], width: float) -> str:
    a = transcoord(a)
    b = transcoord(b)
    # 直線ABの距離
    l = math.hypot(b[0] - a[0], b[1] - a[1])
    # 単位ベクトル
    u = ((b[0] - a[0]) / l, (b[1] - a[1]) / l)
    wu = (u[0] * width / 2, u[1] * width / 2)
    # 点Aから点Bへの直線を太らせたときの直方体の各頂点C,D,E,F (反時計回り)
    c = (a[0] - wu[1], a[1] + wu[0])
    d = (a[0] + wu[1], a[1] - wu[0])
    e = (b[0] + wu[1], b[1] - wu[0])
    f = (b[0] - wu[1], b[1] + wu[0])
    # 初期位置をCとする
    path = f"M {fmt(c[0])} {fmt(c[1])} "
    # C->Dはキャップを作る
    path += make_cap(c, d)
    # D->Eは直線
    path += f"L {fmt(e[0])} {fmt(e[1])} "
    # E->Fはキャップを作る
    path += make_cap(e, f)
    # F->Cはパスを閉じればOK
    path += "Z"
    return path
