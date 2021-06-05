from fastapi import APIRouter, HTTPException, Depends, Security
from sqlalchemy.orm import Session
from src.crud.crud_user import user
from src.schemas.user import User, UserCreate
from src.schemas.msg import Msg
from src.schemas.token import Token, TokenDecode
from src.api.deps import get_db, security_bearer, current_user, get_jwt
from src.core.security import verify_password, create_tokens
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from src.blacklist import BLACKLIST
from functools import partial


class UserRouter:
    router = APIRouter()

    @router.delete("/{user_id}", response_model=User)
    def delete(user_id: int, db: Session = Depends(get_db)):
        db_user = user.find_by_id(db, user_id)
        if db_user:
            user.delete_from_db(db, user)
            return db_user
        raise HTTPException(
            status_code=404,
            detail={"message": f"User with user_id '{user_id}' not found"},
        )

    @router.get("/{user_id}", response_model=User)
    def get(user_id: int, db: Session = Depends(get_db)):
        db_user = user.find_by_id(db, user_id)
        if db_user:
            return db_user
        raise HTTPException(
            status_code=404,
            detail={"message": f"User with user_id '{user_id}' not found"},
        )


class UserRegisterRouter:
    router = APIRouter()

    @router.post("/register", response_model=Msg)
    def register(new_user: UserCreate, db: Session = Depends(get_db)):
        db_user = user.find_by_username(db, new_user.username)
        if db_user:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": f"User with username {new_user.username} already exists!"
                },
            )
        db_user = user.save_to_db(db, user=new_user)
        return {"message": f"User with username {new_user.username} created Succesfull"}


class UserAuthenticationRouter:
    router = APIRouter()

    @router.post("/auth", response_model=Token)
    def authenticate(
        info_user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
    ):
        db_user = user.find_by_username(db, info_user.username)
        if db_user and verify_password(info_user.password, db_user.password):
            access_token, refresh_token = create_tokens(subject=db_user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        raise HTTPException(status_code=401, detail={"message": "invalid credentials"})


class UserRefresherRouter:
    router = APIRouter()

    @router.post("/refresh")
    def refresh(credentials: HTTPAuthorizationCredentials = Security(security_bearer)):
        print(credentials)
        return {"hola": "mundo"}

class UserLogoutRouter:
    router = APIRouter()

    @router.post("/logout")
    def logout(jwt_payload: TokenDecode= Depends(partial(get_jwt, "access"))):
        jti = jwt_payload.jti
        BLACKLIST.add(jti)
        return {"message": "succesfully logged out!"}
    