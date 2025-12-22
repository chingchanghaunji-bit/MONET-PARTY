from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, Response
from dotenv import load_dotenv
import os
import uuid
import re
import secrets
import io
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
# PRODUCTION: PostgreSQL database handler (requires DATABASE_URL environment variable)
try:
    from modules.db_handler import (
        init_db,
        get_user,
        add_user,
        update_user,
        delete_user,
        fetch_all_users,
        get_stats
    )
except ImportError as e:
    print(f"❌ CRITICAL: Failed to import database handler: {e}")
    print("❌ Make sure psycopg2-binary is installed and Python version is 3.11.9")
    raise

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

# Add custom Jinja2 filter for timestamp conversion
def timestamp_to_datetime(timestamp):
    """Convert Unix timestamp to datetime string"""
    try:
        from datetime import datetime
        return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(timestamp)

app.jinja_env.filters['timestamp_to_datetime'] = timestamp_to_datetime

# FIXED: Ensure qrcodes directory exists (critical for Render deployment)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# ---------------------------------------------------
# MAIL CONFIG (Optional - app works without email)
# ---------------------------------------------------
_mail_port_raw = os.getenv("MAIL_PORT")
# safe fallback to 587 if None or invalid
_mail_port_safe = int(_mail_port_raw) if _mail_port_raw and _mail_port_raw.isdigit() else 587

app.config["MAIL_PORT"] = _mail_port_safe
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME") or os.getenv("MAIL_USER")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL") == "True"

# Initialize Flask-Mail
init_mail(app)

# ---------------------------------------------------
# DATABASE CONFIGURATION (PostgreSQL)
# ---------------------------------------------------
# DATABASE_URL is checked at startup, not at import time
# This prevents blocking during app import
DATABASE_URL = os.getenv('DATABASE_URL')


# ---------------------------------------------------
# STARTUP FUNCTION (Runs after app is created, not at import)
# ---------------------------------------------------
def initialize_app():
    """Initialize database and app configuration - called after app creation"""
    # Check DATABASE_URL
    if not DATABASE_URL:
        print("❌ ERROR: DATABASE_URL environment variable not set!")
        print("❌ Please create a PostgreSQL database in Render and set DATABASE_URL")
        print("❌ The app cannot function without a valid DATABASE_URL")
        print("❌ Go to Render Dashboard → Your Web Service → Environment → Add DATABASE_URL")
        # Don't raise - let Gunicorn start, but log the error
        return False
    
    print("✅ DATABASE_URL found - connecting to PostgreSQL")
    # Mask password in logs for security
    safe_url = DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL
    print(f"📁 Database: {safe_url}")
    
    # Initialize database (safe migration, idempotent)
    try:
        init_db()
        from modules.db_handler import get_stats
        stats = get_stats()
        print(f"📊 Database stats: {stats}")
        print("✅ PostgreSQL database initialized successfully")
        print("✅ Tables use IF NOT EXISTS - data persists across redeploys")
        print("✅ Migrations are idempotent - safe for redeploys")
        return True
    except Exception as e:
        print(f"❌ Error initializing PostgreSQL database: {e}")
        print("⚠️  Make sure DATABASE_URL is set correctly in Render environment variables")
        print("⚠️  Verify PostgreSQL database is running and accessible")
        import traceback
        traceback.print_exc()
        # Don't raise - let app start, but database operations will fail
        return False


# Initialize app on first request (non-blocking)
# Flask 3.x compatible - use before_request with flag
_app_initialized = False

@app.before_request
def startup():
    """Initialize app on first request (Flask 3.x compatible)"""
    global _app_initialized
    if not _app_initialized:
        _app_initialized = True
        initialize_app()


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

        # OPTIMIZED: Generate QR code with faster settings
        generate_qr(ticket_id, qr_path)

        # OPTIMIZED: Update database first (fast operation)
        # Note: update_user() now automatically creates backup, so no need for separate backup thread
        update_user(
            email,
            name=name,
            phone=phone,
            registered=1,
            ticket_id=ticket_id,
            registered_at=datetime.now().isoformat()
        )
        
        # OPTIMIZED: Return success page immediately (backup is automatic, email runs in background)

        # Run email in background (non-blocking)
        try:
            import threading
            def email_async():
                try:
                    send_email(email, name, ticket_id, qr_path)
                except Exception as e:
                    print(f"Warning: Email sending failed: {e}")
            
            # Start email in background thread
            email_thread = threading.Thread(target=email_async, daemon=True)
            email_thread.start()
        except Exception as e:
            print(f"Warning: Could not start email thread: {e}")

        # Return success page immediately (fast response)
        return render_template("success.html", name=name, ticket_id=ticket_id, qr_path=qr_path)

    return render_template("register.html")


@app.route("/verify/login", methods=["GET", "POST"])
def verify_login():
    """Verification requires admin login - redirect to admin login"""
    flash("Verification requires admin access. Please login as admin.", "info")
    return redirect(url_for("admin_login"))


@app.route("/verify/logout")
def verify_logout():
    """Logout from verification system (uses admin session)"""
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


def verify_required(f):
    """Decorator to require admin login for verification (admin-only)"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Verification is admin-only - use admin session check
        if "admin" not in session or not session.get("admin"):
            flash("Access denied. Admin login required for verification.", "error")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/verify", methods=["GET", "POST"])
@verify_required
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

        # Get admin credentials with proper environment variable handling
        # Support ADMIN_USER/ADMIN_PASS, ADMIN_ID/ADMIN_PASSWORD, and ADMIN_SECRET
        # Works on both local and Render production
        admin_user = os.getenv("ADMIN_USER") or os.getenv("ADMIN_ID") or "admin"
        admin_pass = os.getenv("ADMIN_PASS") or os.getenv("ADMIN_PASSWORD") or os.getenv("ADMIN_SECRET") or "admin123"

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
    # FIXED: Fetch ALL users - no limit, ensures all data up to 150+ users is displayed
    try:
        users = fetch_all_users()
        stats = get_stats()
        # Add user count to stats for display
        stats['displayed_count'] = len(users)
        
        # Add database info for PostgreSQL
        from modules.db_handler import get_connection_pool, DATABASE_URL
        import os
        db_info = {
            'type': 'PostgreSQL',
            'url': DATABASE_URL or 'Not configured',
            'is_render': os.getenv('RENDER') is not None,
            'pool_active': get_connection_pool() is not None,
            'connection_status': 'Connected' if get_connection_pool() else 'Not connected'
        }
        
        return render_template("admin_dashboard.html", users=users, stats=stats, db_info=db_info)
    except Exception as e:
        print(f"❌ Error in admin_dashboard: {e}")
        import traceback
        traceback.print_exc()
        flash(f"Error loading dashboard: {str(e)}", "error")
        return render_template("admin_dashboard.html", users=[], stats={'total': 0, 'registered': 0, 'verified': 0, 'pending': 0, 'displayed_count': 0}, db_info={})


@app.route("/admin/add", methods=["POST"])
@login_required
def add_allowed():
    email = request.form["email"].strip().lower()
    add_user(email)
    flash(f"User {email} added successfully!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/edit/<path:email>", methods=["GET", "POST"])
@login_required
def edit_user(email):
    """Edit user information"""
    # FIXED: Properly decode email from URL (handles special characters like +, @, etc.)
    from urllib.parse import unquote
    email = unquote(email)
    
    user = get_user(email=email)
    
    if not user:
        flash(f"User not found: {email}", "error")
        return redirect(url_for("admin_dashboard"))
    
    if request.method == "POST":
        # Get form data
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        registered = request.form.get("registered", "0") == "1"
        verified = request.form.get("verified", "0") == "1"
        ticket_id = request.form.get("ticket_id", "").strip().upper()
        money_amount = request.form.get("money_amount", "").strip()
        
        # Validate phone number if provided
        if phone:
            phone_cleaned = re.sub(r'\D', '', phone)
            if phone_cleaned.startswith('91') and len(phone_cleaned) == 12:
                phone_cleaned = phone_cleaned[2:]
            if len(phone_cleaned) == 10:
                phone = f"+91 {phone_cleaned[:5]} {phone_cleaned[5:]}"
            elif len(phone_cleaned) > 0:
                flash("Invalid phone number format. Please use 10-digit Indian mobile number.", "error")
                return render_template("admin_edit_user.html", user=user)
        
        # Validate money amount
        try:
            if money_amount:
                money_amount = float(money_amount)
                if money_amount < 0:
                    flash("Money amount cannot be negative.", "error")
                    return render_template("admin_edit_user.html", user=user)
            else:
                money_amount = 0.0
        except ValueError:
            flash("Invalid money amount. Please enter a valid number.", "error")
            return render_template("admin_edit_user.html", user=user)
        
        # Update user data
        update_data = {}
        if name:
            update_data["name"] = name
        if phone:
            update_data["phone"] = phone
        if ticket_id:
            update_data["ticket_id"] = ticket_id
        update_data["money_amount"] = money_amount
        
        update_data["registered"] = 1 if registered else 0
        update_data["verified"] = 1 if verified else 0
        
        # Update timestamps
        if registered and not user.get("registered"):
            update_data["registered_at"] = datetime.now().isoformat()
        if verified and not user.get("verified"):
            update_data["verified_at"] = datetime.now().isoformat()
        
        # Update user
        update_user(email, **update_data)
        # Note: update_user() now automatically creates backup
        
        flash(f"User {email} updated successfully!", "success")
        return redirect(url_for("admin_dashboard"))
    
    return render_template("admin_edit_user.html", user=user)


@app.route("/admin/delete/<email>", methods=["POST"])
@login_required
def delete_user_admin(email):
    """Delete a user from the database"""
    user = get_user(email=email)
    
    if not user:
        flash("User not found!", "error")
        return redirect(url_for("admin_dashboard"))
    
    # Delete the user
    deleted = delete_user(email)
    
    if deleted:
        # Note: delete_user() now automatically creates backup
        flash(f"User {email} deleted successfully!", "success")
    else:
        flash(f"Failed to delete user {email}!", "error")
    
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/backup")
@login_required
def admin_backup():
    """Database backup info - PostgreSQL handles backups automatically"""
    from modules.db_handler import get_stats, get_connection_pool
    import os
    
    stats = get_stats()
    db_info = {
        'type': 'PostgreSQL',
        'url': os.getenv('DATABASE_URL', 'Not set'),
        'stats': stats,
        'pool_status': 'Active' if get_connection_pool() else 'Inactive'
    }
    
    # PostgreSQL on Render has automatic backups, no manual backup needed
    return render_template("admin_backup.html", 
                         backup_created=False,
                         db_info=db_info,
                         backups=[],
                         is_postgresql=True)

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


@app.route("/download/ticket/<ticket_id>")
def download_ticket(ticket_id):
    """Download full ticket (QR code + ticket ID) as image"""
    from PIL import Image, ImageDraw, ImageFont
    
    try:
        # Load QR code image
        qr_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{ticket_id}.png")
        if not os.path.exists(qr_path):
            return "Ticket not found", 404
        
        qr_img = Image.open(qr_path)
        
        # Get user info
        user = get_user(ticket_id=ticket_id)
        if not user:
            return "User not found", 404
        
        name = user.get("name", "Guest")
        
        # Create full ticket image
        ticket_width = 600
        ticket_height = 800
        ticket_img = Image.new('RGB', (ticket_width, ticket_height), color='#1a1a2e')
        draw = ImageDraw.Draw(ticket_img)
        
        # Try to load a font, fallback to default if not available
        try:
            title_font = ImageFont.truetype("arial.ttf", 24)
            subtitle_font = ImageFont.truetype("arial.ttf", 16)
            ticket_font = ImageFont.truetype("arial.ttf", 32)
            text_font = ImageFont.truetype("arial.ttf", 18)
            small_font = ImageFont.truetype("arial.ttf", 12)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            ticket_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Draw header
        draw.rectangle([(0, 0), (ticket_width, 80)], fill='#6366f1')
        draw.text((ticket_width/2, 35), "AFTER PARTY - ENTRY TICKET", fill='white', font=title_font, anchor='mm')
        draw.text((ticket_width/2, 60), "Registration Successful", fill='white', font=subtitle_font, anchor='mm')
        
        # Resize and paste QR code
        qr_size = 300
        qr_resized = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        ticket_img.paste(qr_resized, ((ticket_width - qr_size) // 2, 120))
        
        # Draw ticket ID
        draw.text((ticket_width/2, 460), "Ticket ID:", fill='white', font=text_font, anchor='mm')
        draw.text((ticket_width/2, 500), ticket_id, fill='#6366f1', font=ticket_font, anchor='mm')
        
        # Draw name
        draw.text((ticket_width/2, 540), f"Name: {name}", fill='white', font=text_font, anchor='mm')
        
        # Draw warning
        draw.text((ticket_width/2, 580), "⚠️ IMPORTANT WARNING", fill='#ff9800', font=text_font, anchor='mm')
        draw.text((ticket_width/2, 600), "Loss of this code will lead to loss of pass", fill='white', font=small_font, anchor='mm')
        draw.text((ticket_width/2, 620), "NO REFUND will be provided in case of misuse", fill='white', font=small_font, anchor='mm')
        
        # Draw footer
        draw.text((ticket_width/2, 750), f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fill='#888888', font=small_font, anchor='mm')
        draw.text((ticket_width/2, 770), "© 2026 AFTER PARTY - LIGHT-BEAM VERIFICATION SYSTEM", fill='#888888', font=small_font, anchor='mm')
        
        # Save to bytes
        img_io = io.BytesIO()
        ticket_img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return Response(
            img_io,
            mimetype='image/png',
            headers={
                'Content-Disposition': f'attachment; filename=Full_Ticket_{ticket_id}.png'
            }
        )
    except Exception as e:
        print(f"Error generating ticket: {e}")
        return "Error generating ticket", 500


@app.route("/admin/export")
@login_required
def export_data():
    """Export all registered user data as a formatted text file"""
    users = fetch_all_users()
    
    # Create formatted text content
    lines = []
    lines.append("=" * 120)
    lines.append("PARTY ENTRY SYSTEM - REGISTERED USERS DATA EXPORT")
    lines.append("=" * 120)
    lines.append(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Total Records: {len(users)}")
    lines.append("=" * 120)
    lines.append("")
    
    # Header row
    header = f"{'S.No.':<6} {'Name':<25} {'Email':<30} {'Phone':<18} {'Ticket ID':<12} {'Money Amount':<15} {'Registered':<12} {'Verified':<12} {'Created At':<20} {'Registered At':<20} {'Verified At':<20}"
    lines.append(header)
    lines.append("-" * 140)
    
    # Data rows
    for idx, user in enumerate(users, 1):
        email = user[0] or 'N/A'
        name = user[1] or 'N/A'
        phone = user[2] or 'N/A'
        registered = 'Yes' if user[3] == 1 else 'No'
        ticket_id = user[4] or 'N/A'
        verified = 'Yes' if user[5] == 1 else 'No'
        money_amount = f"₹{user[9]:.2f}" if user[9] else '₹0.00'
        created_at = user[6][:19] if user[6] else 'N/A'
        registered_at = user[7][:19] if user[7] else 'N/A'
        verified_at = user[8][:19] if user[8] else 'N/A'
        
        # Format row with proper spacing
        row = f"{idx:<6} {name[:24]:<25} {email[:29]:<30} {phone[:17]:<18} {ticket_id[:11]:<12} {money_amount:<15} {registered:<12} {verified:<12} {created_at[:19]:<20} {registered_at[:19]:<20} {verified_at[:19]:<20}"
        lines.append(row)
    
    lines.append("")
    lines.append("=" * 120)
    lines.append("End of Report")
    lines.append("=" * 120)
    
    # Create response with text file
    content = "\n".join(lines)
    response = Response(
        content,
        mimetype='text/plain',
        headers={
            'Content-Disposition': f'attachment; filename=party_registrations_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        }
    )
    
    return response


@app.route("/admin/export/excel")
@login_required
def export_data_excel():
    """Export all registered user data as Excel file (.xlsx)"""
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
    except ImportError:
        return "Excel export requires openpyxl. Please install it: pip install openpyxl", 500
    
    users = fetch_all_users()
    
    # Create workbook and worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Party Registrations"
    
    # Define styles
    header_fill = PatternFill(start_color="6366f1", end_color="6366f1", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    center_align = Alignment(horizontal='center', vertical='center')
    
    # Header row
    headers = [
        'S.No.', 'Email', 'Name', 'Phone', 'Ticket ID', 'Money Amount',
        'Registered', 'Verified', 'Created At', 'Registered At', 'Verified At'
    ]
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = border
    
    # Data rows
    for idx, user in enumerate(users, 1):
        row_num = idx + 1
        email = user[0] or 'N/A'
        name = user[1] or 'N/A'
        phone = user[2] or 'N/A'
        registered = 'Yes' if user[3] == 1 else 'No'
        ticket_id = user[4] or 'N/A'
        verified = 'Yes' if user[5] == 1 else 'No'
        money_amount = f"₹{user[9]:.2f}" if user[9] else '₹0.00'
        created_at = user[6][:19] if user[6] else 'N/A'
        registered_at = user[7][:19] if user[7] else 'N/A'
        verified_at = user[8][:19] if user[8] else 'N/A'
        
        row_data = [
            idx, email, name, phone, ticket_id, money_amount,
            registered, verified, created_at, registered_at, verified_at
        ]
        
        for col_num, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.value = value
            cell.border = border
            if col_num == 1:  # S.No. column
                cell.alignment = center_align
    
    # Auto-adjust column widths
    for col_num in range(1, len(headers) + 1):
        column_letter = get_column_letter(col_num)
        max_length = 0
        for row in ws[column_letter]:
            try:
                if len(str(row.value)) > max_length:
                    max_length = len(str(row.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Add summary info
    ws.cell(row=len(users) + 3, column=1).value = f"Total Records: {len(users)}"
    ws.cell(row=len(users) + 4, column=1).value = f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Save to bytes
    excel_io = io.BytesIO()
    wb.save(excel_io)
    excel_io.seek(0)
    
    return Response(
        excel_io,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': f'attachment; filename=party_registrations_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        }
    )


# ---------------------------------------------------
# GRACEFUL SHUTDOWN
# ---------------------------------------------------
import atexit
def close_db_pool():
    """Close database connection pool on shutdown"""
    try:
        from modules.db_handler import close_pool
        close_pool()
    except:
        pass

atexit.register(close_db_pool)

# ---------------------------------------------------
# RUN APP
# ---------------------------------------------------
# ---------------------------------------------------
# PRODUCTION: App is started by Gunicorn
# ---------------------------------------------------
# No app.run() - Gunicorn handles server startup
# All initialization happens in startup() function
# This ensures the app is import-safe and doesn't block

# Print startup info (non-blocking)
if not DATABASE_URL:
    print("⚠️  WARNING: DATABASE_URL not set - database features will not work")
else:
    print("✅ DATABASE_URL configured - will initialize on first request")

# Check admin credentials (warnings only, no blocking)
admin_user = os.getenv("ADMIN_USER") or os.getenv("ADMIN_ID")
admin_pass = os.getenv("ADMIN_PASS") or os.getenv("ADMIN_PASSWORD") or os.getenv("ADMIN_SECRET")

if not admin_user or not admin_pass:
    print("⚠️  WARNING: Admin credentials not set - using defaults (admin/admin123)")
    print("⚠️  Set ADMIN_USER and ADMIN_PASS in environment variables for production!")
else:
    print("✅ Admin credentials configured")

print("🚀 Flask app initialized - ready for Gunicorn")
print("📝 Routes: /register, /admin/login, /verify (admin-only)")
