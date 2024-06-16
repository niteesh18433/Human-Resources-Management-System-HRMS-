from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class Employee(Base):
    __tablename__ = 'employees'
    employee_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    hire_date = Column(Date)

class Department(Base):
    __tablename__ = 'departments'
    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String, index=True)

class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, index=True)

class PerformanceReview(Base):
    __tablename__ = 'performance_reviews'
    review_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.employee_id'))
    reviewer_id = Column(Integer, ForeignKey('employees.employee_id'))
    review_date = Column(Date)
    performance_score = Column(Integer)
    comments = Column(String)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# CRUD operations for employees
@app.post("/employees/")
def create_employee(employee: Employee, db: Session = Depends(get_db)):
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@app.get("/employees/")
def read_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return employees

@app.get("/employees/{employee_id}")
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in employee.dict().items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return {"message": "Employee deleted successfully"}

# Similar CRUD operations for departments, roles, and performance_reviews can be added here

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
