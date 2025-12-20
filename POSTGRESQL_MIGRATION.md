# 🐘 PostgreSQL Migration Guide

## ✅ Migration Complete!

Your application has been migrated from SQLite to PostgreSQL for production stability on Render.

## What Changed

1. **Database:** SQLite → PostgreSQL
2. **Connection:** File-based → Connection pooling with `DATABASE_URL`
3. **Persistence:** Ephemeral filesystem → Persistent PostgreSQL database
4. **Backups:** Manual file backups → Automatic Render PostgreSQL backups

## Setup Instructions

### Step 1: Create PostgreSQL Database in Render

1. Go to your Render dashboard
2. Click **New +** → **PostgreSQL**
3. Configure:
   - **Name:** `monet-party-db` (or your preferred name)
   - **Database:** `monet_party` (or your preferred name)
   - **User:** Auto-generated
   - **Region:** Same as your web service
4. Click **Create Database**

### Step 2: Get DATABASE_URL

After creating the database:
1. Go to your PostgreSQL database in Render
2. Find **Internal Database URL** or **External Database URL**
3. Copy the connection string (looks like: `postgresql://user:password@host:port/database`)

### Step 3: Set Environment Variable

1. Go to your **Web Service** in Render
2. Go to **Environment** tab
3. Add new environment variable:
   ```
   Key: DATABASE_URL
   Value: [paste the PostgreSQL connection string]
   ```
4. Save

### Step 4: Deploy

The code is already pushed to GitHub. If auto-deploy is enabled, Render will automatically redeploy. Otherwise:
1. Go to your Web Service
2. Click **Manual Deploy** → **Deploy latest commit**

## Verification

After deployment, check:

1. **Render Logs:**
   ```
   ✅ DATABASE_URL found - connecting to PostgreSQL
   ✅ PostgreSQL connection pool created
   ✅ Database initialized (table exists or created)
   ✅ PostgreSQL database initialized successfully
   ```

2. **Admin Dashboard:**
   - Login to admin panel
   - Check **Database Status** card
   - Should show:
     - ✅ Database Type: PostgreSQL
     - ✅ Connection Status: Connected
     - ✅ Storage: Persistent

3. **Test Functionality:**
   - Add a test user
   - Register a user
   - Verify a ticket
   - All should work normally

## Features

### Connection Pooling
- Uses connection pooling (1-5 connections)
- Automatic reconnection on failures
- Graceful error handling

### Data Persistence
- ✅ Data persists across redeploys
- ✅ Data persists across restarts
- ✅ Data persists across crashes
- ✅ No data loss

### Automatic Backups
- Render automatically backs up PostgreSQL databases
- No manual backup needed
- Point-in-time recovery available

## Troubleshooting

### Error: "DATABASE_URL environment variable is required"

**Solution:** Make sure you've set the `DATABASE_URL` environment variable in Render with your PostgreSQL connection string.

### Error: "could not connect to server"

**Possible causes:**
1. Database not created yet
2. Wrong DATABASE_URL
3. Database region mismatch
4. Network issues

**Solution:**
1. Verify database exists in Render
2. Check DATABASE_URL is correct
3. Ensure database and web service are in same region
4. Check Render status page

### Error: "relation 'allowed' does not exist"

**Solution:** The table will be created automatically on first startup. If this error persists:
1. Check logs for initialization errors
2. Verify DATABASE_URL has proper permissions
3. Manually create table if needed (see SQL below)

## Manual Table Creation (if needed)

If table creation fails, you can manually create it:

```sql
CREATE TABLE IF NOT EXISTS allowed (
    email VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    phone VARCHAR(50),
    registered INTEGER DEFAULT 0,
    ticket_id VARCHAR(50),
    verified INTEGER DEFAULT 0,
    created_at TIMESTAMP,
    registered_at TIMESTAMP,
    verified_at TIMESTAMP
);
```

## Migration from SQLite (if you have existing data)

If you have existing SQLite data to migrate:

1. Export data from SQLite:
   ```bash
   sqlite3 database.db .dump > data.sql
   ```

2. Convert SQLite SQL to PostgreSQL format (adjust data types)

3. Import to PostgreSQL:
   ```bash
   psql $DATABASE_URL < data.sql
   ```

Or use a migration tool like `pgloader` for automatic conversion.

## Environment Variables Summary

**Required:**
- `DATABASE_URL` - PostgreSQL connection string

**Optional (existing):**
- `SECRET_KEY` - Flask session secret
- `ADMIN_USER` - Admin username
- `ADMIN_PASS` - Admin password
- `MAIL_*` - Email configuration

## Support

If you encounter issues:
1. Check Render logs for detailed error messages
2. Verify DATABASE_URL is set correctly
3. Ensure PostgreSQL database is running
4. Check database connection limits

## Benefits

✅ **No more data loss** - PostgreSQL persists across all restarts  
✅ **Better performance** - Connection pooling and optimized queries  
✅ **Automatic backups** - Render handles backups automatically  
✅ **Scalability** - Can handle more concurrent users  
✅ **Production-ready** - Industry-standard database solution

