from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///sqlite3.db")
engine.connect()

Base = declarative_base()
# Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
