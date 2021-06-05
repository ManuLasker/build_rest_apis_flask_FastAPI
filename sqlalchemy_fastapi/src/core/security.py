from datetime import datetime, timedelta
from typing import Any, Dict, Tuple
from src.core.config import settings
from jose import jwt
from passlib.context import CryptContext
from uuid import uuid4
from functools import wraps

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
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
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    additional_claims = {"is_admin": False}
    if subject == 1:
        additional_claims["is_admin"] = True

    encode_access_jwt = create_access_token(
        subject, iat=now, nbf=now, expire=expire, additional_claims=additional_claims
    )
    encode_refresh_jwt = create_refresh_token(
        subject, iat=now, nbf=now, expire=expire, additional_claims=additional_claims
    )

    return encode_access_jwt, encode_refresh_jwt


def create_token(
    subject: int,
    token_type: str,
    jti: str,
    iat: datetime,
    nbf: datetime,
    expire: datetime,
    additional_claims: Dict[str, Any],
) -> str:

    decode_token = dict(
        fresh=True if token_type == "access" else False,
        iat=iat,
        jti=jti,
        nbf=nbf,
        type=token_type,
        sub=str(subject),
        exp=expire,
    )
    decode_token.update(additional_claims)
    return jwt.encode(decode_token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def handle_args(
    iat: datetime = None,
    nbf: datetime = None,
    expire: datetime = None,
    expire_delta: timedelta = None,
):
    now = datetime.utcnow()
    if expire is None:
        if expire_delta:
            expire = now + expire_delta
        else:
            expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    if nbf is None:
        nbf = now
    if iat is None:
        iat = now
    return iat, nbf, expire


def create_access_token(
    subject: int,
    iat: datetime = None,
    nbf: datetime = None,
    expire: datetime = None,
    expire_delta: timedelta = None,
    additional_claims: Dict[str, Any] = None,
) -> str:

    iat, nbf, expire = handle_args(iat, nbf, expire, expire_delta)
    return create_token(
        subject, "access", str(uuid4()), iat, nbf, expire, additional_claims
    )


def create_refresh_token(
    subject: int,
    iat: datetime = None,
    nbf: datetime = None,
    expire_delta: timedelta = None,
    expire: datetime = None,
    additional_claims: Dict[str, Any] = None,
):
    iat, nbf, expire = handle_args(iat, nbf, expire, expire_delta)
    return create_token(
        subject, "refresh", str(uuid4()), iat, nbf, expire, additional_claims
    )