from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field  # for Data validation
from starlette import status



app = FastAPI()


class Book:
    id : int
    title : str
    author : str
    description : str
    rating : int
    published_date : int


    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self. title = title
        self. author = author
        self. description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='id is not needed on create', default=None)  # if not include none then always have to pass id in request body
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6 )
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example" : {
                "title" : "book title",
                "author" : "book author",
                "description" : "book description",
                "rating" : 5,
                "published_date": 2029
            }
        }
    }



BOOKS = [
    Book(1,'Computer Science', 'alen', 'great book', 5, 2030),
    Book(2,'Be fast with fast api', 'ronan', 'awsome book',5, 2030),
    Book(3,'Master endpoint', 'Mia', 'nice book',5, 2029),
    Book(4,'HP1', 'Author 1', 'great book',2, 2028),
    Book(5,'HP2', 'Author 2', 'great book',3, 2027),
    Book(6,'HP3', 'Author 3', 'great book',1, 2026)

]


@app.get("/books",status_code = status.HTTP_200_OK)   #Defining explicit status code using starlet
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}",status_code = status.HTTP_200_OK)
async def read_book_by_id(book_id: int = Path(gt=0)):
        for book in BOOKS:
            if book.id == book_id:
                return book

        raise HTTPException(status_code=404, detail="Item Not Found")


@app.get("/books/",status_code = status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0 , lt=6)):
    book_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_return.append(book)

    return book_return



@app.get("/books/publish/",status_code = status.HTTP_200_OK)
async def read_books_by_publish_date(published_date: int = Query(gt=1999, lt=2031)):
    books_return=[]
    for book in BOOKS:
        if book.published_date == published_date:
            books_return.append(book)

    return books_return



@app.post("/create_book", status_code = status.HTTP_201_CREATED)
async def create_book(book_request : BookRequest):  # type of BookRequest
    new_book = Book(**book_request.dict())      # converting the request to book object - **kwargs Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))



def find_book_id(book : Book):

    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1   # Using Ternary operator

    #if len(BOOKS) > 0:
    #    book.id = BOOKS[-1].id + 1
    #else:
    #    book.id = 1
    return book



@app.put("/books/update_book",status_code = status.HTTP_204_NO_CONTENT)
async  def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail="Item Not Found")



@app.delete("/books/{book_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail="Item Not Found")
