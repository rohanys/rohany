from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float
    employee_id: Optional[str] = None
    attendance: list = []
    evaluations: list = []
    penalties: list = []

employees_db = {}
next_employee_id = 1

@app.post("/employees/", response_model=Employee)
def create_employee(employee: Employee):
    global next_employee_id
    if employee.id in employees_db:
        raise HTTPException(status_code=400, detail="Employee already exists")
    employee.employee_id = f"EMP-{next_employee_id}"
    employees_db[employee.id] = employee
    next_employee_id += 1
    return employee

@app.get("/employees/", response_model=List[Employee])
def read_employees():
    return list(employees_db.values())

@app.get("/employees/{employee_id}", response_model=Employee)
def read_employee(employee_id: int):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employees_db[employee_id]

@app.put("/employees/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, employee: Employee):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    employees_db[employee_id] = employee
    return employee

@app.delete("/employees/{employee_id}", response_model=Employee)
def delete_employee(employee_id: int):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employees_db.pop(employee_id)

@app.post("/employees/{employee_id}/attendance")
def record_attendance(employee_id: int, date: str, status: str):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    employees_db[employee_id].attendance.append({"date": date, "status": status})
    return {"message": "Attendance recorded successfully"}

@app.post("/employees/{employee_id}/evaluations")
def record_evaluation(employee_id: int, date: str, rating: float, comments: str):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    employees_db[employee_id].evaluations.append({"date": date, "rating": rating, "comments": comments})
    return {"message": "Evaluation recorded successfully"}

@app.post("/employees/{employee_id}/penalties")
def record_penalty(employee_id: int, date: str, reason: str, amount: float):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    employees_db[employee_id].penalties.append({"date": date, "reason": reason, "amount": amount})
    return {"message": "Penalty recorded successfully"}
