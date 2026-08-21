from app.supabase.client import get_supabase_client
from fastapi import Request,Response, HTTPException,status
from app.utils.refresh_session import get_refresh_session
supabase=get_supabase_client()

def verify_user(request:Request,response:Response):

    access_token=request.cookies.get("access_token")
    refresh_token=request.cookies.get("refresh_token")
    if access_token:
        try:
            user_info=supabase.auth.get_user(access_token)
            return user_info.user
        except Exception:
            pass

    
    if refresh_token:
        print(f"this is refresh token:{refresh_token}")
        try:
            new_tokens=get_refresh_session(response,refresh_token)
            user_info=supabase.auth.get_user(new_tokens["access_token"])
            return user_info.user
     
        except   Exception:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please log in again"

        )
    raise HTTPException(status_code=401, detail="Authentication required." )

    


