# DataLix AI - Render Deployment Guide

This guide will walk you through deploying DataLix AI to Render.com, a modern cloud platform that simplifies deploying full-stack applications.

## Prerequisites

- A Render account ([Sign up here](https://render.com))
- A Supabase account with a configured database
- API keys for AI providers (Google Gemini and/or Groq)
- Git repository with your DataLix AI code

## Architecture Overview

DataLix AI consists of two services that need to be deployed:

1. **Web Service** (Node.js/React) - Port 5000
   - Frontend React application
   - Express backend server
   - Proxies requests to Python backend

2. **Python Backend Service** (FastAPI) - Port 8001
   - Data processing and AI chat functionality
   - Handles file uploads and analysis

## Deployment Steps

### Step 1: Set Up Supabase Database

1. Log in to your Supabase account
2. Create a new project or use an existing one
3. Navigate to **SQL Editor**
4. Run the initialization script from `init_database_with_rls.sql`
5. Collect the following credentials from **Project Settings > API**:
   - Project URL (SUPABASE_URL)
   - Anon/Public Key (SUPABASE_ANON_KEY)
   - Service Role Key (SUPABASE_SERVICE_ROLE_KEY)
6. Get the database connection string from **Project Settings > Database**:
   - Connection string (DATABASE_URL)

### Step 2: Deploy Python Backend Service

1. **Create Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click **New +** → **Web Service**
   - Connect your Git repository

2. **Configure Service Settings**
   ```
   Name: datalix-python-backend
   Region: Choose closest to your users
   Branch: main
   Root Directory: python_backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port 8001
   Instance Type: Starter (or higher for production)
   ```

3. **Add Environment Variables**
   Click **Advanced** → **Add Environment Variable**:
   ```
   SUPABASE_URL=your-supabase-project-url
   SUPABASE_ANON_KEY=your-supabase-anon-key
   SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
   DATABASE_URL=your-postgres-connection-string
   GEMINI_API_KEY=your-gemini-api-key (optional)
   GROQ_API_KEY=your-groq-api-key (optional)
   PORT=8001
   ```

   **Note:** You must provide at least ONE AI provider key (GEMINI_API_KEY or GROQ_API_KEY)

4. **Deploy**
   - Click **Create Web Service**
   - Wait for the build to complete (5-10 minutes)
   - Note the service URL (e.g., `https://datalix-python-backend.onrender.com`)

### Step 3: Deploy Main Web Service

1. **Create Second Web Service**
   - Return to Render Dashboard
   - Click **New +** → **Web Service**
   - Connect the same Git repository

2. **Configure Service Settings**
   ```
   Name: datalix-web
   Region: Same as Python backend
   Branch: main
   Root Directory: (leave blank - uses repository root)
   Runtime: Node
   Build Command: npm install && npm run build
   Start Command: npm start
   Instance Type: Starter (or higher for production)
   ```

3. **Add Environment Variables**
   ```
   NODE_ENV=production
   PORT=5000
   DATABASE_URL=your-postgres-connection-string
   SUPABASE_URL=your-supabase-project-url
   SUPABASE_ANON_KEY=your-supabase-anon-key
   SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
   VITE_SUPABASE_URL=your-supabase-project-url
   VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
   PYTHON_BACKEND_URL=https://datalix-python-backend.onrender.com
   ```

   **Important:** Replace `PYTHON_BACKEND_URL` with your actual Python backend URL from Step 2

4. **Deploy**
   - Click **Create Web Service**
   - Wait for the build to complete (10-15 minutes)
   - Your application will be available at the provided URL

### Step 4: Configure CORS (if needed)

If you encounter CORS issues, update `python_backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-render-web-service.onrender.com",
        "http://localhost:5000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Step 5: Test Your Deployment

1. Visit your main web service URL
2. Create an account
3. Upload a sample dataset
4. Test the chat functionality
5. Verify AI responses are working

## Environment Variables Reference

### Required for Both Services

| Variable | Description | Example |
|----------|-------------|---------|
| `SUPABASE_URL` | Your Supabase project URL | `https://xxxxx.supabase.co` |
| `SUPABASE_ANON_KEY` | Supabase anonymous/public key | `eyJhbGc...` |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key | `eyJhbGc...` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |

### Python Backend Only

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | One AI provider required |
| `GROQ_API_KEY` | Groq API key | One AI provider required |
| `PORT` | Backend service port | No (defaults to 8001) |

### Web Service Only

| Variable | Description | Required |
|----------|-------------|----------|
| `NODE_ENV` | Node environment | Yes (set to `production`) |
| `PORT` | Web service port | Yes (set to `5000`) |
| `VITE_SUPABASE_URL` | Frontend Supabase URL | Yes |
| `VITE_SUPABASE_ANON_KEY` | Frontend Supabase key | Yes |
| `PYTHON_BACKEND_URL` | Python backend URL | Yes |

## Common Issues & Solutions

### Issue: Build Fails with "Module not found"

**Solution:** Clear build cache and redeploy
- Go to service settings
- Click **Manual Deploy** → **Clear build cache & deploy**

### Issue: Python Backend Times Out

**Solution:** Increase instance size
- Free tier may be too slow for ML operations
- Upgrade to Starter or Standard instance type

### Issue: Sessions Not Persisting

**Solution:** Verify DATABASE_URL is set correctly
- Check Supabase connection string format
- Ensure database has proper tables (run init script)

### Issue: AI Chat Not Working

**Solution:** Verify AI provider keys
- Check GEMINI_API_KEY or GROQ_API_KEY is set
- Verify keys are valid in provider dashboard
- Check Python backend logs for errors

### Issue: File Uploads Failing

**Solution:** Check file size limits
- Render has default request size limits
- For large files, consider Render's disk storage

## Performance Optimization

### 1. Enable Build Caching
Render automatically caches dependencies between builds.

### 2. Use Environment-Specific Plans
- **Development:** Free tier is sufficient for testing
- **Production:** Starter or Standard for reliability

### 3. Database Connection Pooling
Already configured in the application via Supabase.

### 4. Static Asset Optimization
Build command includes Vite optimization:
```bash
npm run build
```

## Monitoring & Logs

### View Logs
1. Go to your service dashboard
2. Click **Logs** tab
3. Monitor real-time application logs

### Set Up Alerts
1. Navigate to service settings
2. Configure notification preferences
3. Set up email/Slack alerts for errors

## Updating Your Deployment

### Automatic Deploys (Recommended)
Render automatically deploys when you push to your branch:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

### Manual Deploy
1. Go to service dashboard
2. Click **Manual Deploy**
3. Select **Deploy latest commit**

## Custom Domain Setup

1. Go to service **Settings**
2. Scroll to **Custom Domain**
3. Click **Add Custom Domain**
4. Follow DNS configuration instructions
5. Wait for SSL certificate provisioning

## Security Best Practices

1. **Never commit secrets to Git**
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Use strong Supabase service keys**
   - Rotate keys periodically
   - Restrict database access via RLS policies

3. **Enable HTTPS only**
   - Render provides free SSL certificates
   - Force HTTPS redirects

4. **Implement rate limiting**
   - Already configured in the application
   - Monitor usage in Render dashboard

## Cost Estimation

### Free Tier (for testing)
- 750 hours/month per service
- Sleeps after inactivity
- Limited resources

### Starter Plan (recommended for production)
- $7/month per service ($14 total)
- Always-on
- Better performance

### Standard Plan (for scale)
- $25/month per service ($50 total)
- Enhanced resources
- Priority support

## Support & Resources

- [Render Documentation](https://render.com/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [DataLix AI Documentation](./DOCUMENTATION.md)
- [GitHub Issues](https://github.com/yourusername/datalix-ai/issues)

## Next Steps After Deployment

1. Set up monitoring and alerts
2. Configure custom domain (optional)
3. Test all features thoroughly
4. Set up backup strategy for database
5. Document deployment-specific configurations
6. Share application URL with users

---

**Deployed successfully?** You now have a production-ready DataLix AI instance running on Render! 🚀
