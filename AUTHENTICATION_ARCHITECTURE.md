# DataLix AI - Authentication Architecture with Supabase & RLS

## Overview

DataLix AI uses **Supabase Authentication** with **Row Level Security (RLS)** to provide secure, multi-tenant data isolation. This document explains how user authentication and data access works.

## Authentication Flow

### 🔐 User Signup

```
┌─────────┐         ┌──────────────┐         ┌─────────────────┐         ┌──────────────┐
│  User   │────1───▶│   Frontend   │────2───▶│ Python Backend  │────3───▶│   Supabase   │
│ Browser │         │  (React)     │         │   (FastAPI)     │         │    Auth      │
└─────────┘         └──────────────┘         └─────────────────┘         └───────┬──────┘
     ▲                                                                            │
     │                                                                            │4
     │                                                                            ▼
     │              ┌──────────────────────────────────────────────┐   ┌────────────────┐
     └──────7───────│          JWT Token + User Info               │   │  auth.users    │
                    └──────────────────────────────────────────────┘   │  (Supabase)    │
                                                                        └────────┬───────┘
                                                                                 │5
                                                                                 │ (Trigger)
                                                                                 ▼
                                                                        ┌────────────────┐
                                                                        │   profiles     │
                                                                        │  (Your DB)     │
                                                                        └────────────────┘
```

**Step-by-step:**
1. User fills signup form (email, password, username)
2. Frontend sends `POST /api/auth/signup` to Python backend
3. Backend calls `supabase.auth.sign_up()` with credentials
4. Supabase creates user in `auth.users` table (managed by Supabase)
5. Database trigger `on_auth_user_created` automatically creates matching profile in `profiles` table
6. Supabase returns JWT access token
7. Frontend receives token and user info, stores in session

### 🔑 User Login

```
User enters credentials → Backend calls supabase.auth.sign_in_with_password()
→ Supabase validates credentials → Returns JWT token → User authenticated
```

### 🛡️ Token Verification

Every API request includes the JWT token in the `Authorization` header:

```
Authorization: Bearer <jwt-token>
```

The backend verifies the token using `supabase_admin.auth.get_user(token)`, which:
- Validates token signature
- Checks expiration
- Returns user ID from token
- Fetches `is_master` flag from `profiles` table

## Database Schema

### Tables Overview

```
auth.users (Managed by Supabase)
├── id (UUID)
├── email
├── encrypted_password
└── user_metadata (stores username)

profiles (Your custom table)
├── id (UUID) → references auth.users(id)
├── username (TEXT)
├── email (TEXT)
├── is_master (INTEGER) → 0 = regular, 1 = unlimited quota
└── created_at (TIMESTAMP)

sessions (Your custom table)
├── id (UUID)
├── user_id (UUID) → references profiles(id)
├── name (TEXT)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

messages (Your custom table)
├── id (UUID)
├── session_id (UUID) → references sessions(id)
├── role (TEXT) → 'user' | 'assistant'
├── content (TEXT)
├── chart_data (JSONB)
├── data_preview (JSONB)
├── suggested_actions (JSONB)
├── function_calls (JSONB)
├── error (TEXT)
└── created_at (TIMESTAMP)
```

## Row Level Security (RLS)

### What is RLS?

Row Level Security ensures users can **only access their own data** at the **database level**. Even if there's a bug in your application code, users cannot access other users' data.

### How It Works

RLS uses PostgreSQL policies that filter queries based on `auth.uid()`:

```sql
-- Example: Users can only see their own sessions
CREATE POLICY "Users can view own sessions"
    ON sessions
    FOR SELECT
    USING (auth.uid() = user_id);
```

When a user makes a query:
```sql
-- User thinks they're running:
SELECT * FROM sessions;

-- PostgreSQL actually runs (with RLS):
SELECT * FROM sessions WHERE user_id = 'current-user-id';
```

### RLS Policies in DataLix AI

#### Profiles Table
```sql
✅ SELECT: Users can view their own profile
✅ UPDATE: Users can update their own profile (except is_master)
✅ INSERT: Allowed during signup
❌ DELETE: Not allowed
❌ is_master: Only admins can change (via direct SQL)
```

#### Sessions Table
```sql
✅ SELECT: Users can view their own sessions
✅ INSERT: Users can create sessions for themselves
✅ UPDATE: Users can update their own sessions
✅ DELETE: Users can delete their own sessions
❌ Other users' sessions: Completely hidden
```

#### Messages Table
```sql
✅ SELECT: Users can view messages in their own sessions
✅ INSERT: Users can create messages in their own sessions
✅ UPDATE: Users can update messages in their own sessions
✅ DELETE: Users can delete messages in their own sessions
❌ Other users' messages: Completely hidden
```

## Data Isolation Example

### Scenario: Two Users

```
User A (id: aaa-111)
└── Session 1 (id: session-a1)
    ├── Message 1
    └── Message 2

User B (id: bbb-222)
└── Session 1 (id: session-b1)
    ├── Message 1
    └── Message 2
```

### What Each User Can Access

**User A logged in:**
```sql
SELECT * FROM sessions;
-- Returns: session-a1 ONLY

SELECT * FROM messages;
-- Returns: Messages from session-a1 ONLY
```

**User B logged in:**
```sql
SELECT * FROM sessions;
-- Returns: session-b1 ONLY

SELECT * FROM messages;
-- Returns: Messages from session-b1 ONLY
```

**Attempted Breach:**
```sql
-- User A tries to access User B's session
SELECT * FROM sessions WHERE id = 'session-b1';
-- Returns: EMPTY (RLS blocks it)

-- User A tries to bypass with raw query
SELECT * FROM messages WHERE session_id = 'session-b1';
-- Returns: EMPTY (RLS blocks it)
```

## Master User Feature

Master users have **unlimited message quota** and bypass the 10 messages/day limit for regular users.

### Setting a Master User

This can only be done via direct SQL (admin access required):

```sql
-- Make a user master
UPDATE profiles SET is_master = 1 WHERE email = 'admin@example.com';

-- Verify master users
SELECT username, email, is_master FROM profiles WHERE is_master = 1;

-- Remove master status
UPDATE profiles SET is_master = 0 WHERE email = 'admin@example.com';
```

### How It Works

1. When checking message quota, backend queries:
```python
is_master = get_user(user_id).is_master
if is_master == 1:
    # Skip quota check
    allow_message()
else:
    # Enforce 10 messages/day limit
    check_quota()
```

## API Endpoints

### Authentication Endpoints

```
POST /api/auth/signup
Body: { email, password, username }
Returns: { user, session, access_token }

POST /api/auth/signin
Body: { email, password }
Returns: { user, session, access_token }

GET /api/auth/verify
Headers: Authorization: Bearer <token>
Returns: { id, email, username, isMaster }

POST /api/auth/signout
Headers: Authorization: Bearer <token>
Returns: { message: "Signed out successfully" }
```

### Protected Endpoints

All other endpoints require authentication:

```
Headers:
  Authorization: Bearer <jwt-token>

Example:
POST /api/chat
Headers: { Authorization: "Bearer eyJhbG..." }
Body: { sessionId, message }
```

## Security Features

### 1. Password Security
- ✅ Passwords hashed by Supabase (bcrypt)
- ✅ Never stored in plain text
- ✅ Never returned in API responses

### 2. Session Security
- ✅ JWT tokens with expiration
- ✅ Tokens validated on every request
- ✅ Refresh tokens for extended sessions

### 3. Data Isolation
- ✅ RLS enforced at database level
- ✅ Users cannot access other users' data
- ✅ Even SQL injection cannot bypass RLS

### 4. Input Validation
- ✅ Email validation (Pydantic EmailStr)
- ✅ Password requirements enforced by Supabase
- ✅ SQL injection prevention (parameterized queries)

## Environment Variables

Required for Supabase Auth:

```bash
# Supabase Project Settings
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJhbG...  # For client-side operations
SUPABASE_SERVICE_ROLE_KEY=eyJhbG...  # For admin operations

# Database Connection
DATABASE_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres
```

## Troubleshooting

### "Not authenticated" errors
- Check that token is included in Authorization header
- Verify token hasn't expired
- Check that user exists in Supabase Auth

### "Permission denied" errors
- Verify RLS policies are created
- Check that RLS is enabled on tables
- Ensure user owns the resource they're accessing

### Profile not created
- Check trigger exists: `on_auth_user_created`
- Verify trigger function: `handle_new_user()`
- Check Supabase logs for errors

### Master user not working
- Verify `is_master = 1` in database
- Check backend is reading `is_master` correctly
- Ensure user re-authenticated after change

## Migration from Old System

If you previously used the custom `users` table with bcrypt passwords:

1. **New users:** Just sign up normally - works automatically
2. **Existing users:** Must create new Supabase Auth accounts (passwords cannot be migrated)
3. **Database:** Run `init_database_with_rls.sql` to create new schema

See `SUPABASE_RLS_MIGRATION_GUIDE.md` for detailed steps.

## Summary

✅ **Secure**: Supabase handles authentication, RLS enforces data isolation
✅ **Simple**: Signup/login just work, no manual session management
✅ **Scalable**: RLS policies enforce security as you grow
✅ **Flexible**: Master user system for unlimited access
✅ **Standard**: Uses industry-standard JWT tokens and PostgreSQL RLS

Your data is safe! 🔒
