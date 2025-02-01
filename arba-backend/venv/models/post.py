from pydantic import BaseModel

class Post(BaseModel):
    post_id: str
    image: str  
    caption: str
