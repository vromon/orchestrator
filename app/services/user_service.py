from app.utils.verify_user import verify_user

def get_user_profile(request ,user):
    
    return {"id":user.id,"email":user.email}