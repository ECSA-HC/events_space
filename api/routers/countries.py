import math
from sqlalchemy import or_, case
from core.database import get_db
from models.models import Country
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query


router = APIRouter()

CATEGORY_ORDER = case(
    (Country.category == "ecsa_member", 1),
    (Country.category == "african", 2),
    else_=3,
)


@router.get("")
@router.get("/")
async def get_countries(
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = 300,
    search: str = "",
):
    search_filter = or_(
        Country.country.ilike(f"%{search}%"),
        Country.short_code.ilike(f"%{search}%"),
    )

    countries_query = (
        db.query(Country)
        .filter(search_filter)
        .order_by(CATEGORY_ORDER, Country.country)
    )

    total_count = countries_query.count()
    countries = countries_query.offset(skip).limit(limit).all()

    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": [
        {
            "id": c.id,
            "country": c.country,
            "short_code": c.short_code,
            "category": c.category,
        }
        for c in countries
    ]}
