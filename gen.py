import math
import xml.etree.ElementTree as ET
from pathlib import Path
import sys

if len(sys.argv) != 2:
    print("❌ 引数が不正です。使用法: python gen.py <font_name>")
    sys.exit(1)

# 入力SVGファイル (ストローク)
INPUT_FILE = Path(f"strokes/{sys.argv[1]}.svg")
if not INPUT_FILE.is_file():
    print(f"❌ 入力ファイルが見つかりません: {INPUT_FILE}")
    sys.exit(1)

# 出力SVGファイル (アウトライン)
OUTPUT_FILE = Path(f"fonts/{sys.argv[1]}.svg")

# 数値の出力フォーマット
def fmt(x: float) -> str:
    s = f"{round(x, 3):.3f}"
    return s.rstrip("0").rstrip(".") if "." in s else s

# === 座標変換（左下原点 → 左上原点 + パディング）===
def transform_point(x, y):
    PAD_LEFT = 12
    PAD_BOTTOM = 10
    PAD_TOP = 38
    BASELINE_Y = 1638  # = 2048 - 410

    y = -y  # Y反転
    y += BASELINE_Y + PAD_BOTTOM + PAD_TOP
    x += PAD_LEFT
    return x, y

# === 円をパスに変換 ===
def point_to_path(x, y, r):
    # four 3-point bezier curves to approximate a circle
    x, y = transform_point(x, y)
    return f"M {x - r} {y} A {r} {r} 0 1 0 {x + r} {y} A {r} {r} 0 1 0 {x - r} {y} Z"

# === ラインをパスに変換 ===
def line_to_path(x1, y1, x2, y2, stroke_width):
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    if length == 0: return ""

    # 単位ベクトルと法線
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    r = stroke_width / 2

    # 両端と角の点
    a = (x1 - uy * r, y1 + ux * r)
    b = (x1 + uy * r, y1 - ux * r)
    c = (x2 + uy * r, y2 - ux * r)
    d = (x2 - uy * r, y2 + ux * r)

    # 中心点
    start = (x1, y1)
    end = (x2, y2)

    # 座標変換
    a, b, c, d, start, end = [transform_point(*pt) for pt in [a, b, c, d, start, end]]

    # 両端の半円の頂点
    ab = (start[0] - r * ux, start[1] + r * uy)
    cd = (end[0] + r * ux, end[1] - r * uy)

    K = 0.552284749831    # ベジェ曲線の近似係数
    dc = (K * r * ux, K * r * uy) # 3次ベジエ曲線の制御点計算用の差分

    # ベジェ終端のQ制御点を中心点に（両端の半円を近似）
    d_path = (
        # A
        f"M {fmt(a[0])} {fmt(a[1])} "
        # A to AB (3-point bezier)
        f"C {fmt(a[0] - dc[0])} {fmt(a[1] + dc[1])} {fmt(ab[0] - dc[1])} {fmt(ab[1] - dc[0])} {fmt(ab[0])} {fmt(ab[1])} "
        # AB to B (3-point bezier)
        f"C {fmt(ab[0] + dc[1])} {fmt(ab[1] + dc[0])} {fmt(b[0] - dc[0])} {fmt(b[1] + dc[1])} {fmt(b[0])} {fmt(b[1])} "
        # B to C
        f"L {fmt(c[0])} {fmt(c[1])} "
        # C to CD (3-point bezier)
        f"C {fmt(c[0] + dc[0])} {fmt(c[1] - dc[1])} {fmt(cd[0] + dc[1])} {fmt(cd[1] + dc[0])} {fmt(cd[0])} {fmt(cd[1])} "
        # CD to D (3-point bezier)
        f"C {fmt(cd[0] - dc[1])} {fmt(cd[1] - dc[0])} {fmt(d[0] + dc[0])} {fmt(d[1] - dc[1])} {fmt(d[0])} {fmt(d[1])} "
        # D to A (end)
        f"Z"
    )
    return d_path

# === SVG読み込み ===
tree = ET.parse(INPUT_FILE)
root = tree.getroot()

# 新しいSVGルート作成（フォント用サイズ）
new_svg = ET.Element("svg", {
    "xmlns": "http://www.w3.org/2000/svg",
    "width": "1024",
    "height": "2048",
    "viewBox": "0 0 1024 2048"
})

# 赤い線を変換して追加
for elem in root:
    if elem.tag.endswith("line") and elem.attrib.get("stroke", "").lower() == "red":
        x1 = float(elem.attrib["x1"])
        y1 = float(elem.attrib["y1"])
        x2 = float(elem.attrib["x2"])
        y2 = float(elem.attrib["y2"])
        stroke_width = float(elem.attrib.get("stroke-width", "1"))
        d = line_to_path(x1, y1, x2, y2, stroke_width)
        path_elem = ET.Element("path", {"d": d, "fill": "black"})
        new_svg.append(path_elem)

# ファイル保存
ET.indent(ET.ElementTree(new_svg), space="")
ET.ElementTree(new_svg).write(OUTPUT_FILE, encoding="utf-8", xml_declaration=False)
print(f"✅ 変換完了: {OUTPUT_FILE}")
