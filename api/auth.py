import base64

VALID_USERNAME = "admin"
VALID_PASSWORD = "secret123"


def authenticate_credentials(auth_header):
    """
    Validates HTTP Basic Authentication header.
    Returns True if credentials are valid, False otherwise.
    """
    if not auth_header or not auth_header.startswith("Basic "):
        return False

    try:
        encoded_credentials = auth_header.split(" ")[1]
        decoded = base64.b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded.split(":", 1)
        return username == VALID_USERNAME and password == VALID_PASSWORD
    except Exception:
        return False