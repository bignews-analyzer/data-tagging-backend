from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

import schemas
import models
from api.depends import get_db
from api.security_auth import JWTBearer
from datetime import date
from crud import crud_data

router = APIRouter()

@router.get('', response_model=list[schemas.Article])
def data_list(
        skip: int = 0,
        limit: int = 100,
        min_length: int = 0,
        start_date: date = date(year=2010, month=1, day=1),
        end_date: date = date(year=2023, month=12, day=31),
        company: list[int] = Query(list(range(121, 241))),
        # order_by: str = 'post_time',
        desc: int = 0,
        token: dict = Depends(JWTBearer()),
        db: Session = Depends(get_db)):

    order_by: str = 'post_time'
    return crud_data.get_datas(db, skip, limit, min_length, start_date, end_date, company, order_by, desc)
