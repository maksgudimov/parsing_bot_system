import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String(255), unique=True, nullable=False)


class BestProduct(Base):
    __tablename__ = "best_product"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_id = Column(Integer)


class LogSendProdcut(Base):
    __tablename__ = "log_send_product"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, unique=True)
    shop_id = Column(Integer)
    was_send = Column(Boolean, default=False)
    datetime_created = Column(DateTime, default=datetime.datetime.now())

