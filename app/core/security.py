from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt

from app.core.config import settings


def create_access_token(
    subject: str,
    data: Dict[str, Any] | None = None,
    expires_minutes: int | None = None,
) -> str:
    """Generate a signed JWT token."""
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes or settings.JWT_EXPIRE_MINUTES)

    payload: Dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    if data:
        payload.update(data)

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
