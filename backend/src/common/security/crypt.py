import bcrypt
from src.core import config

def hash_password(password: str) -> str:
    """
    Hash a plain password using bcrypt.
    
    Returns:
        hashed password as string
    """
    salt = bcrypt.gensalt(rounds=config.bcrypt_salt_rounds)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")
