from flask import Blueprint, session, redirect, url_for, flash, request, get_flashed_messages
from google_auth_oauthlib.flow import Flow
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError
from googleapiclient.discovery import build
import os

auth_bp = Blueprint('auth', __name__)

GOOGLE_CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), "../credentials.json")
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']

@auth_bp.route('/login')
def login():
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:3773/oauth2callback'
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@auth_bp.route('/oauth2callback')
def oauth2callback():
    try:
        if 'state' not in session:
            flash("Session expired or invalid OAuth flow. Please try logging in again.", "danger")
            return redirect(url_for('auth.login'))
        state = session['state']
        flow = Flow.from_client_secrets_file(
            GOOGLE_CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            state=state,
            redirect_uri='http://localhost:3773/oauth2callback'
        )
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        service = build('gmail', 'v1', credentials=credentials)
        # Fetch user info and store in session
        user_info = service.users().getProfile(userId='me').execute()
        session['email'] = user_info['emailAddress']
        flash("Logged in with Google!", "success")
        return redirect(url_for('dashboard.dashboard'))
    except MismatchingStateError:
        flash("Security error: Session expired or mismatched. Please try logging in again.", "danger")
        return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    get_flashed_messages()  # This will consume any pending flash messages
    return redirect(url_for('auth.login'))