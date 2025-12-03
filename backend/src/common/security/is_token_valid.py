import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime

def is_token_valid(token: str) -> bool:
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        exp = payload.get("exp")
        if exp is None:
            return False
        now = int(datetime.utcnow().timestamp())
        return exp > now
    except (ExpiredSignatureError, InvalidTokenError):
        return False
    except Exception:
        return False