from src.models.user import User

def get_all_users():
    """
    Fetch all users from the auth-service DB.
    Returns:
        list[dict]: List of user dictionaries
    """
    users = User.query.all()
    return [user.to_dict() for user in users]
