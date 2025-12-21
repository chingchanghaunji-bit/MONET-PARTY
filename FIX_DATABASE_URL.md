# 🔧 FIX: DATABASE_URL Error - Step by Step

## ❌ Error You're Seeing:
```
ValueError: DATABASE_URL environment variable is required. Set it in Render dashboard.
Exited with status 1
```

## ✅ Solution: Set DATABASE_URL in Render

### Step 1: Create PostgreSQL Database in Render

1. Go to **Render Dashboard**: https://dashboard.render.com
2. Click **"New +"** button (top right)
3. Select **"PostgreSQL"**
4. Fill in:
   - **Name**: `monet-party-db` (or any name you like)
   - **Database**: `monet_party` (or leave default)
   - **User**: (auto-generated)
   - **Region**: Choose closest to your web service (e.g., Singapore)
   - **PostgreSQL Version**: Latest (14 or 15)
   - **Plan**: Free (or Starter if you need more)
5. Click **"Create Database"**
6. Wait 2-3 minutes for database to be created

### Step 2: Copy Database URL

1. Once database is created, click on it
2. Go to **"Connections"** tab
3. Find **"Internal Database URL"** (for same-region services) or **"External Database URL"** (if web service is in different region)
4. **Copy the entire URL** - it looks like:
   ```
   postgresql://user:password@hostname:5432/database_name
   ```

### Step 3: Set DATABASE_URL in Web Service

1. Go back to Render Dashboard
2. Click on your **Web Service** ("MONET PARTY")
3. Go to **"Environment"** tab (left sidebar)
4. Click **"Add Environment Variable"**
5. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the database URL you copied
6. Click **"Save Changes"**

### Step 4: Redeploy

1. After saving, Render will automatically start a new deployment
2. OR manually trigger: Click **"Manual Deploy"** → **"Deploy latest commit"**
3. Wait 3-5 minutes
4. Check logs - you should now see:
   ```
   ✅ DATABASE_URL found - connecting to PostgreSQL
   ✅ PostgreSQL connection pool created
   ✅ Database initialized
   ```

## 🎯 Quick Checklist

- [ ] PostgreSQL database created in Render
- [ ] Database URL copied (Internal or External)
- [ ] `DATABASE_URL` environment variable added to web service
- [ ] Deployment triggered
- [ ] Logs show "✅ DATABASE_URL found"

## ⚠️ Important Notes

1. **Internal vs External URL:**
   - Use **Internal Database URL** if web service and database are in same region
   - Use **External Database URL** if they're in different regions
   - Internal is faster and more secure

2. **Database Region:**
   - For best performance, create database in same region as your web service
   - Check your web service region in Settings → Region

3. **Free Tier Limits:**
   - Free PostgreSQL databases sleep after 90 days of inactivity
   - Consider upgrading to Starter plan for always-on database

## 🆘 Still Having Issues?

If deployment still fails after setting DATABASE_URL:

1. **Verify URL Format:**
   - Should start with `postgresql://` or `postgres://`
   - Should contain username, password, hostname, port, and database name

2. **Check Database Status:**
   - Make sure database shows "Available" status
   - Not "Paused" or "Suspended"

3. **Check Web Service Region:**
   - If using Internal URL, ensure web service and database are in same region

4. **Clear Build Cache:**
   - Settings → Advanced → "Clear build cache"
   - Then redeploy

---

**After fixing, your app will:**
- ✅ Connect to PostgreSQL
- ✅ Create tables automatically
- ✅ Store all user data persistently
- ✅ Survive redeploys and restarts

