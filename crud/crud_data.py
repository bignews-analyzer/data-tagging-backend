from sqlalchemy.orm import Session
import models
import schemas

def get_datas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ArticleData).offset(skip).limit(limit).all()
