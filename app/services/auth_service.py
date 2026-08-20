from app.supabase.client import get_supabase_client
from fastapi import Response
supabase=get_supabase_client()
def user_signup(user):
    email=user.email
    password=str(user.password)
    response=supabase.auth.sign_up(
       { "email":email,
        "password":password,
    }

    )
    

    if response:
        
        return response.user
    
    
def user_login(user,response:Response):
    email=user.email
    password=str(user.password)
    auth_response=supabase.auth.sign_in_with_password({
        "email":email,
        "password":password,
    })
    print(f"signin response:{auth_response}")
    response.set_cookie(
        key="access_token",
        value=response.session.access_token,
        httponly=True,
        secure=False,
        max_age=3600

    )
    response.set_cookie(
        key="refresh_token",
        value=response.session.refresh_token,
        httponly=True,
        secure=False,
        max_age=30*24*3600

    )
    return response.user
    

