# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, books
from .database import engine, Base
from .exceptions.handlers import register_exception_handlers

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Books API",
    description="A FastAPI application for managing books with JWT authentication (obviously.ai take home)",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For take home only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
register_exception_handlers(app)

# Include routers
app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Authentication"]
)

app.include_router(
    books.router,
    prefix="/api/books",
    tags=["Books"]
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Books API",
        "documentation": "/api/docs",
        "version": app.version
    }