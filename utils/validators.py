from email_validator import validate_email, EmailNotValidError

def validate_email_address(email):
    try:
        validate_email(email)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)

def sanitize_input(text):
    import bleach
    return bleach.clean(text)