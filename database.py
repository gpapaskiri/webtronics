from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_config

conf = get_config("postgres")
SQLALCHEMY_DATABASE_URL = f"postgresql://{conf['user']}:{conf['password']}@{conf['host']}:{conf['port']}/{conf['db']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
