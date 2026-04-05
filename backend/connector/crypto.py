from django.conf import settings
from cryptography.fernet import Fernet

# Generate a key for encryption. In a real application, this key should be
# stored securely and not hard-coded. For example, in an environment variable
# or a secret management service.
# To generate a key, you can run:
# from cryptography.fernet import Fernet
# key = Fernet.generate_key()
# print(key)
# For this example, we'll use a key from the settings.
if not settings.SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in settings for encryption.")

# Ensure the secret key is a valid Fernet key (32 url-safe base64-encoded bytes)
# For simplicity, we'll use the first 32 bytes of the Django secret key
# and encode it to base64, but a dedicated key is recommended.
import base64
key = base64.urlsafe_b64encode(settings.SECRET_KEY.encode()[:32])
cipher_suite = Fernet(key)

def encrypt_password(password: str) -> str:
    """Encrypts a password."""
    if not password:
        return ''
    encrypted_text = cipher_suite.encrypt(password.encode())
    return encrypted_text.decode()

def decrypt_password(encrypted_password: str) -> str:
    """Decrypts an encrypted password."""
    if not encrypted_password:
        return ''
    decrypted_text = cipher_suite.decrypt(encrypted_password.encode())
    return decrypted_text.decode()
