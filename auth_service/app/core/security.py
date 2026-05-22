"""
Password hashing using bcrypt.
Implements SCRUM-88 subtask: SCRUM-102 Password Hashing.
"""
from passlib.context import CryptContext

# pbkdf2_sha256 (very secure, platform-independent and avoids passlib/bcrypt bugs)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Hash a plain-text password. Returns the bcrypt hash string."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a stored hash."""
    return pwd_context.verify(plain_password, hashed_password)
