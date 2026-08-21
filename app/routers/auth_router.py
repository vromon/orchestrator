from fastapi import APIRouter,Response
from app.services.auth_service import user_signup
from app.services.auth_service import user_login
from app.schemas.auth_schema import UserSignup
from app.schemas.auth_schema import UserLogin
auth_router=APIRouter(prefix="/auth")
@auth_router.post("/register")
def register(user:UserSignup):
    return user_signup(user)
@auth_router.post("/login")
def login(user:UserLogin,response:Response):
    return user_login(user,response)