from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from UserApp.database import Base
from fastapi.testclient import TestClient
import pytest
from UserApp.main import app
from UserApp.models import Users


SQLALCHEMY_DATABASE_URL = "sqlite:///./testuserdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():  # open a connection when client wnat to fetch the data and then close the same later
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)


@pytest.fixture
def test_user():
    user = Users(
        name="exampleUser",
        email="exampleUser123@gmail.com",
        phone="9462733220",
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
