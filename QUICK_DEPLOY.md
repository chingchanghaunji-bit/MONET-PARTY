# 🚀 Quick Deploy Guide

## Your GitHub Repo
✅ **Already pushed:** `https://github.com/chingchanghaunji-bit/MONET-PARTY.git`

---

## 🌐 Deploy to Render.com (Easiest - 5 minutes)

### Step 1: Sign Up
1. Go to **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (use your GitHub account)

### Step 2: Create Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your GitHub account (if not already)
4. Find and select: **`MONET-PARTY`** repository
5. Click **"Connect"**

### Step 3: Configure
Fill in these settings:

- **Name:** `cyberpass` (or any name you like)
- **Region:** Choose closest to you
- **Branch:** `main`
- **Root Directory:** `party_entry_app` ⚠️ **IMPORTANT!**
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app.py`

### Step 4: Environment Variables
Click **"Environment"** tab, then **"Add Environment Variable"** for each:

```
FLASK_ENV = production
FLASK_DEBUG = False
PORT = 10000
HOST = 0.0.0.0
SECRET_KEY = your-random-secret-key-here
ADMIN_USER = admin
ADMIN_PASS = your-secure-password-here
MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = your-email@gmail.com
MAIL_PASSWORD = your-gmail-app-password
```

**Note:** For Gmail, you need an **App Password** (not your regular password):
1. Go to https://myaccount.google.com/apppasswords
2. Generate a new app password
3. Use that 16-character password for `MAIL_PASSWORD`

### Step 5: Deploy!
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for build
3. Your site will be live at: **`https://cyberpass.onrender.com`** (or your custom name)

---

## 🚂 Deploy to Railway.app (Alternative)

### Step 1: Sign Up
1. Go to **https://railway.app**
2. Sign up with **GitHub**

### Step 2: New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose **`MONET-PARTY`**

### Step 3: Configure
1. Click on your service
2. Go to **"Settings"** tab
3. Set **Root Directory:** `party_entry_app`
4. **Start Command:** `python app.py`

### Step 4: Environment Variables
Go to **"Variables"** tab, add all the same variables as Render.com above.

### Step 5: Deploy
Railway auto-deploys! Your URL will be: **`https://your-app.railway.app`**

---

## ✅ After Deployment

Your website will be live at:
- **Main:** `https://your-app.onrender.com`
- **Admin:** `https://your-app.onrender.com/admin/login`

**Test it:**
1. Visit your live URL
2. Try registering a user
3. Login to admin panel
4. Test QR code generation

---

## 🆘 Need Help?

Check `DEPLOYMENT.md` for detailed troubleshooting!

