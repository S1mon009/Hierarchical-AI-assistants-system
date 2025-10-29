from fastapi import APIRouter, Form, HTTPException
from pydantic import ValidationError
from src.schemas.auth import RegisterForm

router = APIRouter()

@router.post("/register")
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    repeat_password: str = Form(...)
):
    try:
        # Tworzymy model Pydantic z danych z form-data
        form = RegisterForm(
            username=username,
            email=email,
            password=password,
            repeat_password=repeat_password
        )
        # Tutaj dodajesz logikę zapisu do bazy
        return {"message": "Registration successful"}
    except ValidationError as e:
        errors = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        raise HTTPException(status_code=400, detail=errors) from e
