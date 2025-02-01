import base64
from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
import jwt
from jwt import PyJWTError
from typing import List

from models import Post, User
from schemas import PostCreate, PostResponse
from database import get_db

# OAuth2PasswordBearer is used to extract the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Helper function to decode and verify the JWT token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["exp"] < datetime.utcnow().timestamp():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        return payload["sub"]
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

router = APIRouter()

# Convert bytea image data to base64 encoding
def encode_image(image_data: bytes) -> str:
    """Converts bytea image data to a base64-encoded string."""
    return base64.b64encode(image_data).decode('utf-8')

# Create a new post (protected by JWT)
@router.post('/posts', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(caption: str = Form(...), image: UploadFile = File(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Verify the token to get the user email
    email = verify_token(token)

    # Check if the user exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Read the image file as binary data
    image_data = await image.read()  # This reads the image content as bytes

    # Create new post and save to the database
    post_id = str(uuid4())  # Generate a unique post ID
    new_post = Post(post_id=post_id, user_email=email, image=image_data, caption=caption)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return PostResponse(post_id=new_post.post_id, user_email=new_post.user_email, image=encode_image(new_post.image), caption=new_post.caption)

# Get all posts (protected by JWT)
@router.get('/posts', response_model=List[PostResponse])
def get_all_posts(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Verify the token to get the user email
    verify_token(token)

    # Fetch all posts from the database
    posts = db.query(Post).all()

    # Convert the image from bytea to base64 for each post
    for post in posts:
        post.image = encode_image(post.image)  # Convert image from bytea to base64

    return posts

# Edit a post (only the owner can edit)
@router.put('/posts/{post_id}', response_model=PostResponse)
async def edit_post(
    post_id: str,
    caption: str = Form(None),
    image: UploadFile = File(None),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # Verify token and get user email
    email = verify_token(token)

    # Find the post by ID
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Ensure the authenticated user is the owner of the post
    if post.user_email != email:
        raise HTTPException(status_code=403, detail="You are not allowed to edit this post")

    # Update the post's details if provided
    if caption:
        post.caption = caption
    if image:
        image_data = await image.read()  # Read the new image as bytes
        post.image = image_data

    db.commit()
    db.refresh(post)

    return PostResponse(post_id=post.post_id, user_email=post.user_email, image=encode_image(post.image), caption=post.caption)

# Delete a post (only the owner can delete)
@router.delete('/posts/{post_id}', status_code=status.HTTP_200_OK)  # Use 200 OK instead of 204
def delete_post(post_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Verify token and get user email
    email = verify_token(token)

    # Find the post by ID
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Ensure the authenticated user is the owner of the post
    if post.user_email != email:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this post")

    # Delete the post
    db.delete(post)
    db.commit()

    return {"detail": "Post deleted successfully"}
