from app.supabase.client import get_supabase_client
from fastapi import Response
from app.utils.set_cookies import set_cookies
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

    set_cookies(response,auth_response.session.access_token,auth_response.session.refresh_token)
    
    return auth_response.user
    

