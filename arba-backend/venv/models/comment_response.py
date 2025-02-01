from pydantic import BaseModel
from datetime import datetime

class CommentResponse(BaseModel):
    comment_id: str  # Unique comment ID
    user_email: str
    post_id: str
    text: str
    created_at: datetime


