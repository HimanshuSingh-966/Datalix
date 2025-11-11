from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
import os
from supabase import create_client, Client

router = APIRouter()

# Supabase client
supabase_url = os.getenv("SUPABASE_URL", "")
supabase_key = os.getenv("SUPABASE_ANON_KEY", "")

if not supabase_url or not supabase_key:
    print("⚠️  Warning: Supabase credentials not found. Set SUPABASE_URL and SUPABASE_ANON_KEY")
    supabase: Optional[Client] = None
else:
    supabase: Client = create_client(supabase_url, supabase_key)

# Request models
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    username: str

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    user: Dict
    session: Dict
    access_token: str

@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignUpRequest):
    """Register a new user with Supabase Auth"""
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    try:
        # Sign up with Supabase
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {
                    "username": request.username
                }
            }
        })
        
        if response.user is None:
            raise HTTPException(status_code=400, detail="Signup failed")
        
        return {
            "user": {
                "id": response.user.id,
                "email": response.user.email,
                "username": request.username
            },
            "session": {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token
            },
            "access_token": response.session.access_token
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signin", response_model=AuthResponse)
async def signin(request: SignInRequest):
    """Sign in a user with Supabase Auth"""
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        if response.user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Get user metadata
        username = response.user.user_metadata.get('username', response.user.email.split('@')[0])
        
        return {
            "user": {
                "id": response.user.id,
                "email": response.user.email,
                "username": username
            },
            "session": {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token
            },
            "access_token": response.session.access_token
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/signout")
async def signout(authorization: Optional[str] = Header(None)):
    """Sign out a user"""
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    try:
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            supabase.auth.sign_out()
        
        return {"message": "Signed out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def get_current_user(authorization: Optional[str] = Header(None)) -> Dict:
    """Dependency to get current authenticated user"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    try:
        token = authorization.split(" ")[1]
        user_response = supabase.auth.get_user(token)
        
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        username = user_response.user.user_metadata.get('username', user_response.user.email.split('@')[0])
        
        return {
            "id": user_response.user.id,
            "email": user_response.user.email,
            "username": username
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
