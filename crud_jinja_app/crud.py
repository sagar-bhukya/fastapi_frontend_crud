from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id, models.Item.deleted_at == None).first()

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Item).filter(models.Item.deleted_at == None).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = get_item(db, item_id)
    if db_item is None:
        return None
    db_item.title = item.title
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if db_item:
        db_item.deleted_at = datetime.utcnow()
        db.commit()
        return db_item
    return None
