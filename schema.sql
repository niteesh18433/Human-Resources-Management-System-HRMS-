CREATE DATABASE hrms_db;

USE hrms_db;

CREATE TABLE employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INT,
    role_id INT,
    hire_date DATE NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id),
    INDEX (department_id),
    INDEX (role_id)
);

CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE roles (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE performance_reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    review_date DATE NOT NULL,
    review_text TEXT NOT NULL,
    reviewer_id INT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    INDEX (employee_id),
    INDEX (reviewer_id)
);
