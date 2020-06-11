from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database_config import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    amount = Column(Integer, default=0)
    trades = relationship("Trade", cascade="all, delete-orphan",
                          passive_deletes=True, backref="users")


class Trade(Base):
    __tablename__ = "trades"
    trade_id = Column(Integer, primary_key=True)
    stock_id = Column(String)
    user_id = Column(Integer, ForeignKey(User.user_id, ondelete='CASCADE'))
    total = Column(Integer, nullable=False)
    stock_price = Column(Integer, nullable=False)
    lower_bound = Column(Integer, nullable=False)
    upper_bound = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.now())
