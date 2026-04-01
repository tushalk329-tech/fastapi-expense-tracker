from fastapi import HTTPException
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path,  Request, status
from database import SessionLocal
from starlette import status
from starlette.responses import RedirectResponse
from models import Expenses
from router.auth import get_current_user
from datetime import date



router = APIRouter(
    prefix="/expense",
    tags=['expense']
)



class ExpenseRequest(BaseModel):
    description:str=Field(min_length=2, max_length=500)
    category:str=Field(min_length=2, max_length=50)
    amount:float=Field(gt=0)




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, details='Authentication Failed')
    return db.query(Expenses).filter(Expenses.owner_id == user.get('id')).all()

@router.get("/{expense_id}", status_code=status.HTTP_200_OK)
async def read_expense(user:user_dependency, db: db_dependency, expense_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, details='Authentication Failed')

    expense_model = db.query(Expenses).filter(Expenses.id == expense_id) \
        .filter(Expenses.owner_id == user.get('id')).first()
    if expense_model is not None:
        return expense_model
    raise HTTPException(status_code=404, detail='Expense not found.')


@router.post("/expense", status_code=status.HTTP_201_CREATED)
async def create_expense(user:user_dependency,expense_request: ExpenseRequest, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, details='Authentication Failed')
    expense_model = Expenses(**expense_request.dict(), owner_id=user.get('id'))
    db.add(expense_model)
    db.commit()


@router.put("/expense{expense.id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_expense(user:user_dependency,expense_request: ExpenseRequest,
                         db: db_dependency, expense_id: int = Path(gt=0)):
    expense_model = db.query(Expenses).filter(Expenses.id == expense_id).first()
    if expense_model is None:
        raise HTTPException(status_code=404, detail='Expense not found')
    expense_model = db.query(Expenses).filter(Expenses.id == expense_id) \
        .filter(Expenses.owner_id == user.get('id')).first()
    if expense_model is None:
        raise HTTPException(status_code=404, detail='Expense not found.')

    expense_model.amount = expense_request.amount
    expense_model.category= expense_request.category
    expense_model.description= expense_request.description

    db.add(expense_model)
    db.commit

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(user:user_dependency,
                         db: db_dependency,
                         expense_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, details='Authentication Failed')

    expense_model= db.query(Expenses).filter(Expenses.id == expense_id)\
    .filter(Expenses.owner_id == user.get('id')).first()
    if expense_model is None:
        raise HTTPException(status_code=404, detail='Expense not found')
    db.query(Expenses).filter(Expenses.id == expense_id)\
        .filter(Expenses.owner_id == user.get('id')).delete()
    db.commit()
























