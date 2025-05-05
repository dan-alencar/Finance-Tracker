import hashlib
import uuid

class User:
    def __init__(self, first_name, last_name, user_id=None, security_hash=None):
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id or str(uuid.uuid4())
        self.security_hash = security_hash

    def set_security_key(self, binary_key):
        """Hashes and stores the key."""
        self.security_hash = hashlib.sha256(binary_key.encode()).hexdigest()

    def verify_key(self, binary_key):
        """Verifies a given key against stored hash."""
        return hashlib.sha256(binary_key.encode()).hexdigest() == self.security_hash
