# Email Blaster

A Flask-based email campaign management system with Gmail integration.

## Features
- Gmail OAuth2 Authentication
- Mass Email Campaign Management
- Email Tracking System
- Personalized Email Templates
- Real-time Dashboard

## Tech Stack
- Python 3.x
- Flask
- Gmail API
- SQLite/PostgreSQL
- HTML/CSS/JavaScript

## Project Structure
```bash
email-blaster/
├── mail-blaster/
│   ├── blueprints/
│   │   ├── auth.py         # Authentication handling
│   │   ├── compose.py      # Email composition
│   │   ├── dashboard.py    # Dashboard views
│   │   └── tracking.py     # Email tracking
│   ├── static/
│   │   ├── compose.css
│   │   ├── compose.js
│   │   ├── dashboard.css
│   │   └── dashboard.js
│   ├── src/
│   │   ├── compose/
│   │   │   └── compose.html
│   │   ├── dashboard.html
│   │   └── login.html
│   └── app.py