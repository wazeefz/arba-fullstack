from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List
from uuid import uuid4
from datetime import datetime
from models.comment import Comment
from models.comment_response import CommentResponse
from models.user import User
from models.post import Post
from mock_data.mock_data import posts, comments, users
import jwt
from jwt import PyJWTError
from fastapi.security import OAuth2PasswordBearer
from mock_data.mock_data import users, posts, SECRET_KEY, ALGORITHM

# OAuth2PasswordBearer is used to extract the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Helper function to decode and verify the JWT token
def verify_token(token: str):
    try:
        # Decode the JWT token using the SECRET_KEY and ALGORITHM
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        # Ensure the token is not expired
        if payload["exp"] < datetime.utcnow().timestamp():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        # Return the email from the token (we'll use it to identify the user)
        return payload["sub"]
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or expired token")

# Create a router instance
router = APIRouter()

# Route to create a comment on a post
@router.post("/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: Comment, token: str = Depends(oauth2_scheme)):
    # Verify the token to get the user email
    user_email = verify_token(token)

    # Check if the user exists
    user = next((u for u in users if u.email == user_email), None)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Check if the post exists
    post = next((p for p in posts if p.post_id == comment.post_id), None)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # Create a unique comment ID
    comment_id = str(uuid4())
    
    # Create a timestamp for when the comment was created
    created_at = datetime.utcnow()
    
    # Create a new CommentResponse instance
    new_comment = CommentResponse(
        comment_id=comment_id,
        user_email=user_email,
        post_id=comment.post_id,
        text=comment.text,
        created_at=created_at
    )
    
    # Add the comment to the in-memory storage
    comments.append(new_comment)
    
    return new_comment

# Route to get comments for a specific post (post_id is sent in the request body)
class PostRequestBody(BaseModel):
    post_id: str

@router.get("/comments", response_model=List[CommentResponse])
def get_comments_for_post(post_id: str, token: str = Depends(oauth2_scheme)):
    # Verify the token to ensure the user is authenticated
    verify_token(token)

    # Get all comments for the given post_id
    post_comments = [comment for comment in comments if comment.post_id == post_id]
    
    # Instead of raising a 404 error, return an empty list if no comments are found
    if not post_comments:
        return []

    return post_comments

# Route to edit a comment
class CommentUpdate(BaseModel):
    comment_id: str
    post_id: str
    text: str

@router.put("/comments", response_model=CommentResponse)
async def edit_comment(comment_update: CommentUpdate, token: str = Depends(oauth2_scheme)):
    # Verify the token to get the user email
    user_email = verify_token(token)

    # Find the comment by ID
    comment = next((c for c in comments if c.comment_id == comment_update.comment_id), None)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    # Check if the post exists
    post = next((p for p in posts if p.post_id == comment_update.post_id), None)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # Ensure that the user can only edit their own comment
    if comment.user_email != user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only edit your own comment")

    # Update the comment fields
    comment.text = comment_update.text
    comment.post_id = comment_update.post_id  # If the post ID should be changeable
    
    return comment

# Route to delete a comment
@router.delete("/comments/{comment_id}", status_code=status.HTTP_200_OK)
def delete_comment(comment_id: str, token: str = Depends(oauth2_scheme)):
    # Verify the token to get the user email
    user_email = verify_token(token)

    # Find the comment index
    comment_index = next((i for i, c in enumerate(comments) if c.comment_id == comment_id), None)
    if comment_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    # Ensure the authenticated user is the owner of the comment
    if comments[comment_index].user_email != user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this comment")

    # Remove the comment from the list
    comments.pop(comment_index)

    return {"detail": "Comment deleted successfully"}
