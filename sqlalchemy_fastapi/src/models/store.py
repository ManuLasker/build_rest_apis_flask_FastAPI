from src.db.base import Base
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
    
class Store(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80))
    
    items = relationship("Item")