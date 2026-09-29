from fastapi import APIRouter, Query
from app.schemas.estimate import EstimateRequest
from app.services import estimate_service
router = APIRouter()
@router.get("/estimate")
def get_est(
    box_id: int = Query(...),
    overlap: float | None = None,
    wrap_style: str = "cross",
    save: bool = False,
    double_layer: bool = False,
    lining_coefficient: float | None = None,
):
    return estimate_service.run_estimate(
        box_id, overlap, wrap_style, save, "", double_layer, lining_coefficient
    )
@router.post("/estimate")
def post_est(body: EstimateRequest):
    return estimate_service.run_estimate(
        body.box_id,
        body.overlap,
        body.wrap_style,
        body.save,
        body.note,
        body.double_layer,
        body.lining_coefficient,
    )
