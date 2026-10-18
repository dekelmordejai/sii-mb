from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Indicator, utc_now_iso
from app.schemas import IndicatorInput, IndicatorPage, IndicatorPatch, IndicatorView

router = APIRouter(prefix="/api/v1/indicators", tags=["indicators"])


@router.get("", response_model=IndicatorPage)
def list_indicators(
    q: str | None = Query(default=None, max_length=160),
    limit: int = Query(default=30, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_db),
):
    where = []
    if q and q.strip():
        term = f"%{q.strip()}%"
        where.append(or_(Indicator.name.ilike(term), Indicator.code.ilike(term), Indicator.domain.ilike(term)))
    total = session.scalar(select(func.count()).select_from(Indicator).where(*where)) or 0
    items = session.scalars(
        select(Indicator).where(*where).order_by(Indicator.created_at.desc(), Indicator.id.desc())
        .offset(offset).limit(limit)
    ).all()
    return IndicatorPage(items=items, total=total, limit=limit, offset=offset)


@router.post("", response_model=IndicatorView, status_code=201)
def create_indicator(payload: IndicatorInput, session: Session = Depends(get_db)):
    # Institutional identifier is stable and independent of name, area, or dashboard.
    identifier = str(uuid4())
    indicator = Indicator(
        id=identifier,
        code=f"IND-{uuid4().hex[:12].upper()}",
        **payload.model_dump(),
        status="draft",
    )
    session.add(indicator)
    session.commit()
    session.refresh(indicator)
    return indicator


@router.get("/{indicator_id}", response_model=IndicatorView)
def get_indicator(indicator_id: str, session: Session = Depends(get_db)):
    indicator = session.get(Indicator, indicator_id)
    if indicator is None:
        raise HTTPException(status_code=404, detail="Indicador no encontrado")
    return indicator


@router.patch("/{indicator_id}", response_model=IndicatorView)
def update_indicator(indicator_id: str, payload: IndicatorPatch, session: Session = Depends(get_db)):
    indicator = session.get(Indicator, indicator_id)
    if indicator is None:
        raise HTTPException(status_code=404, detail="Indicador no encontrado")
    if indicator.status != "draft":
        raise HTTPException(status_code=409, detail="Solo pueden editarse indicadores en borrador")
    changes = payload.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(indicator, key, value)
    if changes:
        indicator.updated_at = utc_now_iso()
        session.commit()
        session.refresh(indicator)
    return indicator
