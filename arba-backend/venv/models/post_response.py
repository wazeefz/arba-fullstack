from pydantic import BaseModel
from models.user import User  

class PostResponse(BaseModel):
    post_id: str
    user_email: str
    image: str
    caption: str
