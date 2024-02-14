from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc, asc
import models
from datetime import date
import schemas

def get_datas(
        db: Session,
        skip: int,
        limit: int,
        min_length: int,
        start_date: date,
        end_date: date,
        company: list[int],
        order_by: str,
        desc_int: int,):
    datas = db.query(models.ArticleData)\
        .filter(and_(models.ArticleData.post_time >= start_date, models.ArticleData.post_time <= end_date))\
        .filter(models.ArticleData.company.in_(company))\
        .filter(func.char_length(models.ArticleData.content) >= min_length)
    if desc_int == 1:
        datas = datas.order_by(desc(models.ArticleData.post_time))
    else:
        datas = datas.order_by(asc(models.ArticleData.post_time))
    print(datas.count())
    return datas.offset(skip).limit(limit).all()
