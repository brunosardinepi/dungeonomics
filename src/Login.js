import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Col, Container, Form, Row } from 'react-bootstrap';

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
        localStorage.setItem('dungeonomicsLastResourceId', null);
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

  useEffect(() => {
    const usernameInput = document.getElementById("username");
    usernameInput.focus();
  }, []);

  return (
    <>
      <Container className="h-100">
        <Row className="h-100 justify-content-center align-items-center">
          <Col xs={10} md={6} lg={4} className="text-center">
            <img
              alt="Dungeonomics logo"
              className="mb-3"
              src="/logo_nav.svg"
            />
            <Form>
              <Form.Control
                className="form-control-dark mb-2"
                id="username"
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
              <div className="d-grid mt-3">
                <Button
                  className="fw-bold text-uppercase"
                  onClick={handleSubmit}
                  size="sm"
                  variant="danger"
                >
                  Log in
                </Button>
              </div>
            </Form>
          </Col>
        </Row>
      </Container>
    </>
  );
}
