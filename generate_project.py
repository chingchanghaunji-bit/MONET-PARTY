import os

# --- Folder structure ---
folders = [
    "party_entry_app",
    "party_entry_app/static",
    "party_entry_app/static/qrcodes",
    "party_entry_app/templates",
    "party_entry_app/modules"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# --- Files and their content ---
files = {

    # app.py
    "party_entry_app/app.py": '''
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
from modules.db_handler import init_db, get_user, add_user, update_user, fetch_all_users
from modules.qr_generator import generate_qr
from modules.email_sender import send_email
from functools import wraps
import uuid

load_dotenv()

app = Flask(__name__)
app.secret_key = "super_secret_key"
app.config['UPLOAD_FOLDER'] = 'static/qrcodes'

# Initialize DB
init_db()

# --- Login required decorator ---
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return wrapper

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        name = request.form['name']
        phone = request.form['phone']

        user = get_user(email)
        if not user:
            return "❌ You are not authorized."
        if user['registered']:
            return "⚠️ Already registered."

        ticket_id = str(uuid.uuid4())[:8].upper()
        qr_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{ticket_id}.png")
        generate_qr(ticket_id, qr_path)

        update_user(email, name=name, phone=phone, registered=1, ticket_id=ticket_id)
        send_email(email, name, ticket_id, qr_path)

        return render_template('success.html', name=name, ticket_id=ticket_id, qr_path=qr_path)

    return render_template('register.html')

@app.route('/verify', methods=['GET','POST'])
def verify():
    if request.method == 'POST':
        code = request.form['ticket_id'].strip().upper()
        user = get_user(ticket_id=code)
        if not user:
            msg = "❌ Invalid Ticket!"
        elif user['verified']:
            msg = f"🚫 Ticket {code} already used!"
        else:
            msg = f"✅ Access Granted to {user['name']}!"
            update_user(user['email'], verified=1)
        return render_template('result.html', msg=msg)
    return render_template('verify.html')

# --- Admin Routes ---
@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        if user == os.getenv('ADMIN_USER') and pw == os.getenv('ADMIN_PASS'):
            session['admin'] = user
            return redirect(url_for('admin_dashboard'))
        return "❌ Invalid credentials."
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    users = fetch_all_users()
    return render_template('admin_dashboard.html', users=users)

@app.route('/admin/add', methods=['POST'])
@login_required
def add_allowed():
    email = request.form['email'].strip().lower()
    add_user(email)
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    os.makedirs('static/qrcodes', exist_ok=True)
    app.run(debug=True)
''',

    # db_handler.py
    "party_entry_app/modules/db_handler.py": '''
import sqlite3

DB_PATH = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS allowed (
                    email TEXT PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    registered INTEGER DEFAULT 0,
                    ticket_id TEXT,
                    verified INTEGER DEFAULT 0
                )""")
    conn.commit()
    conn.close()

def get_user(email=None, ticket_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if email:
        c.execute("SELECT * FROM allowed WHERE email=?", (email,))
    else:
        c.execute("SELECT * FROM allowed WHERE ticket_id=?", (ticket_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "email": row[0],
            "name": row[1],
            "phone": row[2],
            "registered": row[3],
            "ticket_id": row[4],
            "verified": row[5]
        }
    return None

def add_user(email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO allowed (email) VALUES (?)", (email,))
    conn.commit()
    conn.close()

def update_user(email, **kwargs):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for key, value in kwargs.items():
        c.execute(f"UPDATE allowed SET {key}=? WHERE email=?", (value, email))
    conn.commit()
    conn.close()

def fetch_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM allowed")
    rows = c.fetchall()
    conn.close()
    return rows
''',

    # qr_generator.py
    "party_entry_app/modules/qr_generator.py": '''
import qrcode

def generate_qr(data, path):
    img = qrcode.make(data)
    img.save(path)
''',

    # email_sender.py
    "party_entry_app/modules/email_sender.py": '''
from flask_mail import Mail, Message
from flask import Flask
import os

app = Flask(__name__)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == "True"
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

def send_email(email, name, ticket_id, qr_path):
    with app.app_context():
        msg = Message("Your Party Ticket 🎟️",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email])
        msg.body = f"Hi {name},\\n\\nYour Ticket ID: {ticket_id}\\nShow this QR at entry.\\n\\nHave fun!"
        with open(qr_path, "rb") as fp:
            msg.attach(filename=f"{ticket_id}.png", content_type='image/png', data=fp.read())
        mail.send(msg)
''',

    # .env
    "party_entry_app/.env": '''MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=yourgmail@gmail.com
MAIL_PASSWORD=your_app_password
ADMIN_USER=admin
ADMIN_PASS=YourStrongPassword123
''',

    # Templates
    "party_entry_app/templates/index.html": '''<html><body><h1>Welcome to the Party</h1>
<a href="/register">Register</a> | <a href="/verify">Verify Ticket</a></body></html>''',

    "party_entry_app/templates/register.html": '''<html><body>
<h2>Register</h2>
<form method="POST">
Name: <input name="name" required><br>
Phone: <input name="phone" required><br>
Email: <input name="email" required><br>
<input type="submit" value="Register">
</form>
</body></html>''',

    "party_entry_app/templates/success.html": '''<html><body>
<h2>Registration Successful!</h2>
<p>Hi {{name}}, your Ticket ID: {{ticket_id}}</p>
<img src="{{qr_path}}">
</body></html>''',

    "party_entry_app/templates/verify.html": '''<html><body>
<h2>Verify Ticket</h2>
<form method="POST">
Ticket ID: <input name="ticket_id" required>
<input type="submit" value="Verify">
</form>
</body></html>''',

    "party_entry_app/templates/result.html": '''<html><body>
<h2>Verification Result</h2>
<p>{{msg}}</p>
</body></html>''',

    "party_entry_app/templates/admin_login.html": '''<html><body>
<h2>Admin Login</h2>
<form method="POST">
Username: <input name="username" required><br>
Password: <input name="password" type="password" required><br>
<input type="submit" value="Login">
</form>
</body></html>''',

    "party_entry_app/templates/admin_dashboard.html": '''<html><body>
<h2>Admin Dashboard</h2>
<form method="POST" action="/admin/add">
Add allowed email: <input name="email" required>
<input type="submit" value="Add">
</form>
<table border="1">
<tr><th>Email</th><th>Name</th><th>Phone</th><th>Registered</th><th>Ticket ID</th><th>Verified</th></tr>
{% for user in users %}
<tr>
<td>{{user[0]}}</td><td>{{user[1]}}</td><td>{{user[2]}}</td>
<td>{{user[3]}}</td><td>{{user[4]}}</td><td>{{user[5]}}</td>
</tr>
{% endfor %}
</table>
<a href="/admin/logout">Logout</a>
</body></html>'''
}

# --- Write files ---
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Full Party Entry App created in 'party_entry_app' folder!")
print("Next steps: create virtual env, install dependencies, run app.py")
