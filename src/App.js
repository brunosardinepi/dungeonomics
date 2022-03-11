import React from "react";
import { Helmet } from "react-helmet";
import { BrowserRouter, Link, Navigate, NavLink, Outlet, Route, Routes } from "react-router-dom";
import { Button, Container, Navbar, OverlayTrigger, Tooltip } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCogs, faDiceD20 } from '@fortawesome/free-solid-svg-icons';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';
import Dashboard from './Dashboard';
import Home from './routes/Home';
import Login from './Login';
import Signup from './Signup';

export default class App extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      logged_in: localStorage.getItem('dungeonomicsAccessToken') ? true : false
    };
  }

  componentDidMount() {
    if (!this.state.logged_in) {
      <Navigate to="/login" replace />
    }
  }

  render() {
    return (
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />} >
            <Route path="/" element={<Home />} />
            <Route path="dashboard" element={<Dashboard />} />
          </Route>
          <Route path="login" element={<Login />} />
          <Route path="signup" element={<Signup />} />
        </Routes>
      </BrowserRouter>
    );
  }
}

function Layout(props) {
  const dashboardTooltip = (props) => (
    <Tooltip {...props}>
      <p className="mb-0"><span className="fw-bold">Dashboard</span><br />The dashboard contains all of your resources.</p>
    </Tooltip>
  );

  const accountTooltip = (props) => (
    <Tooltip {...props}>
      <p className="mb-0"><span className="fw-bold">Account</span><br />Manage your account and view site information.</p>
    </Tooltip>
  );

  return (
    <>
      <Helmet>
        <meta charSet="utf-8" />
        <title>Dungeonomics</title>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossOrigin="anonymous"></script>
      </Helmet>

      <Navbar expand="md" bg="dark" variant="dark">
        <Container fluid>
          <Link
            to="/"
          >
            <img
              alt="Dungeonomics logo"
              src="/logo_nav.svg"
              className="align-text-top"
            />
          </Link>
          <Button
            className="navbar-toggler"
            data-bs-toggle="collapse"
            data-bs-target="#navbarCollapse"
            aria-controls="navbarCollapse"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </Button>
          <div className="collapse navbar-collapse" id="navbarCollapse">
            <ul className="navbar-nav ms-auto mb-2 mb-md-0">
              <OverlayTrigger
                placement="bottom"
                overlay={dashboardTooltip}
              >
                <li className="nav-item">
                  <NavLink to="dashboard" className="nav-link">
                    <FontAwesomeIcon
                      icon={faDiceD20}
                      fixedWidth
                    />
                    <span className="d-inline d-sm-none ms-2">Dashboard</span>
                  </NavLink>
                </li>
              </OverlayTrigger>
              <OverlayTrigger
                placement="bottom"
                overlay={accountTooltip}
              >
                <li className="nav-item">
                  <NavLink to="dashboard" className="nav-link">
                    <FontAwesomeIcon
                      icon={faCogs}
                      fixedWidth
                    />
                    <span className="d-inline d-sm-none ms-2">Account</span>
                  </NavLink>
                </li>
              </OverlayTrigger>
            </ul>
          </div>
        </Container>
      </Navbar>

      <main className="container-fluid py-3">
        <Outlet />
      </main>
    </>
  );
}
