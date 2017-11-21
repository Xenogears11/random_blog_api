"""Database init"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# get Base object for Table classes
Base = declarative_base()

# get connect_str
with open('res/connect_str.txt', 'r', encoding='utf-8') as file:
    line = file.read()
    connect_str = line.rstrip()

engine = create_engine(connect_str)
DBSession = sessionmaker(bind=engine)
