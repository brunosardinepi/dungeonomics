import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  Button,
  Col,
  Form,
  OverlayTrigger,
  Row,
  Tooltip,
} from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faBars,
  faPlus,
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
import CreateResourceModal from './CreateResourceModal';
import CreateResourceAttributeModal from './CreateResourceAttributeModal';

export default function Dashboard() {
  const [showCreateResourceModal, setShowCreateResourceModal] = useState(false);
  const handleCreateResourceModalClose = () => setShowCreateResourceModal(false);
  const [showCreateResourceAttributeModal, setShowCreateResourceAttributeModal] = useState(false);
  const handleCreateResourceAttributeModalClose = () => setShowCreateResourceAttributeModal(false);
  const [editorState, setEditorState] = useState(EditorState.createEmpty());
  const [resources, setResources] = useState([]);
  const [resource, setResource] = useState({});
  const [resourceChildren, setResourceChildren] = useState([]);
  const [filteredResources, setFilteredResources] = useState([]);
  const editorRef = useRef(null);
  const [mentionOpen, setMentionOpen] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [editorReadOnly, setEditorReadOnly] = useState(true);
  const [editButtonText, setEditButtonText] = useState('Edit');
  const [resourceGroups, setResourceGroups] = useState([]);
  const handleSetEditButtonText = (data) => setEditButtonText(data);
  const handleSetEditorReadOnly = (data) => setEditorReadOnly(data);
  const handleSetResource = (data) => setResource(data);
  const handleSetResourceChildren = (data) => setResourceChildren(data);
  const handleSetResources = (data) => setResources(data);
  const handleSetFilteredResources = (data) => setFilteredResources(data);

  const { MentionSuggestions, plugins } = useMemo(() => {
    const mentionPlugin = createMentionPlugin({
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
        return x.name.toLowerCase().includes(query);
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
      setTimeout(() => { editorRef.current.focus() }, 500);
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
        parseInt(data) === 200 ? highlightEditor('success') : highlightEditor('danger');
      });

    // Set the last save time.
    localStorage.setItem('dungeonomicsLastSaveTime', Date.now());
  }

  function deleteResource() {
    if (
      window.confirm("Are you sure you want to delete this? It can't be undone.")
    ) {
      apiRequest(
        'DELETE',
        `http://garrett.dungeonomics.com:8000/resources/${resource.id}/delete/`,
        {},
      )
        .then(() => {
          // Remove the resource from our resource list.
          const newResources = resources.filter((x) => x.id !== parseInt(resource.id));
          setResources(newResources);
          setFilteredResources(newResources);
          // Set the new active resource to be the first in our list.
          setResource(newResources[0]);
          // Set localStorage resource.
          localStorage.setItem('dungeonomicsLastResourceId', newResources[0].id);
        });
    };
  }

/*
  function createResource() {
    const name = document.getElementById('resourceName').value;
    let parent = document.getElementById('resourceParent').value;
    parent === "0" ? parent = '' : parent = parseInt(parent);
    const content = document.getElementById('resourceChildContent').value;
    const action = document.getElementById('modalSubmit').innerHTML;
    const tags = document.getElementById('resourceTags').value;

    let requestMethod = "POST";
    let requestUrl = "http://garrett.dungeonomics.com:8000/resources/create/";
    if (action === 'Update') {
      requestMethod = "PUT";
      if (editResource === true) {
        requestUrl = `http://garrett.dungeonomics.com:8000/resources/${resource.id}/update/`;
      } else {
        requestUrl = `http://garrett.dungeonomics.com:8000/resources/${resourceChild.id}/update/`;
      }
    }

    apiRequest(
      requestMethod,
      requestUrl,
      {
        'name': name,
        'parent': parent,
        'content': content,
        'tags': tags
      },
    )
      .then(data => {
        if (parent === '') {
          // Set the current resource to the newly created one.
          setResource(data);

          if (editResource === true) {
            // Update the resources list with the newly updated object.
            let newResources = resources.filter((x) => x.id !== parseInt(data.id));
            newResources = [...newResources, data];
            newResources.sort((a, b) => (a.name.toLowerCase() > b.name.toLowerCase()) ? 1 : -1);
            setResources(newResources);
            setFilteredResources(newResources);
          } else {
            let newResources = [...resources, data];
            newResources.sort((a, b) => (a.name.toLowerCase() > b.name.toLowerCase()) ? 1 : -1);

            // Add the new resource to the resources list in a non-mutative way.
            setResources(newResources);

            // Reset the filtered resources and use the newly created resources list.
            setFilteredResources(newResources);

            // Update the editor for the new resource so we're ready to edit it.
            updateEditorContent(data);

            // Reset the resourceChildren to blank.
            setResourceChildren([]);

            // Set the localStorage last resource ID to the newly created resource.
            localStorage.setItem('dungeonomicsLastResourceId', data.id);

            // Set the editor to "edit" mode.
            setEditorReadOnly(false);
            setEditButtonText('Done');
          }
        } else if (requestMethod === "PUT") {
          // Update the resourceChildren list with the newly updated object.
          let newResourceChildren = resourceChildren.filter((x) => x.id !== parseInt(data.id));
          newResourceChildren = [...newResourceChildren, data];
          newResourceChildren.sort((a, b) => (a.name.toLowerCase() > b.name.toLowerCase()) ? 1 : -1);
          setResourceChildren(newResourceChildren);
        } else {
          const newResourceChildren = [...resourceChildren, data];
          newResourceChildren.sort((a, b) => (a.name.toLowerCase() > b.name.toLowerCase()) ? 1 : -1);
          setResourceChildren(newResourceChildren);
        }
        // Hide the modal.
        setShowCreateResourceModal(false);

        // After the resource is created, set the focus to the editor.
        setTimeout(() => { editorRef.current.focus() }, 500);
      })
      .then(() => {
        apiRequest('GET', 'http://garrett.dungeonomics.com:8000/resources/groups/', {})
          .then(data => {
            setResourceGroups(data);
          })
      });
  }
*/

  function showResourceChildContentRow(show) {
    const resourceChildContentRow = document.getElementById('resourceChildContentRow');
    if (show === true) {
      resourceChildContentRow.classList.remove('d-none');
    } else {
      resourceChildContentRow.classList.add('d-none');
    }
  }

  function handleCreateResourceModalShow(event) {
    setShowCreateResourceModal(true);
    event.currentTarget.blur();
  }

  function handleCreateResourceAttributeModalShow(event) {
    setShowCreateResourceAttributeModal(true);
    event.currentTarget.blur();
  }

  function getResourceFromId(id) {
    return resources.find((x) => x.id === parseInt(id));
  }

  function getResourceTagNames(resource) {
    const resourceTagNames = resource.groups.map(x => x.name);
    console.log('resourceTagNames', resourceTagNames);
    return resourceTagNames.join(', ');
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

  function getResourceChildren(resource) {
    apiRequest(
      'GET',
      `http://garrett.dungeonomics.com:8000/resources/${resource.id}/children/`,
      {}
    )
      .then(data => {
        setResourceChildren(data);
      })
  }

  function onResourceClick(event) {
    const resource = getResourceFromId(event.target.getAttribute('data-id'));
    setResource(resource);
    localStorage.setItem('dungeonomicsLastResourceId', resource.id);
    updateEditorContent(resource);
    getResourceChildren(resource);
  }

  function toggleResources() {
    const resourceListRow = document.getElementById('resource-list-row');
    const resourceListParentContainer = document.getElementById('resource-list-parent-container');
    resourceListRow.classList.toggle('d-none');
    resourceListParentContainer.classList.toggle('h-50');
    resourceListParentContainer.classList.toggle('h-lg-100');
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

  const resourceChildrenList = resourceChildren.map((x) =>
    <Row key={x.id}>
      <Col xs="auto">
        <Button
          className="p-0"
          variant="link"
          onClick={handleCreateResourceModalShow}
          data-child={x.id}
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

  const createResourceTooltip = (props) => (
    <Tooltip {...props}>
      <p>Create a new resource.</p>
      <p className="mb-0">Resources can be <span className="fw-bold">campaigns</span>, <span className="fw-bold">monsters</span>, <span className="fw-bold">PCs</span>, <span className="fw-bold">NPCs</span>, <span className="fw-bold">items</span>, <span className="fw-bold">spells</span>, <span className="fw-bold">maps</span>, or anything else you need to track.</p>
    </Tooltip>
  );

  const createResourceChildTooltip = (props) => (
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
      <p className="mb-0">Click to edit {resource.name}</p>
    </Tooltip>
  );

  const draftEditorEditButtonTooltip = (props) => (
    <Tooltip {...props}>
      <p className="mb-0">Click to enable editing for {resource.name}'s content in the editor below.</p>
    </Tooltip>
  );

  const draftEditorSaveButtonTooltip = (props) => (
    <Tooltip {...props}>
      <p className="mb-0">Click to save {resource.name}'s content in the editor below.</p>
    </Tooltip>
  );

  const hideResourcesTooltip = (props) => (
    <Tooltip {...props}>
      <p>Hide or show the resource list.</p>
      <p className="mb-0">Useful on mobile when the resource list is taking up too much of your screen.</p>
    </Tooltip>
  );

  useEffect(() => {
    apiRequest('GET', 'http://garrett.dungeonomics.com:8000/resources/', {})
      .then(data => {
        setResources(data);
        setFilteredResources(data);

        // Get the last object in localStorage.
        const lastResourceId = localStorage.getItem('dungeonomicsLastResourceId');
        let lastResource = null;
        if (lastResourceId !== null) {
          lastResource = data.find((x) => x.id === parseInt(lastResourceId));
        }
        if (data.length > 0 && typeof lastResource === 'undefined') {
          lastResource = data[0];
        }
        setResource(lastResource);
        updateEditorContent(lastResource);
        getResourceChildren(lastResource);
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
                  onClick={handleCreateResourceModalShow}
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
                  onClick={handleCreateResourceModalShow}
                  data-resource={resource.id}
                >
                  {resource.name}
                </Button>
              </OverlayTrigger>
            </Col>
            <Col xs="auto">
              <OverlayTrigger
                placement="bottom"
                overlay={createResourceChildTooltip}
              >
                <Button
                  size="sm"
                  variant="dark"
                  data-parent={resource.id}
                  onClick={handleCreateResourceAttributeModalShow}
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
                  {resourceChildrenList}
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
                      <span className="fw-bold">B</span>old
                    </Button>
                    <Button
                      onClick={_onItalicClick}
                      variant="dark"
                    >
                      <span className="fw-bold">I</span>talic
                    </Button>
                    <Button
                      onClick={_onUnderlineClick}
                      variant="dark"
                    >
                      <span className="fw-bold">U</span>nderline
                    </Button>
                    <Button
                      onClick={_onCodeClick}
                      variant="dark"
                    >
                      <span className="fw-bold">C</span>ode
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

              <CreateResourceModal
                focusEditor={focusEditor}
                handleClose={handleCreateResourceModalClose}
                handleSetEditButtonText={handleSetEditButtonText}
                handleSetEditorReadOnly={handleSetEditorReadOnly}
                handleSetFilteredResources={handleSetFilteredResources}
                handleSetResource={handleSetResource}
                handleSetResourceChildren={handleSetResourceChildren}
                handleSetResources={handleSetResources}
                resources={resources}
                show={showCreateResourceModal}
                updateEditorContent={updateEditorContent}
              />

              <CreateResourceAttributeModal
                handleClose={handleCreateResourceAttributeModalClose}
                handleSetResourceChildren={handleSetResourceChildren}
                resources={resources}
                resourceChildren={resourceChildren}
                parent={resource}
                show={showCreateResourceAttributeModal}
              />

            </Col>
          </Row>
        </Col>
      </Row>
    </>
  );
}
