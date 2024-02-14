from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import schemas
import models
from api.depends import get_db

router = APIRouter()

@router.get('', response_model=schemas.Article)
def test_item(db: Session = Depends(get_db)):
    return db.query(models.ArticleData).first()
