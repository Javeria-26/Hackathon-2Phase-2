import pytest
from fastapi import status
from jose import jwt
from datetime import datetime, timedelta
from app.config import get_settings


@pytest.mark.asyncio
async def test_user_isolation(client, auth_token, test_user_id):
    """Test that users can only see their own todos."""
    # Create todo for user 1
    headers_user1 = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(
        "/todos",
        json={"title": "User 1 Todo"},
        headers=headers_user1
    )
    todo_id = response.json()["id"]

    # Create token for user 2
    settings = get_settings()
    payload = {
        "sub": "different-user-456",
        "email": "user2@example.com",
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token_user2 = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    headers_user2 = {"Authorization": f"Bearer {token_user2}"}

    # User 2 tries to access User 1's todo
    response = client.get(f"/todos/{todo_id}", headers=headers_user2)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # User 2 tries to update User 1's todo
    response = client.put(
        f"/todos/{todo_id}",
        json={"title": "Hacked"},
        headers=headers_user2
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # User 2 tries to delete User 1's todo
    response = client.delete(f"/todos/{todo_id}", headers=headers_user2)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Verify User 1's todo is still intact
    response = client.get(f"/todos/{todo_id}", headers=headers_user1)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "User 1 Todo"
