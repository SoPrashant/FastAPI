from fastapi import FastAPI, Depends, Path, HTTPException
from .models import Base, Users
from .database import engine, SessionLocal
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field, EmailStr, constr


app = FastAPI()

#Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class UserRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None)


@app.get('/', status_code=status.HTTP_200_OK)
async def read_all(db : db_dependency):
    return db.query(Users).all()



@app.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(db : db_dependency, user_id : int = Path(gt=0)):
    user_model = db.query(Users).filter(Users.id == user_id).first()
    if user_model is not None:
        return user_model
    raise HTTPException(status_code=404, detail='User not found.')


@app.post("/user", status_code=status.HTTP_201_CREATED)
async def add_user(db : db_dependency, user_request: UserRequest):
    user_model = Users(**user_request.dict())

    db.add(user_model)
    db.commit()


@app.patch("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(
    db: db_dependency,
    user_request: UserRequest,
    user_id: int = Path(gt=0)
):
        user_model = db.query(Users).filter(Users.id == user_id).first()
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


@app.put("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(db : db_dependency, user_request: UserRequest, user_id : int = Path(gt=0)):
    user_model = db.query(Users).filter(Users.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found.")

    user_model.name = user_request.name
    user_model.email = user_request.email
    user_model.phone = user_request.phone

    db.add(user_model)
    db.commit()


@app.delete("/user/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: db_dependency, user_id: int= Path(gt=0)):
    user_model = db.query(Users).filter(Users.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()






