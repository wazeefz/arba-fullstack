from pydantic import BaseModel

class Comment(BaseModel):
    post_id: str     
    text: str  
