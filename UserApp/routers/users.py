from fastapi import Depends, Path, HTTPException, APIRouter
from ..models import Users
from ..database import SessionLocal
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field, EmailStr
from .auth import get_current_user


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class UserRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None)


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Users).filter(Users.owner_id == user.get("id")).all()


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(
    user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = (
        db.query(Users)
        .filter(Users.id == user_id)
        .filter(Users.owner_id == user.get("id"))
        .first()
    )
    if user_model is not None:
        return user_model
    raise HTTPException(status_code=404, detail="User not found.")


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def add_user(user: user_dependency, db: db_dependency, user_request: UserRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = Users(**user_request.dict(), owner_id=user.get("id"))

    db.add(user_model)
    db.commit()


@router.patch("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def partially_update_user(
    user: user_dependency,
    db: db_dependency,
    user_request: UserRequest,
    user_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = (
        db.query(Users)
        .filter(Users.id == user_id)
        .filter(Users.owner_id == user.get("id"))
        .first()
    )
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found.")

    if user_request.name is not None:
        user_model.name = user_request.name
    if user_request.email is not None:
        user_model.email = user_request.email
    if user_request.phone is not None:
        user_model.phone = user_request.phone

    db.add(user_model)
    db.commit()


@router.put("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(
    user: user_dependency,
    db: db_dependency,
    user_request: UserRequest,
    user_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = (
        db.query(Users)
        .filter(Users.id == user_id)
        .filter(Users.owner_id == user.get("id"))
        .first()
    )

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found.")

    user_model.name = (
        user_request.name if user_request.name is not None else user_model.name
    )
    user_model.email = (
        user_request.email if user_request.email is not None else user_model.email
    )
    user_model.phone = (
        user_request.phone if user_request.phone is not None else user_model.phone
    )

    db.add(user_model)
    db.commit()


@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = (
        db.query(Users)
        .filter(Users.id == user_id)
        .filter(Users.owner_id == user.get("id"))
        .first()
    )
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found.")

    db.query(Users).filter(Users.id == user_id).filter(
        Users.owner_id == user.get("id")
    ).delete()
    db.commit()
