"""JWT authentication utilities."""
from datetime import datetime, timedelta
from typing import Optional
import jwt
from pydantic import BaseModel


class TokenData(BaseModel):
    user_id: str
    email: Optional[str] = None
    scopes: list[str] = []


def create_token(data: TokenData, secret: str, algorithm: str = "HS256", expires_in: int = 30) -> str:
    """Create a signed JWT token."""
    payload = data.model_dump()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expires_in)
    payload["iat"] = datetime.utcnow()
    return jwt.encode(payload, secret, algorithm=algorithm)


def verify_token(token: str, secret: str, algorithm: str = "HS256") -> TokenData:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        return TokenData(**payload)
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {e}")
