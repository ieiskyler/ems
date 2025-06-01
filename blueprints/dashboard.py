from flask import Blueprint, render_template, session, redirect, url_for, request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
import re

dashboard_bp = Blueprint('dashboard', __name__)

def get_email_body(msg_data):
    def find_body(payload):
        # Prefer HTML
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/html' and 'data' in part.get('body', {}):
                    return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain' and 'data' in part.get('body', {}):
                    return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
            # Recursively search nested parts
            for part in payload['parts']:
                result = find_body(part)
                if result:
                    return result
        elif 'body' in payload and 'data' in payload['body']:
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
        return ""
    payload = msg_data.get('payload', {})
    return find_body(payload)

def get_header(headers, name):
    for h in headers:
        if h['name'].lower() == name.lower():
            return h['value']
    return ''

@dashboard_bp.route('/')
def dashboard():
    if 'credentials' not in session:
        return redirect(url_for('auth.login'))
    creds = Credentials(**session['credentials'])
    service = build('gmail', 'v1', credentials=creds)

    # Fetch max 10 sent emails
    sent_results = service.users().messages().list(userId='me', labelIds=['SENT'], maxResults=10).execute()
    sent_emails = []
    for msg in sent_results.get('messages', []):
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data['payload'].get('headers', [])
        # Determine status
        status = 'Unread' if 'UNREAD' in msg_data.get('labelIds', []) else 'Read'
        sent_emails.append({
            'subject': get_header(headers, 'Subject'),
            'to': get_header(headers, 'To'),
            'date': get_header(headers, 'Date'),
            'snippet': msg_data.get('snippet', ''),
            'body': get_email_body(msg_data),
            'status': status
        })

    # Fetch max 10 received emails
    inbox_results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=10).execute()
    received_emails = []
    for msg in inbox_results.get('messages', []):
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data['payload'].get('headers', [])
        status = 'Unread' if 'UNREAD' in msg_data.get('labelIds', []) else 'Read'
        received_emails.append({
            'subject': get_header(headers, 'Subject'),
            'from': get_header(headers, 'From'),
            'date': get_header(headers, 'Date'),
            'snippet': msg_data.get('snippet', ''),
            'body': get_email_body(msg_data),
            'status': status
        })

    return render_template(
        'dashboard.html',
        sent_emails=sent_emails,
        received_emails=received_emails
    )