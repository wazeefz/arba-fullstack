import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserResponse, UserLogin
from crud import create_user
from database import get_db
from sqlalchemy.exc import NoResultFound

# Replace these with your actual secret key and algorithm.
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

router = APIRouter()

def create_access_token(email: str, name: str):
    """Generate a JWT token for the user."""
    expiration = datetime.utcnow() + timedelta(weeks=1)  # Token expires in 1 week
    token_data = {"sub": email, "name": name, "exp": expiration}
    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

# Get all users from the database
@router.get('/users', response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Sign Up Endpoint - Register a new user
@router.post('/users/signup', response_model=UserResponse)
def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Create and save the new user to the database
    new_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return the newly created user directly, FastAPI will handle converting it to UserResponse
    return new_user  # This will return the user in the expected format with id, name, and email fields

# Login Endpoint - Authenticate a user and return a token
@router.post('/users/login')
def login(login_request: UserLogin, db: Session = Depends(get_db)):
    # Find the user by email
    db_user = db.query(User).filter(User.email == login_request.email).first()

    if not db_user or not bcrypt.checkpw(login_request.password.encode('utf-8'), db_user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate a JWT token for the authenticated user
    token = create_access_token(db_user.email, db_user.name)

    # Return the token along with user details (without returning the password)
    return {"message": "Login successful", "token": token, "name": db_user.name, "email": db_user.email}
