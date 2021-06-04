from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from src.crud.crud_store import store
from src.schemas.store import Store, StoreCreate
from src.api.deps import get_db
from typing import Dict, List, Optional


class StoreRouter:
    router = APIRouter()
    
    @router.get("/{name}", response_model=Store)
    def get(name:str, db: Session = Depends(get_db)):
        db_store = store.get_by_name(db, name)
        if db_store:
            return db_store
        raise HTTPException(status_code=404, 
                            detail={"message":f"A store with name {name} does not exist!"})
    
    @router.post("/{name}", response_model=Store)
    def post(name:str, new_store: Optional[StoreCreate] = None, db: Session = Depends(get_db)):
        if store.get_by_name(db, name):
            raise HTTPException(
                status_code=400,
                detail={"message": f"A product with name {name} already exists!"}
            )
        db_store = store.save_to_db(db, name, new_store)
        return db_store
        
    @router.delete("/{name}", response_model=Store)
    def delete(name:str, db:Session = Depends(get_db)):
        db_store = store.get_by_name(db, name)
        if db_store:
            return store.delete_from_db(db, db_store)
        raise HTTPException(
            status_code=400, detail={"message":f"Item with name '{name}' not found"}
        )

class StoreListRouter:
    router = APIRouter()
    
    @router.get("/", response_model=Dict[str, Optional[List[Store]]])
    def get(db:Session = Depends(get_db)):
        return {"stores": store.get_all_stores(db)}