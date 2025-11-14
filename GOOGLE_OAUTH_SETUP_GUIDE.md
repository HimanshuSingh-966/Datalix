# Google OAuth Setup Guide for DataLix 2.0

This guide will walk you through setting up Google OAuth authentication with Supabase for DataLix 2.0.

## Prerequisites

- A Supabase project (you should already have this)
- A Google Cloud Platform account

---

## Part 1: Configure Google OAuth in Google Cloud Console

### Step 1: Create a Google Cloud Project (if you don't have one)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click "New Project"
4. Enter a project name (e.g., "DataLix 2.0")
5. Click "Create"

### Step 2: Enable Google OAuth

1. In Google Cloud Console, navigate to **APIs & Services** → **OAuth consent screen**
2. Choose **External** (unless you have a Google Workspace account)
3. Click **Create**

### Step 3: Configure OAuth Consent Screen

Fill in the required information:

- **App name**: DataLix 2.0
- **User support email**: Your email address
- **App logo**: (Optional) Upload your app logo
- **App domain**: (Optional for development)
- **Authorized domains**: (Leave empty for local development)
- **Developer contact email**: Your email address

Click **Save and Continue**

### Step 4: Configure Scopes

1. Click **Add or Remove Scopes**
2. Add these scopes:
   - `.../auth/userinfo.email`
   - `.../auth/userinfo.profile`
3. Click **Update** then **Save and Continue**

### Step 5: Add Test Users (for development)

1. Click **Add Users**
2. Add your email address and any other test users
3. Click **Save and Continue**

### Step 6: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **+ Create Credentials** → **OAuth client ID**
3. Choose **Web application**
4. Configure the following:

   **Name**: DataLix Web Client

   **Authorized JavaScript origins**:
   - For local development: `http://localhost:5000`
   - For Replit: `https://YOUR-REPL-NAME.YOUR-USERNAME.repl.co` or your custom domain

   **Authorized redirect URIs**:
   - **Important**: Add your Supabase callback URL
   - Format: `https://YOUR-PROJECT-ID.supabase.co/auth/v1/callback`
   - Example: `https://abcdefghijklmnop.supabase.co/auth/v1/callback`
   
   To find your Supabase project URL:
   - Go to your Supabase Dashboard
   - Click on your project
   - Go to **Settings** → **API**
   - Copy the "URL" (it looks like `https://xxxxx.supabase.co`)
   - Add `/auth/v1/callback` to the end

5. Click **Create**

### Step 7: Save Your Credentials

You'll see a dialog with:
- **Client ID**: Looks like `123456789-abc123.apps.googleusercontent.com`
- **Client Secret**: Looks like `GOCSPX-abc123...`

**Important**: Copy both of these - you'll need them for Supabase configuration!

---

## Part 2: Configure Google OAuth in Supabase

### Step 1: Access Supabase Dashboard

1. Go to [Supabase Dashboard](https://app.supabase.com/)
2. Select your DataLix project

### Step 2: Enable Google Provider

1. Navigate to **Authentication** → **Providers**
2. Find **Google** in the list
3. Toggle it **ON**

### Step 3: Configure Google Provider

Enter the credentials from Google Cloud Console:

1. **Client ID**: Paste the Client ID from Step 7 above
2. **Client Secret**: Paste the Client Secret from Step 7 above
3. **Authorized Client IDs** (optional): Leave empty for now
4. Click **Save**

### Step 4: Configure Redirect URLs

1. Still in **Authentication** settings, go to **URL Configuration**
2. Add your application URLs to **Site URL**:
   - For local development: `http://localhost:5000`
   - For Replit: Your Replit URL (e.g., `https://your-repl.replit.app`)
3. Add redirect URLs to **Redirect URLs**:
   - `http://localhost:5000/api/auth/callback`
   - `https://your-repl.replit.app/api/auth/callback`
4. Click **Save**

---

## Part 3: Update Your Environment Variables

Make sure your Replit Secrets include:

1. **SUPABASE_URL**: Your Supabase project URL
   - Example: `https://abcdefghijklmnop.supabase.co`

2. **SUPABASE_ANON_KEY**: Your Supabase anon/public key
   - Found in: Supabase Dashboard → Settings → API → Project API keys → `anon` `public`

3. **SUPABASE_SERVICE_ROLE_KEY**: Your Supabase service role key
   - Found in: Supabase Dashboard → Settings → API → Project API keys → `service_role`
   - ⚠️ **Warning**: This key has full access - keep it secret!

4. **REPL_SLUG** (automatically set by Replit): Your Replit app URL

---

## Part 4: Test Google OAuth

### Test Flow

1. Restart your application (the workflow should auto-restart)
2. Go to the authentication page
3. Click **"Continue with Google"**
4. You should be redirected to Google's sign-in page
5. Select your Google account
6. Grant permissions
7. You'll be redirected back to DataLix and automatically signed in!

### Troubleshooting

#### Error: "redirect_uri_mismatch"

**Problem**: The redirect URI doesn't match what's configured in Google Console.

**Solution**:
1. Check that you added `https://YOUR-PROJECT-ID.supabase.co/auth/v1/callback` to Google Console
2. Make sure there are no typos or extra spaces
3. The URLs must match exactly

#### Error: "Access blocked: This app's request is invalid"

**Problem**: OAuth consent screen not properly configured.

**Solution**:
1. Go back to Google Cloud Console → OAuth consent screen
2. Make sure you added the required scopes
3. Add yourself as a test user if the app is in "Testing" mode

#### Error: "Invalid client: no application name"

**Problem**: OAuth consent screen is incomplete.

**Solution**:
1. Complete all required fields in the OAuth consent screen
2. Make sure App name and Support email are filled in

#### No redirect after Google sign-in

**Problem**: Redirect URLs not configured in Supabase.

**Solution**:
1. Go to Supabase Dashboard → Authentication → URL Configuration
2. Add your app URL to Redirect URLs
3. Include both local and production URLs

#### "Email not confirmed" error

**Problem**: This is for email/password auth, not OAuth.

**Solution**:
- Google OAuth doesn't require email confirmation
- The email is already verified by Google
- If you see this, you're not using the OAuth flow correctly

---

## Part 5: Production Deployment

When deploying to production:

1. **Update Google Console**:
   - Add your production domain to Authorized JavaScript origins
   - Add your production callback URL to Authorized redirect URIs

2. **Update Supabase**:
   - Add your production URL to Redirect URLs
   - Update Site URL to your production domain

3. **Publish your OAuth Consent Screen**:
   - Go to Google Cloud Console → OAuth consent screen
   - Click "Publish App"
   - Submit for verification if needed (for production apps)

---

## Part 6: Features Enabled

With Google OAuth, users can:

✅ Sign in with one click using their Google account
✅ No need to create a password
✅ Email is automatically verified (by Google)
✅ Profile information (name, email, photo) automatically imported
✅ Seamless authentication experience

---

## Security Notes

1. **Never commit secrets**: Keep your Client Secret and Service Role Key secure
2. **HTTPS in production**: Always use HTTPS for production OAuth flows
3. **Validate redirect URLs**: Only whitelist your own domains
4. **Row Level Security**: Enable RLS on your Supabase tables
5. **Limit scopes**: Only request the Google scopes you actually need

---

## Quick Reference

### Key URLs to Configure

| Service | Setting | Value |
|---------|---------|-------|
| Google Console | Authorized JavaScript origins | `http://localhost:5000`, `https://your-repl.replit.app` |
| Google Console | Authorized redirect URIs | `https://YOUR-PROJECT.supabase.co/auth/v1/callback` |
| Supabase | Site URL | `https://your-repl.replit.app` |
| Supabase | Redirect URLs | `http://localhost:5000/api/auth/callback`, `https://your-repl.replit.app/api/auth/callback` |

### Getting Help

If you encounter issues:

1. Check the browser console for errors
2. Check the Python backend logs
3. Verify all URLs match exactly (no trailing slashes, correct protocol)
4. Make sure Google OAuth is enabled in Supabase
5. Confirm you added yourself as a test user in Google Console

---

## What's Next?

Now that Google OAuth is configured, you can:

1. Test the sign-in flow
2. Add additional OAuth providers (GitHub, Apple, etc.)
3. Customize the user profile with Google data
4. Implement role-based access control

Happy authenticating! 🎉
