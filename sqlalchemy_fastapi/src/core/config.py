import secrets
from typing import Optional, Any
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    SQLALCHEMY_SQLITE_DATABASE_URI: str
    STARTUP_EVENT_NAME: str = "startup"
    SHUTDOWN_EVENT_NAME: str = "shutdown"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    ALGORITHM : str = "HS256"

    
    @validator("SQLALCHEMY_SQLITE_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, sqlite_uri: Optional[str]) -> Any:
        message = "This is not a SQLITE database"
        if ":" in sqlite_uri:
            data_uri_split = sqlite_uri.split(":")
            assert len(data_uri_split) == 2, message + " or does not have a specific file name"
            assert data_uri_split[0] == "sqlite", message
        else:
            raise ValueError(message)
        return sqlite_uri

settings = Settings()