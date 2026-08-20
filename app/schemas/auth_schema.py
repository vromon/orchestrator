from pydantic import BaseModel
from pydantic import EmailStr

class UserRegister(BaseModel):
    email:EmailStr
    password:str