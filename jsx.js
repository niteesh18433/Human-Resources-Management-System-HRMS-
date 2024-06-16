import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
    const [employees, setEmployees] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/employees')
            .then(response => setEmployees(response.data))
            .catch(error => console.error('Error fetching employees:', error));
    }, []);

    return (
        <div>
            <h1>Employee List</h1>
            <ul>
                {employees.map(employee => (
                    <li key={employee.employee_id}>
                        {employee.first_name} {employee.last_name} - {employee.email}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;
