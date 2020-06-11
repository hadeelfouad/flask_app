import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get("DB_URL", "postgresql://admin:admin@localhost:5432/thndr"))
Session = sessionmaker(bind=engine)
Base = declarative_base()
