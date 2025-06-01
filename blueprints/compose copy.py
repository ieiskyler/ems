from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import uuid, csv
from datetime import datetime

compose_bp = Blueprint('compose', __name__, url_prefix='/compose')
TRACKING_FILE = "tracking.csv"

def create_message(sender, to, subject, message_text):
    from email.mime.text import MIMEText
    import base64
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

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

            # Remove tracking URL generation for now
            #tracking_id = str(uuid.uuid4())
            #tracking_url = url_for('track', tracking_id=tracking_id, _external=True) + f"?email={msgRecip}&name={recipName}&subject={personalized_sub}"
            #personalized_msg = personalized_msg.replace("{tracking_url}", tracking_url)

            msg = create_message(session['email'], msgRecip, personalized_sub, personalized_msg)
            with open(TRACKING_FILE, "a", newline='') as f:
                writer = csv.writer(f)
                #remove tracking_id for now
                writer.writerow([msgRecip, recipName, personalized_sub, "SENT"])
            try:
                service.users().messages().send(userId='me', body=msg).execute()
            except Exception as e:
                failed.append(msgRecip)
        if failed:
            flash(f"Failed to send to: {', '.join(failed)}", "danger")
        else:
            flash("All emails sent successfully!", "success")
        return redirect(url_for('compose.compose'))
    return render_template('compose/compose.html')