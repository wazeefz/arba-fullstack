from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from typing import List
from pydantic import BaseModel

from models import Comment, Post, User
from schemas import CommentCreate, CommentResponse
from database import get_db
import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

# OAuth2PasswordBearer is used to extract the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Helper function to decode and verify the JWT token
def verify_token(token: str):
    try:
        # Decode the JWT token using the SECRET_KEY and ALGORITHM
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Ensure the token is not expired
        if payload["exp"] < datetime.utcnow().timestamp():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        # Return the email from the token (we'll use it to identify the user)
        return payload["sub"]
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or expired token")

router = APIRouter()

# Route to create a comment on a post
@router.post("/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Verify the token to get the user email
    user_email = verify_token(token)

    # Check if the user exists
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Check if the post exists
    post = db.query(Post).filter(Post.post_id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # Create a new Comment instance
    new_comment = Comment(
        comment_id=str(uuid4()),
        user_email=user_email,
        post_id=comment.post_id,
        text=comment.text,
        created_at=datetime.utcnow()
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return CommentResponse(
        comment_id=new_comment.comment_id,
        user_email=new_comment.user_email,
        post_id=new_comment.post_id,
        text=new_comment.text,
        created_at=new_comment.created_at
    )

# Route to get comments for a specific post
@router.get("/comments", response_model=List[CommentResponse])
def get_comments_for_post(post_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Verify the token to ensure the user is authenticated
    verify_token(token)

    # Get all comments for the given post_id
    post_comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    if not post_comments:
        return []
    
    return post_comments

# Route to edit a comment
class CommentUpdate(BaseModel):
    comment_id: str
    text: str

@router.put("/comments", response_model=CommentResponse)
async def edit_comment(comment_update: CommentUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Verify the token to get the user email
    user_email = verify_token(token)

    # Find the comment by ID
    comment = db.query(Comment).filter(Comment.comment_id == comment_update.comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    # Ensure that the user can only edit their own comment
    if comment.user_email != user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only edit your own comment")

    # Update the comment fields
    comment.text = comment_update.text
    db.commit()
    db.refresh(comment)

    return CommentResponse(
        comment_id=comment.comment_id,
        user_email=comment.user_email,
        post_id=comment.post_id,
        text=comment.text,
        created_at=comment.created_at
    )

# Route to delete a comment
@router.delete("/comments/{comment_id}", status_code=status.HTTP_200_OK)
def delete_comment(comment_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Verify the token to get the user email
    user_email = verify_token(token)

    # Find the comment by ID
    comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    # Ensure the authenticated user is the owner of the comment
    if comment.user_email != user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this comment")

    # Delete the comment from the database
    db.delete(comment)
    db.commit()

    return {"detail": "Comment deleted successfully"}
