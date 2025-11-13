# Supabase RLS Migration Guide

## Overview
This guide will help you migrate from the old `users` table to the new `profiles` table with Row Level Security (RLS) enabled.

## What's Changing?

### Before (Old System)
- ❌ User credentials stored in custom `users` table with bcrypt passwords
- ❌ No Row Level Security - users could potentially access other users' data
- ❌ Manual password hashing and session management

### After (New System)
- ✅ Supabase handles authentication via `auth.users` table
- ✅ Profile data stored in `profiles` table (username, is_master flag)
- ✅ Row Level Security enabled on all tables (sessions, messages, profiles)
- ✅ Database trigger automatically creates profile when user signs up
- ✅ Multi-tenant isolation - users can ONLY access their own data

## Data Storage Architecture

```
┌─────────────────────────────────────────────────────┐
│  SUPABASE AUTH (Managed by Supabase)                │
│  ┌──────────────┐                                   │
│  │ auth.users   │  ← Email, password hash, metadata │
│  └──────┬───────┘                                   │
└─────────┼─────────────────────────────────────────┘
          │
          │ (Trigger creates profile)
          ▼
┌─────────────────────────────────────────────────────┐
│  YOUR DATABASE (Custom Tables with RLS)             │
│  ┌──────────────┐                                   │
│  │ profiles     │  ← Username, is_master, email     │
│  │ (id = auth)  │                                   │
│  └──────┬───────┘                                   │
│         │                                            │
│         │ (User ID links everything)                │
│         ▼                                            │
│  ┌──────────────┐                                   │
│  │ sessions     │  ← User's analysis sessions       │
│  └──────┬───────┘                                   │
│         │                                            │
│         ▼                                            │
│  ┌──────────────┐                                   │
│  │ messages     │  ← Chat messages in sessions      │
│  └──────────────┘                                   │
└─────────────────────────────────────────────────────┘
```

## Step-by-Step Migration

### Step 1: Backup Current Data (IMPORTANT!)

Before making any changes, export your current data:

1. Go to Supabase Dashboard → Table Editor
2. Export your `users`, `sessions`, and `messages` tables to CSV
3. Keep these backups safe!

### Step 2: Apply New Database Schema

1. **Open Supabase SQL Editor:**
   - Go to your Supabase project dashboard
   - Click on "SQL Editor" in the left sidebar
   - Click "New Query"

2. **Run the migration script:**
   - Copy the contents of `init_database_with_rls.sql`
   - Paste into the SQL Editor
   - Click "Run" (or press Cmd/Ctrl + Enter)

3. **Verify the changes:**
   ```sql
   -- Check that profiles table exists
   SELECT * FROM profiles LIMIT 1;
   
   -- Check that RLS is enabled
   SELECT tablename, rowsecurity 
   FROM pg_tables 
   WHERE schemaname = 'public' 
   AND tablename IN ('profiles', 'sessions', 'messages');
   
   -- Should show rowsecurity = true for all tables
   ```

### Step 3: Migrate Existing Users (If Any)

**⚠️ IMPORTANT:** If you have existing users in the old `users` table, you need to create Supabase Auth accounts for them first:

**Option A: Manual Migration (Recommended for few users)**
1. Have each user sign up again through the application
2. The trigger will automatically create their profile

**Option B: Programmatic Migration (For many users)**
```sql
-- This is a MANUAL process that requires Supabase Admin API
-- You cannot migrate passwords automatically (they're bcrypt hashed)
-- Users will need to reset passwords or sign up again
```

**Option C: Fresh Start (If in development)**
```sql
-- If you're okay starting fresh, just drop the old table:
DROP TABLE IF EXISTS users CASCADE;

-- The new schema is already in place from Step 2
```

### Step 4: Update Environment Variables

Make sure your `.env` file has these Supabase credentials:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Database URL (from Supabase Settings → Database → Connection String)
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
```

### Step 5: Test the New Flow

1. **Test Signup:**
   - Go to your app's signup page
   - Create a new account
   - Check Supabase Dashboard:
     - Authentication → Users (should see new user)
     - Table Editor → profiles (should see matching profile)

2. **Test Login:**
   - Sign in with the new account
   - Create a session, upload data, send messages
   - Verify all data is saved correctly

3. **Test RLS (Row Level Security):**
   ```sql
   -- Try to access another user's session (should return empty)
   SELECT * FROM sessions WHERE user_id != auth.uid();
   -- Should return no results!
   ```

4. **Test Master User:**
   ```sql
   -- Set a user as master
   UPDATE profiles SET is_master = 1 WHERE email = 'admin@example.com';
   
   -- Verify
   SELECT username, email, is_master FROM profiles WHERE is_master = 1;
   ```

## Row Level Security Policies

The new schema includes these RLS policies:

### Profiles Table
- ✅ Users can view their own profile
- ✅ Users can update their own profile (except is_master)
- ✅ Users can insert during signup
- ❌ Users cannot view other users' profiles
- ❌ Users cannot change is_master flag (admin only)

### Sessions Table
- ✅ Users can view their own sessions
- ✅ Users can create, update, and delete their own sessions
- ❌ Users cannot access other users' sessions

### Messages Table
- ✅ Users can view messages in their own sessions
- ✅ Users can create, update, delete messages in their own sessions
- ❌ Users cannot access messages in other users' sessions

## Troubleshooting

### Issue: "permission denied for table profiles"
**Solution:** Make sure you ran the RLS policies from `init_database_with_rls.sql`

### Issue: "Profile not created after signup"
**Solution:** Check that the trigger exists:
```sql
SELECT * FROM pg_trigger WHERE tgname = 'on_auth_user_created';
```

If missing, run this from the SQL file:
```sql
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_new_user();
```

### Issue: "Users can see other users' data"
**Solution:** Verify RLS is enabled:
```sql
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
```

## Verifying RLS is Working

Run this test in Supabase SQL Editor:

```sql
-- Set the JWT context to simulate a user (replace with actual user ID)
SELECT set_config('request.jwt.claims', '{"sub":"user-id-here"}', true);

-- This should only return the current user's data
SELECT * FROM profiles WHERE id = auth.uid();
SELECT * FROM sessions WHERE user_id = auth.uid();
```

## What Happens in Your Code

After migration:

1. **Signup Flow:**
   - User fills form → `POST /api/auth/signup`
   - Backend calls `supabase.auth.sign_up()`
   - Supabase creates entry in `auth.users`
   - Database trigger automatically creates entry in `profiles`
   - User gets JWT token
   - ✅ Complete!

2. **Login Flow:**
   - User enters credentials → `POST /api/auth/signin`
   - Backend calls `supabase.auth.sign_in_with_password()`
   - Supabase validates credentials
   - User gets JWT token
   - ✅ Complete!

3. **Data Access:**
   - All queries automatically filtered by `auth.uid()`
   - Users can ONLY see their own sessions and messages
   - RLS enforces this at database level
   - ✅ Secure!

## Next Steps

After migration:
1. ✅ Users are stored in Supabase Auth
2. ✅ Profiles are in `profiles` table
3. ✅ RLS is enabled on all tables
4. ✅ Multi-tenant data isolation working
5. 🎉 Your app is now secure!

## Questions?

- Check Supabase Dashboard → Table Editor → profiles (should see users)
- Check Supabase Dashboard → Authentication → Users (should match)
- Test with multiple accounts to verify isolation
