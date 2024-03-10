import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String, UniqueConstraint

from models.base import Base


class User(Base):
    __tablename__ = "user"

    __table_args__ = (UniqueConstraint("username", name="username_unique"),)

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    username = Column(String(128), nullable=False)
    short_description = Column(String)
    long_bio = Column(String)
    # email pass etc
