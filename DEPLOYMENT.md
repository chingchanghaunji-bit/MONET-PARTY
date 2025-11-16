# 🚀 CYBERPASS - Deployment Guide

## ✅ Code Pushed to GitHub
Repository: `https://github.com/chingchanghaunji-bit/MONET-PARTY.git`

## 🌐 Hosting Options

### Option 1: Render.com (Recommended - Free Tier Available)

#### Step 1: Create Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended)

#### Step 2: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub account
3. Select repository: `chingchanghaunji-bit/MONET-PARTY`
4. Branch: `main`

#### Step 3: Configure Settings
- **Name**: `cyberpass` (or your choice)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: `party_entry_app`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

#### Step 4: Environment Variables
Add these in **Environment** section:
```
FLASK_ENV=production
FLASK_DEBUG=False
PORT=10000
HOST=0.0.0.0
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password
```

#### Step 5: Deploy
- Click **"Create Web Service"**
- Wait for deployment (5-10 minutes)
- Your site will be live at: `https://cyberpass.onrender.com` (or your custom name)

---

### Option 2: Railway.app (Free Tier Available)

#### Step 1: Create Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

#### Step 2: New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose: `MONET-PARTY`

#### Step 3: Configure
- Railway auto-detects Python
- **Root Directory**: Set to `party_entry_app`
- **Start Command**: `python app.py`

#### Step 4: Environment Variables
Add in **Variables** tab:
```
FLASK_ENV=production
PORT=10000
HOST=0.0.0.0
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password
```

#### Step 5: Deploy
- Railway auto-deploys
- Get your URL: `https://your-app.railway.app`

---

### Option 3: Heroku (Paid - $5/month minimum)

#### Step 1: Install Heroku CLI
Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

#### Step 2: Login
```bash
heroku login
```

#### Step 3: Create App
```bash
cd party_entry_app
heroku create cyberpass
```

#### Step 4: Set Environment Variables
```bash
heroku config:set FLASK_ENV=production
heroku config:set PORT=10000
heroku config:set HOST=0.0.0.0
heroku config:set MAIL_USERNAME=your-email@gmail.com
heroku config:set MAIL_PASSWORD=your-app-password
heroku config:set ADMIN_USERNAME=admin
heroku config:set ADMIN_PASSWORD=your-secure-password
```

#### Step 5: Deploy
```bash
git push heroku main
```

---

## 📧 Email Configuration (Gmail)

### Step 1: Enable 2-Factor Authentication
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification

### Step 2: Generate App Password
1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select **"Mail"** and **"Other (Custom name)"**
3. Name it: `Cyberpass`
4. Copy the 16-character password
5. Use this in `MAIL_PASSWORD` environment variable

---

## 🔒 Security Checklist

- [ ] Change default admin credentials
- [ ] Use strong admin password
- [ ] Set up email with app password (not regular password)
- [ ] Enable HTTPS (automatic on Render/Railway)
- [ ] Keep environment variables secret
- [ ] Don't commit `.env` file to GitHub

---

## 🎯 Quick Deploy Commands

### Render.com
1. Sign up → New Web Service
2. Connect GitHub → Select repo
3. Set Root Directory: `party_entry_app`
4. Build: `pip install -r requirements.txt`
5. Start: `python app.py`
6. Add environment variables
7. Deploy!

### Railway.app
1. Sign up → New Project
2. Deploy from GitHub
3. Set Root Directory: `party_entry_app`
4. Add environment variables
5. Auto-deploys!

---

## 🐛 Troubleshooting

### Port Issues
- Ensure `PORT` env var is set (Render uses 10000, Railway auto-assigns)
- Check `HOST=0.0.0.0` is set

### Database Issues
- SQLite database is created automatically
- Database persists on Render/Railway

### Email Not Sending
- Verify app password (not regular password)
- Check SMTP settings
- Test email credentials locally first

### Build Fails
- Check `requirements.txt` is up to date
- Verify Python version in `runtime.txt`
- Check build logs for errors

---

## 📝 Post-Deployment

1. **Test Registration**: Register a test user
2. **Test Admin Login**: Login with admin credentials
3. **Test Email**: Verify emails are sending
4. **Test QR Code**: Generate and scan QR codes
5. **Test Verification**: Verify tickets work

---

## 🔗 Your Live URLs

After deployment, you'll get:
- **Main Site**: `https://your-app.onrender.com` (or railway.app)
- **Admin Panel**: `https://your-app.onrender.com/admin/login`

---

## 📞 Support

If you encounter issues:
1. Check deployment logs
2. Verify environment variables
3. Test locally first
4. Check hosting platform status

---

**🎮 Your cyberpunk party entry system is ready to go live! ⚡**

