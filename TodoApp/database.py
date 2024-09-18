from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import  declarative_base

#SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:User1234!@localhost/TodoApplicationDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

#SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:Pr%40sha7t@127.0.0.1:3306/TodoApplicationDatabse'  #Pr%40sha78t -> Pr@sha7t

#engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()