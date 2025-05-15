"""
This module defines the User model for the authentication service, 
including methods for password management and data serialization.
"""
from src.extensions import db, bcrypt

class User(db.Model):
    """
    Represents a user in the system with authentication details and utility methods 
    for password management and data serialization.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="user")  # nuevo

    def set_password(self, password):
        """
        Hashes the provided password and stores it in the password_hash attribute.
        Args:
            password (str): The plaintext password to be hashed.
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        """
        Verify if the provided password matches the stored password hash.
        Args:
            password (str): The plaintext password to verify.
        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Converts the user object into a dictionary representation.
        Returns:
            dict: A dictionary containing the user's id, name, and email.
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }
