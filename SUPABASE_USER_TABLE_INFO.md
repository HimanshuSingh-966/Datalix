# Supabase User Table Information

## Where Are Users Stored?

When you sign up using Supabase authentication, your users are stored in **Supabase's built-in authentication table**, NOT in a custom users table.

### The Two Tables:

1. **`auth.users`** (Supabase System Table - BUILT-IN)
   - This is Supabase's own authentication table
   - Located in the `auth` schema (separate from `public` schema)
   - **This is where your signup creates users automatically**
   - You can view this table in Supabase Dashboard → Authentication → Users

2. **`public.users`** (Custom Table - OPTIONAL)
   - This is a custom table you can create if needed
   - Located in the `public` schema (your app's schema)
   - **Not created automatically by Supabase auth**
   - Only needed if you want to store additional user data beyond what Supabase auth provides

## How to View Your Users

### Method 1: Supabase Dashboard (Easiest)
1. Go to your Supabase project dashboard at https://supabase.com/dashboard
2. Click on your project
3. Click **"Authentication"** in the left sidebar
4. Click **"Users"** tab
5. **You should see all signed-up users here!**

### Method 2: SQL Editor
Run this query in Supabase SQL Editor:

```sql
SELECT 
    id,
    email,
    created_at,
    user_metadata
FROM auth.users
ORDER BY created_at DESC;
```

This will show all users in the auth.users table.

## What Data Is Stored in auth.users?

When someone signs up through your app, Supabase stores:

- `id`: Unique user ID (UUID)
- `email`: User's email address
- `encrypted_password`: Hashed password (secure, cannot be reversed)
- `created_at`: When the account was created
- `last_sign_in_at`: Last login timestamp
- `user_metadata`: Custom data (like username) stored as JSON

### Viewing User Metadata (Username)

To see the username you stored during signup:

```sql
SELECT 
    email,
    user_metadata->>'username' as username,
    created_at
FROM auth.users
ORDER BY created_at DESC;
```

## Do You Need a Custom Users Table?

**Short answer: No, not yet.**

You only need a custom `public.users` table if you want to store additional profile information that Supabase auth doesn't handle, such as:
- Profile pictures
- Bio/description
- Preferences/settings
- Additional custom fields

For basic authentication (email, username, password), Supabase's `auth.users` table is sufficient.

## If You Want to Create a Custom Users Table (Optional)

If you decide you need additional user data, you can create a `public.users` table that links to `auth.users`:

```sql
-- Create custom users table
CREATE TABLE public.users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT UNIQUE,
    bio TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own profile
CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

-- Policy: Users can update their own profile
CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE USING (auth.uid() = id);
```

Then, when a user signs up, you would:
1. Create user in `auth.users` (done by Supabase auth automatically)
2. Insert additional data in `public.users` (you'd need to do this manually)

## Current Implementation

In your current setup:
- ✅ Users ARE being created in `auth.users` automatically
- ✅ Username is stored in `user_metadata` field
- ❌ There is NO `public.users` table (and you don't need one unless you want extra fields)

## How to Verify Signup Worked

1. **Check Supabase Dashboard:**
   - Go to Authentication → Users
   - You should see your test account there

2. **Check using SQL:**
   ```sql
   SELECT COUNT(*) FROM auth.users;
   ```
   This should return the number of signed-up users.

3. **Check specific user:**
   ```sql
   SELECT * FROM auth.users WHERE email = 'your-test-email@example.com';
   ```

## Summary

- ✅ Your signups ARE working and creating users
- ✅ Users are stored in `auth.users` (Supabase's system table)
- ✅ You can view them in the Authentication section of Supabase Dashboard
- ❌ There is no `public.users` table (and you don't need one for basic auth)
- ✅ Your username is safely stored in the `user_metadata` JSON field

The user table IS being updated - it's just in the `auth` schema, not the `public` schema!
