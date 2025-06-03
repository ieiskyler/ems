from flask import Flask
import os
import csv
from dotenv import load_dotenv
import logging


logging.basicConfig(level=logging.INFO)
load_dotenv(dotenv_path='~/Downloads/test/email-blaster/ems/.env')

# Change this to 0 https and 1 for http
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

DB_PARAMS = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

app = Flask(__name__, template_folder='src', static_folder='static')
app.secret_key = os.getenv('SECRET_KEY')

from blueprints.auth import auth_bp
from blueprints.dashboard import dashboard_bp
from blueprints.compose import compose_bp
from blueprints.tracking import tracking_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(compose_bp)
app.register_blueprint(tracking_bp)

if __name__ == '__main__':  
    app.run(debug=True, port=3773)
    
    
    
    
"""TRACKING_FILE = "tracking.csv"
CSV_HEADER = ['recipient_email', 'recipient_name', 'subject', 'status', 'tracking_id', 'opened', 'clicked']

# Ensure CSV header exists
if not os.path.exists(TRACKING_FILE) or os.path.getsize(TRACKING_FILE) == 0:
    with open(TRACKING_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADER)
"""