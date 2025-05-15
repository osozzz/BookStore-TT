"""
Utility functions for generating and verifying JSON Web Tokens (JWTs)
used for authentication purposes.
"""
import os
from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "default-dev-secret")

def generate_token(user_id, name, role, expires_in=3600):
    """
    Generate a JWT token for a user.
    Args:
        user_id (int): The ID of the user.
        name (str): The name of the user.
        role (str): The user's role.
        expires_in (int, optional): Token expiration in seconds. Defaults to 3600.
    Returns:
        str: Encoded JWT token.
    """
    payload = {
        "id": user_id,
        "name": name,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token):
    """
	Verifies and decodes a JWT token.
	Args:
		token (str): The JWT token to be verified.
	Returns:
		dict: A dictionary containing the decoded token data if valid, 
			or an error message if the token is invalid or expired.
	"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {
            "id": payload["id"],
            "name": payload["name"]
        }
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
