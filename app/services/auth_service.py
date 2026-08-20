from app.supabase.client import get_supabase_client
supabase=get_supabase_client()
def register_user(user):
    email=user.email
    password=user.password
    response=supabase.auth.sign_up(
       { "email":email,
        "password":password,
    }

    )
    

    if response:
        
        return response.user
    
    
