from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class AuthUsers(Base):
    __tablename__ = "authusers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    owner_id = Column(Integer, ForeignKey(AuthUsers.id))
