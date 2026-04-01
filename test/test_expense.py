import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app
from database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from router.expense import get_db
from models import Base

# Create a separate test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

# Create tables in test DB
Base.metadata.create_all(bind=engine)




# Override function
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Tell FastAPI to use test DB instead
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)



def test_create_user():
    response = client.post("/auth/", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 201


def test_login():
    response = client.post("/auth/token", data={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_expense():
    login = client.post("/auth/token", data={
        "username": "testuser",
        "password": "testpassword"
    })
    token = login.json()["access_token"]

    response = client.post("/expense/expense", json={
        "description": "Test expense",
        "category": "Food",
        "amount": 100.0
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201


def test_read_all_expenses():
    login = client.post("/auth/token", data={
        "username": "testuser",
        "password": "testpassword"
    })
    token = login.json()["access_token"]

    response = client.get("/expense/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)




