from fastapi import APIRouter
from src.api.endpoints import (
    ItemRouter,
    ItemListRouter,
    UserRegisterRouter,
    UserAuthenticationRouter,
    UserRouter,
    UserRefresherRouter,
    UserLogoutRouter,
    StoreListRouter,
    StoreRouter,
)

UserLogoutRouter
# add api router
api_router = APIRouter()
# add item router
api_router.include_router(ItemRouter.router, prefix="/item", tags=["item"])
# add items router
api_router.include_router(ItemListRouter.router, prefix="/items", tags=["items"])
# add user router
api_router.include_router(UserRouter.router, prefix="/user", tags=["user"])
# add store router
api_router.include_router(StoreRouter.router, prefix="/store", tags=["store"])
# add stores router
api_router.include_router(StoreListRouter.router, prefix="/stores", tags=["stores"])
# add register user router
api_router.include_router(UserRegisterRouter.router, tags=["user"])
# add authentication router
api_router.include_router(UserAuthenticationRouter.router, tags=["user"])
# add router refresh
api_router.include_router(UserRefresherRouter.router, tags=["user"])
# add logout user router
api_router.include_router(UserLogoutRouter.router, tags=["user"])
