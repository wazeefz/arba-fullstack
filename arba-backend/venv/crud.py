from sqlalchemy.orm import Session
from models import User, Post, Comment
from schemas import UserCreate, PostCreate, PostResponse, CommentCreate, CommentResponse
import bcrypt
from datetime import datetime
from uuid import uuid4
import io

# Helper function to save an uploaded file (image) into the database
def save_image_to_db(image):
    # Read the image into a binary format to store in the database
    image_content = image.file.read()
    return image_content

# Create User
def create_user(db: Session, user: UserCreate):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise Exception("User already exists")
    
    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    db_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get all Users
def get_all_users(db: Session):
    return db.query(User).all()

# Create Post
def create_post(db: Session, caption: str, image, user_email: str):
    # Save the image content into the database
    image_content = save_image_to_db(image)

    post_id = str(uuid4())  # Generate a unique post ID
    new_post = Post(post_id=post_id, user_email=user_email, image=image_content, caption=caption)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get all Posts
def get_all_posts(db: Session):
    return db.query(Post).all()

# Get Post by ID
def get_post_by_id(db: Session, post_id: str):
    return db.query(Post).filter(Post.post_id == post_id).first()

# Edit Post
def edit_post(db: Session, post_id: str, caption: str, image, user_email: str):
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise Exception("Post not found")

    # Ensure the authenticated user is the owner of the post
    if post.user_email != user_email:
        raise Exception("You are not allowed to edit this post")

    # Update the post's details if provided
    if caption:
        post.caption = caption
    if image:
        image_content = save_image_to_db(image)
        post.image = image_content

    db.commit()
    db.refresh(post)
    return post

# Delete Post
def delete_post(db: Session, post_id: str, user_email: str):
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise Exception("Post not found")

    # Ensure the authenticated user is the owner of the post
    if post.user_email != user_email:
        raise Exception("You are not allowed to delete this post")

    # Delete the post
    db.delete(post)
    db.commit()
    return post

# Create Comment
def create_comment(db: Session, comment: CommentCreate, user_email: str):
    # Check if the post exists
    post = db.query(Post).filter(Post.post_id == comment.post_id).first()
    if not post:
        raise Exception("Post not found")

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
    return new_comment

# Get Comments for a Post
def get_comments_for_post(db: Session, post_id: str):
    return db.query(Comment).filter(Comment.post_id == post_id).all()

# Edit Comment
def edit_comment(db: Session, comment_id: str, text: str, user_email: str):
    comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if not comment:
        raise Exception("Comment not found")

    # Ensure that the user can only edit their own comment
    if comment.user_email != user_email:
        raise Exception("You can only edit your own comment")

    # Update the comment's text
    comment.text = text
    db.commit()
    db.refresh(comment)
    return comment

# Delete Comment
def delete_comment(db: Session, comment_id: str, user_email: str):
    comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if not comment:
        raise Exception("Comment not found")

    # Ensure the authenticated user is the owner of the comment
    if comment.user_email != user_email:
        raise Exception("You are not allowed to delete this comment")

    # Delete the comment
    db.delete(comment)
    db.commit()
    return comment
