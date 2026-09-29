import math

import pytest

from app.engines.wrap_math import paper_area, ribbon_estimate

def test_book_box():
    r = paper_area(0.30, 0.20, 0.15, 1.15)
    assert r["box_surface"] == 0.27
    assert r["paper_m2"] == 0.31

def test_ribbon_cross():
    rb = ribbon_estimate(0.30, 0.20, 0.15, "cross")
    assert rb["ribbon_m"] > 0.5

def test_single_layer_matches_legacy_paper():
    r = paper_area(1, 1, 1, 1.15)
    assert r["paper_m2"] == 6.9
    assert r["outer_paper_m2"] == 6.9
    assert r["inner_paper_m2"] == 0.0
    assert r["total_paper_m2"] == 6.9
    assert r["double_layer"] is False
    assert r["lining_coefficient"] is None

def test_double_layer_splits_areas():
    r = paper_area(1, 1, 1, 1.15, True, 1.0)
    assert r["outer_paper_m2"] == 6.9
    assert r["inner_paper_m2"] == 6.0
    assert r["total_paper_m2"] == 12.9
    assert r["paper_m2"] == 6.9
    assert r["double_layer"] is True
    assert r["lining_coefficient"] == 1.0

def test_double_layer_book_box():
    r = paper_area(0.30, 0.20, 0.15, 1.15, True, 0.5)
    assert r["box_surface"] == 0.27
    assert r["outer_paper_m2"] == 0.31
    assert r["inner_paper_m2"] == 0.135
    assert r["total_paper_m2"] == 0.445

@pytest.mark.parametrize("bad", [0, -1, math.nan, math.inf, -math.inf, None])
def test_double_layer_requires_positive_coefficient(bad):
    with pytest.raises(ValueError):
        paper_area(1, 1, 1, 1.15, True, bad)

def test_single_layer_never_validates_coefficient():
    r = paper_area(1, 1, 1, 1.15, False, 0)
    assert r["inner_paper_m2"] == 0.0
    assert r["total_paper_m2"] == r["outer_paper_m2"]
