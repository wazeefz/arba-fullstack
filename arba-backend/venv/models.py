from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from database import Base
import uuid
from datetime import datetime  # Import datetime for created_at timestamp

# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    posts = relationship("Post", back_populates="owner", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")

# Post Model
class Post(Base):
    __tablename__ = "posts"

    post_id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    caption = Column(Text, nullable=False)
    image = Column(BYTEA, nullable=True)  # Store image as binary data (BYTEA)
    user_email = Column(String, ForeignKey("users.email", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

# Comment Model
class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    text = Column(Text, nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.post_id", ondelete="CASCADE"), nullable=False)
    user_email = Column(String, ForeignKey("users.email", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)  # Use datetime.utcnow for a timestamp

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
