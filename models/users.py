from datetime import datetime

from sqlalchemy import Integer, String, func, DateTime
from sqlalchemy.orm import Mapped,mapped_column

from models.base import Base


class User(Base):
    __tablename__ = "users"

    id:Mapped[int]=mapped_column(Integer, primary_key=True, autoincrement=True)
    username:Mapped[str]=mapped_column(String(32),unique=True,nullable=False)
    password:Mapped[str]=mapped_column(String(60),nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=func.now())