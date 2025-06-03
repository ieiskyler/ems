import imaplib
import email
import os
import psycopg2
import re
from email.header import decode_header

DB_PARAMS = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

def check_for_bounce():
    # Connect to the email server
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(os.getenv('GMAIL_USERNAME'), os.getenv('GMAIL_APP_PASSWORD'))
        mail.select('inbox')
        
        # Search for messages from the mailer daemon
        result, data = mail.search(None, 'FROM "mailer-daemon@googlemail.com"')      
        
        if result == 'OK':
            email_ids = data[0].split()  # List of email IDs
            for eid in email_ids:
                # Fetch the email message by ID
                _, msg_data = mail.fetch(eid, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Extract bounced email from the message body
                        bounced_email = extract_bounced_email(msg)
                        
                        if bounced_email:  # Update only if a valid email is found
                            update_bounce_status(bounced_email)

        mail.logout()
    except Exception as e:
        print(f"Failed to connect/check for bounces: {e}")

def extract_bounced_email(msg):
    # Check the body for bounced email details
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True).decode(errors='ignore')
                # Use regex to extract the email address from the message body
                match = re.search(r"Your message wasn't delivered to ([\w\.-]+@[\w\.-]+)", payload)
                if match:
                    return match.group(1)  # Return the recipient email found

    else:
        payload = msg.get_payload(decode=True).decode(errors='ignore')
        match = re.search(r"Your message wasn't delivered to ([\w\.-]+@[\w\.-]+)", payload)
        if match:
            return match.group(1)

    print("No bounced email address found in the message.")
    return None

def update_bounce_status(bounced_email):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE email_tracking SET bouncing = TRUE WHERE recipient_email = %s
            """,
            (bounced_email,)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Failed to update database record: {e}")

# Call the bounce check function
if __name__ == "__main__":
    check_for_bounce()