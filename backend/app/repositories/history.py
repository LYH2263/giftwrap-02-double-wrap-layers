import json
from datetime import datetime, timezone
from app.db import connect

def insert_run(box_id, overlap, result, note=""):
    c = connect()
    try:
        cur = c.execute(
            "INSERT INTO calc_runs(box_id,overlap,result_json,note,created_at) VALUES (?,?,?,?,?)",
            (box_id, overlap, json.dumps(result, ensure_ascii=False), note, datetime.now(timezone.utc).isoformat()),
        )
        c.commit()
        return int(cur.lastrowid)
    finally:
        c.close()

def _with_result(row):
    d = dict(row)
    res = json.loads(d.pop("result_json"))
    if "outer_paper_m2" not in res:
        # legacy record written before double-layer support
        outer = float(res.get("paper_m2", 0.0))
        res["outer_paper_m2"] = outer
        res["inner_paper_m2"] = 0.0
        res["total_paper_m2"] = outer
        res.setdefault("double_layer", False)
        res.setdefault("lining_coefficient", None)
    d["result"] = res
    return d

_SELECT = (
    "SELECT r.*, b.name box_name FROM calc_runs r "
    "LEFT JOIN boxes b ON b.id=r.box_id "
)

def get_run(run_id):
    c = connect()
    try:
        row = c.execute(_SELECT + "WHERE r.id=?", (run_id,)).fetchone()
        return _with_result(row) if row else None
    finally:
        c.close()

def list_runs(limit=50):
    c = connect()
    try:
        rows = c.execute(_SELECT + "ORDER BY r.id DESC LIMIT ?", (limit,)).fetchall()
        return [_with_result(row) for row in rows]
    finally:
        c.close()
