# ==========================================
# Password Security
# ==========================================

import hashlib
import os


class PasswordManager:

    ITERATIONS = 120000

    # --------------------------------------
    # Hash Password
    # --------------------------------------

    @staticmethod
    def hash_password(password):

        salt = os.urandom(16)

        password_bytes = password.encode("utf-8")

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password_bytes,
            salt,
            PasswordManager.ITERATIONS
        )

        return (
            salt.hex()
            + ":"
            + password_hash.hex()
        )

    # --------------------------------------
    # Verify Password
    # --------------------------------------

    @staticmethod
    def verify_password(password, stored_password):

        try:

            salt_hex, hash_hex = stored_password.split(":")

            salt = bytes.fromhex(salt_hex)

            stored_hash = bytes.fromhex(hash_hex)

            password_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt,
                PasswordManager.ITERATIONS
            )

            return password_hash == stored_hash

        except (ValueError, TypeError):

            return False