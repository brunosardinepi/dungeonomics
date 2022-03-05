import React, { useState } from "react";
import {
  Button,
  Col,
  Form,
  Modal,
  OverlayTrigger,
  Row,
  Tooltip,
} from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faQuestionCircle } from '@fortawesome/free-solid-svg-icons';
import apiRequest from "./apiRequest";
import { Typeahead } from 'react-bootstrap-typeahead';
import 'react-bootstrap-typeahead/css/Typeahead.css';
import 'react-bootstrap-typeahead/css/Typeahead.bs5.css';
import { resourceNameSuggestionOptions } from './resourceNameSuggestionOptions.js';

export default function CreateResourceAttributeModal(props) {
  const [name, setName] = useState('');
  const [value, setValue] = useState('');
  const handleTypeaheadChange = event => setName(event);
  const handleValueChange = event => setValue(event.target.value);

  function createResourceAttribute() {
    console.log('name', name);
    console.log('value', value)
    console.log('props.parent', props.parent);
    apiRequest(
      "POST",
      "http://garrett.dungeonomics.com:8000/resources/create/",
      {
        'name': name,
        'content': value,
        'parent': props.parent.id
      },
    )
      .then(data => {
        console.log(data);

        // Add the new resource attribute to the resource children list.
        let newResourceChildren = [...props.resourceChildren, data];
        console.log('newResourceChildren', newResourceChildren);
        newResourceChildren.sort((a, b) => (a.name.toLowerCase() > b.name.toLowerCase()) ? 1 : -1);
        props.handleSetResourceChildren(newResourceChildren);

        // Hide the modal.
        props.handleClose();
      });
  }

  function onShow() {
    const resourceNameInput = document.getElementById('resourceName');
    resourceNameInput.focus();
  }

  function handleModalKeyPress(event) {
    // Save/create the new resource when the user hits Enter.
    if (event.charCode === 13) {
      createResourceAttribute();
    }
  }

  const closeModalTooltip = (props) => (
    <Tooltip {...props}>
      <p className="mb-0">Close this modal without saving the resource.</p>
    </Tooltip>
  );

  const resourceParentTooltip = (props) => (
    <Tooltip {...props}>
      <p>If this resource belongs by itself and is not related to a resource you've already created, leave the Resource Parent blank.</p>
      <p className="mb-0">If this resource is an attribute or subset of an existing resource you've created, set that previously created resource as the Resource Parent.</p>
    </Tooltip>
  );

  const resourceParentList = props.resources.map((x) =>
    <option
      value={x.id}
      key={x.id}
    >
      {x.name}
    </option>
  );

  return (
    <>
      <Modal
        show={props.show}
        onShow={onShow}
        onHide={props.handleClose}
      >
        <Modal.Header closeButton>
          <Modal.Title>Create a new resource attribute</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group as={Row} className="mb-3" controlId="resourceParent">
            <Form.Label column="sm" sm={4}>
              <OverlayTrigger
                placement="bottom"
                overlay={resourceParentTooltip}
                className="me-1"
              >
                <Button variant="link" className="p-0 me-1">
                  <FontAwesomeIcon icon={faQuestionCircle} fixedWidth />
                </Button>
              </OverlayTrigger>
              <span className="align-middle">Resource parent</span>
            </Form.Label>
            <Col sm={8}>
              <Form.Select
                className="form-control-dark"
                size="sm"
                defaultValue={props.parent.id}
              >
                <option value={0}>---</option>
                {resourceParentList}
              </Form.Select>
            </Col>
          </Form.Group>
          <Form.Group as={Row} className="mb-3" controlId="resourceName">
            <Form.Label column="sm" sm={2}>
              Name
            </Form.Label>
            <Col sm={10}>
              <Typeahead
                id="resource-name-suggestion-dropdown"
                placeholder="Resource name (e.g., Strength)"
                minLength={1}
                highlightOnlyResult={true}
                options={resourceNameSuggestionOptions}
                size="sm"
                onChange={(selected) => setName(selected[0])}
                onInputChange={handleTypeaheadChange}
                inputProps={{
                  className: 'form-control form-control-dark',
                  id: 'resourceName',
                }}
              />
            </Col>
          </Form.Group>
          <Form.Group
            as={Row}
            className="mb-3"
            controlId="resourceValue"
          >
            <Form.Label column="sm" sm={2}>
              Value
            </Form.Label>
            <Col sm={10}>
              <Form.Control
                size="sm"
                type="text"
                placeholder="Resource value (e.g., 18)"
                className="form-control-dark"
                onChange={handleValueChange}
                onKeyPress={handleModalKeyPress}
              />
            </Col>
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <OverlayTrigger
            placement="bottom"
            overlay={closeModalTooltip}
          >
            <Button size="sm" variant="secondary" onClick={props.handleClose}>
              Close
            </Button>
          </OverlayTrigger>
          <Button
            id="modalSubmit"
            className="ms-auto"
            size="sm"
            variant="primary"
            onClick={createResourceAttribute}
          >
            Create
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
