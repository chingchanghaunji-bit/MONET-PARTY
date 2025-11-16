# 🚀 Hosting Guide - Render.com

## Step 1: Code is Now on GitHub ✅

Your code should be on GitHub at:
https://github.com/chingchanghaunji-bit/MONET-PARTY

## Step 2: Deploy to Render.com (FREE)

### Quick Steps:

1. **Sign Up:**
   - Go to: https://render.com
   - Click "Get Started for Free"
   - Sign up with GitHub (recommended)

2. **Create New Web Service:**
   - Click "New +" button
   - Select "Web Service"
   - Click "Connect GitHub" (if not connected)
   - Authorize Render to access your GitHub
   - Select repository: `MONET-PARTY`
   - Click "Connect"

3. **Configure Service:**
   ```
   Name: monet-party (or any name)
   Region: Choose closest to you
   Branch: main
   Root Directory: (leave empty)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   ```

4. **Add Environment Variables:**
   Click "Add Environment Variable" and add these:
   ```
   SECRET_KEY = (any random string, e.g., "monet-party-secret-key-2024")
   ADMIN_USER = admin
   ADMIN_PASS = (choose a secure password)
   PORT = 5000
   HOST = 0.0.0.0
   FLASK_DEBUG = False
   ```

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Render will build and deploy your app

6. **Get Your URL:**
   - After deployment, you'll get a URL like:
   - `https://monet-party.onrender.com`
   - Or: `https://monet-party-xxxx.onrender.com`

## Step 3: Access Your Website

Once deployed, your website will be live at:
- **Home:** https://your-app-name.onrender.com
- **Admin:** https://your-app-name.onrender.com/admin/login
  - Username: `admin`
  - Password: (the one you set in environment variables)

## Alternative: Railway.app (Also FREE)

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
   - Add the same variables as above

4. **Get URL:**
   - Railway will give you a URL automatically

## Troubleshooting

### Build Failed:
- Check build logs in Render/Railway dashboard
- Make sure `requirements.txt` exists
- Verify all files are on GitHub

### Application Error:
- Check environment variables are set correctly
- Check application logs
- Make sure PORT and HOST are set

### Can't Connect to GitHub:
- Make sure repository is public (or connected GitHub account)
- Verify repository exists: https://github.com/chingchanghaunji-bit/MONET-PARTY

## After Deployment

Your website will be live and accessible from anywhere!

**Features:**
- ✅ Modern UI with dark theme
- ✅ Admin dashboard
- ✅ QR code generation
- ✅ Ticket verification
- ✅ User management

---

**Need Help?** Check the logs in your hosting dashboard for specific error messages.


