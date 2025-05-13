"""
Client module for accessing the server with DID authentication.
"""

import os
import json
import logging
import asyncio
import aiohttp
from pathlib import Path
from typing import Tuple, Dict, Optional
from urllib.parse import urlparse

from agent_connect.authentication import DIDWbaAuthHeader

# Configure logging
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
logger = logging.getLogger(__name__)

# Constants
SERVER_URL = "http://localhost:8000"
TEST_ENDPOINT = "/test"
# Get current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get project root directory (parent directory of current directory)
root_dir = os.path.dirname(script_dir)
# Use absolute path
DID_DOCUMENT_PATH = str(Path(root_dir) / "use_did_test_public/did.json")
PRIVATE_KEY_PATH = str(Path(root_dir) / "use_did_test_public/key-1_private.pem")


async def test_did_auth(url: str, auth_client: DIDWbaAuthHeader) -> Optional[str]:
    """
    Test DID authentication and get token.

    Args:
        url: URL to test
        auth_client: DID authentication client

    Returns:
        Optional[str]: The token if authentication is successful and a token is received, otherwise None
    """
    try:
        # Get authentication header
        headers = auth_client.get_auth_header(url)
        logger.info(f"Sending request to {url} with Authentication header")

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                logger.info(f"Received response with status code: {response.status}")
                logger.info(f"Response headers: {response.headers}")

                if response.status == 200:
                    # Update token and get return value
                    token = auth_client.update_token(url, dict(response.headers))

                    if token:
                        logger.info(
                            f"Successfully authenticated and received token: {token[:30]}..."
                        )
                        return token
                    else:
                        logger.warning(
                            "Authentication successful but no token received or token format incorrect"
                        )
                        logger.warning(f"Response headers: {response.headers}")
                        return None
                else:
                    response_text = await response.text()
                    logger.error(
                        f"Authentication failed with status code: {response.status}"
                    )
                    logger.error(f"Response: {response_text}")
                    return None
    except Exception as e:
        logger.error(f"Error during authentication test: {e}")
        logger.error("Stack trace:", exc_info=True)
        return None


async def verify_token(url: str, auth_client: DIDWbaAuthHeader) -> bool:
    """
    Verify token by making a request with it.

    Args:
        url: URL to test
        auth_client: DID authentication client

    Returns:
        bool: Whether the token is valid
    """
    try:
        # Get authentication header (using stored token)
        headers = auth_client.get_auth_header(url)
        logger.info(f"Verifying token at {url}")

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                logger.info(f"Received response with status code: {response.status}")
                logger.info(f"Response headers: {response.headers}")

                if response.status == 200:
                    logger.info("Token verification successful")
                    return True
                else:
                    response_text = await response.text()
                    logger.error(
                        f"Token verification failed with status code: {response.status}"
                    )
                    logger.error(f"Response: {response_text}")

                    # If the token is invalid, clear the token
                    auth_client.clear_token(url)
                    return False
    except Exception as e:
        logger.error(f"Error during token verification: {e}")
        logger.error("Stack trace:", exc_info=True)
        return False


async def main():
    """Main function to run the client."""
    try:
        # 1. Create DID authentication client
        auth_client = DIDWbaAuthHeader(
            did_document_path=DID_DOCUMENT_PATH, private_key_path=PRIVATE_KEY_PATH
        )
        logger.info("Created DID authentication client")

        # 2. Test DID authentication and get token
        test_url = f"{SERVER_URL}{TEST_ENDPOINT}"
        logger.info(f"Testing DID authentication at {test_url}")
        token = await test_did_auth(test_url, auth_client)

        if token is None:
            logger.error("DID authentication test failed or no token received")
            return

        logger.info("DID authentication test successful and token received")

        # 3. Verify token
        logger.info("Verifying token...")
        token_valid = await verify_token(test_url, auth_client)

        if token_valid:
            logger.info("Token verification successful")
        else:
            logger.error("Token verification failed")

    except Exception as e:
        logger.error(f"Error in main function: {e}")
        logger.error("Stack trace:", exc_info=True)


# Directly run the client code
if __name__ == "__main__":
    # Run the client
    logger.info("Starting DID authentication client")
    asyncio.run(main())
