# 🚀 DEPLOY YOUR WEBSITE NOW!

## ⚠️ IMPORTANT: GitHub Pages CANNOT Run Flask Apps!

**GitHub Pages** = Only static HTML/CSS/JS (no Python/Flask)  
**Your App** = Flask (needs a Python server)

**Solution:** Deploy to **Render.com** (FREE) - Takes 5 minutes!

---

## 📋 STEP-BY-STEP: Deploy to Render.com

### Step 1: Sign Up (1 minute)
1. Go to **https://render.com** (already opened in your browser)
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (use the same GitHub account)

### Step 2: Create Web Service (2 minutes)
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your GitHub account (if not already connected)
4. Find and select: **`MONET-PARTY`** repository
5. Click **"Connect"**

### Step 3: Configure Settings (1 minute)
Fill in these **EXACT** settings:

```
Name: cyberpass
Region: (choose closest to you)
Branch: main
Root Directory: party_entry_app  ⚠️ VERY IMPORTANT!
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python app.py
```

### Step 4: Add Environment Variables (1 minute)
Click **"Environment"** tab, then click **"Add Environment Variable"** for each:

**Copy and paste these one by one:**

```
FLASK_ENV = production
FLASK_DEBUG = False
PORT = 10000
HOST = 0.0.0.0
SECRET_KEY = change-this-to-random-string-12345
ADMIN_USER = admin
ADMIN_PASS = your-secure-password-here
MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = your-email@gmail.com
MAIL_PASSWORD = your-gmail-app-password
```

**For Gmail App Password:**
1. Go to: https://myaccount.google.com/apppasswords
2. Generate new app password
3. Copy the 16-character password
4. Use it for `MAIL_PASSWORD`

### Step 5: Deploy! (5-10 minutes)
1. Click **"Create Web Service"** button
2. Wait 5-10 minutes for build
3. Your site will be live at: **`https://cyberpass.onrender.com`**

---

## ✅ After Deployment

Your website URLs:
- **Main Site:** `https://cyberpass.onrender.com`
- **Admin Panel:** `https://cyberpass.onrender.com/admin/login`
  - Username: `admin`
  - Password: (whatever you set in ADMIN_PASS)

---

## 🎯 Quick Checklist

- [ ] Signed up on Render.com
- [ ] Connected GitHub account
- [ ] Selected MONET-PARTY repository
- [ ] Set Root Directory: `party_entry_app`
- [ ] Added all environment variables
- [ ] Clicked "Create Web Service"
- [ ] Waited for deployment (5-10 min)
- [ ] Tested the live URL!

---

## 🆘 Problems?

**Build fails?**
- Check Root Directory is `party_entry_app`
- Verify all environment variables are added

**Website shows error?**
- Check deployment logs in Render dashboard
- Verify PORT=10000 and HOST=0.0.0.0 are set

**Need help?**
- Check `DEPLOYMENT.md` for detailed troubleshooting

---

**🎮 Your cyberpunk party entry system will be LIVE in 10 minutes! ⚡**

