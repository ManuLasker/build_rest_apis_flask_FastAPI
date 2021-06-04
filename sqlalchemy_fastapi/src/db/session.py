from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

engine = create_engine(settings.SQLALCHEMY_SQLITE_DATABASE_URI,
                       pool_pre_ping=True, connect_args={"check_same_thread": False})
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)