import hashlib
import secrets 
import bcrypt

def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256 with a random salt
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode("utf8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password by comparing it with the stored hash.
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode("utf-8")) 
