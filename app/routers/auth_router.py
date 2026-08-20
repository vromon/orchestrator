from fastapi import APIRouter
from app.services.auth_service import register_user
from app.schemas.auth_schema import UserRegister
auth_router=APIRouter(prefix="/auth")
@auth_router.post("/register")
def register(user:UserRegister):
    return register_user(user)