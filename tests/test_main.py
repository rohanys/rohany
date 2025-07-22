import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_create_employee():
    response = client.post("/employees/", json={"id": 1, "name": "John Doe", "department": "IT", "salary": 50000})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert "employee_id" in data

def test_read_employees():
    response = client.get("/employees/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_record_attendance():
    client.post("/employees/", json={"id": 2, "name": "Jane Doe", "department": "HR", "salary": 60000})
    response = client.post("/employees/2/attendance", params={"date": "2024-07-21", "status": "Present"})
    assert response.status_code == 200
    assert response.json() == {"message": "Attendance recorded successfully"}

def test_record_evaluation():
    client.post("/employees/", json={"id": 3, "name": "Peter Jones", "department": "Finance", "salary": 70000})
    response = client.post("/employees/3/evaluations", params={"date": "2024-07-21", "rating": 4.5, "comments": "Excellent work"})
    assert response.status_code == 200
    assert response.json() == {"message": "Evaluation recorded successfully"}

def test_record_penalty():
    client.post("/employees/", json={"id": 4, "name": "Mary Smith", "department": "Marketing", "salary": 80000})
    response = client.post("/employees/4/penalties", params={"date": "2024-07-21", "reason": "Late arrival", "amount": 50})
    assert response.status_code == 200
    assert response.json() == {"message": "Penalty recorded successfully"}
