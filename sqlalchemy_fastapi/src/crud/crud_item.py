from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.item import Item
from src.schemas.item import ItemCreate, ItemUpdate


class CRUDItem:
    def __init__(self, ItemModel: Item):
        self.ItemModel = ItemModel

    def get_by_name(self, db: Session, name: str) -> Optional[Item]:
        return db.query(self.ItemModel).filter(self.ItemModel.name == name).first()
    
    def save_to_db(self, db: Session, name:str, item: ItemCreate) -> Item:
        db_item = Item(name=name, **item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    def delete_from_db(self, db: Session, item: Item) -> Item:
        db.delete(item)
        db.commit()
        return item

    def update(self, db: Session, item: Item, updatedItem: ItemUpdate) -> Item:
        for key, value in updatedItem.dict().items():
            setattr(item, key, value)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    
    def get_all_items(self, db:Session) -> Optional[List[Item]]:
        return db.query(self.ItemModel).all()

item = CRUDItem(Item)