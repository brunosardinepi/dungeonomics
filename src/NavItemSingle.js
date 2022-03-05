import React from "react";
import { NavLink } from "react-router-dom";
import { Button } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

export default class NavItemSingle extends React.Component{
  render() {
    return (
      <>
        <li className="mb-1">
          <NavLink to={this.props.link}>
            <Button
              className="btn-toggle align-items-center"
              variant=""
            >
              <FontAwesomeIcon
                icon={this.props.icon}
                className="me-2"
                fixedWidth
              />
              {this.props.text}
            </Button>
          </NavLink>
        </li>
      </>
    );
  }
}
