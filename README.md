# 🎉 MONET PARTY - Party Entry System

A modern, secure party entry management system with QR code verification, built with Flask.

## Features

- ✨ Modern, responsive UI with dark theme
- 🎟️ QR code ticket generation
- 🔐 Admin-approved registration system
- 📱 Ticket verification system
- 📊 Admin dashboard with statistics
- 📧 Email notifications (optional)

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/chingchanghaunji-bit/MONET-PARTY.git
cd MONET-PARTY
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
- Windows:
  ```bash
  venv\Scripts\activate
  ```
- Linux/Mac:
  ```bash
  source venv/bin/activate
  ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the server:
```bash
python app.py
```

Or use the simple starter:
```bash
python run.py
```

6. Open your browser:
- Home: http://localhost:5000
- Admin: http://localhost:5000/admin/login
  - Username: `admin`
  - Password: `admin123`

## Project Structure

```
MONET-PARTY/
├── app.py                 # Main Flask application
├── run.py                 # Simple server starter
├── requirements.txt       # Python dependencies
├── database.db           # SQLite database (auto-created)
├── modules/
│   ├── db_handler.py     # Database operations
│   ├── qr_generator.py   # QR code generation
│   └── email_sender.py   # Email functionality
├── static/
│   ├── css/
│   │   └── style.css     # Modern styling
│   └── js/
│       └── main.js       # JavaScript functionality
└── templates/
    ├── index.html        # Home page
    ├── register.html     # Registration page
    ├── verify.html       # Ticket verification
    ├── success.html      # Registration success
    ├── result.html       # Verification result
    ├── admin_login.html  # Admin login
    └── admin_dashboard.html  # Admin panel
```

## Configuration

Create a `.env` file (optional) for custom settings:

```env
SECRET_KEY=your-secret-key-here
ADMIN_USER=admin
ADMIN_PASS=your-password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## Usage

### For Administrators

1. Login to admin panel
2. Add authorized user emails
3. Monitor registrations and verifications

### For Users

1. Get approved by admin
2. Register with your email
3. Receive QR code and ticket ID
4. Show at party entrance

## Technology Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **QR Codes:** qrcode library

## License

This project is open source and available for use.

---

**Made with ❤️ for seamless party management**

