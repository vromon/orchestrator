from fastapi import APIRouter,Request, Depends
from app.services.user_service import get_user_profile
from app.utils.verify_user import verify_user
user_router=APIRouter(prefix="/user")
@user_router.get("/profile")
def user_profile_router(request:Request,user=Depends(verify_user)):
    
    return  get_user_profile(request,user)
