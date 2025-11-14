# DataLix 2.0 - Complete Documentation

**Last Updated:** November 14, 2025

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Google OAuth Setup](#google-oauth-setup)
3. [Authentication Architecture](#authentication-architecture)
4. [Database Schema](#database-schema)
5. [Data Storage Strategy](#data-storage-strategy)
6. [Deployment Guide](#deployment-guide)
7. [Troubleshooting](#troubleshooting)

---

## Project Overview

DataLix 2.0 is an AI-powered data analysis platform that makes data science accessible through natural language conversations. Built with React, Node.js, FastAPI (Python), and Supabase.

### Key Features

- **File Upload**: CSV, Excel, JSON, Parquet support with drag-and-drop
- **AI Chat**: Natural language data analysis using Gemini/Groq AI
- **Data Quality**: Automated quality scoring and recommendations
- **Data Cleaning**: Missing values, outliers, duplicates handling
- **Statistics**: Descriptive stats, correlations, distributions
- **Visualizations**: Interactive Plotly charts (scatter, bar, heatmap, etc.)
- **Machine Learning**: Anomaly detection, clustering, PCA, t-SNE
- **User Authentication**: Supabase Auth with Google OAuth
- **Session Management**: Multiple chat sessions per user

---

## Google OAuth Setup

### Prerequisites

- Supabase project
- Google Cloud Platform account

### Step 1: Configure Google Cloud Console

#### 1.1 Create OAuth Consent Screen

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services → OAuth consent screen**
3. Choose **External** user type
4. Configure:
   - **App name**: DataLix 2.0
   - **User support email**: Your email
   - **Developer contact email**: Your email

#### 1.2 Add OAuth Scopes

Click **Add or Remove Scopes** and add:
- `.../auth/userinfo.email`
- `.../auth/userinfo.profile`
- `openid`

#### 1.3 Publish the App

- Click **Publish App** button
- Confirm publishing (allows anyone to sign in)

#### 1.4 Create OAuth Credentials

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth client ID**
3. Choose **Web application**
4. Configure:
   - **Name**: DataLix Web Client
   - **Authorized redirect URIs**: `https://YOUR-PROJECT-ID.supabase.co/auth/v1/callback`
     - Example: `https://xhykynxfmbzljvmtvnxt.supabase.co/auth/v1/callback`
5. Save your **Client ID** and **Client Secret**

### Step 2: Configure Supabase

1. Go to [Supabase Dashboard](https://app.supabase.com/)
2. Navigate to **Authentication → Providers**
3. Find **Google** and toggle it ON
4. Enter:
   - **Client ID**: From Google Cloud Console
   - **Client Secret**: From Google Cloud Console
5. Click **Save**

### Step 3: Set Environment Variables

Add to your Replit Secrets:

```bash
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

### Common OAuth Issues

#### 403 Error: "You do not have access to this page"

**Causes:**
- OAuth consent screen not published
- Missing required scopes
- Client ID/Secret mismatch

**Solutions:**
1. Verify app is "In production" status in Google Console
2. Confirm all three scopes are added (email, profile, openid)
3. Double-check Client ID and Secret in Supabase match Google Console exactly
4. Wait 2-3 minutes for Google changes to propagate

#### redirect_uri_mismatch

**Solution:** Verify redirect URI in Google Console is exactly:
```
https://YOUR-PROJECT-ID.supabase.co/auth/v1/callback
```

---

## Authentication Architecture

### Overview

DataLix uses Supabase Authentication with Row Level Security (RLS) for secure, multi-tenant data isolation.

### Authentication Flow

```
User Signup/Login
    ↓
Frontend (React)
    ↓
Python Backend (/api/auth/signup or /signin)
    ↓
Supabase Auth
    ├─ Creates/validates user in auth.users
    ├─ Returns JWT token
    └─ Trigger creates profile in profiles table
    ↓
Frontend receives token
    ↓
Token stored in localStorage
    ↓
User authenticated!
```

### Database Structure

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
└── created_at (TIMESTAMP)
```

### Row Level Security (RLS)

RLS ensures users can **only access their own data** at the database level.

#### How It Works

```sql
-- Users can only see their own sessions
CREATE POLICY "Users can view own sessions"
    ON sessions
    FOR SELECT
    USING (auth.uid() = user_id);
```

When a user queries:
```sql
SELECT * FROM sessions;
-- PostgreSQL actually runs:
SELECT * FROM sessions WHERE user_id = 'current-user-id';
```

### Message Rate Limiting

DataLix implements message quotas to manage usage:

#### Quota System

- **Regular Users**: 10 messages per day
- **Master Users**: Unlimited messages
- **Daily Reset**: Quotas reset at midnight UTC

#### UI Indicators

**For Regular Users:**
- Badge in header showing remaining messages (e.g., "7/10")
- Footer text showing "X messages remaining today"
- Error toast when limit reached: "Daily message limit reached. Limit resets at midnight UTC."

**For Master Users:**
- Crown icon badge with "Unlimited" text
- No message counter
- No limits applied

#### Setting a Master User

```sql
-- Make a user master (admin access required)
UPDATE profiles SET is_master = 1 WHERE email = 'admin@example.com';

-- Verify
SELECT username, email, is_master FROM profiles WHERE is_master = 1;
```

#### Verifying Quota Status

```sql
-- Check today's message count for a user
SELECT COUNT(*) 
FROM messages m
JOIN sessions s ON m.session_id = s.id
WHERE s.user_id = 'user-id-here'
AND m.created_at >= CURRENT_DATE
AND m.role = 'user';

-- Check user's master status
SELECT is_master FROM profiles WHERE id = 'user-id-here';
```

#### How It Works

1. User sends message → Backend counts today's messages for user
2. If count >= 10 and not master → Return 429 error
3. If count < 10 or is master → Allow message
4. Frontend displays remaining count in UI

---

## Database Schema

### Database Migration

Run this in Supabase SQL Editor to set up the database:

```sql
-- Create profiles table
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    is_master INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create sessions table
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    name TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    chart_data JSONB,
    data_preview JSONB,
    suggested_actions JSONB,
    function_calls JSONB,
    error TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_messages_session_id ON messages(session_id);

-- Create trigger for profile creation
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, username, email)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'username', split_part(NEW.email, '@', 1)),
    NEW.email
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- RLS Policies for profiles
CREATE POLICY "Users can view own profile"
    ON profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON profiles FOR UPDATE
    USING (auth.uid() = id);

-- RLS Policies for sessions
CREATE POLICY "Users can view own sessions"
    ON sessions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create own sessions"
    ON sessions FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own sessions"
    ON sessions FOR DELETE
    USING (auth.uid() = user_id);

-- RLS Policies for messages
CREATE POLICY "Users can view own messages"
    ON messages FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM sessions
            WHERE sessions.id = messages.session_id
            AND sessions.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can create messages in own sessions"
    ON messages FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM sessions
            WHERE sessions.id = messages.session_id
            AND sessions.user_id = auth.uid()
        )
    );
```

---

## Data Storage Strategy

### Hybrid Storage Architecture

DataLix uses two storage systems:

#### 1. PostgreSQL Database (Persistent)

**What's stored:**
- User accounts
- Session metadata
- Chat message history
- Chart configurations
- Data previews

**Why PostgreSQL:**
- ✅ Survives server restarts
- ✅ Searchable conversation history
- ✅ Secure with RLS
- ✅ Supports rollback

#### 2. In-Memory Python (Temporary)

**What's stored:**
- Full datasets (pandas DataFrames)
- Active transformations
- Calculation results
- ML models

**Why In-Memory:**
- ⚡ Lightning fast calculations
- 🐼 Native pandas operations
- 💾 No database bloat
- 🧹 Automatic cleanup

### Data Flow Example

```
Upload "sales.csv"
    ↓
Python loads into memory (pandas DataFrame)
    ↓
Session metadata saved to PostgreSQL
    ↓
User: "Show correlation matrix"
    ↓
Python calculates from in-memory DataFrame
    ↓
Result and chart saved to PostgreSQL messages table
    ↓
User: "Export cleaned data"
    ↓
Python exports from in-memory DataFrame
```

### What Persists vs What's Temporary

**✅ Persistent (survives restarts):**
- User accounts
- Chat conversations
- Session history
- Chart configurations

**❌ Temporary (lost on restart):**
- Uploaded datasets
- Calculated statistics
- ML models

**💡 Best Practice:**
Export cleaned datasets before closing if you want to keep them.

---

## Deployment Guide

### Environment Variables Required

```bash
# Node.js
NODE_ENV=production
PORT=5000

# AI Provider (at least one required)
GEMINI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Frontend (Vite)
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
```

### Replit Deployment

1. Set all environment variables in Replit Secrets
2. Click "Run" - the workflow "Start application" will start automatically
3. App will be available at your Replit URL

---

## Troubleshooting

### Google OAuth 403 Error

**Problem:** "You do not have access to this page" when trying to sign in with Google

**Solutions:**
1. Verify OAuth consent screen is published ("In production")
2. Check Client ID and Client Secret match exactly
3. Confirm redirect URI is: `https://YOUR-PROJECT-ID.supabase.co/auth/v1/callback`
4. Verify scopes include: email, profile, openid
5. Wait 2-3 minutes for Google changes to propagate

### Authentication Issues

**"Not authenticated" errors:**
- Check JWT token is in Authorization header
- Verify token hasn't expired
- Re-login to get fresh token

**"Permission denied" errors:**
- Verify RLS policies are enabled
- Check user owns the resource they're accessing

### Database Issues

**Profile not created after signup:**
- Check trigger exists: `on_auth_user_created`
- Verify trigger function: `handle_new_user()`
- Check Supabase logs for errors

**Users can see other users' data:**
- **CRITICAL:** Enable RLS on all tables
- Verify RLS policies are created correctly

### Application Issues

**File upload fails:**
- Check file size (max 50MB)
- Verify file format (CSV, Excel, JSON, Parquet)
- Check server logs

**AI not responding:**
- Verify at least one AI API key is set (GEMINI_API_KEY or GROQ_API_KEY)
- Check API key is valid
- Review backend logs for errors

---

## Quick Reference

### Key URLs

| Service | URL |
|---------|-----|
| Google Cloud Console | https://console.cloud.google.com/ |
| Supabase Dashboard | https://app.supabase.com/ |
| Gemini API Keys | https://makersuite.google.com/app/apikey |
| Groq API Keys | https://console.groq.com/keys |

### Important File Locations

- Frontend: `client/src/`
- Backend API: `server/`
- Python Backend: `python_backend/`
- Database Schema: `shared/schema.ts`

---

## Getting Help

If you encounter issues:

1. Check this documentation
2. Review application logs in Replit
3. Check Supabase logs in dashboard
4. Verify all environment variables are set
5. Test locally with same configuration

---

**For the latest information, see the project repository.**
