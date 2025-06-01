from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def init_security(app):
    # SSL/TLS Security
    Talisman(app, 
        force_https=True,
        strict_transport_security=True,
        session_cookie_secure=True
    )

    # Rate Limiting
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

    return limiter