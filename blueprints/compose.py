from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import uuid
from flask import url_for, session
import psycopg2
import os

compose_bp = Blueprint('compose', __name__, url_prefix='/compose')
DB_PARAMS = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

def create_message(sender, to, subject, message_text):
    from email.mime.text import MIMEText
    import base64
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}


def save_email_tracking_to_db(recipient_email, recipient_name, subject, status, tracking_id):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO email_tracking (recipient_email, recipient_name, subject, status, tracking_id, opened, clicked)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (recipient_email, recipient_name, subject, status, tracking_id, False, False)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Failed to insert record into database: {e}")

@compose_bp.route('/', methods=['GET', 'POST'])
def compose():
    if 'credentials' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        creds = Credentials(**session['credentials'])
        service = build('gmail', 'v1', credentials=creds)
        recipients = []
        for line in request.form['recipients'].splitlines():
            parts = line.strip().split(',')
            if len(parts) == 2:
                recipients.append({'email': parts[0], 'name': parts[1]})
        msgText = request.form['message']
        msgSub = request.form['subject']
        failed = []
        for recip in recipients:
            msgRecip = recip['email']
            recipName = recip['name']
            personalized_msg = msgText.replace("{name}", recipName)
            personalized_sub = msgSub.replace("{name}", recipName)

            tracking_id = str(uuid.uuid4())
            tracking_url = url_for('tracking.track', tracking_id=tracking_id, _external=True)

            # Add tracking pixel and example tracked link to the body
            body_with_tracking = personalized_msg + \
                f'<img src="{tracking_url}" width="1" height="1" style="display:none;">'
            msg = create_message(session['email'], msgRecip, personalized_sub, body_with_tracking)

            save_email_tracking_to_db(msgRecip, recipName, personalized_sub, "SENT", tracking_id)

            try:
                service.users().messages().send(userId='me', body=msg).execute()
            except Exception as e:
                failed.append(msgRecip)
                print(f"Failed to send email to {msgRecip}: {e}")

        if failed:
            flash(f"Failed to send to: {', '.join(failed)}", "danger")
        else:
            flash("All emails sent successfully!", "success")
        return redirect(url_for('compose.compose'))
    return render_template('compose/compose.html')



"""# Write a new row with empty opened/clicked columns
            with open(TRACKING_FILE, "a", newline='') as f:
                writer = csv.writer(f)
                writer.writerow([msgRecip, recipName, personalized_sub, "SENT", tracking_id])
            try:
                service.users().messages().send(userId='me', body=msg).execute()
            except Exception as e:
                failed.append(msgRecip)
                """