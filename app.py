from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from dotenv import load_dotenv
import os
import uuid
import re
import secrets
from datetime import datetime

# --- LOAD ENV SAFELY ---
# FIXED: Load .env file if it exists (local development)
# On Render, environment variables are set directly, so this won't override them
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    # On Render/production, environment variables are set directly
    # load_dotenv() will use existing environment variables
    load_dotenv(override=False)

# --- IMPORT DB FUNCTIONS ---
from modules.db_handler import (
    init_db,
    get_user,
    add_user,
    update_user,
    fetch_all_users,
    get_stats
)

# --- QR + EMAIL ---
from modules.qr_generator import generate_qr
from modules.email_sender import init_mail, send_email


# ---------------------------------------------------
# FLASK APP SETUP
# ---------------------------------------------------
app = Flask(__name__)
# FIXED: Ensure secret key is set for session management (critical for admin panel)
app.secret_key = os.getenv("SECRET_KEY") or "dev-secret-key-change-in-production-please"
app.config["UPLOAD_FOLDER"] = os.path.join("static", "qrcodes")

# FIXED: Ensure qrcodes directory exists (critical for Render deployment)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# ---------------------------------------------------
# MAIL CONFIG (FIXED!)
# ---------------------------------------------------
_mail_port_raw = os.getenv("MAIL_PORT")
print("DEBUG: MAIL_PORT raw from env ->", repr(_mail_port_raw))

# safe fallback to 587 if None or invalid
_mail_port_safe = int(_mail_port_raw) if _mail_port_raw and _mail_port_raw.isdigit() else 587

app.config["MAIL_PORT"] = _mail_port_safe
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL") == "True"

# Initialize Flask-Mail
init_mail(app)

# ---------------------------------------------------
# INITIALIZE DATABASE
# ---------------------------------------------------
init_db()


# ---------------------------------------------------
# LOGIN REQUIRED DECORATOR
# ---------------------------------------------------
from functools import wraps
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # FIXED: Improved session check for production
        if "admin" not in session or not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return wrapper


# ---------------------------------------------------
# ROUTES
# ---------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        name = request.form["name"]
        phone = request.form["phone"].strip()
        
        # FIXED: Normalize Indian phone number - handle both formats
        # Accept: 10 digits OR +91 + 10 digits OR 91 + 10 digits
        phone_cleaned = re.sub(r'\D', '', phone)  # Remove all non-digits
        
        # Handle different input formats
        if phone_cleaned.startswith('91') and len(phone_cleaned) == 12:
            phone_cleaned = phone_cleaned[2:]  # Remove country code if present
        elif phone_cleaned.startswith('91') and len(phone_cleaned) == 11:
            # Handle case where user typed 91 + 9 digits (should be 10)
            phone_cleaned = phone_cleaned[2:] if len(phone_cleaned) > 10 else phone_cleaned
        
        # Validate: must be exactly 10 digits
        if len(phone_cleaned) != 10:
            return render_template("register.html", error="Please enter a valid 10-digit Indian mobile number (e.g., 9876543210 or +91 98765 43210)")
        
        # Format as Indian number: +91 XXXXX XXXXX (standardized format)
        phone = f"+91 {phone_cleaned[:5]} {phone_cleaned[5:]}"

        user = get_user(email=email)
        if not user:
            return render_template("register.html", error="You are not authorized to register. Please contact the administrator.")

        if user["registered"]:
            return render_template("register.html", error="You have already registered. Check your email for your ticket.")

        ticket_id = str(uuid.uuid4())[:8].upper()
        qr_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{ticket_id}.png")

        generate_qr(ticket_id, qr_path)

        update_user(
            email,
            name=name,
            phone=phone,
            registered=1,
            ticket_id=ticket_id,
            registered_at=datetime.now().isoformat()
        )

        send_email(email, name, ticket_id, qr_path)

        return render_template("success.html", name=name, ticket_id=ticket_id, qr_path=qr_path)

    return render_template("register.html")


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        code = request.form["ticket_id"].strip().upper()
        user = get_user(ticket_id=code)

        if not user:
            msg = "❌ Invalid Ticket!"
        elif user["verified"]:
            msg = f"🚫 Ticket {code} already used!"
        else:
            msg = f"✅ Access Granted to {user['name']}!"
            update_user(user["email"], verified=1, verified_at=datetime.now().isoformat())

        return render_template("result.html", msg=msg)

    return render_template("verify.html")


# ---------------------------------------------------
# ADMIN
# ---------------------------------------------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        user = request.form.get("username", "").strip()
        pw = request.form.get("password", "").strip()

        # FIXED: Get admin credentials with proper environment variable handling
        # Works on both local and Render production
        admin_user = os.getenv("ADMIN_USER", "admin")
        admin_pass = os.getenv("ADMIN_PASS", "admin123")

        # Debug logging (remove in production if needed)
        if not admin_user or not admin_pass:
            print("WARNING: Admin credentials not set in environment variables")

        if user == admin_user and pw == admin_pass:
            session["admin"] = user
            session.permanent = True  # Make session persistent
            return redirect(url_for("admin_dashboard"))

        return render_template("admin_login.html", error="Invalid credentials. Please try again.")

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("index"))


@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    users = fetch_all_users()
    stats = get_stats()
    return render_template("admin_dashboard.html", users=users, stats=stats)


@app.route("/admin/add", methods=["POST"])
@login_required
def add_allowed():
    email = request.form["email"].strip().lower()
    add_user(email)
    flash(f"User {email} added successfully!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/api/stats")
@login_required
def api_stats():
    return jsonify(get_stats())

@app.route("/api/search")
@login_required
def api_search():
    query = request.args.get("q", "").lower()
    users = fetch_all_users()
    filtered = [u for u in users if query in str(u).lower()]
    return jsonify(filtered)


# ---------------------------------------------------
# RUN APP
# ---------------------------------------------------
if __name__ == "__main__":
    os.makedirs("static/qrcodes", exist_ok=True)
    
    # FIXED: Ensure secret key is set (critical for sessions on Render)
    if not app.secret_key or app.secret_key == "dev-secret-key-change-in-production-please":
        # Generate a random secret key if not set (for development only)
        app.secret_key = secrets.token_hex(32)
        print("⚠️  WARNING: Using auto-generated secret key. Set SECRET_KEY in environment for production!")
    
    # FIXED: Check environment variables for production (Render)
    admin_user = os.getenv("ADMIN_USER")
    admin_pass = os.getenv("ADMIN_PASS")
    
    if not admin_user or not admin_pass:
        print("\n" + "="*50)
        print("⚠️  DEFAULT ADMIN CREDENTIALS (Development Mode):")
        print("   Username: admin")
        print("   Password: admin123")
        print("   ⚠️  Set ADMIN_USER and ADMIN_PASS in Render environment variables for production!")
        print("="*50 + "\n")
    else:
        print("\n✅ Admin credentials loaded from environment variables")
    
    print("\n🚀 Starting Party Entry System...")
    port = int(os.environ.get("PORT", 10000))
    print(f"📍 Server running on port: {port}")
    print("🔐 Admin login: /admin/login")
    print("📝 Register: /register")
    print("✅ Verify: /verify\n")
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False  # Disable debug mode in production
    )
