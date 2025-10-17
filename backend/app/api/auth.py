"""Authentication endpoints - placeholder for MVP."""
from fastapi import APIRouter

router = APIRouter()


@router.post("/register")
async def register():
    """Register new user."""
    return {"message": "Registration endpoint - implement with JWT auth"}


@router.post("/login")
async def login():
    """User login."""
    return {"message": "Login endpoint - implement with JWT auth"}
