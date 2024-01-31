from datetime import datetime, timedelta
from typing import Optional, Any
import jwt

try:
    from settings import SECRET_KEY
except ImportError:
    raise ImportError("Couldn't import SECRET_KEY from settings.py")

JWT_ALGORITHM = "HS256"


def encode_jwt(data: dict, secret: str = SECRET_KEY, lifetime_seconds: Optional[int] = None,
               algorithm: str = JWT_ALGORITHM) -> str:
    payload = data.copy()
    if lifetime_seconds:
        expire = datetime.now() + timedelta(seconds=lifetime_seconds)
        payload["exp"] = expire
    return jwt.encode(payload=payload, key=secret, algorithm=algorithm)


def decode_jwt(token: str, secret: str = SECRET_KEY, algorithm: str = JWT_ALGORITHM) -> dict[str, Any]:
    return jwt.decode(token, secret, algorithms=algorithm)
