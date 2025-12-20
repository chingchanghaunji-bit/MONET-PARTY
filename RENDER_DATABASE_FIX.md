# 🔧 Fix Database Persistence on Render

## Problem
Your database data is disappearing because **Render uses an ephemeral filesystem**. When Render restarts or redeploys your app, all files in the default location get wiped, including your `database.db` file.

## Solution Options

### Option 1: Use Render Persistent Disk (Recommended for Free/Starter Plans)

1. **Enable Persistent Disk in Render:**
   - Go to your Render dashboard
   - Select your web service
   - Go to **Settings** → **Disk**
   - Enable **Persistent Disk** (if available on your plan)
   - Note the mount path (usually `/opt/render/project/src`)

2. **Set Environment Variable:**
   - In Render dashboard, go to **Environment** tab
   - Add new environment variable:
     ```
     Key: DB_PATH
     Value: /opt/render/project/src/database.db
     ```
   - Save and redeploy

### Option 2: Use Cloud Database Service (Best for Production)

For better reliability, use a managed database service:

#### PostgreSQL (Recommended)
1. In Render dashboard, create a **PostgreSQL** database
2. Get the connection string
3. Update your code to use PostgreSQL instead of SQLite
4. Set environment variables for database connection

#### MongoDB Atlas (Alternative)
1. Create free MongoDB Atlas account
2. Get connection string
3. Update code to use MongoDB

### Option 3: External Backup Service

Use an external backup service (S3, Google Cloud Storage) to automatically backup your database:
- Set up automatic backups to cloud storage
- Restore from backup on startup if database is missing

## Quick Fix (Temporary)

If you need a quick fix right now:

1. **Set DB_PATH environment variable in Render:**
   ```
   DB_PATH=/opt/render/project/src/database.db
   ```

2. **Or use a subdirectory:**
   ```
   DB_PATH=/opt/render/project/src/data/database.db
   ```

3. **Redeploy your service**

## Verification

After setting up persistent storage:

1. Check Render logs for database path:
   ```
   📁 Database path: /opt/render/project/src/database.db
   📁 Database absolute path: /opt/render/project/src/database.db
   ```

2. Add a test user in admin panel
3. Restart your Render service
4. Check if the user still exists

## Current Status

The app now:
- ✅ Uses configurable database path via `DB_PATH` environment variable
- ✅ Logs database path on startup for debugging
- ✅ Shows warning in admin dashboard about persistence
- ✅ Has delete button functionality working

## Next Steps

1. **Immediate:** Set `DB_PATH` environment variable in Render
2. **Short-term:** Enable persistent disk if available
3. **Long-term:** Migrate to PostgreSQL or MongoDB for production

