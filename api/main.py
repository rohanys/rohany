from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float
    employee_id: Optional[str] = None
    attendance: list = []
    evaluations: list = []
    penalties: list = []
    rewards: list = []

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

EMPLOYEES_DB = {}
NEXT_EMPLOYEE_ID = 1

@app.post("/employees/", response_model=Employee)
def create_employee(employee: Employee):
    global NEXT_EMPLOYEE_ID
    if employee.id in EMPLOYEES_DB:
        raise HTTPException(status_code=400, detail="الموظف موجود بالفعل")
    employee.employee_id = f"EMP-{NEXT_EMPLOYEE_ID}"
    EMPLOYEES_DB[employee.id] = employee
    NEXT_EMPLOYEE_ID += 1
    return employee

@app.get("/employees/", response_model=List[Employee])
def read_employees():
    return list(EMPLOYEES_DB.values())

@app.get("/employees/{employee_id}", response_model=Employee)
def read_employee(employee_id: int):
    if employee_id not in EMPLOYEES_DB:
        raise HTTPException(status_code=404, detail="لم يتم العثور على الموظف")
    return EMPLOYEES_DB[employee_id]

@app.put("/employees/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, employee: Employee):
    if employee_id not in EMPLOYEES_DB:
        raise HTTPException(status_code=404, detail="لم يتم العثور على الموظف")
    EMPLOYEES_DB[employee_id] = employee
    return employee

@app.delete("/employees/{employee_id}", response_model=Employee)
def delete_employee(employee_id: int):
    if employee_id not in EMPLOYEES_DB:
        raise HTTPException(status_code=404, detail="لم يتم العثور على الموظف")
    return EMPLOYEES_DB.pop(employee_id)

@app.post("/employees/{employee_id}/attendance")
def record_attendance(employee_id: int, date: str, status: str):
    if employee_id not in EMPLOYEES_DB:
        raise HTTPException(status_code=404, detail="لم يتم العثور على الموظف")
    EMPLOYEES_DB[employee_id].attendance.append({"date": date, "status": status})
    return {"message": "تم تسجيل الحضور بنجاح"}

@app.post("/employees/{employee_id}/evaluations")
def record_evaluation(employee_id: int, date: str, rating: float, comments: str):
    if employee_id not in EMPLOYEES_DB:
        raise HTTPException(status_code=404, detail="لم يتم العثور على الموظف")
    EMPLOYEES_DB[employee_id].evaluations.append({"date": date, "rating": rating, "comments": comments})
    return {"message": "تم تسجيل التقييم بنجاح"}

@app.post("/employees/{employee_id}/penalties")
def record_penalty(employee_id: int, date: str, reason: str, amount: float):
    if employee_id not in EMPLOYEES_DB:
        raise HTTPException(status_code=404, detail="لم يتم العثور على الموظف")
    EMPLOYEES_DB[employee_id].penalties.append({"date": date, "reason": reason, "amount": amount})
    return {"message": "تم تسجيل العقوبة بنجاح"}

@app.post("/employees/{employee_id}/rewards")
def record_reward(employee_id: int, date: str, reason: str, amount: float):
    if employee_id not in EMPLOYEES_DB:
        raise HTTPException(status_code=404, detail="لم يتم العثور على الموظف")
    EMPLOYEES_DB[employee_id].rewards.append({"date": date, "reason": reason, "amount": amount})
    return {"message": "تم تسجيل المكافأة بنجاح"}

from fastapi.responses import FileResponse

@app.get("/")
async def read_index():
    return FileResponse('frontend/index.html')
