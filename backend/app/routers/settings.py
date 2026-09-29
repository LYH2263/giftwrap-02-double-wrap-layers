import math

from fastapi import APIRouter, HTTPException
from app.repositories import settings_repo
from app.schemas.settings import SettingUpdate

router = APIRouter()

_ALLOWED = {"overlap", "lining_coefficient"}

@router.get("/settings")
def settings(): return settings_repo.get_all()

@router.put("/settings/{key}")
def update_setting(key: str, body: SettingUpdate):
    if key not in _ALLOWED or not math.isfinite(body.value) or body.value <= 0:
        raise HTTPException(422, "setting must be a positive finite number")
    settings_repo.set_setting(key, body.value)
    return settings_repo.get_all()
