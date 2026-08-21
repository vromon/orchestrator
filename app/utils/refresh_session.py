from fastapi import Response
from app.utils.set_cookies import set_cookies
from app.supabase.client import get_supabase_client
supabase=get_supabase_client()
def get_refresh_session(response:Response,refresh_token):

    refresh_response=supabase.auth.refresh_session(refresh_token)

    new_access_token=refresh_response.session.access_token

    new_refresh_token=refresh_response.session.refresh_token

    set_cookies(response,new_access_token,new_refresh_token)
   
    return {"access_token":new_access_token,"refresh_token":new_refresh_token}