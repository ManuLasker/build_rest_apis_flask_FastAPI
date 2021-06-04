from datetime import datetime, timedelta
from typing import Tuple
from src.core.config import settings
from jose import jwt
from passlib.context import CryptContext
from uuid import uuid4
from functools import wraps

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def encrypt_password(func):
    @wraps(func)
    def encrypt_password_func(*args, **kwargs):
        kwargs["user"].password = get_password_hash(kwargs["user"].password)
        return func(*args, **kwargs)
    return encrypt_password_func

def create_tokens(
    subject: int,
    expires_delta: timedelta = None,
) -> Tuple[str, str]:
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    additional_claims = {"is_admin": False}
    if subject == 1:
        additional_claims["is_admin"] = True
    
    # Create access token
    decode_acces_jwt = dict(fresh=True, iat=now, jti=str(uuid4()),
                            type="access", sub=subject, nbf=now, exp=expire)
    decode_acces_jwt.update(additional_claims)
    # Create refresh token
    decode_refresh_jwt = dict(fresh=False, iat=now, jti=str(uuid4()),
                            type="refresh", sub=subject, nbf=now, exp=expire)
    decode_refresh_jwt.update(additional_claims)
    
    encode_access_jwt = jwt.encode(decode_acces_jwt, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    encode_refresh_jwt = jwt.encode(decode_refresh_jwt, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encode_access_jwt, encode_refresh_jwt