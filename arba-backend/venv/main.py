from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.prod.post_router import router as post_router
from routers.prod.user_router import router as user_router
from routers.prod.comment_router import router as comment_router
from database import init_db  # Import the init_db function

app = FastAPI()

# CORS configuration (restrict origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)

# Root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Optional: Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    print("Starting up G...")
    # Call the init_db function to create tables
    init_db()

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down G...")
