from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey  #type:ignore
from datetime import date



class User(Base):
    __tablename__ = 'users'
    id= Column(Integer, primary_key=True, index=True)
    email= Column(String, unique=True)
    username= Column(String)
    first_name= Column(String)
    last_name= Column(String)
    hashed_password= Column(String)
    is_active= Column(Boolean, default=True)
    date = Column(Date, default=date.today)


class Expenses(Base):
    __tablename__ = 'expense'
    id= Column(Integer, primary_key=True, index=True)
    amount= Column(Float)
    category= Column(String)
    description= Column(String)
    date = Column(Date, default=date.today)
    owner_id= Column(Integer, ForeignKey("users.id"))
