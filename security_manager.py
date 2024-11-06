import hashlib
import hmac
import os
import time

class SecurityManager:
    def __init__(self):
        # Store allowed users and access levels in a dictionary for quick lookup
        self.user_data = {}  # Structure: {username: {"password_hash": ..., "access_level": ...}}
        self.active_sessions = {}  # Tracks user sessions, e.g., {username: session_token}

    # ---- 1. Add User ----
    def add_user(self, username: str, password: str, access_level: str) -> str:
        """
        Adds a new user with a hashed password and access level.
        """
        if username in self.user_data:
            return "User already exists."
        password_hash = self.hash_password(password)
        self.user_data[username] = {"password_hash": password_hash, "access_level": access_level}
        return f"User '{username}' added with access level '{access_level}'."

    # ---- 2. Verify User ----
    def verify_user(self, username: str, password: str) -> bool:
        """
        Verifies a user by checking the hashed password.
        """
        user_info = self.user_data.get(username)
        if not user_info:
            return False
        return self.check_password(password, user_info["password_hash"])

    # ---- 3. Create Session ----
    def create_session(self, username: str) -> str:
        """
        Creates a session for a verified user.
        """
        session_token = self.generate_token()
        self.active_sessions[username] = session_token
        return session_token

    # ---- 4. Check Session ----
    def check_session(self, username: str, session_token: str) -> bool:
        """
        Checks if a session token is valid for a given user.
        """
        return self.active_sessions.get(username) == session_token

    # ---- 5. Hash Password ----
    def hash_password(self, password: str) -> str:
        """
        Hashes a password with a unique salt.
        """
        salt = os.urandom(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return salt.hex() + password_hash.hex()

    # ---- 6. Check Password ----
    def check_password(self, password: str, hashed: str) -> bool:
        """
        Checks if the password matches the stored hashed password.
        """
        salt = bytes.fromhex(hashed[:32])
        original_hash = hashed[32:]
        check_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
        return hmac.compare_digest(check_hash, original_hash)

    # ---- 7. Generate Token ----
    def generate_token(self) -> str:
        """
        Generates a secure session token.
        """
        return hashlib.sha256(os.urandom(32)).hexdigest()

    # ---- 8. Encrypt Data ----
    def encrypt_data(self, data: str, key: str) -> str:
        """
        Encrypts data using a symmetric encryption algorithm.
        """
        # Placeholder for encryption logic (e.g., using Fernet from cryptography library)
        return "encrypted_data"

    # ---- 9. Decrypt Data ----
    def decrypt_data(self, encrypted_data: str, key: str) -> str:
        """
        Decrypts encrypted data using a symmetric encryption algorithm.
        """
        # Placeholder for decryption logic
        return "decrypted_data"

# Example Usage
if __name__ == "__main__":
    security_manager = SecurityManager()
    
    # Add a user
    print(security_manager.add_user("Alice", "password123", "admin"))
    
    # Verify user
    is_verified = security_manager.verify_user("Alice", "password123")
    print("User verified:", is_verified)
    
    # Create session
    if is_verified:
        session_token = security_manager.create_session("Alice")
        print("Session Token:", session_token)
        
        # Check session
        print("Session valid:", security_manager.check_session("Alice", session_token))