import math
import xml.etree.ElementTree as ET
from pathlib import Path
import sys

from scripts.line_to_path import line_to_path
from scripts.arc_to_path import arc_to_path
from scripts.bezier_to_path import bezier_to_path
from scripts.parse_path import parse_path, Command

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

# SVG読み込み
tree = ET.parse(INPUT_FILE)
root = tree.getroot()

# 新しいSVGルート作成
new_svg = ET.Element("svg", {
    "xmlns": "http://www.w3.org/2000/svg",
    "width": "1024",
    "height": "2048",
    "viewBox": "0 0 1024 2048"
})

# 赤い線を変換して追加
for elem in root:
    if elem.tag.endswith("line") and elem.attrib.get("stroke", "").lower() == "red":
        # red line -> outline of line
        a = (float(elem.attrib["x1"]), float(elem.attrib["y1"]))
        b = (float(elem.attrib["x2"]), float(elem.attrib["y2"]))
        stroke_width = float(elem.attrib.get("stroke-width", "1"))
        d = line_to_path(a, b, stroke_width)
        new_svg.append(ET.Element("path", {"d": d}))
    elif elem.tag.endswith("line") and elem.attrib.get("stroke", "").lower() == "blue":
        # blue line -> outline of 90 degree arc
        a = (float(elem.attrib["x1"]), float(elem.attrib["y1"]))
        b = (float(elem.attrib["x2"]), float(elem.attrib["y2"]))
        stroke_width = float(elem.attrib.get("stroke-width", "1"))
        d = arc_to_path(a, b, stroke_width)
        new_svg.append(ET.Element("path", {"d": d}))
    elif elem.tag.endswith("path") and elem.attrib.get("stroke", "").lower() == "red":
        # red cubic bezier curve -> outline of cubic bezier curve
        d = elem.attrib.get("d", "")
        stroke_width = float(elem.attrib.get("stroke-width", "1"))
        commands = parse_path(d)
        a, b, c, d = None, None, None, None
        for cmd in commands:
            if cmd.name == "M":
                a = (cmd.params[0], cmd.params[1])
            elif cmd.name == "C":
                c = (cmd.params[0], cmd.params[1])
                d = (cmd.params[2], cmd.params[3])
                b = (cmd.params[4], cmd.params[5])
        if a and b and c and d:
            d = bezier_to_path(a, b, c, d, stroke_width)
            new_svg.append(ET.Element("path", {"d": d}))
    # elif elem.tag.endswith("circle") and elem.attrib.get("stroke", "").lower() == "red":
    #     cx = float(elem.attrib["cx"])
    #     cy = float(elem.attrib["cy"])
    #     r = float(elem.attrib["r"])
    #     d = circle_to_path(cx, cy, r)
    #     path_elem = ET.Element("path", {"d": d})
    #     new_svg.append(path_elem)
    # elif elem.tag.endswith("ellipse") and elem.attrib.get("stroke", "").lower() == "red":
    #     cx = float(elem.attrib["cx"])
    #     cy = float(elem.attrib["cy"])
    #     rx = float(elem.attrib["rx"])
    #     ry = float(elem.attrib["ry"])
    #     d = circle_to_path(cx, cy, rx, ry)
    #     path_elem = ET.Element("path", {"d": d})
    #     new_svg.append(path_elem)

# ファイル保存
ET.indent(ET.ElementTree(new_svg), space="")
ET.ElementTree(new_svg).write(OUTPUT_FILE, encoding="utf-8", xml_declaration=False)
print(f"✅ 変換完了: {OUTPUT_FILE}")
