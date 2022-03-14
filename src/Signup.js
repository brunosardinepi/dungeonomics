import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Alert, Button, Col, Container, Form, Row } from 'react-bootstrap';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [shouldRedirect, setShouldRedirect] = useState(false);
  const [showAlert, setShowAlert] = useState(false);
  const [alertText, setAlertText] = useState('');

  const handleUsernameChange = (event) => setUsername(event.target.value);
  const handlePasswordChange = (event) => setPassword(event.target.value);
  const handlePasswordConfirmChange = (event) => setPasswordConfirm(event.target.value);

  function handleSubmit() {
    try {
      fetch('http://garrett.dungeonomics.com:8000/signup/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          username: username,
          password: password,
          passwordConfirm: passwordConfirm
        }),
      })
      .then((response) => {
        if (response.status === 201) {
          setShouldRedirect(true);
        } else if (response.status === 499) {
          setAlertText("A user with that name already exists!");
          setShowAlert(true);
        } else {
          setAlertText("An unknown error has occurred. Please reach out to us if you need help.");
          setShowAlert(true);
        }
      });
    } catch (error) {
      throw error;
    }
  }

  function handleKeyPress(event) {
    if (event.charCode === 13) {
      handleSubmit();
    }
  }

  const navigate = useNavigate();

  useEffect(() => {
    if (shouldRedirect === true) {
      navigate('/login');
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
            <Alert variant="danger" show={showAlert}>
              {alertText}
            </Alert>
            <Form>
              <Form.Control
                className="form-control-dark mb-2"
                id="username"
                name="username"
                onChange={handleUsernameChange}
                onKeyPress={handleKeyPress}
                placeholder="Username"
                size="sm"
                type="text"
              />
              <Form.Control
                className="form-control-dark mb-2"
                name="password"
                onChange={handlePasswordChange}
                onKeyPress={handleKeyPress}
                placeholder="Password"
                size="sm"
                type="password"
              />
              <Form.Control
                className="form-control-dark"
                name="passwordConfirm"
                onChange={handlePasswordConfirmChange}
                onKeyPress={handleKeyPress}
                placeholder="Password (again)"
                size="sm"
                type="password"
              />
              <div className="d-grid mt-3">
                <Button
                  className="fw-bold text-uppercase"
                  onClick={handleSubmit}
                  size="sm"
                  variant="success"
                >
                  Sign up
                </Button>
              </div>
              <div className="d-grid mt-1">
                <Button
                  className="fw-bold text-uppercase"
                  onClick={() => setShouldRedirect(true)}
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
