from typing import Optional
from pydantic import BaseModel

# Shared properties What every body can see
class ItemBase(BaseModel):
    price: Optional[float] = None
    
# Properties to receive on item creation
class ItemCreate(ItemBase):
    price: float
    store_id: int
    
# Properties to receive on item update
class ItemUpdate(ItemCreate):
    pass

# Properties share by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    name: str
    price: float
    store_id: int
    
    class Config:
        orm_mode = True
        
# Properties to return to client
class Item(ItemInDBBase):
    pass

# Properties stores in DB
class ItemInDB(ItemInDBBase):
    from src.schemas.store import StoreInDB
    store: StoreInDB