from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime

# --- LOAD ENV SAFELY ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

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
app.secret_key = os.getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = os.path.join("static", "qrcodes")

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
        if "admin" not in session:
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
        phone = request.form["phone"]

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
        user = request.form["username"]
        pw = request.form["password"]

        # Get admin credentials with defaults
        admin_user = os.getenv("ADMIN_USER", "admin")
        admin_pass = os.getenv("ADMIN_PASS", "admin123")

        if user == admin_user and pw == admin_pass:
            session["admin"] = user
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
    # Set default secret key if not in env
    if not app.secret_key:
        app.secret_key = "dev-secret-key-change-in-production"
    
    # Set default admin credentials if not in env
    if not os.getenv("ADMIN_USER"):
        print("\n" + "="*50)
        print("⚠️  DEFAULT ADMIN CREDENTIALS:")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Change these in .env file for production!")
        print("="*50 + "\n")
    
    print("\n🚀 Starting Party Entry System...")
    print("📍 Server running at: http://localhost:5000")
    print("🔐 Admin login: http://localhost:5000/admin/login")
    print("📝 Register: http://localhost:5000/register")
    print("✅ Verify: http://localhost:5000/verify\n")
    
    # Get port from environment variable (for hosting) or use default
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    debug = os.environ.get("FLASK_DEBUG", "True") == "True"
    
    try:
        app.run(debug=debug, host=host, port=port, use_reloader=False)
    except OSError as e:
        if "Address already in use" in str(e) or "WinError 10048" in str(e):
            print(f"\n❌ Port {port} is already in use!")
            print("   Trying port 5001 instead...\n")
            app.run(debug=debug, host=host, port=5001, use_reloader=False)
        else:
            raise
