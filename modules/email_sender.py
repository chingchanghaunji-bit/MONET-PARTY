
from flask_mail import Mail, Message
from flask import current_app

mail = None

def init_mail(app):
    global mail
    mail = Mail(app)
    return mail

def send_email(email, name, ticket_id, qr_path):
    try:
        if not mail:
            print("Warning: Mail not initialized. Email not sent.")
            return
        msg = Message(
            "Your Party Ticket 🎟️ - Party Entry System",
            sender=current_app.config.get('MAIL_USERNAME', 'noreply@partypass.com'),
            recipients=[email]
        )
        msg.html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h1 style="color: #6366f1; text-align: center;">🎉 Your Party Ticket is Ready!</h1>
                <p>Hi <strong>{name}</strong>,</p>
                <p>Your registration was successful! Here's your party ticket information:</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center;">
                    <p style="margin: 10px 0;"><strong>Ticket ID:</strong></p>
                    <p style="font-size: 24px; font-weight: bold; letter-spacing: 3px; color: #6366f1; font-family: monospace;">{ticket_id}</p>
                </div>
                
                <p style="text-align: center; margin: 20px 0;">
                    <strong>Your QR Code is attached to this email.</strong>
                </p>
                
                <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 4px;">
                    <p style="margin: 0;"><strong>📋 Important Instructions:</strong></p>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        <li>Save your QR code image</li>
                        <li>Remember your Ticket ID: <strong>{ticket_id}</strong></li>
                        <li>Bring a valid ID to the party</li>
                        <li>Show your QR code or Ticket ID at the entrance</li>
                    </ul>
                </div>
                
                <p style="margin-top: 30px;">We look forward to seeing you at the party!</p>
                <p style="color: #666; font-size: 14px; margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">
                    This is an automated message. Please do not reply to this email.
                </p>
            </div>
        </body>
        </html>
        """
        msg.body = f"""Hi {name},

Your Party Ticket is Ready!

Ticket ID: {ticket_id}

Your QR code is attached to this email. Please save it and bring it to the party.

Important Instructions:
- Save your QR code image
- Remember your Ticket ID: {ticket_id}
- Bring a valid ID to the party
- Show your QR code or Ticket ID at the entrance

We look forward to seeing you at the party!

---
This is an automated message. Please do not reply to this email.
"""
        with open(qr_path, "rb") as fp:
            msg.attach(filename=f"{ticket_id}.png", content_type='image/png', data=fp.read())
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")
        # Don't fail registration if email fails
