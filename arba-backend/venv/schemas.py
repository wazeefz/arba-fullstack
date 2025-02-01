from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

# User Pydantic Model
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# Add this to your schemas.py
class UserLogin(BaseModel):
    email: str
    password: str


# Post Pydantic Model
class PostCreate(BaseModel):
    caption: str
    image: Optional[bytes] = None  # Image is optional and handled as binary data (bytes)
    user_email: str

class PostResponse(BaseModel):
    post_id: UUID  # Use UUID instead of str
    caption: str
    image: Optional[bytes] = None  # Image stored as binary data (bytes)
    user_email: str

    class Config:
        orm_mode = True

# Comment Pydantic Model
class CommentCreate(BaseModel):
    post_id: UUID
    text: str

class CommentResponse(BaseModel):
    comment_id: UUID  # Use UUID instead of str
    post_id: UUID
    user_email: str
    text: str
    created_at: datetime  # Use datetime instead of str

    class Config:
        orm_mode = True
