from .database import Base
from sqlalchemy import Column, Integer, String



class Users(Base):
    __tablename__='users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)