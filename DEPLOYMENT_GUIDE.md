# DataLix AI Deployment Guide for Render

This guide will help you deploy your DataLix AI AI-powered data analysis platform to Render.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Supabase Database Setup](#supabase-database-setup)
4. [Render Deployment](#render-deployment)
5. [Environment Variables](#environment-variables)
6. [Post-Deployment](#post-deployment)
7. [Troubleshooting](#troubleshooting)

---

## Overview

DataLix AI is a full-stack application with:
- **Frontend**: React + Vite (served by Express)
- **Backend API**: Python FastAPI
- **Database**: PostgreSQL (Supabase)
- **AI**: Gemini API and/or Groq API

The deployment architecture:
```
[Render Web Service]
├── Node.js/Express (Port 5000) → Serves React frontend
│   └── Proxies /api/* → Python backend
└── Python FastAPI (Port 8001) → Handles data processing & AI
```

---

## Prerequisites

### 1. GitHub Repository
Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

**Important**: Add `.env` to `.gitignore`:
```
node_modules/
.env
python_backend/__pycache__/
.cache/
client/dist/
```

### 2. Required API Keys
You'll need at least ONE of these AI providers:
- **Gemini API Key** (Recommended): Get from https://makersuite.google.com/app/apikey
- **Groq API Key** (Alternative): Get from https://console.groq.com/keys

### 3. Supabase Account (Optional but Recommended)
- Create account at https://supabase.com
- For production-grade authentication and database

---

## Supabase Database Setup

### Option A: Using Supabase (Recommended for Production)

1. **Create a new Supabase project**
   - Go to https://database.new
   - Name your project (e.g., "datalix-prod")
   - Choose a strong database password
   - Select region closest to your users

2. **Set up database tables**
   
   Go to SQL Editor in Supabase dashboard and run:
   
   ```sql
   -- Create users table
   CREATE TABLE users (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       username TEXT NOT NULL UNIQUE,
       email TEXT NOT NULL UNIQUE,
       password TEXT NOT NULL,
       created_at TIMESTAMP NOT NULL DEFAULT NOW()
   );

   CREATE UNIQUE INDEX idx_users_username ON users(username);
   CREATE UNIQUE INDEX idx_users_email ON users(email);

   -- Create sessions table
   CREATE TABLE sessions (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
       name TEXT,
       created_at TIMESTAMP NOT NULL DEFAULT NOW(),
       updated_at TIMESTAMP NOT NULL DEFAULT NOW()
   );

   CREATE INDEX idx_sessions_user_id ON sessions(user_id);
   CREATE INDEX idx_sessions_updated_at ON sessions(updated_at DESC);

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

   CREATE INDEX idx_messages_session_id ON messages(session_id);
   CREATE INDEX idx_messages_created_at ON messages(created_at DESC);
   CREATE INDEX idx_messages_role ON messages(role);
   CREATE INDEX idx_messages_chart_data ON messages USING GIN (chart_data);
   CREATE INDEX idx_messages_data_preview ON messages USING GIN (data_preview);

   -- Create trigger to update sessions.updated_at
   CREATE OR REPLACE FUNCTION update_sessions_updated_at()
   RETURNS TRIGGER AS $$
   BEGIN
       NEW.updated_at = NOW();
       RETURN NEW;
   END;
   $$ LANGUAGE plpgsql;

   CREATE TRIGGER sessions_updated_at_trigger
       BEFORE UPDATE ON sessions
       FOR EACH ROW
       EXECUTE FUNCTION update_sessions_updated_at();
   ```

3. **Enable Row Level Security (RLS)** - IMPORTANT for user data isolation!

   ```sql
   -- Enable RLS on all tables
   ALTER TABLE users ENABLE ROW LEVEL SECURITY;
   ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
   ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

   -- Users can only see their own profile
   CREATE POLICY "Users can view own profile"
   ON users FOR SELECT
   USING (auth.uid()::text = id::text);

   -- Users can only see their own sessions
   CREATE POLICY "Users can view own sessions"
   ON sessions FOR SELECT
   USING (auth.uid()::text = user_id::text);

   CREATE POLICY "Users can create own sessions"
   ON sessions FOR INSERT
   WITH CHECK (auth.uid()::text = user_id::text);

   CREATE POLICY "Users can delete own sessions"
   ON sessions FOR DELETE
   USING (auth.uid()::text = user_id::text);

   -- Users can only see messages from their own sessions
   CREATE POLICY "Users can view own messages"
   ON messages FOR SELECT
   USING (
       EXISTS (
           SELECT 1 FROM sessions 
           WHERE sessions.id = messages.session_id 
           AND sessions.user_id = auth.uid()::text
       )
   );

   CREATE POLICY "Users can create messages in own sessions"
   ON messages FOR INSERT
   WITH CHECK (
       EXISTS (
           SELECT 1 FROM sessions 
           WHERE sessions.id = messages.session_id 
           AND sessions.user_id = auth.uid()::text
       )
   );
   ```

4. **Get your Supabase credentials**
   - Project Settings → API
   - Copy:
     - Project URL (`SUPABASE_URL`)
     - `anon` public key (`SUPABASE_ANON_KEY`)
     - `service_role` secret key (`SUPABASE_SERVICE_ROLE_KEY`)

### Option B: In-Memory Storage (Development Only)
- Skip Supabase setup
- Data will be lost on server restart
- Not recommended for production

---

## Render Deployment

### Step 1: Create Web Service

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click "New +" → "Web Service"

2. **Connect GitHub Repository**
   - Authorize Render to access your GitHub
   - Select your repository

3. **Configure Service**
   
   | Setting | Value |
   |---------|-------|
   | **Name** | `datalix-app` (or your choice) |
   | **Region** | Select closest to your users |
   | **Branch** | `main` |
   | **Root Directory** | Leave blank |
   | **Runtime** | Node |
   | **Build Command** | `npm install && npm run build && pip install -r python_backend/requirements.txt` |
   | **Start Command** | `npm start` |
   | **Plan** | Free (or paid for better performance) |

4. **Advanced Settings**
   - **Auto-Deploy**: Yes (recommended)

---

## Environment Variables

In Render Web Service → Environment → Add Environment Variables:

### Required Variables

```bash
# Node.js
NODE_ENV=production
PORT=5000

# AI Provider (at least ONE is required)
GEMINI_API_KEY=your_gemini_api_key_here
# OR
GROQ_API_KEY=your_groq_api_key_here

# Supabase (if using Supabase)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
```

### How to Add Variables in Render:

1. Go to your Web Service
2. Click "Environment" in left sidebar
3. Click "Add Environment Variable"
4. Enter key and value
5. Click "Save Changes"

**Important**: After adding all variables, click "Save Changes" and the service will automatically redeploy.

---

## Post-Deployment

### 1. Verify Deployment

Once deployed, your app will be available at:
```
https://your-app-name.onrender.com
```

### 2. Test the Application

1. **Access the app** → Should show login/signup page
2. **Create an account** → Test authentication
3. **Upload a dataset** (CSV, Excel, JSON, or Parquet)
4. **Send a message** → "Show me statistics"
5. **Verify AI response** → Should see charts/tables

### 3. Monitor Logs

In Render Dashboard → Your Service → Logs (left sidebar)

Look for:
```
✓ Gemini AI configured
✓ Supabase authentication enabled
Frontend server running on http://0.0.0.0:5000
Python backend exited with code 0
```

---

## Troubleshooting

### Problem: Build Fails

**Error**: `pip: command not found`

**Solution**: Render might need Python explicitly installed. Update build command:
```bash
npm install && npm run build && python3 -m pip install -r python_backend/requirements.txt
```

---

### Problem: Python Backend Not Starting

**Check logs for**:
```
Python backend exited with code 1
```

**Solutions**:
1. Verify `requirements.txt` exists in `python_backend/`
2. Check Python dependencies are compatible
3. Ensure PORT environment variable is set

---

### Problem: "Not authenticated" errors

**Causes**:
- Missing `Authorization` header in requests
- Invalid or expired token
- Supabase credentials incorrect

**Solutions**:
1. Check browser console for errors
2. Verify token is stored in localStorage
3. Re-login to get fresh token
4. Verify Supabase environment variables are correct

---

### Problem: Users Can See Each Other's Data

**This is a CRITICAL security issue!**

**Solution**: Ensure RLS policies are enabled in Supabase (see [Supabase Database Setup](#supabase-database-setup))

To verify:
1. Create two accounts
2. Upload data in account A
3. Login to account B
4. Check if you can see account A's sessions → Should be EMPTY

---

### Problem: AI Not Responding

**Check**:
1. At least one AI provider key is set (`GEMINI_API_KEY` or `GROQ_API_KEY`)
2. API key is valid (not expired/revoked)
3. Check logs for API errors

**Test API keys locally**:
```python
import google.generativeai as genai
genai.configure(api_key="YOUR_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Hello")
print(response.text)
```

---

### Problem: File Upload Fails

**Common causes**:
- File size too large (> 50MB)
- Unsupported file format
- Malformed CSV/Excel file

**Solutions**:
1. Check file is valid CSV, Excel, JSON, or Parquet
2. Try smaller file first
3. Check server logs for detailed error

---

### Problem: Slow Cold Starts (Free Tier)

**Symptom**: First request after 15 minutes takes 30-60 seconds

**Explanation**: Render free tier spins down services after inactivity

**Solutions**:
1. **Upgrade to paid tier** ($7/month) - no spin down
2. **Keep-alive service** - Ping your app every 14 minutes
3. **Accept the limitation** - First user sees loading spinner

Example keep-alive using cron-job.org:
- Create free account at https://cron-job.org
- Add job: `https://your-app.onrender.com/api/health` every 14 minutes

---

### Problem: Database Connection Errors

**Error**: `connection to server failed`

**Solutions**:
1. Verify `SUPABASE_URL` is correct
2. Check Supabase project is active (not paused)
3. Verify service role key has correct permissions
4. Check Supabase dashboard for outages

---

## Performance Optimization

### 1. Enable Caching
Add to Python backend (`main.py`):
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_operation(session_id: str):
    # Your code here
    pass
```

### 2. Database Indexing
Already included in SQL schema above. Verify indexes exist:
```sql
SELECT * FROM pg_indexes WHERE tablename IN ('users', 'sessions', 'messages');
```

### 3. Optimize Large Datasets
For datasets > 1M rows:
- Consider sampling data for visualizations
- Use pagination for data preview
- Implement lazy loading

---

## Scaling Considerations

### When to Upgrade

Consider paid tier ($7-25/month) when:
- **Users**: > 100 active users
- **Datasets**: Regularly processing > 100MB files
- **Requests**: > 1000 API calls/day
- **Uptime**: Need 100% availability (no cold starts)

### Horizontal Scaling

For high traffic:
1. **Separate Python backend** → Deploy as separate Render service
2. **Add Redis** → Cache statistics and visualizations
3. **Use CDN** → CloudFlare for static assets
4. **Database pooling** → Connection pooling for Supabase

---

## Security Checklist

Before going to production:

- [ ] RLS policies enabled in Supabase
- [ ] All secrets in environment variables (not code)
- [ ] HTTPS enabled (automatic on Render)
- [ ] CORS properly configured
- [ ] Input validation on all endpoints
- [ ] Rate limiting implemented
- [ ] Error messages don't expose sensitive data
- [ ] Dependencies updated (no known vulnerabilities)

---

## Backup Strategy

### Database Backups

**Supabase Free Tier**:
- Daily automatic backups (7 days retention)

**Supabase Pro Tier**:
- Point-in-time recovery
- 30 days retention

**Manual backup**:
```bash
# Export from Supabase dashboard
# Or use pg_dump
pg_dump -h db.xxx.supabase.co -U postgres -d postgres > backup.sql
```

---

## Monitoring

### Application Monitoring

1. **Render Logs** - Real-time application logs
2. **Supabase Logs** - Database query performance
3. **Error Tracking** - Consider Sentry for production

### Health Checks

Endpoint: `https://your-app.onrender.com/api/health`

Returns:
```json
{
  "status": "healthy",
  "python_version": "3.11"
}
```

---

## Cost Breakdown

### Free Tier (Suitable for MVP/Testing)
- Render Web Service: Free
- Supabase: Free (500MB database, 50,000 monthly active users)
- Gemini API: Free tier (60 requests/minute)
- **Total**: $0/month

**Limitations**:
- 15-minute spin down on inactivity
- Limited compute resources
- 90-day database retention (Render PostgreSQL)

### Paid Tier (Production Ready)
- Render Web Service: $7/month (Starter)
- Supabase Pro: $25/month (8GB database)
- Gemini API: Pay-as-you-go
- **Total**: ~$32/month + API usage

---

## Additional Resources

- **Render Docs**: https://render.com/docs
- **Supabase Docs**: https://supabase.com/docs
- **Gemini API**: https://ai.google.dev/docs
- **Groq API**: https://console.groq.com/docs

---

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review Render logs for errors
3. Verify all environment variables are set correctly
4. Test locally first with the same environment variables

---

## Quick Deploy Checklist

- [ ] Push code to GitHub
- [ ] Create Supabase project and run SQL setup
- [ ] Create Render Web Service
- [ ] Add all environment variables
- [ ] Wait for deployment to complete
- [ ] Test authentication
- [ ] Test file upload
- [ ] Test AI chat functionality
- [ ] Verify user data isolation
- [ ] Set up monitoring

---

**Congratulations!** Your DataLix AI application is now deployed and ready for use! 🎉
