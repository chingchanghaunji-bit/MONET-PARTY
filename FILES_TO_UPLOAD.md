# 📁 Files to Upload to GitHub (Manual Upload)

## ✅ FILES TO UPLOAD (Required)

### Root Directory Files:
- ✅ `app.py` - Main Flask application
- ✅ `run.py` - Simple server starter
- ✅ `requirements.txt` - Python dependencies
- ✅ `README.md` - Project documentation
- ✅ `Procfile` - For hosting platforms
- ✅ `runtime.txt` - Python version
- ✅ `.gitignore` - Git ignore rules

### Folders to Upload (with all contents):

1. **`modules/`** folder (all files inside):
   - ✅ `db_handler.py`
   - ✅ `email_sender.py`
   - ✅ `qr_generator.py`
   - ✅ `__init__.py` (if exists)

2. **`templates/`** folder (all HTML files):
   - ✅ `index.html`
   - ✅ `register.html`
   - ✅ `verify.html`
   - ✅ `success.html`
   - ✅ `result.html`
   - ✅ `admin_login.html`
   - ✅ `admin_dashboard.html`

3. **`static/`** folder (with subfolders):
   - ✅ `static/css/style.css`
   - ✅ `static/js/main.js`
   - ✅ `static/qrcodes/` (folder - can be empty, will be created automatically)

## ❌ FILES TO EXCLUDE (Don't Upload)

- ❌ `database.db` - Database file (will be created automatically)
- ❌ `venv/` - Virtual environment folder (NOT needed)
- ❌ `__pycache__/` - Python cache files
- ❌ `*.pyc` - Compiled Python files
- ❌ `.env` - Environment variables (if exists)
- ❌ `static/qrcodes/*.png` - Generated QR codes
- ❌ `START.bat` - Windows batch file (optional)
- ❌ `PUSH_TO_GITHUB.bat` - Windows batch file (optional)
- ❌ `QUICK_DEPLOY.bat` - Windows batch file (optional)
- ❌ `README_START.txt` - Local instructions (optional)
- ❌ `GITHUB_SETUP.md` - Local guide (optional)
- ❌ `DEPLOY_INSTRUCTIONS.md` - Local guide (optional)
- ❌ `FILES_TO_UPLOAD.md` - This file (optional)

## 📋 Step-by-Step Manual Upload

### Method 1: GitHub Web Interface

1. **Go to your repository:**
   - https://github.com/chingchanghaunji-bit/MONET-PARTY

2. **Click "Add file" → "Upload files"**

3. **Upload files in this order:**

   **First, upload root files:**
   - Drag and drop: `app.py`, `run.py`, `requirements.txt`, `README.md`, `Procfile`, `runtime.txt`, `.gitignore`

   **Then create folders and upload:**

   **Create `modules/` folder:**
   - Click "Add file" → "Create new file"
   - Type: `modules/db_handler.py`
   - Copy content from your local file
   - Repeat for: `modules/email_sender.py`, `modules/qr_generator.py`

   **Create `templates/` folder:**
   - Click "Add file" → "Create new file"
   - Type: `templates/index.html`
   - Copy content from your local file
   - Repeat for all HTML files in templates folder

   **Create `static/` folder:**
   - Create: `static/css/style.css`
   - Create: `static/js/main.js`
   - Create: `static/qrcodes/` (empty folder, or add a `.gitkeep` file)

4. **Commit:**
   - Write commit message: "Initial commit: Party Entry System"
   - Click "Commit changes"

### Method 2: Create Files One by One

For each file:
1. Click "Add file" → "Create new file"
2. Type the full path (e.g., `templates/index.html`)
3. Copy and paste the file content
4. Click "Commit new file"

## 📁 Final Structure on GitHub Should Look Like:

```
MONET-PARTY/
├── app.py
├── run.py
├── requirements.txt
├── README.md
├── Procfile
├── runtime.txt
├── .gitignore
├── modules/
│   ├── db_handler.py
│   ├── email_sender.py
│   └── qr_generator.py
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── verify.html
│   ├── success.html
│   ├── result.html
│   ├── admin_login.html
│   └── admin_dashboard.html
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── qrcodes/
        └── .gitkeep (optional, to keep folder)
```

## ✅ Quick Checklist

Before deploying, make sure you have:
- [ ] app.py
- [ ] requirements.txt
- [ ] All files in modules/ folder
- [ ] All files in templates/ folder
- [ ] All files in static/ folder (css and js)
- [ ] Procfile
- [ ] runtime.txt
- [ ] README.md (optional but recommended)

## 🚀 After Uploading

Once all files are on GitHub:
1. Go to Render.com or Railway.app
2. Connect your GitHub account
3. Select MONET-PARTY repository
4. Deploy!

---

**Note:** The `venv/` folder is NOT needed - hosting platforms will create their own virtual environment.

