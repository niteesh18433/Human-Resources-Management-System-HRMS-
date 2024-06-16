from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pymysql

app = FastAPI()

# Database Configuration
db = pymysql.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="hrms_db"
)

# Create Employee Table if it doesn't exist
with db.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INT PRIMARY KEY AUTO_INCREMENT,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            department_id INT,
            role_id INT,
            hire_date DATE NOT NULL
        )
    """)
    db.commit()

# Employee Model
class Employee(BaseModel):
    first_name: str
    last_name: str
    email: str
    department_id: int
    role_id: int
    hire_date: str

# API Endpoint to Add a New Employee
@app.post("/employees", response_model=Employee)
async def create_employee(employee: Employee):
    with db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO employees (first_name, last_name, email, department_id, role_id, hire_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (employee.first_name, employee.last_name, employee.email, employee.department_id, employee.role_id, employee.hire_date))
        db.commit()
        employee_id = cursor.lastrowid

    return {**employee.dict(), "employee_id": employee_id}

# API Endpoint to Get All Employees
@app.get("/employees", response_model=List[Employee])
async def read_employees():
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

    return employees

# API Endpoint to Get a Specific Employee by ID
@app.get("/employees/{employee_id}", response_model=Employee)
async def read_employee(employee_id: int):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
        employee = cursor.fetchone()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return employee
