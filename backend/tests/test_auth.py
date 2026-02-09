import pytest
from fastapi import status
from jose import jwt
from datetime import datetime, timedelta
from app.config import get_settings


def test_missing_token(client):
    """Test request without authentication token."""
    response = client.get("/todos")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_invalid_token(client):
    """Test request with invalid token."""
    headers = {"Authorization": "Bearer invalid-token"}
    response = client.get("/todos", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_expired_token(client, test_user_id):
    """Test request with expired token."""
    settings = get_settings()

    # Create expired token
    payload = {
        "sub": test_user_id,
        "exp": datetime.utcnow() - timedelta(hours=1)  # Expired 1 hour ago
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/todos", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_valid_token(client, auth_headers):
    """Test request with valid token."""
    response = client.get("/todos", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
