# 🚀 Complete Deployment Guide

## Step 1: Install Git (REQUIRED)

**Download Git:**
- Go to: https://git-scm.com/download/win
- Download "64-bit Git for Windows Setup"
- Run the installer
- **IMPORTANT:** Check "Add Git to PATH" during installation
- Restart your computer after installation

**Verify Installation:**
Open PowerShell and type:
```powershell
git --version
```
You should see a version number like `git version 2.43.0`

## Step 2: Push Code to GitHub

### Method A: Using the Batch File (Easiest)

1. **After installing Git**, go to `party_entry_app` folder
2. **Double-click** `PUSH_TO_GITHUB.bat`
3. Follow the prompts

### Method B: Manual Push (Step by Step)

Open PowerShell in the `party_entry_app` folder:

```powershell
# Step 1: Initialize Git
git init

# Step 2: Add remote repository
git remote add origin https://github.com/chingchanghaunji-bit/MONET-PARTY.git

# Step 3: Add all files
git add .

# Step 4: Commit
git commit -m "Initial commit: Party Entry System"

# Step 5: Set main branch
git branch -M main

# Step 6: Push (you'll need GitHub credentials)
git push -u origin main
```

**For GitHub Authentication:**
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your password)
- Create token: https://github.com/settings/tokens
  - Click "Generate new token (classic)"
  - Select scopes: `repo` (full control)
  - Copy the token and use it as password

## Step 3: Verify Code is on GitHub

1. Go to: https://github.com/chingchanghaunji-bit/MONET-PARTY
2. You should see your files (app.py, templates/, static/, etc.)
3. If you see "No description" or empty repository, the push didn't work

## Step 4: Deploy to Render.com (FREE)

### Detailed Steps:

1. **Sign Up:**
   - Go to: https://render.com
   - Click "Get Started for Free"
   - Sign up with GitHub (recommended)

2. **Create New Web Service:**
   - Click "New +" button
   - Select "Web Service"
   - Click "Connect GitHub account" (if not connected)
   - Select repository: `MONET-PARTY`
   - Click "Connect"

3. **Configure Service:**
   - **Name:** monet-party (or any name)
   - **Region:** Choose closest to you
   - **Branch:** main
   - **Root Directory:** (leave empty)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`

4. **Environment Variables:**
   Click "Add Environment Variable" and add:
   ```
   SECRET_KEY = (any random string, e.g., "my-secret-key-12345")
   ADMIN_USER = admin
   ADMIN_PASS = (your admin password)
   PORT = 5000
   HOST = 0.0.0.0
   FLASK_DEBUG = False
   ```

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your site will be at: `https://monet-party.onrender.com`

## Step 5: Alternative - Railway.app (FREE)

1. **Sign Up:**
   - Go to: https://railway.app
   - Click "Start a New Project"
   - Sign up with GitHub

2. **Deploy:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `MONET-PARTY` repository
   - Railway will auto-detect Flask

3. **Add Environment Variables:**
   - Click on your service
   - Go to "Variables" tab
   - Add the same variables as Render.com

4. **Get URL:**
   - Railway will give you a URL like: `https://monet-party-production.up.railway.app`

## Troubleshooting

### "Repository not found" Error:
- Make sure you've pushed code to GitHub first
- Check: https://github.com/chingchanghaunji-bit/MONET-PARTY
- Repository must be public (or you need to connect GitHub account)

### "Build failed" Error:
- Check the build logs in Render/Railway dashboard
- Make sure `requirements.txt` exists
- Make sure `app.py` is in the root directory

### "Application Error" after deployment:
- Check environment variables are set correctly
- Check logs in the hosting dashboard
- Make sure PORT and HOST are set correctly

### Code not on GitHub:
1. Make sure Git is installed
2. Make sure you're in the `party_entry_app` folder
3. Run the push commands again
4. Check GitHub website to verify files are there

## Quick Checklist

- [ ] Git installed and verified
- [ ] Code pushed to GitHub (check GitHub website)
- [ ] Signed up on Render.com or Railway.app
- [ ] Connected GitHub account
- [ ] Created web service
- [ ] Added environment variables
- [ ] Deployment successful
- [ ] Website URL working

---

**Need Help?** Check the logs in your hosting dashboard for specific error messages.

