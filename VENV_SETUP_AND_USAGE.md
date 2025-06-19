# Python Virtual Environment Setup and Usage

## Why Use a Virtual Environment?
A virtual environment (venv) isolates your Python project's dependencies from your system Python and other projects. This prevents version conflicts and keeps your project self-contained.

## Understanding PowerShell Script Files (.ps1)
The `.ps1` extension stands for "PowerShell Script" - it's not PowerShell version 1, but rather the standard file extension for PowerShell script files. Here's what you need to know:

- `.ps1` is to PowerShell what `.py` is to Python - it's the standard file extension
- The activation script is named `Activate.ps1` because it's a PowerShell script that sets up your virtual environment
- When you run `.\venv\Scripts\Activate.ps1`, you're telling PowerShell to:
  - `.\` means "run this script from the current directory"
  - `venv\Scripts\` is the path to the script
  - `Activate.ps1` is the script file itself

## Understanding Virtual Environment Persistence
The virtual environment consists of two parts:
1. **The `venv` folder**: This is permanent and contains all your project's Python packages
2. **The activation state**: This is temporary and only exists while your PowerShell window is open

When you close PowerShell:
- ✅ The `venv` folder and all installed packages remain on your computer
- ✅ Your project's dependencies are still there
- ❌ You just need to activate the environment again in your new PowerShell window

Think of it like turning on a light switch:
- The light bulb (venv folder) is always there
- The switch (activation) needs to be turned on each time you enter the room (open a new PowerShell window)

## How to Activate the Virtual Environment
1. **Open PowerShell** and navigate to your project directory:
   ```powershell
   cd C:\Users\neilw\Projects\listener-maths-crossword
   ```

2. **Set the Execution Policy (if needed):**
   PowerShell restricts running scripts for security. You may see an error like:
   > running scripts is disabled on this system

   If you get a permission error when trying to set the execution policy, you have two options:

   **Option 1 (Recommended for most users):** Set the policy for your user account only:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

   **Option 2:** Run PowerShell as Administrator and set the policy for all users:
   - Right-click on PowerShell
   - Select "Run as Administrator"
   - Then run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
   ```

   The `-Scope CurrentUser` option is recommended as it's safer and doesn't require administrator privileges.

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
- The policy can be set at different scopes:
  - `CurrentUser`: Only affects your user account (safer, doesn't require admin rights)
  - `LocalMachine`: Affects all users (requires administrator privileges)

## Can I Permanently Change the Policy?
Yes, and it's recommended to set it permanently for your user account. This way, you won't need to change it each time you open a new PowerShell window. Use:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

This is safe because:
1. It only affects your user account
2. It still maintains security by requiring downloaded scripts to be signed
3. It allows you to run local scripts (like your venv activation script)

---

If you have any questions, refer to the [Microsoft documentation on execution policies](https://go.microsoft.com/fwlink/?LinkID=135170). 