"""
Client module for accessing the server with DID authentication.
"""

import os
import json
import logging
import asyncio
import aiohttp
from pathlib import Path
from typing import Dict, Optional
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from urllib.parse import urlparse

# Import agent_connect for DID authentication
from agent_connect.authentication.did_wba import (
    generate_auth_header
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class DIDAuthClient:
    """
    Simplified DID authentication client providing HTTP authentication headers.
    """
    
    def __init__(self, did_document_path: str, private_key_path: str):
        """
        Initialize the DID authentication client.
        
        Args:
            did_document_path: Path to the DID document.
            private_key_path: Path to the private key.
        """
        self.did_document_path = did_document_path
        self.private_key_path = private_key_path
        
        # State variables
        self.did_document = None
        self.auth_headers = {}  # Store DID authentication headers by domain
        self.tokens = {}  # Store tokens by domain
        
        logger.info("DIDAuthClient initialized")
    
    def _get_domain(self, server_url: str) -> str:
        """Get domain from URL"""
        parsed_url = urlparse(server_url)
        domain = parsed_url.netloc.split(':')[0]
        return domain
    
    def _load_did_document(self) -> Dict:
        """Load DID document"""
        try:
            if self.did_document:
                return self.did_document
                
            base_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            did_path = base_dir / self.did_document_path
            
            with open(did_path, 'r') as f:
                did_document = json.load(f)
            
            self.did_document = did_document
            logger.info(f"Loaded DID document: {did_path}")
            return did_document
        except Exception as e:
            logger.error(f"Error loading DID document: {e}")
            raise
    
    def _load_private_key(self) -> ec.EllipticCurvePrivateKey:
        """Load private key"""
        try:
            base_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            key_path = base_dir / self.private_key_path
            
            with open(key_path, 'rb') as f:
                private_key_data = f.read()
            
            private_key = serialization.load_pem_private_key(
                private_key_data,
                password=None
            )
            
            logger.debug(f"Loaded private key: {key_path}")
            return private_key
        except Exception as e:
            logger.error(f"Error loading private key: {e}")
            raise
    
    def _sign_callback(self, content: bytes, method_fragment: str) -> bytes:
        """Sign callback function"""
        try:
            private_key = self._load_private_key()
            signature = private_key.sign(
                content,
                ec.ECDSA(hashes.SHA256())
            )
            
            logger.debug(f"Signed content, method fragment: {method_fragment}")
            return signature
        except Exception as e:
            logger.error(f"Error signing content: {e}")
            raise
    
    def _generate_auth_header(self, domain: str) -> str:
        """Generate DID authentication header"""
        try:
            did_document = self._load_did_document()
            
            auth_header = generate_auth_header(
                did_document,
                domain,
                self._sign_callback
            )
            
            logger.info(f"Generated authentication header for domain {domain}: {auth_header[:30]}...")
            return auth_header
        except Exception as e:
            logger.error(f"Error generating authentication header: {e}")
            raise
    
    def get_auth_header(self, server_url: str, force_new: bool = False) -> Dict[str, str]:
        """
        Get authentication header.
        
        Args:
            server_url: Server URL.
            force_new: Whether to force generate a new DID authentication header.
            
        Returns:
            Dict[str, str]: HTTP header dictionary.
        """
        domain = self._get_domain(server_url)
        
        # If there is a token and not forcing a new authentication header, return the token
        if domain in self.tokens and not force_new:
            token = self.tokens[domain]
            logger.info(f"Using existing token for domain {domain}")
            return {"Authorization": f"Bearer {token}"}
        
        # Otherwise, generate or use existing DID authentication header
        if domain not in self.auth_headers or force_new:
            self.auth_headers[domain] = self._generate_auth_header(domain)
        
        logger.info(f"Using DID authentication header for domain {domain}")
        return {"Authorization": self.auth_headers[domain]}
    
    def update_token(self, server_url: str, headers: Dict[str, str]) -> Optional[str]:
        """
        Update token from response headers.
        
        Args:
            server_url: Server URL.
            headers: Response header dictionary.
            
        Returns:
            Optional[str]: Updated token, or None if no valid token is found.
        """
        domain = self._get_domain(server_url)
        auth_header = headers.get("Authorization")
        
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header[7:]  # Remove "Bearer " prefix
            self.tokens[domain] = token
            logger.info(f"Updated token for domain {domain}: {token[:30]}...")
            return token
        else:
            logger.debug(f"No valid token found in response headers for domain {domain}")
            return None
    
    def clear_token(self, server_url: str) -> None:
        """
        Clear token for the specified domain.
        
        Args:
            server_url: Server URL.
        """
        domain = self._get_domain(server_url)
        if domain in self.tokens:
            del self.tokens[domain]
            logger.info(f"Cleared token for domain {domain}")
        else:
            logger.debug(f"No stored token for domain {domain}")
    
    def clear_all_tokens(self) -> None:
        """Clear all tokens for all domains"""
        self.tokens.clear()
        logger.info("Cleared all tokens for all domains")

# Example usage
async def example_usage():
    # Create client
    client = DIDAuthClient(
        did_document_path="use_did_test_public/did.json",
        private_key_path="use_did_test_public/key-1_private.pem"
    )
    
    server_url = "http://localhost:9870"
    
    # Get authentication header (first call, returns DID authentication header)
    headers = client.get_auth_header(server_url)
    
    # Send request
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{server_url}/agents/travel/hotel/ad/ph/12345/ad.json", 
            headers=headers
        ) as response:
            # Check response
            print(f"Status code: {response.status}")
            
            # If authentication is successful, update token
            if response.status == 200:
                client.update_token(server_url, dict(response.headers))
            
            # If authentication fails and a token was used, clear the token and retry
            elif response.status == 401:
                print("Invalid token, clearing and using DID authentication")
                client.clear_token(server_url)
                # Retry request here
    
    # Get authentication header again (if a token was obtained in the previous step, this will return a token authentication header)
    headers = client.get_auth_header(server_url)
    print(f"Header for second request: {headers}")
    
    # Force use of DID authentication header
    headers = client.get_auth_header(server_url, force_new=True)
    print(f"Forced use of DID authentication header: {headers}")
    
    # Test different domain
    another_server_url = "http://api.example.com"
    headers = client.get_auth_header(another_server_url)
    print(f"Header for another domain: {headers}")

if __name__ == "__main__":
    asyncio.run(example_usage()) 