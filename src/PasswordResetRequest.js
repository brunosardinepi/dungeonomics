import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Alert, Button, Col, Container, Form, Row } from 'react-bootstrap';

export default function Login() {
  const [email, setEmail] = useState('');
  const [shouldRedirectToSignup, setShouldRedirectToSignup] = useState(false);
  const [shouldRedirectToLogin, setShouldRedirectToLogin] = useState(false);
  const [shouldRedirectToPasswordResetAction, setShouldRedirectToPasswordResetAction] = useState(false);

  const handleEmailChange = (event) => setEmail(event.target.value);

  function handleSubmit() {
    try {
      fetch('http://garrett.dungeonomics.com:8000/app/password-reset/request/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email
        }),
      })
      .then(response => response.json())
      .then((data) => {
        setShouldRedirectToPasswordResetAction(true);
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
    if (shouldRedirectToSignup === true) {
      navigate('/signup');
    } else if (shouldRedirectToLogin === true) {
      navigate('/login');
    } else if (shouldRedirectToPasswordResetAction === true) {
      navigate('/password-reset/action');
    }
  });

  useEffect(() => {
    const emailInput = document.getElementById("email");
    emailInput.focus();
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
                When you click "send password reset code," we'll email you a
                password reset code and redirect you to the password reset form.
                Paste your password reset code from your email into the form and
                enter a new password. When finished, we'll redirect you to sign in
                with your new password.
              </p>
            </Alert>
            <Form>
              <Form.Control
                className="form-control-dark mb-2"
                id="email"
                name="email"
                onChange={handleEmailChange}
                onKeyPress={handleKeyPress}
                placeholder="Email"
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
                  Send password reset code
                </Button>
              </div>
              <div className="d-grid">
                <Button
                  onClick={() => setShouldRedirectToPasswordResetAction(true)}
                  variant="link"
                >
                  I have a password reset code
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
