import bcrypt

def create_password_hash(password: str) -> str:
    """Create a password hash using bcrypt.
    """

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    return hashed.decode()

def check_password(password: str, hashed: str) -> bool:
    """Check a password against a hash.
    """

    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )
