from typing import Generator, Tuple
from src.db.session import session_local
from src.core.config import settings
from fastapi import Security, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, exceptions
from src.schemas.token import TokenDecode
from sqlalchemy.orm import Session
from src.schemas.user import User, UserPermission
from src.crud.crud_user import user
from src.blacklist import BLACKLIST

# Simple JWT just as flask-jwt-extended
security_bearer = HTTPBearer()


def get_db() -> Generator:
    try:
        db = session_local()
        yield db
    finally:
        db.close()


def current_user(
    token_type: str,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security_bearer),
) -> Tuple[User, UserPermission]:
    # get jwt token
    jwt = get_jwt(token_type, credentials)
    db_user = user.find_by_id(db, jwt.sub)
    if user:
        return db_user, UserPermission(**jwt.dict())
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "the user corresponding to this jwt is not in the database"
            },
        )


def decode_token(jwt_encode: str) -> TokenDecode:
    try:
        payload = jwt.decode(
            jwt_encode, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except exceptions.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Expired signature! reauthenticate instead"},
        )
    except exceptions.JWSSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Bad Jason signature!"},
        )
    except exceptions.JWTError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail={"message": "Bad signature!"}
        )
    return TokenDecode(**payload)


def get_jwt(
    token_type: str,
    credentials: HTTPAuthorizationCredentials = Security(security_bearer),
) -> TokenDecode:
    jwt = decode_token(credentials.credentials)
    if jwt.jti in BLACKLIST:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "this jwt token was already logged out"},
        )
    if token_type == jwt.type:
        return jwt
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": f"You need an {token_type} token, not a {jwt.type} token."
            },
        )
