from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class RegisterForm(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32)
    repeat_password: str = Field(..., min_length=8, max_length=32)

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str):
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character")
        return password

    @field_validator("repeat_password")
    @classmethod
    def passwords_match(cls, repeat_password: str, info):
        password = info.data.get("password")
        if password and repeat_password != password:
            raise ValueError("Passwords do not match")
        return repeat_password
