from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.db import init_db
import logging
from fastapi.logger import logger as fastapi_logger
from src.core.config import settings

# Create fastapi app
app = FastAPI(
    title="RestFul API course",
    description="Api for stores, items and users" " created for learning purposes",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# add start app event to initialize db
app.add_event_handler(settings.STARTUP_EVENT_NAME, init_db)


@app.on_event(settings.STARTUP_EVENT_NAME)
def config_log():
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    gunicorn_logger = logging.getLogger("gunicorn")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
    fastapi_logger.handlers = gunicorn_error_logger.handlers
    fastapi_logger.setLevel(gunicorn_logger.level)


# add api router
from src.api import api_router

app.include_router(api_router)
