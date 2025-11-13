from fastapi import APIRouter, HTTPException, Header, Depends
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
supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

# Enable Supabase auth if all credentials are available
USE_SUPABASE = bool(supabase_url and supabase_key and supabase_service_key)

if USE_SUPABASE:
    try:
        from supabase import create_client, Client
        # Create client with anon key for auth operations (signup/signin)
        supabase: Optional[Client] = create_client(
            supabase_url=supabase_url,
            supabase_key=supabase_key
        )
        # Create admin client with service role for admin operations (token verification)
        supabase_admin: Optional[Client] = create_client(
            supabase_url=supabase_url,
            supabase_key=supabase_service_key
        )
        print("✓ Supabase authentication enabled")
    except Exception as e:
        print(f"⚠️  Supabase initialization failed: {e}")
        USE_SUPABASE = False
        supabase = None
        supabase_admin = None
        print("→ Using in-memory authentication")
else:
    print("⚠️  Supabase not configured. Using in-memory authentication")
    supabase = None
    supabase_admin = None

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
            # Create user in Supabase Auth
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
            
            # Create user profile in database
            try:
                supabase_admin.table("users").insert({
                    "id": response.user.id,
                    "username": request.username,
                    "email": response.user.email
                }).execute()
                print(f"✓ User profile created in database for {response.user.email}")
            except Exception as db_error:
                print(f"⚠️  Database profile creation error: {str(db_error)}")
                # Continue even if profile creation fails - auth user was created
            
            # Check if session exists (it might be None if email confirmation is required)
            if response.session is None:
                # Email confirmation required - create a temporary token for the user
                # Store user info with 'supabase:' prefix to distinguish from in-memory users
                access_token = secrets.token_urlsafe(32)
                sessions_db[access_token] = f"supabase:{response.user.id}"
                
                # Store basic user info for token validation
                users_db[f"supabase:{response.user.id}"] = {
                    "id": response.user.id,
                    "email": response.user.email,
                    "username": request.username
                }
                
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
            
            if response.session is None:
                raise HTTPException(status_code=401, detail="Session not created")
            
            username = response.user.user_metadata.get('username', response.user.email.split('@')[0] if response.user.email else 'user')
            
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

async def get_current_user(authorization: Optional[str] = Header(None)) -> Dict:
    """Dependency to get current authenticated user"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    
    # First, check if this is a temporary token in our sessions database
    if token in sessions_db:
        user_key = sessions_db[token]
        
        # Check if this is a Supabase user (prefixed with 'supabase:')
        if user_key.startswith("supabase:") and user_key in users_db:
            user = users_db[user_key]
            return {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"],
                "isMaster": user.get("isMaster", 0)
            }
        
        # Otherwise it's an in-memory auth user
        user = next((u for u in users_db.values() if u["id"] == user_key), None)
        
        if user:
            return {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"],
                "isMaster": user.get("isMaster", 0)
            }
    
    # If not a temporary token and using Supabase, validate as JWT token
    if USE_SUPABASE and supabase_admin:
        try:
            # Use the admin client to verify the user token
            user_response = supabase_admin.auth.get_user(token)
            
            if not user_response or not user_response.user:
                raise HTTPException(status_code=401, detail="Invalid token")
            
            username = user_response.user.user_metadata.get('username', user_response.user.email.split('@')[0] if user_response.user.email else 'user')
            
            # Fetch is_master from database
            is_master = 0
            try:
                user_data = supabase_admin.table("users").select("is_master").eq("id", user_response.user.id).single().execute()
                if user_data.data:
                    is_master = user_data.data.get("is_master", 0)
            except Exception as e:
                print(f"⚠️  Could not fetch is_master: {e}")
            
            return {
                "id": user_response.user.id,
                "email": user_response.user.email,
                "username": username,
                "isMaster": is_master
            }
        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ Auth error: {str(e)}")
            raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")
    
    # If we get here, token is invalid
    raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/verify")
async def verify_token(user: Dict = Depends(get_current_user)):
    """Verify authentication token and return user info"""
    return user

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

