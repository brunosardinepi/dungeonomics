import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Alert, Button, Col, Container, Form, Row } from 'react-bootstrap';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [passwordReset, setPasswordReset] = useState('');
  const [shouldRedirect, setShouldRedirect] = useState(false);
  const [shouldRedirectToSignup, setShouldRedirectToSignup] = useState(false);
  const [shouldRedirectToLogin, setShouldRedirectToLogin] = useState(false);
  const [shouldRedirectToPasswordResetRequest, setShouldRedirectToPasswordResetRequest] = useState(false);
  const [showAlert, setShowAlert] = useState(false);
  const [alertText, setAlertText] = useState('');

  const handleUsernameChange = (event) => setUsername(event.target.value);
  const handlePasswordChange = (event) => setPassword(event.target.value);
  const handlePasswordConfirmChange = (event) => setPasswordConfirm(event.target.value);
  const handlePasswordResetChange = (event) => setPasswordReset(event.target.value);

  function handleSubmit() {
    try {
      fetch(`http://garrett.dungeonomics.com:8000/app/password-reset/${passwordReset}/`, {
        method: 'PATCH',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          username: username,
          password: password,
          passwordConfirm: passwordConfirm,
          passwordReset: passwordReset
        }),
      })
      .then((response) => {
        if (response.status === 200) {
          setShouldRedirect(true);
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
    } else if (shouldRedirectToSignup === true) {
      navigate('/signup');
    } else if (shouldRedirectToLogin === true) {
      navigate('/login');
    } else if (shouldRedirectToPasswordResetRequest === true) {
      navigate('/password-reset/request');
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
            <Alert variant="info">
              <p className="mb-0">
                We should have emailed you a password reset code.
                Paste your password reset code from your email into the form and
                enter a new password. When finished, we'll redirect you to sign in
                with your new password.
              </p>
            </Alert>
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
                placeholder="Email"
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
              <Form.Control
                className="form-control-dark mt-2"
                name="passwordReset"
                onChange={handlePasswordResetChange}
                onKeyPress={handleKeyPress}
                placeholder="Paste your password reset code"
                size="sm"
                type="text"
              />
              <div className="d-grid mt-3 mb-1">
                <Button
                  className="fw-bold text-uppercase"
                  onClick={handleSubmit}
                  size="sm"
                  variant="danger"
                >
                  Reset password
                </Button>
              </div>
              <div className="d-grid">
                <Button
                  onClick={() => setShouldRedirectToPasswordResetRequest(true)}
                  variant="link"
                >
                  I need a password reset code
                </Button>
              </div>
              <div className="d-grid">
                <Button
                  onClick={() => setShouldRedirectToLogin(true)}
                  variant="link"
                >
                  Go to login
                </Button>
              </div>
              <div className="d-grid">
                <Button
                  onClick={() => setShouldRedirectToSignup(true)}
                  variant="link"
                >
                  Go to signup
                </Button>
              </div>
            </Form>
          </Col>
        </Row>
      </Container>
    </>
  );
}
