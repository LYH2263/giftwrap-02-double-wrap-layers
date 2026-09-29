from pydantic import BaseModel

class SettingUpdate(BaseModel):
    # NaN/inf are rejected with a clean 422 by the route isfinite guard
    value: float
