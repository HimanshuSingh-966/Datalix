from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
import os
import uuid
import secrets
from passlib.context import CryptContext

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory user storage (simple implementation)
users_db: Dict[str, Dict] = {}
sessions_db: Dict[str, str] = {}

# Try to use Supabase if configured
supabase_url = os.getenv("SUPABASE_URL", "")
supabase_key = os.getenv("SUPABASE_ANON_KEY", "")
# Temporarily disable Supabase auth to use in-memory auth for testing
USE_SUPABASE = False  # Set to True to enable Supabase auth in production

if USE_SUPABASE:
    try:
        from supabase import create_client, Client
        # Create Supabase client with minimal configuration
        supabase: Optional[Client] = create_client(
            supabase_url=supabase_url,
            supabase_key=supabase_key
        )
        print("✓ Supabase authentication enabled")
    except Exception as e:
        print(f"⚠️  Supabase initialization failed: {e}")
        USE_SUPABASE = False
        supabase = None
        print("→ Using in-memory authentication")
else:
    print("⚠️  Supabase not configured. Using in-memory authentication")
    supabase = None

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

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignUpRequest):
    """Register a new user"""
    
    if USE_SUPABASE and supabase:
        try:
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
                raise HTTPException(status_code=400, detail="Signup failed - user not created")
            
            # Check if session exists (it might be None if email confirmation is required)
            if response.session is None:
                # Email confirmation required - create a temporary token for the user
                # In production, you'd send a confirmation email
                access_token = secrets.token_urlsafe(32)
                sessions_db[access_token] = response.user.id
                
                return {
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "username": request.username
                    },
                    "session": {
                        "access_token": access_token,
                        "refresh_token": access_token
                    },
                    "access_token": access_token
                }
            
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
            print(f"Supabase signup error: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    else:
        # In-memory auth
        if request.email in users_db:
            raise HTTPException(status_code=400, detail="User already exists")
        
        user_id = str(uuid.uuid4())
        access_token = secrets.token_urlsafe(32)
        
        users_db[request.email] = {
            "id": user_id,
            "email": request.email,
            "username": request.username,
            "password": hash_password(request.password)
        }
        
        sessions_db[access_token] = user_id
        
        return {
            "user": {
                "id": user_id,
                "email": request.email,
                "username": request.username
            },
            "session": {
                "access_token": access_token,
                "refresh_token": access_token
            },
            "access_token": access_token
        }

@router.post("/signin", response_model=AuthResponse)
async def signin(request: SignInRequest):
    """Sign in a user"""
    
    if USE_SUPABASE and supabase:
        try:
            response = supabase.auth.sign_in_with_password({
                "email": request.email,
                "password": request.password
            })
            
            if response.user is None:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
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
    else:
        # In-memory auth
        if request.email not in users_db:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        user = users_db[request.email]
        if not verify_password(request.password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = secrets.token_urlsafe(32)
        sessions_db[access_token] = user["id"]
        
        return {
            "user": {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"]
            },
            "session": {
                "access_token": access_token,
                "refresh_token": access_token
            },
            "access_token": access_token
        }

@router.post("/signout")
async def signout(authorization: Optional[str] = Header(None)):
    """Sign out a user"""
    
    if USE_SUPABASE and supabase:
        try:
            if authorization and authorization.startswith("Bearer "):
                supabase.auth.sign_out()
            return {"message": "Signed out successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        # In-memory auth
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            if token in sessions_db:
                del sessions_db[token]
        return {"message": "Signed out successfully"}

async def get_current_user(authorization: Optional[str] = Header(None)) -> Dict:
    """Dependency to get current authenticated user"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    
    if USE_SUPABASE and supabase:
        try:
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
    else:
        # In-memory auth
        if token not in sessions_db:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = sessions_db[token]
        user = next((u for u in users_db.values() if u["id"] == user_id), None)
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return {
            "id": user["id"],
            "email": user["email"],
            "username": user["username"]
        }
