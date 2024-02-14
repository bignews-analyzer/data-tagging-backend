from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import schemas
import models
from api.depends import get_db
from api.security_auth import JWTBearer

from crud import crud_data

router = APIRouter()

@router.get('', response_model=list[schemas.Article])
def data_list(skip: int = 0, limit: int = 100, token: dict = Depends(JWTBearer()), db: Session = Depends(get_db)):
    return crud_data.get_datas(db, skip, limit)
