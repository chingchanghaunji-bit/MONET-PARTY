# 🚀 Render Deployment Guide

Complete step-by-step guide to deploy your Party Entry System on Render.

---

## 📋 Prerequisites

1. **GitHub Account** - Your code is already on GitHub: `https://github.com/chingchanghaunji-bit/MONET-PARTY.git`
2. **Render Account** - Sign up at [render.com](https://render.com) (free tier available)
3. **GitHub Repository** - Ensure all code is pushed to the `main` branch

---

## 🎯 Step 1: Create Render Account

1. Go to [https://render.com](https://render.com)
2. Click **"Get Started for Free"** or **"Sign Up"**
3. Sign up with your **GitHub account** (recommended - easier integration)
4. Authorize Render to access your GitHub repositories

---

## 🎯 Step 2: Create New Web Service

1. In Render Dashboard, click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your GitHub account if not already connected
4. Find and select your repository: **`chingchanghaunji-bit/MONET-PARTY`**
5. Click **"Connect"**

---

## 🎯 Step 3: Configure Web Service

Fill in the following settings:

### Basic Settings:
- **Name:** `monet-party` (or any name you prefer)
- **Region:** Choose closest to your users (e.g., `Oregon (US West)`)
- **Branch:** `main` (should be auto-selected)
- **Root Directory:** Leave **EMPTY** (your app is at root level)
- **Runtime:** `Python 3` (auto-detected)
- **Build Command:** Leave **EMPTY** (Render auto-detects from `requirements.txt`)
- **Start Command:** Leave **EMPTY** (Render uses `Procfile` which contains: `web: python app.py`)

### Advanced Settings (Optional):
- **Auto-Deploy:** `Yes` (deploys automatically on git push)
- **Health Check Path:** Leave empty (or use `/`)

---

## 🎯 Step 4: Set Environment Variables

Click on **"Environment"** tab or scroll down to **"Environment Variables"** section.

Click **"Add Environment Variable"** for each of the following:

### Required Environment Variables:

#### 1. SECRET_KEY (REQUIRED)
```
Key: SECRET_KEY
Value: [Generate a secure random string - see below]
```

**How to generate SECRET_KEY:**
- Option 1: Run in terminal: `python -c "import secrets; print(secrets.token_hex(32))"`
- Option 2: Use any secure random string (at least 32 characters)
- Option 3: Use online generator: https://randomkeygen.com/

**Example:**
```
SECRET_KEY = a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

#### 2. ADMIN_USER (Optional - Recommended)
```
Key: ADMIN_USER
Value: admin
```
Or use your preferred admin username.

#### 3. ADMIN_PASS (Optional - Recommended)
```
Key: ADMIN_PASS
Value: [Your secure password]
```
⚠️ **IMPORTANT:** Change from default `admin123` for security!

### Optional Environment Variables (For Email):

If you want email functionality, add these:

#### 4. MAIL_SERVER
```
Key: MAIL_SERVER
Value: smtp-relay.brevo.com
```
(Or your SMTP server)

#### 5. MAIL_PORT
```
Key: MAIL_PORT
Value: 587
```

#### 6. MAIL_USE_TLS
```
Key: MAIL_USE_TLS
Value: True
```

#### 7. MAIL_USERNAME
```
Key: MAIL_USERNAME
Value: your-email@example.com
```

#### 8. MAIL_PASSWORD
```
Key: MAIL_PASSWORD
Value: your-smtp-password
```

### Environment Variables Summary:

**Minimum Required:**
```
SECRET_KEY = [your-secret-key-here]
```

**Recommended:**
```
SECRET_KEY = [your-secret-key-here]
ADMIN_USER = admin
ADMIN_PASS = [your-secure-password]
```

**Full Configuration (with email):**
```
SECRET_KEY = [your-secret-key-here]
ADMIN_USER = admin
ADMIN_PASS = [your-secure-password]
MAIL_SERVER = smtp-relay.brevo.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = your-email@example.com
MAIL_PASSWORD = your-smtp-password
```

---

## 🎯 Step 5: Deploy

1. Review all settings
2. Click **"Create Web Service"** button at the bottom
3. Render will start building your application
4. Watch the build logs - it should show:
   - Installing dependencies from `requirements.txt`
   - Building the application
   - Starting the service

---

## 🎯 Step 6: Wait for Deployment

1. **Build Phase:** Takes 2-5 minutes
   - Installing Python packages
   - Setting up environment
   
2. **Deploy Phase:** Takes 1-2 minutes
   - Starting the Flask application
   - Health checks

3. **Status:** Changes from "Building" → "Live" (green)

---

## 🎯 Step 7: Access Your Website

Once deployment is complete:

1. You'll see a **URL** like: `https://monet-party.onrender.com`
2. Click the URL or copy it
3. Your website is now live! 🎉

### Test Your Deployment:

- **Home Page:** `https://your-app.onrender.com/`
- **Register:** `https://your-app.onrender.com/register`
- **Admin Login:** `https://your-app.onrender.com/admin/login`
  - Username: `admin` (or your ADMIN_USER)
  - Password: `admin123` (or your ADMIN_PASS)

---

## 🔧 Troubleshooting

### Build Fails:

1. **Check Build Logs:**
   - Click on your service → "Logs" tab
   - Look for error messages

2. **Common Issues:**
   - Missing dependencies → Check `requirements.txt`
   - Python version mismatch → Check `runtime.txt` (should be `python-3.12.0`)
   - Syntax errors → Check build logs for specific file/line

### App Crashes After Deployment:

1. **Check Runtime Logs:**
   - Click on your service → "Logs" tab
   - Look for runtime errors

2. **Common Issues:**
   - Missing `SECRET_KEY` → Add it in Environment Variables
   - Database errors → SQLite should work automatically
   - Port issues → Render sets PORT automatically, don't override

### Admin Panel Not Working:

1. **Check Environment Variables:**
   - Ensure `SECRET_KEY` is set (required for sessions)
   - Verify `ADMIN_USER` and `ADMIN_PASS` are correct

2. **Clear Browser Cache:**
   - Try incognito/private window
   - Clear cookies for the site

### Phone Number Input Issues:

- Already fixed in latest code!
- Should work correctly on deployed site

---

## 📝 Environment Variables Format Reference

### Format in Render Dashboard:

When adding environment variables in Render, use this format:

```
Key: SECRET_KEY
Value: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

**No quotes needed** - Render handles the values as strings automatically.

### Example .env File (for local development):

If you want to test locally with the same settings, create a `.env` file:

```env
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
ADMIN_USER=admin
ADMIN_PASS=your-secure-password
MAIL_SERVER=smtp-relay.brevo.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-smtp-password
```

⚠️ **Note:** Never commit `.env` file to Git (it's in `.gitignore`)

---

## 🔄 Updating Your Deployment

### Automatic Updates:
- If **Auto-Deploy** is enabled (default), Render automatically deploys when you push to `main` branch
- Just push your changes: `git push origin main`
- Render will rebuild and redeploy automatically

### Manual Deploy:
1. Go to Render Dashboard
2. Click on your service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 📊 Monitoring

### View Logs:
1. Click on your service in Render Dashboard
2. Click **"Logs"** tab
3. View real-time logs or download log history

### Metrics:
- View CPU, Memory usage
- Request metrics
- Response times

---

## 💰 Pricing

**Free Tier Includes:**
- 750 hours/month (enough for 24/7 operation)
- 512 MB RAM
- Sleeps after 15 minutes of inactivity (wakes on first request)
- Free SSL certificate
- Custom domain support

**Upgrade Options:**
- Starter: $7/month - No sleep, more resources
- Professional: $25/month - Better performance

---

## ✅ Deployment Checklist

Before deploying, ensure:

- [x] Code is pushed to GitHub `main` branch
- [x] `Procfile` exists with: `web: python app.py`
- [x] `requirements.txt` has all dependencies
- [x] `runtime.txt` specifies Python version
- [x] `SECRET_KEY` environment variable is set
- [x] `ADMIN_USER` and `ADMIN_PASS` are set (recommended)
- [x] All code changes are committed

---

## 🎉 Success!

Once deployed, your website will be:
- ✅ Live and accessible 24/7
- ✅ Automatically updated on git push
- ✅ Secured with HTTPS (free SSL)
- ✅ Monitored with logs and metrics

**Your website URL:** `https://your-app-name.onrender.com`

---

## 📞 Need Help?

1. Check Render documentation: https://render.com/docs
2. View build/runtime logs in Render Dashboard
3. Check GitHub issues or create a new one

---

**Last Updated:** Based on latest code in repository
**Repository:** https://github.com/chingchanghaunji-bit/MONET-PARTY

