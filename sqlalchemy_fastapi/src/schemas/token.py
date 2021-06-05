from pydantic import BaseModel, validator
from datetime import datetime

class TokenBase(BaseModel):
    access_token: str
class Token(BaseModel):
    access_token: str
    refresh_token: str
    
class TokenDecode(BaseModel):
    fresh: bool
    iat: datetime
    jti: str
    nbf: datetime
    type: str
    sub: int
    exp: datetime
    is_admin: bool
    
    @validator("type", pre=True)
    def validate_type(cls, type_: str) -> str:
        if not type_ in ["access", "refresh"]:
            raise ValueError("type must be one of access or refresh")
        return type_