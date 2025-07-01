# Database Options and Setup Guide

This document summarizes the database options, setup, and best practices for the Listener Maths Crossword project.

---

## Table of Contents
- [Overview](#overview)
- [Why Not Use GitHub for Databases?](#why-not-use-github-for-databases)
- [Recommended Database Options](#recommended-database-options)
  - [1. Local Development (SQLite)](#1-local-development-sqlite)
  - [2. Shared Development (Cloud PostgreSQL)](#2-shared-development-cloud-postgresql)
  - [3. Production Deployment](#3-production-deployment)
- [How to Switch Between Databases](#how-to-switch-between-databases)
- [Quick Setup for Shared Development](#quick-setup-for-shared-development)
- [Summary Table](#summary-table)
- [Best Practices](#best-practices)

---

## Overview

- **SQLite** is used for local, single-user development. Each machine has its own database file.
- **PostgreSQL** (or MySQL) is recommended for shared development and production. Use a cloud provider for easy access from multiple machines.
- **GitHub is NOT suitable** for storing or syncing database files.

---

## Why Not Use GitHub for Databases?
- **Binary files**: SQLite databases are binary and do not merge well with git.
- **Concurrent access**: Multiple users cannot safely edit the same file.
- **Security**: Database files may contain sensitive data.
- **Performance**: Git is not designed for large binary files.
- **Best practice**: Add `instance/crossword_solver.db` to `.gitignore`.

---

## Recommended Database Options

### 1. Local Development (SQLite)
- **Pros:**
  - Simple setup
  - No server required
  - Works offline
- **Cons:**
  - Each machine has its own database
  - Not suitable for sharing or production
- **Usage:**
  - Default for development
  - Database file: `instance/crossword_solver.db`

### 2. Shared Development (Cloud PostgreSQL)
- **Pros:**
  - Shared between all machines
  - Multi-user support
  - Production-like environment
  - Free tiers available
- **Cons:**
  - Requires internet connection
  - Slightly more setup
- **Recommended Providers:**
  - [Railway](https://railway.app/) (free tier)
  - [Supabase](https://supabase.com/) (free tier)
  - [Neon](https://neon.tech/) (free tier)
  - [ElephantSQL](https://www.elephantsql.com/) (free tier)
- **Usage:**
  - Set the `DATABASE_URL` environment variable to your cloud connection string
  - Example: `export DATABASE_URL='your_connection_string'`
  - Run: `FLASK_ENV=production python app.py`

### 3. Production Deployment
- **Pros:**
  - Full production environment
  - Scalable and robust
- **Cons:**
  - May require payment for higher usage
  - More complex setup
- **Recommended Providers:**
  - [Heroku Postgres](https://www.heroku.com/postgres)
  - [Railway](https://railway.app/)
  - [Supabase](https://supabase.com/)
- **Usage:**
  - Same as shared development, but with production-grade credentials and backups

---

## How to Switch Between Databases

In `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///crossword_solver.db')
```
- If `DATABASE_URL` is set, Flask uses the cloud database.
- Otherwise, it falls back to local SQLite.

---

## Quick Setup for Shared Development

1. **Sign up for a free cloud database provider** (e.g., Railway, Supabase)
2. **Create a PostgreSQL database**
3. **Copy the connection string** (e.g., `postgresql://user:password@host:port/dbname`)
4. **Set the environment variable**:
   ```bash
   export DATABASE_URL='your_connection_string'
   ```
5. **Run your app in production mode**:
   ```bash
   FLASK_ENV=production python app.py
   ```
6. **All machines using the same `DATABASE_URL` will share the same data!**

---

## Summary Table

| Use Case         | Recommended DB | How to Share Data?         | GitHub?      |
|------------------|---------------|----------------------------|--------------|
| Local dev        | SQLite        | Copy file (not recommended)| No           |
| Multi-machine    | PostgreSQL    | Use cloud DB               | No           |
| Production       | PostgreSQL    | Use cloud DB               | No           |

---

## Best Practices
- **Never commit your database file to git**
- **Use SQLite for local, single-user development**
- **Use PostgreSQL/MySQL for shared or production environments**
- **Set `DATABASE_URL` for cloud/production use**
- **Back up your production database regularly**
- **Keep credentials secure and out of source control**

---

## See Also
- [SQLAlchemy ORM and Flask State Management](LEARNING_POINTS.md)
- [Flask SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Railway Docs](https://docs.railway.app/)
- [Supabase Docs](https://supabase.com/docs) 