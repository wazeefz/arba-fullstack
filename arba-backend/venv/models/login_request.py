from pydantic import BaseModel
from models.user import User 
from models.post import Post  

class LoginRequest(BaseModel):
    email: str
    password: str
