# Email Blaster

A Flask-based email campaign management system with Gmail integration, real-time dashboard, and email tracking.

---

## Features

- **Gmail OAuth2 Authentication**: Secure login with Google.
- **Mass Email Campaign Management**: Compose and send personalized emails to multiple recipients.
- **Email Tracking System**: Track email opens with a 1x1 pixel.
- **Personalized Email Templates**: Use `{name}` in subject/body for dynamic content.
- **Real-time Dashboard**: View sent and received emails.
- **Bounce Detection**: Detect bounced emails and update tracking.

---

## Tech Stack

- Python 3.x
- Flask
- Gmail API (via Google API Python Client)
- PostgreSQL (for tracking)
- HTML/CSS/JavaScript

---

## Project Structure

```text
email-blaster/
├── app.py
├── .env
├── requirements.txt
├── credentials.json
├── blueprints/
│   ├── auth.py
│   ├── compose.py
│   ├── dashboard.py
│   ├── tracking.py
│   └── bounce_detector.py
├── src/
│   ├── dashboard.html
│   └── compose/
│       └── compose.html
├── static/
│   ├── dashboard.css
│   ├── dashboard.js
│   ├── compose.css
│   └── compose.js
├── utils/
│   └── validators.py
└── tracking.csv (legacy, not used if DB is enabled)
```

---

## Requirements

- Python 3.10+
- PostgreSQL database (for tracking)
- Google Cloud project with Gmail API enabled
- OAuth2 credentials (`credentials.json`)

### Python Packages

See [`requirements.txt`](requirements.txt):

```
psycopg2-binary
flask
python-dotenv
googleapi
email-validator
bleach
google-auth-oauthlib
google-api-python-client
```

Install with:

```sh
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root with:

```
SECRET_KEY=your_flask_secret_key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
GMAIL_USERNAME=your_gmail_address
GMAIL_APP_PASSWORD=your_gmail_app_password
```

---

## Database Setup

Create the `email_tracking` table in your PostgreSQL database:

```sql
CREATE TABLE email_tracking (
    id SERIAL PRIMARY KEY,
    recipient_email VARCHAR(255),
    recipient_name VARCHAR(255),
    subject TEXT,
    status VARCHAR(50),
    tracking_id UUID,
    opened BOOLEAN DEFAULT FALSE,
    clicked BOOLEAN DEFAULT FALSE,
    bouncing BOOLEAN DEFAULT FALSE
);
```

---

## Google API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable the Gmail API.
3. Create OAuth2 credentials and download `credentials.json` to the project root.

---

## Running the App

1. **Set up your `.env` and database as above.**
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the Flask app:**
   ```sh
   python app.py
   ```
4. **Visit** [http://localhost:3773](http://localhost:3773) in your browser.

---

## Usage

- **Login:** Click "Login with Google" and authorize.
- **Compose:** Go to "Compose Email", enter recipients as `email,name` (one per line or comma-separated), subject, and message. Use `{name}` for personalization.
- **Dashboard:** View sent/received emails, open details in modal.
- **Tracking:** Email opens are tracked via a 1x1 pixel and updated in the database.
- **Bounce Detection:** Run `python blueprints/bounce_detector.py` to update bounce status for undelivered emails.

---

## Notes

- The app uses PostgreSQL for tracking. If you want to use CSV tracking, see the commented code in [`blueprints/compose copy.py`](blueprints/compose%20copy.py).
- Make sure your Google account allows access to less secure apps or use an app password if 2FA is enabled.

---

## Troubleshooting

- **OAuth errors:** Ensure redirect URI matches in Google Cloud and `.env`.
- **DB errors:** Check your `.env` and that PostgreSQL is running.
- **Gmail API errors:** Ensure `credentials.json` is correct and API is enabled.

---

## License

MIT License

---

## Authors

- ieiskyler
