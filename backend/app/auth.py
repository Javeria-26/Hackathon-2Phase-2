from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
from app.config import get_settings


security = HTTPBearer()


class TokenData:
    """Parsed JWT token data."""
    def __init__(self, user_id: str, email: str):
        self.user_id = user_id
        self.email = email


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    Verify JWT token and extract user information.

    Raises:
        HTTPException: 401 if token is invalid, expired, or missing required claims
    """
    settings = get_settings()
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode and verify JWT token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        # Extract user ID from token claims (check both 'sub' and 'userId' for Better Auth compatibility)
        user_id: Optional[str] = payload.get("sub") or payload.get("userId")
        email: Optional[str] = payload.get("email")

        if user_id is None:
            raise credentials_exception

        return TokenData(user_id=user_id, email=email or "")

    except JWTError as e:
        # Log the error for debugging (don't expose to client)
        print(f"JWT verification failed: {str(e)}")
        raise credentials_exception


async def get_current_user_id(token_data: TokenData = Depends(verify_token)) -> str:
    """
    Extract user ID from verified token.
    Use this as a dependency in route handlers.
    """
    return token_data.user_id
