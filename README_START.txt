========================================
  HOW TO START THE SERVER
========================================

METHOD 1: Double-click START.bat (EASIEST)
-------------------------------------------
1. Go to the party_entry_app folder
2. Double-click "START.bat"
3. A black window will open - KEEP IT OPEN
4. Wait for "Running on http://127.0.0.1:5000"
5. Open browser: http://localhost:5000

METHOD 2: Manual Start (If START.bat doesn't work)
---------------------------------------------------
1. Open PowerShell or Command Prompt
2. Navigate to party_entry_app folder:
   cd "C:\Users\n\Desktop\generate_project.py\party_entry_app"
3. Activate virtual environment:
   .\venv\Scripts\activate.ps1
   (or: venv\Scripts\activate.bat)
4. Run the server:
   python app.py
5. KEEP THE WINDOW OPEN
6. Open browser: http://localhost:5000

IMPORTANT:
- The server window MUST stay open
- If you close it, the website stops working
- Look for "Running on http://127.0.0.1:5000" message

TROUBLESHOOTING:
- If port 5000 is busy, it will try port 5001
- Check the window for error messages
- Make sure virtual environment is activated

========================================
  ADMIN LOGIN
========================================
URL: http://localhost:5000/admin/login
Username: admin
Password: admin123

========================================


