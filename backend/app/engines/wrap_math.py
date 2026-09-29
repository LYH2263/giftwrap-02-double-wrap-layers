import math


def paper_area(
    length: float,
    width: float,
    height: float,
    overlap: float = 1.15,
    double_layer: bool = False,
    lining_coefficient: float | None = None,
) -> dict:
    L, W, H = float(length), float(width), float(height)
    if min(L, W, H) <= 0:
        raise ValueError("box dimensions must be positive")
    base = 2 * (L * W + L * H + W * H)
    outer = round(base * float(overlap), 3)
    inner = 0.0
    coeff_used = None
    if double_layer:
        if (
            lining_coefficient is None
            or not math.isfinite(float(lining_coefficient))
            or float(lining_coefficient) <= 0
        ):
            raise ValueError("lining_coefficient must be a positive finite number")
        coeff_used = float(lining_coefficient)
        inner = round(base * coeff_used, 3)
    return {
        "box_surface": round(base, 3),
        "overlap": float(overlap),
        "double_layer": bool(double_layer),
        "lining_coefficient": coeff_used,
        "outer_paper_m2": outer,
        "inner_paper_m2": inner,
        "total_paper_m2": round(outer + inner, 3),
        "paper_m2": outer,
    }


def ribbon_estimate(length: float, width: float, height: float, wrap_style: str = "cross") -> dict:
    """Helper: approximate ribbon length in meters (not stored as primary metric)."""
    L, W, H = float(length), float(width), float(height)
    girth = 2 * (W + H)
    if wrap_style == "band":
        meters = girth + 0.3
    else:
        meters = girth * 2 + L + 0.5
    return {"wrap_style": wrap_style, "ribbon_m": round(meters, 2)}
