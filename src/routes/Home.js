import React from "react";
import { Col, ListGroup, Row } from 'react-bootstrap';
import { Timeline } from 'react-twitter-widgets';
import apiRequest from "../apiRequest";

function FeatureList(props) {
  const features = props.features;
  const listItems = features.map(function(feature) {
    const hasUserVote = feature.has_user_vote ? 'list-group-item-success' : 'list-group-item-dark';
    const isNew = feature.new ? <span className="badge bg-danger me-1">New</span> : '';

    return (
      <ListGroup.Item
        key={feature.id}
        action
        href="/"
        className={hasUserVote + " d-flex justify-content-between align-items-center"}
      >
        <span>
          {isNew}
          {feature.description}
        </span>
        <span className="badge bg-dark rounded-pill ms-3">{feature.vote_count}</span>
      </ListGroup.Item>
    );
  });

  return (
    <ListGroup>
      {listItems}
    </ListGroup>
  );
}

export default class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      features: [],
    };
  }

  componentDidMount() {
    apiRequest('GET', 'http://garrett.dungeonomics.com:8000/features/', {})
      .then(data => {
        this.setState({
          features: data,
        });
      });
  }

  render() {
    return (
      <Row className="mt-3">
        <Col lg="8" className="mb-3 mb-lg-0">
          <h2>November 22, 2019</h2>
          <p>Our main developer had a baby and life has been crazy. Some people have asked so just to be clear: even though we aren't updating Dungeonomics as much as in the past, we're still leaving the site up and it will remain free to use.</p>
          <p>Today's updates include a ton of back-end security updates. We also added a search bar above the left-hand contents list on most assets so that you can search for items instead of scrolling through a long list of things.</p>
          <p>Always feel free to send us an email at <a href="mailto:dungeonomics@gmail.com" className="fw-bold">dungeonomics@gmail.com</a> or come talk to us on <a href="https://twitter.com/dungeonomics" className="fw-bold">Twitter</a> or <a href="https://www.reddit.com/r/dungeonomics/" className="fw-bold">Reddit</a>.</p>

          <h2 className="mt-5">Feature voting</h2>
          <p>Click on the features that you want to see added to the site. You can vote once on each feature, and can vote for as many features as you want. The total votes for each feature are to the right in the blue circle. Click again to remove your vote.</p>
          <p>These are all the requests you've sent us to be added. If you want to see your request on here, email us at <a className="alert-link" href="mailto:dungeonomics@gmail.com">dungeonomics@gmail.com</a> and we'll add it. Every week, we'll take the top requests and work on adding them to the site.</p>
          <FeatureList features={this.state.features} />
        </Col>
        <Col lg="4">
          <Timeline
            dataSource={{
              sourceType: 'profile',
              screenName: 'Dungeonomics'
            }}
            options={{
              tweetLimit: '5'
            }}
          />
        </Col>
      </Row>
    );
  }
}
