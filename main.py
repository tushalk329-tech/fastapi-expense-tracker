from fastapi import FastAPI
from models import Base
from database import engine
from router import auth, expense
from database import engine
app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(expense.router)
app.include_router(auth.router)


