from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from models import ScanResult
from schemas import HistoryItem
from dependencies import get_current_user

router = APIRouter()


@router.get("/history", response_model=list[HistoryItem])
def get_history(
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    results = (
        db.query(ScanResult)
        .filter(ScanResult.user_id == current_user.id)
        .order_by(ScanResult.scan_date.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return results
