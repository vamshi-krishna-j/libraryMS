# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from models import Base
#
# from dotenv import load_dotenv
# import os
#
# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")
#
#
# engine = create_engine(DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(bind=engine)
#
# # Create tables (run once)
# Base.metadata.create_all(engine)
#
#
#
#
#
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
