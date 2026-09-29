import pytest
from fastapi import HTTPException

from app import seed
from app.repositories import history, settings_repo
from app.services import estimate_service


@pytest.fixture()
def tmp_db(monkeypatch, tmp_path):
    monkeypatch.setattr("app.db.DB_PATH", tmp_path / "t.db")
    seed.init_db()
    return tmp_path


def test_saved_snapshot_equals_response(tmp_db):
    resp = estimate_service.run_estimate(1, None, "cross", True, "", True, 1.0)
    saved = history.get_run(resp["run_id"])
    res = saved["result"]
    assert res["outer_paper_m2"] == resp["outer_paper_m2"] == 0.31
    assert res["inner_paper_m2"] == resp["inner_paper_m2"] == 0.27
    assert res["total_paper_m2"] == resp["total_paper_m2"] == 0.58
    assert res["double_layer"] is True
    assert res["lining_coefficient"] == 1.0


def test_snapshot_frozen_after_global_default_changes(tmp_db):
    resp = estimate_service.run_estimate(1, None, "cross", True, "", True, 1.0)
    run_id = resp["run_id"]

    settings_repo.set_setting("lining_coefficient", 2.0)

    saved = history.get_run(run_id)["result"]
    assert saved["inner_paper_m2"] == 0.27
    assert saved["total_paper_m2"] == 0.58

    # same params dry-calc again must match the stored snapshot
    again = estimate_service.run_estimate(1, None, "cross", False, "", True, 1.0)
    assert again["outer_paper_m2"] == saved["outer_paper_m2"]
    assert again["inner_paper_m2"] == saved["inner_paper_m2"]
    assert again["total_paper_m2"] == saved["total_paper_m2"]

    # a fresh dry run without explicit coefficient uses the NEW global default
    fresh = estimate_service.run_estimate(1, None, "cross", False, "", True, None)
    assert fresh["inner_paper_m2"] == 0.54


def test_non_positive_coefficient_fails_and_writes_nothing(tmp_db):
    before = len(history.list_runs())
    with pytest.raises(HTTPException) as ei:
        estimate_service.run_estimate(1, None, "cross", True, "", True, 0)
    assert ei.value.status_code == 422
    assert len(history.list_runs()) == before


def test_bad_global_default_fails_and_writes_nothing(tmp_db):
    settings_repo.set_setting("lining_coefficient", 0)
    before = len(history.list_runs())
    with pytest.raises(HTTPException) as ei:
        estimate_service.run_estimate(1, None, "cross", True, "", True, None)
    assert ei.value.status_code == 422
    assert len(history.list_runs()) == before


def test_single_layer_without_coefficient_ok(tmp_db):
    resp = estimate_service.run_estimate(1, None, "cross", True, "", False, None)
    assert resp["inner_paper_m2"] == 0.0
    assert resp["total_paper_m2"] == resp["outer_paper_m2"]
    assert resp["run_id"] is not None


def test_legacy_record_normalized(tmp_db):
    run_id = history.insert_run(1, 1.15, {"paper_m2": 0.31, "box_id": 1}, "")
    got = history.get_run(run_id)["result"]
    assert got["outer_paper_m2"] == 0.31
    assert got["inner_paper_m2"] == 0.0
    assert got["total_paper_m2"] == 0.31
    assert got["double_layer"] is False
    assert history.list_runs()[0]["result"]["total_paper_m2"] == 0.31
