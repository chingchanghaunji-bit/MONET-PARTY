# 📧 Brevo SMTP Setup Guide

## What is Brevo?
Brevo (formerly Sendinblue) is an email service provider that offers:
- ✅ **300 emails/day FREE** (perfect for your party app!)
- ✅ Easy SMTP setup
- ✅ No app passwords needed (just SMTP key)
- ✅ Reliable email delivery

---

## Step 1: Create Brevo Account

1. Go to **https://www.brevo.com**
2. Click **"Sign up free"**
3. Fill in your details:
   - Email address
   - Password
   - Company name (optional)
4. Verify your email address
5. Complete the setup wizard

---

## Step 2: Get Your SMTP Key

1. Login to **https://app.brevo.com**
2. Click on your profile icon (top right)
3. Go to **"SMTP & API"** → **"SMTP"** tab
4. You'll see your **SMTP Key** (starts with `xsmtpib-`)
5. **Copy this key** - you'll need it for deployment!

**Example SMTP Key format:**
```
xsmtpib-1234567890abcdef1234567890abcdef
```

---

## Step 3: Get Your Brevo Email

- Your **MAIL_USERNAME** = The email address you used to sign up for Brevo
- Example: `yourname@example.com`

---

## Step 4: Use in Environment Variables

When deploying, use these values:

```
MAIL_SERVER = smtp-relay.brevo.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = your-brevo-email@example.com
MAIL_PASSWORD = xsmtpib-your-smtp-key-here
```

---

## ✅ Quick Checklist

- [ ] Created Brevo account
- [ ] Verified email address
- [ ] Got SMTP key from Settings → SMTP & API
- [ ] Copied SMTP key (starts with `xsmtpib-`)
- [ ] Ready to use in deployment!

---

## 🆘 Troubleshooting

**Email not sending?**
- Verify SMTP key is correct (starts with `xsmtpib-`)
- Check MAIL_USERNAME is your Brevo account email
- Ensure MAIL_PORT is 587 and MAIL_USE_TLS is True
- Check Brevo dashboard for sending limits

**Need more emails?**
- Free tier: 300 emails/day
- Upgrade plans available on Brevo website

---

**🎯 You're all set! Use these settings when deploying to Render.com**

