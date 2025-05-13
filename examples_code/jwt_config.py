"""
JWT configuration module providing functions to get JWT public and private keys.
"""

import os
import logging
from typing import Optional
from pathlib import Path

# Configure logging
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
logger = logging.getLogger(__name__)

# Get the absolute path to the examples_code directory
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Default paths for key files (using absolute paths)
DEFAULT_PRIVATE_KEY_PATH = str(BASE_DIR / "private_key.pem")
DEFAULT_PUBLIC_KEY_PATH = str(BASE_DIR / "public_key.pem")


def get_jwt_private_key(key_path: str = DEFAULT_PRIVATE_KEY_PATH) -> Optional[str]:
    """
    Get the JWT private key from a PEM file.

    Args:
        key_path: Path to the private key PEM file (default: absolute path to examples_code/private_key.pem)

    Returns:
        Optional[str]: The private key content as a string, or None if the file cannot be read
    """
    # Convert to absolute path if it's a relative path
    if not os.path.isabs(key_path):
        key_path = str(BASE_DIR / key_path)

    if not os.path.exists(key_path):
        logger.error(f"Private key file not found: {key_path}")
        return None

    try:
        with open(key_path, "r") as f:
            private_key = f.read()
        logger.info(f"Successfully read private key from {key_path}")
        return private_key
    except Exception as e:
        logger.error(f"Error reading private key file: {e}")
        return None


def get_jwt_public_key(key_path: str = DEFAULT_PUBLIC_KEY_PATH) -> Optional[str]:
    """
    Get the JWT public key from a PEM file.

    Args:
        key_path: Path to the public key PEM file (default: absolute path to examples_code/public_key.pem)

    Returns:
        Optional[str]: The public key content as a string, or None if the file cannot be read
    """
    # Convert to absolute path if it's a relative path
    if not os.path.isabs(key_path):
        key_path = str(BASE_DIR / key_path)

    if not os.path.exists(key_path):
        logger.error(f"Public key file not found: {key_path}")
        return None

    try:
        with open(key_path, "r") as f:
            public_key = f.read()
        logger.info(f"Successfully read public key from {key_path}")
        return public_key
    except Exception as e:
        logger.error(f"Error reading public key file: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Print the absolute paths being used
    print(f"Private key path: {DEFAULT_PRIVATE_KEY_PATH}")
    print(f"Public key path: {DEFAULT_PUBLIC_KEY_PATH}")

    # Get keys
    private_key = get_jwt_private_key()
    public_key = get_jwt_public_key()

    # Display key information
    if private_key:
        print("\n=== Private Key ===")
        print(private_key)
        print(f"Size: {len(private_key)} bytes")
    else:
        print("\nFailed to read private key")

    if public_key:
        print("\n=== Public Key ===")
        print(public_key)
        print(f"Size: {len(public_key)} bytes")
    else:
        print("\nFailed to read public key")
