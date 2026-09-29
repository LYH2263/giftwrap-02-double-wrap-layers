from pydantic import BaseModel

class EstimateRequest(BaseModel):
    box_id: int
    overlap: float | None = None
    wrap_style: str = "cross"
    save: bool = False
    note: str = ""
    double_layer: bool = False
    # NaN/inf are rejected with a clean 422 by the service-layer isfinite guard
    lining_coefficient: float | None = None
