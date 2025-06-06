# ストローク用の座標は、ベースラインをy=0、上側を+yとし、cx=1000, cy=2000
# アウトライン用の座標は、上端をy=0、下側を+yとし、cx=1024、cy=2048、ベースラインはy=2048-410の位置
# 拡大縮小はせず、パディングで対応(left=12, top=38, right=12, bottom=10)

# ストローク用座標からアウトライン用座標への変換関数
def transcoord(p: tuple[float, float]) -> tuple[float, float]:
    if type(p[0]) is not float:
        print(type(p[0]))
        raise TypeError("Invalid coordinate type")
    if type(p[1]) is not float:
        print(type(p[1]))
        raise TypeError("Invalid coordinate type")
    return (p[0] + 12, p[1] + 1638)
