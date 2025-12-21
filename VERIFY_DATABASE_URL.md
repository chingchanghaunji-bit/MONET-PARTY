# ✅ Verify DATABASE_URL is Set Correctly

## Your Database Connection String:
```
postgresql://afterparty_user:EEtpRrg8Tza5o39M4TnrJI2jMFbXcnzU@dpg-d5393hruibrs73fn3asg-a/afterparty
```

## ⚠️ Important: Set it in the WEB SERVICE, not the database!

### Step 1: Go to Your Web Service
1. In Render Dashboard, find your **Web Service** (not the database)
2. It should be named something like "MONET PARTY" or "afterparty" (web service)
3. Click on it

### Step 2: Check Environment Variables
1. Click **"Environment"** tab (left sidebar)
2. Look for `DATABASE_URL` in the list
3. If it's NOT there, add it:
   - Click **"Add Environment Variable"**
   - **Key:** `DATABASE_URL`
   - **Value:** `postgresql://afterparty_user:EEtpRrg8Tza5o39M4TnrJI2jMFbXcnzU@dpg-d5393hruibrs73fn3asg-a/afterparty`
   - Click **"Save Changes"**

### Step 3: Verify the Value
Make sure:
- ✅ Variable name is exactly: `DATABASE_URL` (case-sensitive, no spaces)
- ✅ Value starts with `postgresql://` (not `postgres://`)
- ✅ No extra spaces before or after the value
- ✅ The entire URL is on one line

### Step 4: Trigger New Deployment
After saving:
1. Render should auto-deploy (watch the "Events" tab)
2. OR manually trigger: Click **"Manual Deploy"** → **"Deploy latest commit"**
3. Wait 3-5 minutes
4. Check logs - you should see:
   ```
   ✅ DATABASE_URL found - connecting to PostgreSQL
   ✅ PostgreSQL connection pool created
   ✅ Database initialized
   ```

## 🔍 Common Issues:

### Issue 1: Variable set in wrong service
- ❌ Setting it in the **database service** won't work
- ✅ Must be set in the **web service**

### Issue 2: Variable name typo
- ❌ `DATABASE_URL ` (with space)
- ❌ `database_url` (lowercase)
- ✅ `DATABASE_URL` (exact match)

### Issue 3: Value format
- ❌ Missing `postgresql://` prefix
- ❌ Extra spaces or line breaks
- ✅ Complete URL on one line

### Issue 4: Not redeployed after setting
- After adding/changing environment variables, you MUST redeploy
- Render doesn't always auto-redeploy when env vars change

## 🎯 Quick Fix Checklist:

- [ ] Opened **Web Service** (not database)
- [ ] Went to **Environment** tab
- [ ] Verified `DATABASE_URL` exists
- [ ] Value matches exactly (no spaces, correct format)
- [ ] Clicked **"Save Changes"**
- [ ] Triggered new deployment
- [ ] Checked logs for success messages

---

**After fixing, your deployment should succeed!**

