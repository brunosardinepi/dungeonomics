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

export default function CreateResourceModal(props) {
  const [name, setName] = useState('');
  const [tags, setTags] = useState('');
  const handleNameChange = event => setName(event.target.value);
  const handleTagChange = event => setTags(event.target.value);

  function createResource() {
    console.log('name', name);
    console.log('tags', tags);
    apiRequest(
      "POST",
      "http://garrett.dungeonomics.com:8000/resources/create/",
      {
        'name': name,
        'tags': tags
      },
    )
      .then(data => {
        console.log(data);
        // Set the current resource to the newly created one.
        props.handleSetResource(data);

        // Add the new resource to the resources list in a non-mutative way.
        let newResources = [...props.resources, data];
        console.log('newResources', newResources);
        newResources.sort((a, b) => (a.name.toLowerCase() > b.name.toLowerCase()) ? 1 : -1);
        props.handleSetResources(newResources);
        props.handleSetFilteredResources(newResources);

        // Update the editor for the new resource so we're ready to edit it.
        props.updateEditorContent(data);

        // Reset the resourceChildren to blank.
        props.handleSetResourceChildren([]);

        // Set the localStorage last resource ID to the newly created resource.
        localStorage.setItem('dungeonomicsLastResourceId', data.id);

        // Set the editor to "edit" mode.
        props.handleSetEditorReadOnly(false);
        props.handleSetEditButtonText('Done');

        // Hide the modal.
        props.handleClose();

        // Move focus to the editor.
        props.focusEditor();
      });
/*
      .then(() => {
        apiRequest('GET', 'http://garrett.dungeonomics.com:8000/resources/groups/', {})
          .then(data => {
            setResourceGroups(data);
          })
      });
*/
  }

  function onShow() {
    const resourceNameInput = document.getElementById('resourceName');
    resourceNameInput.focus();
  }

  function handleModalKeyPress(event) {
    // Save/create the new resource when the user hits Enter.
    if (event.charCode === 13) {
      createResource();
    }
  }

  const closeModalTooltip = (props) => (
    <Tooltip {...props}>
      <p className="mb-0">Close this modal without saving the resource.</p>
    </Tooltip>
  );

  const resourceTagsTooltip = (props) => (
    <Tooltip {...props}>
      <p>Tags are used to group similar resources. You can search for tags in the resource list search bar by typing a hashtag and then the tag name. Example: #monsters</p>
      <p className="mb-0">Enter the tag names without hashtags. If you have multiple tags to apply, separate them with a comma. New tags will be created, existing tags will have this resource added to them.</p>
    </Tooltip>
  );

  return (
    <>
      <Modal
        show={props.show}
        onShow={onShow}
        onHide={props.handleClose}
      >
        <Modal.Header closeButton>
          <Modal.Title>Create a new resource</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group as={Row} className="mb-3" controlId="resourceName">
            <Form.Label column="sm" sm={2}>
              Name
            </Form.Label>
            <Col sm={10}>
              <Form.Control
                size="sm"
                type="text"
                placeholder="Resource name (e.g., My Epic Campaign)"
                className="form-control-dark"
                onChange={handleNameChange}
                onKeyPress={handleModalKeyPress}
              />
            </Col>
          </Form.Group>
          <Form.Group
            as={Row}
            className="mb-3"
            controlId="resourceTags"
          >
            <Form.Label column="sm" sm={2}>
              <OverlayTrigger
                placement="bottom"
                overlay={resourceTagsTooltip}
                className="me-1"
              >
                <Button variant="link" className="p-0 me-1">
                  <FontAwesomeIcon icon={faQuestionCircle} fixedWidth />
                </Button>
              </OverlayTrigger>
              <span className="align-middle">Tags</span>
            </Form.Label>
            <Col sm={10}>
              <Form.Control
                size="sm"
                type="text"
                placeholder="Tags, separated by commas (e.g., campaign, new)"
                className="form-control-dark"
                onChange={handleTagChange}
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
            onClick={createResource}
          >
            Create
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
