# Python Virtual Environment Setup and Usage

## Why Use a Virtual Environment?
A virtual environment (venv) isolates your Python project's dependencies from your system Python and other projects. This prevents version conflicts and keeps your project self-contained.

## How to Activate the Virtual Environment
1. **Open PowerShell** and navigate to your project directory:
   ```powershell
   cd C:\Users\neilw\Projects\listener-maths-crossword
   ```
2. **Set the Execution Policy (if needed):**
   PowerShell restricts running scripts for security. You may see an error like:
   > running scripts is disabled on this system
   To allow activation scripts to run for this session only, enter:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   ```
   This change is temporary and only affects the current PowerShell window.

3. **Activate the Virtual Environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   You should see `(venv)` at the start of your prompt, indicating the environment is active.

4. **Install dependencies (if not already done):**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Deactivate the Virtual Environment:**
   When finished, you can deactivate with:
   ```powershell
   deactivate
   ```

---

## What is the PowerShell Execution Policy?
PowerShell's execution policy is a safety feature that controls whether scripts can run. By default, it may block scripts (like the venv activation script) to protect your system from untrusted code.

- `RemoteSigned` allows scripts created on your computer to run, but requires downloaded scripts to be signed by a trusted publisher.
- Setting the policy with `-Scope Process` only changes it for the current session, so it's safe and temporary.

## Can I Permanently Change the Policy?
You can, but it's not generally recommended for security reasons. If you want to allow scripts to run in all PowerShell sessions, you can run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
This will persist for your user account, but be cautious—this makes it easier for any script to run.

**For most users, setting the policy per session is safest.**

---

If you have any questions, refer to the [Microsoft documentation on execution policies](https://go.microsoft.com/fwlink/?LinkID=135170). 