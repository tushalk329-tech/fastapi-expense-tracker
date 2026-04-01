# FastAPI Expense Tracker

A REST API built with FastAPI for tracking personal expenses with JWT authentication.

## Features
- JWT Authentication (register, login)
- Create, read, update, delete expenses
- Expenses filtered by logged-in user
- Auto date assignment on expense creation

## Tech Stack
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- JWT / bcrypt
- Pytest

## How to Run Locally
1. Clone the repo
2. Create a virtual environment and activate it
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `uvicorn main:app --reload`
5. Visit: `http://127.0.0.1:8000/docs`

## Endpoints
- `POST /auth/` - Register a new user
- `POST /auth/token` - Login and get JWT token
- `GET /expense/` - Get all expenses
- `POST /expense/expense` - Create an expense
- `GET /expense/{expense_id}` - Get single expense
- `PUT /expense/{expense_id}` - Update an expense
- `DELETE /expense/{expense_id}` - Delete an expense