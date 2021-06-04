from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.store import Store
from src.schemas.store import StoreCreate


class CRUDStore:
    def __init__(self, StoreModel: Store):
        self.StoreModel = StoreModel

    def get_by_name(self, db: Session, name: str) -> Optional[Store]:
        return db.query(self.StoreModel).filter(self.StoreModel.name == name).first()

    def save_to_db(self, db: Session, name: str, store: StoreCreate) -> Store:
        if store:
            db_store = Store(name=name, **store.dict())
        else:
            db_store = Store(name=name)
        db.add(db_store)
        db.commit()
        db.refresh(db_store)
        return db_store

    def delete_from_db(self, db: Session, store: Store) -> Store:
        db.delete(store)
        db.commit()
        return store

    def get_all_stores(self, db: Session) -> Optional[List[Store]]:
        return db.query(self.StoreModel).all()


store = CRUDStore(Store)
