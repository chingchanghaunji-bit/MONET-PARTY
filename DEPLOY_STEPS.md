# 🚀 Complete Deployment Steps with Brevo

## ✅ Code Updated for Brevo SMTP!

Your code is now configured to use **Brevo** instead of Gmail. All files have been updated and pushed to GitHub.

---

## 📋 Step-by-Step Deployment

### Part 1: Setup Brevo (5 minutes)

1. **Create Brevo Account**
   - Go to: https://www.brevo.com
   - Sign up for free account
   - Verify your email

2. **Get SMTP Key**
   - Login to: https://app.brevo.com
   - Go to: **Settings** → **SMTP & API** → **SMTP** tab
   - Copy your SMTP key (starts with `xsmtpib-`)
   - Note your Brevo account email address

**See `BREVO_SETUP.md` for detailed Brevo setup!**

---

### Part 2: Deploy to Render.com (10 minutes)

#### Step 1: Sign Up
1. Go to **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (use same account as your repo)

#### Step 2: Create Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your GitHub account (if not already)
4. Find and select: **`MONET-PARTY`** repository
5. Click **"Connect"**

#### Step 3: Configure Settings
Fill in these **EXACT** settings:

**⚠️ IMPORTANT: Check your GitHub repo structure first!**

**If files are at repository root** (you see `app.py` directly):
```
Name: cyberpass
Region: (choose closest to you)
Branch: main
Root Directory: (LEAVE EMPTY)  ⚠️ VERY IMPORTANT!
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python app.py
```

**If files are in `party_entry_app` subdirectory**:
```
Name: cyberpass
Region: (choose closest to you)
Branch: main
Root Directory: party_entry_app  ⚠️ VERY IMPORTANT!
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python app.py
```

**How to check:** Visit https://github.com/chingchanghaunji-bit/MONET-PARTY and see if `app.py` is at root or in a folder.

#### Step 4: Add Environment Variables
Click **"Environment"** tab, then **"Add Environment Variable"** for each:

**Required Variables:**

```
FLASK_ENV = production
FLASK_DEBUG = False
PORT = 10000
HOST = 0.0.0.0
SECRET_KEY = change-this-to-random-string-12345
ADMIN_USER = admin
ADMIN_PASS = your-secure-password-here
```

**Brevo Email Variables:**

```
MAIL_SERVER = smtp-relay.brevo.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = your-brevo-email@example.com
MAIL_PASSWORD = xsmtpib-your-smtp-key-here
```

**Important:**
- Replace `your-brevo-email@example.com` with your actual Brevo account email
- Replace `xsmtpib-your-smtp-key-here` with your actual SMTP key from Brevo
- Replace `your-secure-password-here` with a strong admin password
- Replace `change-this-to-random-string-12345` with a random secret key

#### Step 5: Deploy!
1. Click **"Create Web Service"** button
2. Wait 5-10 minutes for build
3. Your site will be live at: **`https://cyberpass.onrender.com`**

---

## ✅ After Deployment

### Your Live URLs:
- **Main Site:** `https://cyberpass.onrender.com`
- **Admin Panel:** `https://cyberpass.onrender.com/admin/login`
  - Username: `admin` (or what you set in ADMIN_USER)
  - Password: (what you set in ADMIN_PASS)

### Test Your Website:
1. ✅ Visit your live URL
2. ✅ Try registering a test user (admin must add user first)
3. ✅ Login to admin panel
4. ✅ Test QR code generation
5. ✅ Test email sending (check inbox for test email)

---

## 🎯 Quick Checklist

**Brevo Setup:**
- [ ] Created Brevo account
- [ ] Got SMTP key from Brevo dashboard
- [ ] Copied SMTP key and email address

**Render.com Deployment:**
- [ ] Signed up on Render.com
- [ ] Connected GitHub account
- [ ] Selected MONET-PARTY repository
- [ ] Set Root Directory: `party_entry_app`
- [ ] Added all environment variables (including Brevo settings)
- [ ] Clicked "Create Web Service"
- [ ] Waited for deployment (5-10 min)
- [ ] Tested the live URL!

---

## 🆘 Troubleshooting

### Build Fails?
- ✅ Check Root Directory is exactly `party_entry_app`
- ✅ Verify all environment variables are added
- ✅ Check build logs in Render dashboard

### Website Shows Error?
- ✅ Check deployment logs in Render dashboard
- ✅ Verify PORT=10000 and HOST=0.0.0.0 are set
- ✅ Check SECRET_KEY is set

### Emails Not Sending?
- ✅ Verify Brevo SMTP key is correct (starts with `xsmtpib-`)
- ✅ Check MAIL_USERNAME is your Brevo account email
- ✅ Ensure MAIL_PORT=587 and MAIL_USE_TLS=True
- ✅ Check Brevo dashboard for sending limits (300/day free)

### Need Help?
- Check `DEPLOYMENT.md` for detailed troubleshooting
- Check `BREVO_SETUP.md` for Brevo-specific help

---

## 📚 Related Files

- `BREVO_SETUP.md` - Detailed Brevo account setup
- `DEPLOYMENT.md` - Full deployment guide
- `QUICK_DEPLOY.md` - Quick reference
- `DEPLOY_NOW.md` - Step-by-step guide

---

**🎮 Your cyberpunk party entry system with Brevo email is ready to deploy! ⚡**

