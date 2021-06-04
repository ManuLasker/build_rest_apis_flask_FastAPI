from src.db.base import Base
from sqlalchemy import (Integer, Column, Float,
                        String, ForeignKey)
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

class Item(Base):
    id = Column(Integer, primary_key=True, index=True,
                autoincrement=True)
    name = Column(String(80))
    price = Column(Float(precision=2))
    
    store_id = Column(Integer, ForeignKey("stores.id"))
    store = relationship("Store")
