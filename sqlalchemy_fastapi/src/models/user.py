from src.db.base import  Base
from sqlalchemy import Integer, Column, String

class User(Base):
    id = Column(Integer, autoincrement=True,
                primary_key=True, index=True)
    username = Column(String(80))
    password = Column(String(80))
    