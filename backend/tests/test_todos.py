import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_todo(client, auth_headers):
    """Test creating a todo."""
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description"
    }

    response = client.post("/todos", json=todo_data, headers=auth_headers)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["description"] == todo_data["description"]
    assert data["completed"] is False
    assert "id" in data
    assert "user_id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_list_todos(client, auth_headers):
    """Test listing todos."""
    # Create a todo first
    client.post(
        "/todos",
        json={"title": "Test Todo", "description": "Test"},
        headers=auth_headers
    )

    # List todos
    response = client.get("/todos", headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_todo(client, auth_headers):
    """Test getting a specific todo."""
    # Create a todo first
    create_response = client.post(
        "/todos",
        json={"title": "Test Todo", "description": "Test"},
        headers=auth_headers
    )
    todo_id = create_response.json()["id"]

    # Get the todo
    response = client.get(f"/todos/{todo_id}", headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Test Todo"


@pytest.mark.asyncio
async def test_get_todo_not_found(client, auth_headers):
    """Test getting a non-existent todo."""
    response = client.get("/todos/non-existent-id", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_todo(client, auth_headers):
    """Test updating a todo."""
    # Create a todo first
    create_response = client.post(
        "/todos",
        json={"title": "Original Title", "description": "Original Description"},
        headers=auth_headers
    )
    todo_id = create_response.json()["id"]
    original_updated_at = create_response.json()["updated_at"]

    # Update the todo
    update_data = {
        "title": "Updated Title",
        "completed": True
    }
    response = client.put(f"/todos/{todo_id}", json=update_data, headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["completed"] is True
    assert data["updated_at"] != original_updated_at


@pytest.mark.asyncio
async def test_delete_todo(client, auth_headers):
    """Test deleting a todo."""
    # Create a todo first
    create_response = client.post(
        "/todos",
        json={"title": "To Delete", "description": "Will be deleted"},
        headers=auth_headers
    )
    todo_id = create_response.json()["id"]

    # Delete the todo
    response = client.delete(f"/todos/{todo_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify it's deleted
    get_response = client.get(f"/todos/{todo_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_validation_empty_title(client, auth_headers):
    """Test validation for empty title."""
    response = client.post(
        "/todos",
        json={"title": "", "description": "Test"},
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_validation_title_too_long(client, auth_headers):
    """Test validation for title exceeding max length."""
    response = client.post(
        "/todos",
        json={"title": "x" * 201, "description": "Test"},
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_filter_by_completed(client, auth_headers):
    """Test filtering todos by completion status."""
    # Create completed and incomplete todos
    client.post("/todos", json={"title": "Incomplete Todo"}, headers=auth_headers)
    create_response = client.post("/todos", json={"title": "Complete Todo"}, headers=auth_headers)
    todo_id = create_response.json()["id"]

    # Mark one as completed
    client.put(f"/todos/{todo_id}", json={"completed": True}, headers=auth_headers)

    # Filter by completed
    response = client.get("/todos?completed=true", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(todo["completed"] is True for todo in data)


@pytest.mark.asyncio
async def test_filter_by_incomplete(client, auth_headers):
    """Test filtering todos by incomplete status."""
    # Create todos
    client.post("/todos", json={"title": "Incomplete Todo"}, headers=auth_headers)

    # Filter by incomplete
    response = client.get("/todos?completed=false", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(todo["completed"] is False for todo in data)


@pytest.mark.asyncio
async def test_search_by_title(client, auth_headers):
    """Test searching todos by title."""
    # Create todos with different titles
    client.post("/todos", json={"title": "Meeting with team"}, headers=auth_headers)
    client.post("/todos", json={"title": "Buy groceries"}, headers=auth_headers)

    # Search for "meeting"
    response = client.get("/todos?search=meeting", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any("meeting" in todo["title"].lower() for todo in data)


@pytest.mark.asyncio
async def test_search_by_description(client, auth_headers):
    """Test searching todos by description."""
    # Create todo with specific description
    client.post("/todos", json={"title": "Task", "description": "Important meeting notes"}, headers=auth_headers)

    # Search in description
    response = client.get("/todos?search=meeting", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0


@pytest.mark.asyncio
async def test_combined_filters(client, auth_headers):
    """Test combining multiple filters."""
    # Create todos
    create_response = client.post("/todos", json={"title": "Work task", "description": "Important"}, headers=auth_headers)
    todo_id = create_response.json()["id"]
    client.put(f"/todos/{todo_id}", json={"completed": True}, headers=auth_headers)

    # Search with combined filters
    response = client.get("/todos?completed=true&search=work", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(todo["completed"] is True for todo in data)
    assert all("work" in todo["title"].lower() or "work" in todo["description"].lower() for todo in data)
