from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from models.user import User
from typing import List
import jwt
from jwt import PyJWTError
from uuid import uuid4
from datetime import datetime, timedelta

from models.post import Post
from models.post_response import PostResponse

from mock_data.mock_data import users, posts, SECRET_KEY, ALGORITHM

# OAuth2PasswordBearer is used to extract the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

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

# Create a new post (protected by JWT)
@router.post('/posts', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(caption: str = Form(...), image: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    # Verify the token to get the user email
    email = verify_token(token)

    # Check if the user exists
    user = next((u for u in users if u.email == email), None)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Save the image file locally or store it somewhere
    image_path = f"uploads/{image.filename}"
    with open(image_path, "wb") as f:
        f.write(await image.read())

    # Create a unique post ID
    post_id = str(uuid4())
    
    # Create new post and add it to the in-memory storage
    new_post = PostResponse(post_id=post_id, user_email=email, image=image_path, caption=caption)
    posts.append(new_post)
    
    return new_post

# Get all posts (protected by JWT)
@router.get('/posts', response_model=List[PostResponse])
def get_all_posts(token: str = Depends(oauth2_scheme)):
    # Verify the token to get the user email
    verify_token(token)
    
    return posts

# Edit a post (only the owner can edit)
@router.put('/posts/{post_id}', response_model=PostResponse)
async def edit_post(
    post_id: str,
    caption: str = Form(None),
    image: UploadFile = File(None),
    token: str = Depends(oauth2_scheme)
):
    # Verify token and get user email
    email = verify_token(token)

    # Find the post
    post = next((p for p in posts if p.post_id == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Ensure the authenticated user is the owner of the post
    if post.user_email != email:
        raise HTTPException(status_code=403, detail="You are not allowed to edit this post")

    # Update post details if provided
    if caption:
        post.caption = caption
    if image:
        image_path = f"uploads/{image.filename}"
        with open(image_path, "wb") as f:
            f.write(await image.read())
        post.image = image_path

    return post


# Delete a post (only the owner can delete)
@router.delete('/posts/{post_id}', status_code=status.HTTP_200_OK)  # Use 200 OK instead of 204
def delete_post(post_id: str, token: str = Depends(oauth2_scheme)):
    # Verify token and get user email
    email = verify_token(token)

    # Find the post index
    post_index = next((i for i, p in enumerate(posts) if p.post_id == post_id), None)
    if post_index is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # Ensure the authenticated user is the owner of the post
    if posts[post_index].user_email != email:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this post")

    # Remove the post from the list
    posts.pop(post_index)

    # Return a custom success message with status code 200
    return {"detail": "Post deleted successfully"}

