from typing import Generator
from src.db.session import session_local
from fastapi.security import OAuth2PasswordBearer

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/auth"
)

def get_db() -> Generator:
    try:
        db = session_local()
        yield db
    finally:
        db.close()