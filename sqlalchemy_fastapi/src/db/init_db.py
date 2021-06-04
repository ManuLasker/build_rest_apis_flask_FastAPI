from src.db import base
from src.db.session import engine

def init_db() -> None:
    base.Base.metadata.create_all(bind=engine)