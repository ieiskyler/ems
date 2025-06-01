from flask import Blueprint, session, redirect, url_for, request, flash
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

reply_bp = Blueprint('reply', __name__, url_prefix='/reply')

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

@reply_bp.route('/', methods=['POST'])
def reply():
    if 'credentials' not in session:
        return redirect(url_for('auth.login'))
    creds = Credentials(**session['credentials'])
    service = build('gmail', 'v1', credentials=creds)
    to = request.form['to']
    subject = request.form['subject']
    message = request.form['message']
    sender = session.get('email', 'me')
    msg = create_message(sender, to, subject, message)
    try:
        service.users().messages().send(userId='me', body=msg).execute()
        flash("Reply sent!", "success")
    except Exception as e:
        flash(f"Failed to send reply: {e}", "danger")
    return redirect(url_for('dashboard.dashboard'))