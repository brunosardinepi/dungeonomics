import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Col, Form, Row } from 'react-bootstrap';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [shouldRedirect, setShouldRedirect] = useState(false);

  const handleUsernameChange = (event) => setUsername(event.target.value);
  const handlePasswordChange = (event) => setPassword(event.target.value);

  function handleSubmit() {
    try {
      fetch('http://garrett.dungeonomics.com:8000/api/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password
        }),
      })
      .then(response => response.json())
      .then(data => {
        localStorage.setItem('dungeonomicsAccessToken', data.access);
        localStorage.setItem('dungeonomicsRefreshToken', data.refresh);
      })
      .then(() => {
        setShouldRedirect(true);
      });
    } catch (error) {
      throw error;
    }
  }

  const navigate = useNavigate();

  useEffect(() => {
    if (shouldRedirect === true) {
      navigate('/dashboard');
    }
  });

  return (
    <div>
      <h2>Login</h2>
      <Form>
        <Form.Control
          className="form-control-dark"
          name="username"
          onChange={handleUsernameChange}
          placeholder="Username"
          size="sm"
          type="text"
        />
        <Form.Control
          className="form-control-dark"
          name="password"
          onChange={handlePasswordChange}
          placeholder="Password"
          size="sm"
          type="Password"
        />
        <Button onClick={handleSubmit}>
          Login
        </Button>
      </Form>
    </div>
  );
}
