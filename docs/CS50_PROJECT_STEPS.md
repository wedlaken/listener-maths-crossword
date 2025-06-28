# CS50 Project: Interactive Crossword Solver - Key Steps

This document summarizes the essential steps for demonstrating your CS50 project, focusing on database setup, deployment, and full-stack skills.

---

## 1. SQLite Database & Email Registration

- **Database:** Uses SQLite for simplicity (file: `crossword_solver.db`).
- **User Registration:** Users register with email and password (passwords are securely hashed).
- **Persistence:** User progress (puzzle state) is saved in the database.
- **How to Demonstrate:**
  - Show the `User` and `PuzzleSession` models in `app.py`.
  - Show the database file being created and updated as users interact.
  - Optionally, open the database with a tool like DB Browser for SQLite to show the data.

---

## 2. Running the Program on a Server (Deployment)

- **Git-Based Deployment:**
  - Code is managed with Git and pushed to GitHub.
  - Deployment platforms (Heroku, Railway, Render) can auto-deploy from GitHub.
- **Steps:**
  1. Commit and push your code to GitHub.
  2. Create a Heroku (or Railway/Render) app and connect it to your repo.
  3. Set environment variables (e.g., `SECRET_KEY`).
  4. Deploy and open your app in the browser.
- **How to Demonstrate:**
  - Show the deployment process (screenshots or live demo).
  - Access the app from another device/browser to show it works remotely.

---

## 3. Demonstrating Full-Stack Skills

- **Backend:** Python, Flask, SQLAlchemy, SQLite
- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **Database:** User registration, login, and puzzle state persistence
- **Deployment:** Git-based workflow, cloud deployment (Heroku/Railway/Render)
- **Security:** Password hashing, session management
- **How to Demonstrate:**
  - Register a new user and log in.
  - Solve part of the crossword and save progress.
  - Log out, log in again, and show that progress is restored.
  - Show the code structure and explain how frontend and backend communicate (AJAX, API routes).

---

## Quick Reference

- **Local run:**
  ```bash
  python app.py
  ```
- **Deployment:**
  - See `DEPLOYMENT.md` for detailed steps.
- **Database:**
  - File: `crossword_solver.db` (auto-created)
  - Models: `User`, `PuzzleSession` in `app.py`

---

**This checklist will help you demonstrate a range of languages, frameworks, and functionalities for your CS50 project!** 