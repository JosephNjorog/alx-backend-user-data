#!/usr/bin/env python3
"""
This module contains the hash_password function that
uses bcrypt to encrypt the password received
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Returns a salted, hashed password, which is a byte string.

    Args:
        password (str): string type password

    Returns:
        bytes: salted, hashed password
    """
    return bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches the hashed password.

    Args:
        hashed_password (bytes): salted, hashed password
        password (str): string type password

    Returns:
        bool: True if the password is valid, False otherwise
    """
    return bcrypt.checkpw(bytes(password, "utf-8"), hashed_password)
