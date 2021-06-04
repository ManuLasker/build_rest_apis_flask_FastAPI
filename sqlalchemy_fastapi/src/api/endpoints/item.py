from typing import Dict, List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from src.crud.crud_item import item
from src.schemas.item import ItemCreate, Item, ItemUpdate
from src.api.deps import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException


class ItemRouter:
    router = APIRouter()

    @router.get("/{name}", response_model=Item)
    def get(name: str, db: Session = Depends(get_db)):
        db_item = item.get_by_name(db, name)
        if db_item:
            return db_item
        raise HTTPException(
            status_code=404, detail={"message": f"Item with name '{name}' not found"}
        )

    @router.post("/{name}", response_model=Item)
    def post(name: str, new_item: ItemCreate, db: Session = Depends(get_db)):
        if item.get_by_name(db, name):
            raise HTTPException(
                status_code=400,
                detail={"message": f"Item with name '{name}' already exists"},
            )
        db_item = item.save_to_db(db, name, new_item)
        return db_item

    @router.put("/{name}", response_model=Item)
    def put(name: str, updated_item: ItemUpdate, db: Session = Depends(get_db)):
        db_item = item.get_by_name(db, name)
        if db_item:
            return item.update(db, db_item, updated_item)
        db_item = item.save_to_db(db, name, updated_item)
        return db_item

    @router.delete("/{name}", response_model=Item)
    def delete(name: str, db: Session = Depends(get_db)):
        db_item = item.get_by_name(db, name)
        if db_item:
            return item.delete_from_db(db, db_item)
        raise HTTPException(
            status_code=400, detail={"message": f"Item with name '{name}' not found"}
        )


class ItemListRouter:
    router = APIRouter()

    @router.get("/", response_model=Dict[str, Optional[List[Item]]])
    def get(db: Session = Depends(get_db)):
        return {"items": item.get_all_items(db)}
