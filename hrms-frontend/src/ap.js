import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [employees, setEmployees] = useState([]);

  useEffect(() => {
    axios.get('/employees')
      .then(response => {
        setEmployees(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the employees!', error);
      });
  }, []);

  return (
    <div className="App">
      <h1>Employee List</h1>
      <ul>
        {employees.map(employee => (
          <li key={employee.email}>{employee.first_name} {employee.last_name}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
