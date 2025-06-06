# 数値の文字に変換するフォーマット関数 (小数は最大3桁まで)
def fmt(num: float) -> str:
    s = f"{round(num, 3):.3f}" # 強制的に小数点が付く
    return s.rstrip("0").rstrip(".")
