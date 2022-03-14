import React from "react";
import { Col, Row } from 'react-bootstrap';

export default class Home extends React.Component {
  render() {
    return (
      <Row className="mt-3">
        <Col className="mb-3 mb-lg-0">
          <h2>November 22, 2019</h2>
          <p>Our main developer had a baby and life has been crazy. Some people have asked so just to be clear: even though we aren't updating Dungeonomics as much as in the past, we're still leaving the site up and it will remain free to use.</p>
          <p>Today's updates include a ton of back-end security updates. We also added a search bar above the left-hand contents list on most assets so that you can search for items instead of scrolling through a long list of things.</p>
          <p>Always feel free to send us an email at <a href="mailto:dungeonomics@gmail.com" className="fw-bold">dungeonomics@gmail.com</a> or come talk to us on <a href="https://twitter.com/dungeonomics" className="fw-bold">Twitter</a> or <a href="https://www.reddit.com/r/dungeonomics/" className="fw-bold">Reddit</a>.</p>
        </Col>
      </Row>
    );
  }
}
