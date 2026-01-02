#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Root-level app.py for Render deployment
This file imports the actual Flask app from party_entry_app directory
"""
import os
import sys

# Add party_entry_app to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'party_entry_app'))

# Change to party_entry_app directory
os.chdir(os.path.join(os.path.dirname(__file__), 'party_entry_app'))

# Import the actual Flask app
from app import app

# Export app for gunicorn/WSGI
if __name__ == "__main__":
    # For local development/testing
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

