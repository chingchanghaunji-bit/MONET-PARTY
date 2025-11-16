#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple server starter script
"""
import os
import sys

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "="*50)
print("  PARTY ENTRY SYSTEM - STARTING SERVER")
print("="*50)
print("\nStarting Flask server...")
print("\nServer will be available at:")
print("  http://localhost:5000")
print("\nAdmin Login:")
print("  http://localhost:5000/admin/login")
print("  Username: admin")
print("  Password: admin123")
print("\n" + "="*50)
print("Press Ctrl+C to stop the server")
print("="*50 + "\n")

# Import and run the app
from app import app

if __name__ == "__main__":
    os.makedirs("static/qrcodes", exist_ok=True)
    if not app.secret_key:
        app.secret_key = "dev-secret-key-change-in-production"
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
    except OSError as e:
        if "Address already in use" in str(e) or "WinError 10048" in str(e):
            print(f"\nPort 5000 is busy. Trying port 5001...\n")
            app.run(debug=True, host='127.0.0.1', port=5001, use_reloader=False)
        else:
            raise

