# Authentication Fix - Database Setup Guide

## Problem Identified ✅

Your authentication issues are caused by:

1. **No persistent database** - SQLite is ephemeral on Render (gets wiped)
2. **Tables not initialized** - `db.create_all()` wasn't running with Gunicorn
3. **Missing PostgreSQL driver** - psycopg2 not in requirements

## Solution Applied

### Changes Made:

1. ✅ **Updated `app.py`:**
   - Moved `db.create_all()` outside `if __name__` block (now runs with Gunicorn)
   - Added PostgreSQL URL fix for Render
   - Added better error handling and logging
   - Added try/catch blocks around database operations

2. ✅ **Updated `requirements.txt`:**
   - Added `psycopg2-binary>=2.9.9` for PostgreSQL support

## Next Steps: Add PostgreSQL Database on Render

### Step 1: Create PostgreSQL Database

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name:** `listener-crossword-db`
   - **Database:** `listener_crossword`
   - **User:** (auto-generated)
   - **Region:** Same as your web service
   - **Plan:** **Free** (sufficient for this app)
4. Click **"Create Database"**
5. Wait ~2 minutes for provisioning

### Step 2: Connect Database to Web Service

1. Go to your **listener-crossword-solver** web service
2. Click **"Environment"** in left sidebar
3. Click **"Add Environment Variable"**
4. Add:
   - **Key:** `DATABASE_URL`
   - **Value:** Click **"Connect to existing database"** and select `listener-crossword-db`
5. Click **"Save Changes"**

This will trigger a new deployment automatically.

### Step 3: Verify

After deployment completes (~3-4 minutes):

1. Visit: https://listener-maths-crossword.onrender.com/login
2. Try registering a new account
3. Try logging in
4. Should work smoothly now! ✅

## What Fixed It

**Before:**
- SQLite database wiped on every deployment
- Database tables never created on Render
- Users couldn't be saved
- Multiple login attempts needed (luck-based)

**After:**
- PostgreSQL database persists across deployments
- Tables automatically created when app starts
- Users saved permanently
- Login works first time, every time

## Testing Locally

Your local development still uses SQLite (no changes needed):

```bash
cd "/Users/neilwedlake/GitHub Projects/listener-maths-crossword"
python app.py
```

Visit: http://localhost:5001

## Troubleshooting

### If login still fails after PostgreSQL setup:

1. **Check logs on Render:**
   - Go to your web service
   - Click "Logs" tab
   - Look for "Database tables initialized successfully" ✅
   - Or look for error messages ❌

2. **Verify DATABASE_URL:**
   - Go to Environment variables
   - DATABASE_URL should start with `postgresql://`
   - Should be connected to your database

3. **Try manual redeploy:**
   - Click "Manual Deploy" → "Deploy latest commit"
   - Watch logs for any errors

### If you see "postgres://" URL error:

The app now automatically fixes this (line 24 in app.py):
```python
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
```

## Commit These Changes

**Files changed:**
1. `app.py` - Database initialization fix
2. `requirements.txt` - Added PostgreSQL driver

**Commit message:**

**Summary:**
```
Fix: Add PostgreSQL support and database initialization
```

**Description:**
```
- Move db.create_all() outside main block for Gunicorn compatibility
- Add psycopg2-binary for PostgreSQL support
- Fix postgres:// vs postgresql:// URL format issue
- Add better error handling and logging for auth
- Add try/catch blocks for database operations

This fixes authentication issues caused by:
- Ephemeral SQLite database on Render
- Database tables not being created
- Missing PostgreSQL driver

Requires: PostgreSQL database to be created on Render and
connected via DATABASE_URL environment variable
```

## Summary

**Status:** Code fixed, ready to deploy  
**Action needed:** Add PostgreSQL database on Render (5 minutes)  
**Expected result:** Authentication works perfectly  

Let me know once you've added the database and I can help verify it's working!
