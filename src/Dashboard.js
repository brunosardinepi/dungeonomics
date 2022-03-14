import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
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
import {
  faBars,
  faPlus,
  faQuestionCircle,
  faTrashAlt,
} from '@fortawesome/free-solid-svg-icons';
import apiRequest from "./apiRequest";
import {
  convertFromRaw,
  convertToRaw,
  EditorState,
  RichUtils,
} from 'draft-js';
import 'draft-js/dist/Draft.css';
import '@draft-js-plugins/mention/lib/plugin.css';
import Editor from '@draft-js-plugins/editor';
import createMentionPlugin, { defaultSuggestionsFilter } from '@draft-js-plugins/mention';
import mentionsStyles from './MentionsStyles.module.css';
import { Typeahead } from 'react-bootstrap-typeahead';
import 'react-bootstrap-typeahead/css/Typeahead.css';
import 'react-bootstrap-typeahead/css/Typeahead.bs5.css';
import { resourceNameSuggestionOptions } from './resourceNameSuggestionOptions.js';

export default function Dashboard() {
  const [showModal, setShowModal] = useState(false);
  const handleModalClose = () => setShowModal(false);
  const [modalButtonText, setModalButtonText] = useState("Create");
  const [modalAction, setModalAction] = useState(false);
  const [showDeleteResourceButton, setShowDeleteResourceButton] = useState(false);
  const [showResourceParentSelect, setShowResourceParentSelect] = useState(false);
  const [showResourceValueInput, setShowResourceValueInput] = useState(false);
  const [showResourceTagsInput, setShowResourceTagsInput] = useState(true);

  const [showMentionModal, setShowMentionModal] = useState(false);
  const handleMentionModalClose = () => setShowMentionModal(false);
  const [mentionResource, setMentionResource] = useState({'id': 0, 'name': ''});
  const [mentionResourceAttributes, setMentionResourceAttributes] = useState([]);

  const editorRef = useRef(null);
  const [editorState, setEditorState] = useState(EditorState.createEmpty());
  const [editorReadOnly, setEditorReadOnly] = useState(true);
  const [editButtonText, setEditButtonText] = useState('Edit');

  const [resource, setResource] = useState({'id': 0, 'name': ''});
  const [resources, setResources] = useState([]);
  const [resourceName, setResourceName] = useState('');
  const [resourceTags, setResourceTags] = useState('');
  const [resourceGroups, setResourceGroups] = useState([]);
  const [filteredResources, setFilteredResources] = useState([]);

  const [resourceAttribute, setResourceAttribute] = useState({});
  const [resourceAttributes, setResourceAttributes] = useState([]);
  const [resourceAttributeValue, setResourceAttributeValue] = useState('');

  const [mentionOpen, setMentionOpen] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const { MentionSuggestions, plugins } = useMemo(() => {
    const mentionPlugin = createMentionPlugin({
      mentionComponent: mentionProps => {
        return (
          <span
            className={mentionProps.className}
            onClick={() => {
              setMentionResource(mentionProps.children);
              getMentionResourceAttributes(mentionProps.mention);
              setShowMentionModal(true);
            }}
          >
            {mentionProps.children}
          </span>
        );
      },
      entityMutability: 'IMMUTABLE',
      theme: mentionsStyles,
      supportWhitespace: true,
    });
    const { MentionSuggestions } = mentionPlugin;
    const plugins = [mentionPlugin];
    return { plugins, MentionSuggestions };
  }, []);

  const onOpenChange = useCallback((_open) => {
    setMentionOpen(_open);
  }, []);

  const onSearchChange = useCallback(({ value }) => {
    setSuggestions(defaultSuggestionsFilter(value, resources));
  }, [resources]);

  function onResourceFilterChange(event) {
    let query = event.target.value.toLowerCase();
    let newFilteredResources = [];
    if (query.startsWith('#') && query.length > 1) {
      query = query.substring(1);
      // Look for items in resource groups whose name matches the query.
      // Get all resource groups whose name matches the current query.
      const filteredResourceGroups = resourceGroups.filter((x) => {
        return x.name.toLowerCase().startsWith(query);
      });
      // For each filtered group, get the corresponding resources (once) and
      // add to the filtered resources list.
      filteredResourceGroups.forEach((group) => {
        group['resources'].forEach((resourceId) => {
          // Get the resource from the resource id.
          const resourceFromId = getResourceFromId(resourceId);
          if (
            typeof resourceFromId !== 'undefined' &&
            !newFilteredResources.includes(resourceFromId)
          ) {
            newFilteredResources.push(resourceFromId);
          }
        });
      });
    } else {
      // Normal query
      newFilteredResources = resources.filter((resource) => {
          return resource.name.toLowerCase().includes(query);
      });
    }
    setFilteredResources(newFilteredResources);
  }

  function onEditorChange(editorState) {
    setEditorState(editorState);
  }

  function handleKeyCommand(command, editorState) {
    const newState = RichUtils.handleKeyCommand(editorState, command);
    if (newState) {
      onEditorChange(newState);
      return 'handled';
    }
    return 'not-handled';
  }

  function _onBoldClick() {
    onEditorChange(RichUtils.toggleInlineStyle(editorState, 'BOLD'));
  };

  function _onItalicClick() {
    onEditorChange(RichUtils.toggleInlineStyle(editorState, 'ITALIC'));
  };

  function _onUnderlineClick() {
    onEditorChange(RichUtils.toggleInlineStyle(editorState, 'UNDERLINE'));
  };

  function _onCodeClick() {
    onEditorChange(RichUtils.toggleInlineStyle(editorState, 'CODE'));
  };

  function highlightEditor(style) {
    let editor = document.getElementsByClassName('DraftEditor-root');
    let className = `highlight-${style}`
    if (typeof editor !== 'undefined') {
      editor = editor[0];
      editor.classList.toggle(className);
      setTimeout(() => { editor.classList.toggle(className) }, 2000);
    };
  }

  function editContent() {
    const newReadOnlyState = !editorReadOnly;
    setEditorReadOnly(newReadOnlyState);
    if (newReadOnlyState === true) {
      setEditButtonText('Edit');
    } else {
      setEditButtonText('Done');
      focusEditor();
    }
  }

  function focusEditor() {
    setTimeout(() => { editorRef.current.focus() }, 500);
  }

  function saveContent() {
    // Check when the last save occurred and only allow another save if it's been at
    // least 10 seconds between saves.
    const lastSaveTime = localStorage.getItem('dungeonomicsLastSaveTime');
    const timeBetweenSaves = (Date.now() - lastSaveTime) / 1000;

    if (timeBetweenSaves < 10) { return; };

    const contentState = editorState.getCurrentContent();
    const content = JSON.stringify(convertToRaw(contentState));

    apiRequest(
      'PATCH',
      `http://garrett.dungeonomics.com:8000/resources/${resource.id}/update/`,
      {'content': content},
    )
      .then(data => {
        if ("id" in data) {
          highlightEditor('success');

          let newResources = resources.filter((x) => x.id !== parseInt(data.id));
          newResources = [...newResources, data];
          newResources.sort((a, b) => (a.name.toLowerCase() > b.name.toLowerCase()) ? 1 : -1);
          setResource(data);
          setResources(newResources);
          setFilteredResources(newResources);
        } else {
          highlightEditor('danger');
        }
      });

    // Set the last save time.
    localStorage.setItem('dungeonomicsLastSaveTime', Date.now());
  }

  function handleModalShowCreateResource(event) {
    setModalAction("createResource");
    setShowDeleteResourceButton(false);
    setShowResourceParentSelect(false);
    setShowResourceValueInput(false);
    setShowResourceTagsInput(true);
    setModalButtonText("Create");
    setShowModal(true);
    event.currentTarget.blur();
  }

  function handleModalShowCreateResourceAttribute(event) {
    setModalAction("createResourceAttribute");
    setShowDeleteResourceButton(false);
    setShowResourceParentSelect(true);
    setShowResourceValueInput(true);
    setShowResourceTagsInput(false);
    setModalButtonText("Create");
    setShowModal(true);
    event.currentTarget.blur();
  }

  function handleModalShowEditResource(event) {
    setModalAction("editResource");
    setShowDeleteResourceButton(false);
    setResourceName(resource.name);
    setResourceTags(resource.tags);
    setShowResourceParentSelect(false);
    setShowResourceValueInput(false);
    setShowResourceTagsInput(true);
    setModalButtonText("Save");
    setShowModal(true);
    event.currentTarget.blur();
  }

  function handleModalShowEditResourceAttribute(event) {
    const resourceAttribute = getResourceAttributeFromId(event.target.getAttribute('data-id'));
    setResourceAttribute(resourceAttribute);
    setResourceName(resourceAttribute.name);

    setModalAction("editResourceAttribute");
    setShowDeleteResourceButton(true);
    setShowResourceParentSelect(true);
    setShowResourceValueInput(true);
    setShowResourceTagsInput(false);
    setModalButtonText("Save");
    setShowModal(true);
    event.currentTarget.blur();
  }

  function onModalEntered() {
    let input;
    if (modalAction === "editResourceAttribute") {
      input = document.getElementById("resourceValue");
    } else {
      input = document.getElementById("resourceName");
    }

    if (typeof input !== "undefined" && input !== null) {
      input.focus();
    }
  }

  function saveResource() {
    if (resource.id === 1 && modalAction !== "createResource") { return; }
    let method, url, postData;
    if (modalAction === "createResource") {
      method = "POST";
      url = "http://garrett.dungeonomics.com:8000/resources/create/";
      postData = {
        'name': resourceName,
        'tags': resourceTags
      };
    } else if (modalAction === "createResourceAttribute") {
      method = "POST";
      url = "http://garrett.dungeonomics.com:8000/resources/create/";
      postData = {
        'name': resourceName,
        'content': resourceAttributeValue,
        'parent': resource.id
      };
    } else if (modalAction === "editResource") {
      method = "PUT";
      url = `http://garrett.dungeonomics.com:8000/resources/${resource.id}/update/`;
      postData = {
        'name': resourceName,
        'tags': resourceTags
      };
    } else if (modalAction === "editResourceAttribute") {
      method = "PUT";
      url = `http://garrett.dungeonomics.com:8000/resources/${resourceAttribute.id}/update/`;
      postData = {
        'name': resourceName,
        'content': resourceAttributeValue,
        'parent': resource.id
      };
    }

    apiRequest(method, url, postData)
      .then(data => {
        if (modalAction === "createResource") {
          // Set the current resource to the newly created one.
          setResource(data);

          // Add the new resource to the resources list in a non-mutative way.
          let newResources = [...resources, data];
          newResources.sort((a, b) => (a.name.toLowerCase() > b.name.toLowerCase()) ? 1 : -1);

          // If this is the user's first resource, remove the PK 1 resource example.
          const exampleResourceCheck = newResources.filter((x) => x.id === 1);
          if (exampleResourceCheck.length > 0) {
            // Remove the PK 1 resource example.
            newResources = newResources.filter((x) => x.id !== 1);
          }

          setResources(newResources);
          setFilteredResources(newResources);

          // Update the editor for the new resource so we're ready to edit it.
          updateEditorContent(data);

          // Reset the resourceAttributes to blank.
          setResourceAttributes([]);

          // Set the localStorage last resource ID to the newly created resource.
          localStorage.setItem('dungeonomicsLastResourceId', data.id);

          // Set the editor to "edit" mode.
          setEditorReadOnly(false);
          setEditButtonText('Done');

          // Move focus to the editor.
          focusEditor();
        } else if (modalAction === "createResourceAttribute") {
          // Add the new resource attribute to the resource attributes list.
          let newResourceAttributes = [...resourceAttributes, data];
          newResourceAttributes.sort((a, b) => (a.name.toLowerCase() > b.name.toLowerCase()) ? 1 : -1);
          setResourceAttributes(newResourceAttributes);
          setResourceAttribute(data);
        } else if (modalAction === "editResource") {
          // Remove the resource and then add its replacement.
          let newResources = resources.filter((x) => x.id !== parseInt(data.id));
          newResources = [...newResources, data];
          newResources.sort((a, b) => (a.name.toLowerCase() > b.name.toLowerCase()) ? 1 : -1);
          setResource(data);
          setResources(newResources);
          setFilteredResources(newResources);
        } else if (modalAction === "editResourceAttribute") {
          // Remove the resource attribute and then add its replacement.
          let newResourceAttributes = resourceAttributes.filter((x) => x.id !== parseInt(data.id));
          newResourceAttributes = [...newResourceAttributes, data];
          newResourceAttributes.sort((a, b) => (a.name.toLowerCase() > b.name.toLowerCase()) ? 1 : -1);
          setResourceAttributes(newResourceAttributes);
        }

        // Hide the modal.
        setShowModal(false);
      })
      .then(() => {
        apiRequest('GET', 'http://garrett.dungeonomics.com:8000/resources/groups/', {})
          .then(data => {
            setResourceGroups(data);
          })
      });
  }

  function deleteResource() {
    if (window.confirm("Are you sure you want to delete this? It can't be undone.")) {
      apiRequest(
        'DELETE',
        `http://garrett.dungeonomics.com:8000/resources/${resource.id}/delete/`,
        {}
      )
        .then(() => {
          // Remove the resource from our resource list.
          const newResources = resources.filter((x) => x.id !== parseInt(resource.id));
          setResources(newResources);
          setFilteredResources(newResources);
          if (newResources.length > 0) {
            getResourceAttributes(newResources[0]);
            // Set the new active resource to be the first in our list.
            setResource(newResources[0]);
            updateEditorContent(newResources[0]);
            // Set localStorage resource.
            localStorage.setItem('dungeonomicsLastResourceId', newResources[0].id);
          } else {
            // The user has no resources left, so get the example resource.
            apiRequest('GET', 'http://garrett.dungeonomics.com:8000/resources/', {})
              .then(data => {
                setResources(data);
                setFilteredResources(data);
                setResource(data[0]);
                updateEditorContent(data[0]);
                getResourceAttributes(data[0]);
                localStorage.setItem('dungeonomicsLastResourceId', data[0].id);
              });
          }

          // Hide the modal.
          setShowModal(false);
        });
    }
  }

  function deleteResourceAttribute() {
    if (window.confirm("Are you sure you want to delete this? It can't be undone.")) {
      apiRequest(
        'DELETE',
        `http://garrett.dungeonomics.com:8000/resources/${resourceAttribute.id}/delete/`,
        {},
      )
        .then(() => {
          // Remove the resource attribute from our resource attributes list.
          const newResourceAttributes = resourceAttributes.filter((x) => x.id !== parseInt(resourceAttribute.id));
          if (newResourceAttributes.length > 0) {
            setResourceAttributes(newResourceAttributes);
          } else {
            setResourceAttributes([]);
          }

          // Hide the modal.
          setShowModal(false);
        });
    }
  }

  function getResourceFromId(id) {
    return resources.find((x) => x.id === parseInt(id));
  }

  function getResourceAttributeFromId(id) {
    return resourceAttributes.find((x) => x.id === parseInt(id));
  }

  function updateEditorContent(resource) {
    if (resource.content === '') {
      setEditorState(EditorState.createEmpty());
    } else {
      setEditorState(
        EditorState.createWithContent(convertFromRaw(JSON.parse(resource.content)))
      );
    }
  }

  function getResourceAttributes(resource) {
    apiRequest(
      'GET',
      `http://garrett.dungeonomics.com:8000/resources/${resource.id}/attributes/`,
      {}
    )
      .then(data => {
        setResourceAttributes(data);
      })
  }

  function getMentionResourceAttributes(resource) {
    apiRequest(
      'GET',
      `http://garrett.dungeonomics.com:8000/resources/${resource.id}/attributes/`,
      {}
    )
      .then(data => {
        setMentionResourceAttributes(data);
      })
  }

  function onResourceClick(event) {
    const resource = getResourceFromId(event.target.getAttribute('data-id'));
    setResource(resource);
    localStorage.setItem('dungeonomicsLastResourceId', resource.id);
    updateEditorContent(resource);
    getResourceAttributes(resource);
  }

  function toggleResources() {
    const resourceListRow = document.getElementById('resource-list-row');
    const resourceListParentContainer = document.getElementById('resource-list-parent-container');
    resourceListRow.classList.toggle('d-none');
    resourceListParentContainer.classList.toggle('h-50');
    resourceListParentContainer.classList.toggle('h-lg-100');
  }

  function handleModalKeyPress(event) {
    // Save/create the new resource when the user hits Enter.
    if (event.charCode === 13) {
      saveResource();
    }
  }

  function ResourceNameInput() {
    if (["createResourceAttribute", "editResourceAttribute"].includes(modalAction)) {
      return (
        <Form.Group as={Row} className="mb-3" controlId="resourceName">
          <Form.Label column="sm" sm={2}>
            Name
          </Form.Label>
          <Col sm={10}>
            <Typeahead
              defaultInputValue={modalAction === "editResourceAttribute" ? resourceAttribute.name : ''}
              id="resource-name-suggestion-dropdown"
              placeholder="Resource name (e.g., Strength)"
              minLength={1}
              highlightOnlyResult={true}
              options={resourceNameSuggestionOptions}
              size="sm"
              onChange={(selected) => {
                setResourceName(selected[0]);
                const resourceValueInput = document.getElementById("resourceValue");
                resourceValueInput.focus();
              }}
              onInputChange={(e) => setResourceName(e)}
              inputProps={{
                className: 'form-control form-control-dark',
                id: 'resourceName',
              }}
            />
          </Col>
        </Form.Group>
      );
    } else {
      function getDefaultValue() {
        if (modalAction === "editResource") {
          return resource.name;
        } else if (modalAction === "editResourceAttribute") {
          return resourceAttribute.name;
        } else {
          return '';
        }
      }
      return (
        <Form.Group as={Row} className="mb-3" controlId="resourceName">
          <Form.Label column="sm" sm={2}>
            Name
          </Form.Label>
          <Col sm={10}>
            <Form.Control
              className="form-control-dark"
              defaultValue={getDefaultValue()}
              onChange={e => setResourceName(e.target.value)}
              onKeyPress={handleModalKeyPress}
              placeholder="Resource name (e.g., My Epic Campaign)"
              size="sm"
              type="text"
            />
          </Col>
        </Form.Group>
      );
    }
  }

  const resourceList = filteredResources.map((x) =>
    <Button
      className={`d-block p-0 ${x.id === resource.id ? 'btn-active' : ''}`}
      variant="link"
      key={x.id}
      data-id={x.id}
      onClick={onResourceClick}
    >
      {x.name}
    </Button>
  );

  const resourceParentList = resources.map((x) =>
    <option value={x.id} key={x.id}>
      {x.name}
    </option>
  );

  const resourceAttributesList = resourceAttributes.map((x) =>
    <Row key={x.id}>
      <Col xs="auto">
        <Button
          className="p-0"
          variant="link"
          onClick={handleModalShowEditResourceAttribute}
          data-id={x.id}
        >
          {x.name}
        </Button>
      </Col>
      <Col xs="auto">
        <span className="align-middle">
          {x.content}
        </span>
      </Col>
    </Row>
  );

  const mentionResourceAttributesList = mentionResourceAttributes.map((x) =>
    <Row key={x.id}>
      <Col xs="auto">
        <span className="p-0 fw-bold text-white">
          {x.name}
        </span>
      </Col>
      <Col xs="auto">
        {x.content}
      </Col>
    </Row>
  );

  const createResourceTooltip = (props) => (
    <Tooltip {...props}>
      <p>Create a new resource.</p>
      <p className="mb-0">Resources can be <span className="fw-bold">campaigns</span>, <span className="fw-bold">monsters</span>, <span className="fw-bold">PCs</span>, <span className="fw-bold">NPCs</span>, <span className="fw-bold">items</span>, <span className="fw-bold">spells</span>, <span className="fw-bold">maps</span>, or anything else you need to track.</p>
    </Tooltip>
  );

  const createResourceAttributeTooltip = (props) => (
    <Tooltip {...props}>
      <p>Create a new attribute for this resource.</p>
      <p className="mb-0">Resource attributes can be things like <span className="fw-bold">strength</span>, <span className="fw-bold">dexterity</span>, <span className="fw-bold">charisma</span>, <span className="fw-bold">height</span>, <span className="fw-bold">race</span>, <span className="fw-bold">damage vulnerabilities</span>, <span className="fw-bold">size</span>, or anything else related to this resource.</p>
    </Tooltip>
  );

  const deleteResourceTooltip = (props) => (
    <Tooltip {...props}>
      <p>Delete this resource.</p>
      <p className="mb-0">You'll be asked to confirm this before it gets deleted.</p>
    </Tooltip>
  );

  const editResourceTooltip = (props) => (
    <Tooltip {...props}>
      <p className="mb-0">Click to edit this resource.</p>
    </Tooltip>
  );

  const draftEditorEditButtonTooltip = (props) => (
    <Tooltip {...props}>
      <p className="mb-0">Click to enable editing for this resource's content in the editor below.</p>
    </Tooltip>
  );

  const draftEditorSaveButtonTooltip = (props) => (
    <Tooltip {...props}>
      <p className="mb-0">Click to save this resources's content in the editor below.</p>
    </Tooltip>
  );

  const hideResourcesTooltip = (props) => (
    <Tooltip {...props}>
      <p>Hide or show the resource list.</p>
      <p className="mb-0">Useful on mobile when the resource list is taking up too much of your screen.</p>
    </Tooltip>
  );

  const resourceParentTooltip = (props) => (
    <Tooltip {...props}>
      <p>If this resource belongs by itself and is not related to a resource you've already created, leave the Resource Parent blank.</p>
      <p className="mb-0">If this resource is an attribute or subset of an existing resource you've created, set that previously created resource as the Resource Parent.</p>
    </Tooltip>
  );

  const resourceTagsTooltip = (props) => (
    <Tooltip {...props}>
      <p>Tags are used to group similar resources. You can search for tags in the resource list search bar by typing a hashtag and then the tag name. Example: #monsters</p>
      <p className="mb-0">Enter the tag names without hashtags. If you have multiple tags to apply, separate them with a comma. New tags will be created, existing tags will have this resource added to them.</p>
    </Tooltip>
  );

  const closeModalTooltip = (props) => (
    <Tooltip {...props}>
      <p className="mb-0">Close this modal without saving the resource.</p>
    </Tooltip>
  );

  function ModalTitle() {
    if (modalAction === "createResource") {
      return "Create a new resource";
    } else if (modalAction === "editResource") {
      return "Edit resource";
    } else if (modalAction === "createResourceAttribute") {
      return "Create a new resource attribute";
    } else if (modalAction === "editResourceAttribute") {
      return "Edit resource attribute";
    } else {
      return null;
    }
  }

  useEffect(() => {
    apiRequest('GET', 'http://garrett.dungeonomics.com:8000/resources/', {})
      .then(data => {
        setResources(data);
        setFilteredResources(data);

        // Get the last object in localStorage.
        const lastResourceId = localStorage.getItem('dungeonomicsLastResourceId');
        let lastResource;
        if (lastResourceId !== 'null') {
          lastResource = data.find((x) => x.id === parseInt(lastResourceId));
        } else if (data.length > 0) {
          lastResource = data[0];
        } else {
          lastResource = null;
        }
        setResource(lastResource);
        updateEditorContent(lastResource);
        getResourceAttributes(lastResource);
      })

    apiRequest('GET', 'http://garrett.dungeonomics.com:8000/resources/groups/', {})
      .then(data => {
        setResourceGroups(data);
      })
  }, []);

  return (
    <>
      <Row className="h-100">
        <Col lg="3" id="resource-list-parent-container" className="h-50 h-lg-100">
          <Row>
            <Col>
              <Form.Control
                id="resourceFilterInput"
                type="text"
                size="sm"
                className="form-control-dark"
                placeholder="Search"
                onChange={onResourceFilterChange}
              />
            </Col>
            <Col xs="auto">
              <OverlayTrigger
                placement="bottom"
                overlay={createResourceTooltip}
              >
                <Button
                  className="me-1"
                  size="sm"
                  variant="dark"
                  onClick={handleModalShowCreateResource}
                >
                  <FontAwesomeIcon icon={faPlus} fixedWidth />
                </Button>
              </OverlayTrigger>
              <OverlayTrigger
                placement="bottom"
                overlay={hideResourcesTooltip}
              >
                <Button
                  id="toggle-resources-button"
                  size="sm"
                  variant="dark"
                  onClick={toggleResources}
                >
                  <FontAwesomeIcon icon={faBars} fixedWidth />
                </Button>
              </OverlayTrigger>
            </Col>
          </Row>
          <Row className="pt-3" id="resource-list-row">
            <Col className="h-100 overflow-auto scrollbar-dark">
              {resourceList}
            </Col>
          </Row>
        </Col>
        <Col lg="9" className="h-100 py-3 py-lg-0">
          <Row>
            <Col>
              <OverlayTrigger
                placement="bottom"
                overlay={editResourceTooltip}
              >
                <Button
                  className="btn-h4"
                  variant="link"
                  onClick={handleModalShowEditResource}
                >
                  {resource.name}
                </Button>
              </OverlayTrigger>
            </Col>
            <Col xs="auto">
              <OverlayTrigger
                placement="bottom"
                overlay={createResourceAttributeTooltip}
              >
                <Button
                  size="sm"
                  variant="dark"
                  onClick={handleModalShowCreateResourceAttribute}
                  className="me-1"
                >
                  <FontAwesomeIcon icon={faPlus} fixedWidth />
                </Button>
              </OverlayTrigger>
              <OverlayTrigger
                placement="bottom"
                overlay={deleteResourceTooltip}
              >
                <Button
                  size="sm"
                  variant="dark"
                  onClick={deleteResource}
                >
                  <FontAwesomeIcon icon={faTrashAlt} fixedWidth />
                </Button>
              </OverlayTrigger>
            </Col>
          </Row>
          <Row id="resource-content-row" className="overflow-auto scrollbar-dark">
            <Col>
              <Row className="mb-3">
                <Col>
                  {resourceAttributesList}
                </Col>
              </Row>
              <Row>
                <Col xs="auto">
                  <div className="DraftEditor-toolbar">
                    <OverlayTrigger
                      placement="bottom"
                      overlay={draftEditorEditButtonTooltip}
                    >
                      <Button
                        onClick={editContent}
                        variant="dark"
                      >
                        {editButtonText}
                      </Button>
                    </OverlayTrigger>
                    <OverlayTrigger
                      placement="bottom"
                      overlay={draftEditorSaveButtonTooltip}
                    >
                      <Button
                        onClick={saveContent}
                        variant="dark"
                      >
                        Save
                      </Button>
                    </OverlayTrigger>
                  </div>
                </Col>
                <Col xs="auto">
                  <div className="DraftEditor-toolbar">
                    <Button
                      onClick={_onBoldClick}
                      variant="dark"
                    >
                      <span className="fw-bold text-decoration-underline">B</span>old
                    </Button>
                    <Button
                      onClick={_onItalicClick}
                      variant="dark"
                    >
                      <span className="fw-bold text-decoration-underline">I</span>talic
                    </Button>
                    <Button
                      onClick={_onUnderlineClick}
                      variant="dark"
                    >
                      <span className="fw-bold text-decoration-underline">U</span>nderline
                    </Button>
                    <Button
                      onClick={_onCodeClick}
                      variant="dark"
                    >
                      Code
                    </Button>
                  </div>
                </Col>
              </Row>
              <Row>
                <Col>
                  <div
                    className='editor'
                    onClick={() => {
                      editorRef.current.focus();
                    }}
                  >
                    <Editor
                      editorKey={'editor'}
                      editorState={editorState}
                      handleKeyCommand={handleKeyCommand}
                      onChange={setEditorState}
                      readOnly={editorReadOnly}
                      plugins={plugins}
                      ref={editorRef}
                    />
                    <MentionSuggestions
                      open={mentionOpen}
                      onOpenChange={onOpenChange}
                      onSearchChange={onSearchChange}
                      suggestions={suggestions}
                      onAddMention={() => {
                        // get the mention object selected
                      }}
                    />
                  </div>
                </Col>
              </Row>

              <Modal
                show={showModal}
                onEntered={onModalEntered}
                onHide={handleModalClose}
              >
                <Modal.Header closeButton>
                  <Modal.Title><ModalTitle /></Modal.Title>
                </Modal.Header>
                <Modal.Body>
                  <Form.Group
                    as={Row}
                    className={`mb-3 ${showResourceParentSelect === true ? '' : 'd-none'}`}
                    controlId="resourceParent"
                  >
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
                        defaultValue={resource.id}
                      >
                        <option value={0}>---</option>
                        {resourceParentList}
                      </Form.Select>
                    </Col>
                  </Form.Group>
                  {ResourceNameInput()}
                  <Form.Group
                    as={Row}
                    className={`mb-3 ${showResourceValueInput === true ? '' : 'd-none'}`}
                    controlId="resourceValue"
                  >
                    <Form.Label column="sm" sm={2}>
                      Value
                    </Form.Label>
                    <Col sm={10}>
                      <Form.Control
                        defaultValue={modalAction === "editResourceAttribute" ? resourceAttribute.content : ''}
                        size="sm"
                        type="text"
                        placeholder="Resource value (e.g., 18)"
                        className="form-control-dark"
                        onChange={(e) => setResourceAttributeValue(e.target.value)}
                        onKeyPress={handleModalKeyPress}
                      />
                    </Col>
                  </Form.Group>
                  <Form.Group
                    as={Row}
                    className={`mb-3 ${showResourceTagsInput === true ? '' : 'd-none'}`}
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
                        className="form-control-dark"
                        defaultValue={modalAction === "editResource" ? resource.groups : ''}
                        onChange={e => setResourceTags(e.target.value)}
                        onKeyPress={handleModalKeyPress}
                        placeholder="Tags, separated by commas (e.g., campaign, new)"
                        size="sm"
                        type="text"
                      />
                    </Col>
                  </Form.Group>
                </Modal.Body>
                <Modal.Footer>
                  <OverlayTrigger
                    placement="bottom"
                    overlay={closeModalTooltip}
                  >
                    <Button size="sm" variant="secondary" onClick={handleModalClose}>
                      Close
                    </Button>
                  </OverlayTrigger>
                  <Button
                    onClick={deleteResourceAttribute}
                    className={showDeleteResourceButton === true ? '' : 'd-none'}
                    size="sm"
                    variant="danger"
                  >
                    Delete
                  </Button>
                  <Button
                    id="modalSubmit"
                    className="ms-auto"
                    size="sm"
                    variant="primary"
                    onClick={saveResource}
                  >
                    {modalButtonText}
                  </Button>
                </Modal.Footer>
              </Modal>

              <Modal
                show={showMentionModal}
                onHide={handleMentionModalClose}
              >
                <Modal.Header closeButton>
                  <Modal.Title>{mentionResource}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                  {mentionResourceAttributesList.length > 0 ? mentionResourceAttributesList : "This resource doesn't have any attributes yet."}
                </Modal.Body>
              </Modal>

            </Col>
          </Row>
        </Col>
      </Row>
    </>
  );
}
