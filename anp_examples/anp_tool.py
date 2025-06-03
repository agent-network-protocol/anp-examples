import asyncio
import json
import yaml
import aiohttp
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

from agent_connect.authentication import DIDWbaAuthHeader


class ANPTool:
    name: str = "anp_tool"
    description: str = """Interact with other agents using the Agent Network Protocol (ANP).
1. When using, you need to input a document URL and HTTP method.
2. Inside the tool, the URL will be parsed and corresponding APIs will be called based on the parsing results.
3. Note that any URL obtained using ANPTool must be called using ANPTool, do not call it directly yourself.
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "(required) URL of the agent description file or API endpoint",
            },
            "method": {
                "type": "string",
                "description": "(optional) HTTP method, such as GET, POST, PUT, etc., default is GET",
                "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"],
                "default": "GET",
            },
            "headers": {
                "type": "object",
                "description": "(optional) HTTP request headers",
                "default": {},
            },
            "params": {
                "type": "object",
                "description": "(optional) URL query parameters",
                "default": {},
            },
            "body": {
                "type": "object",
                "description": "(optional) Request body for POST/PUT requests",
            },
        },
        "required": ["url"],
    }

    # Declare auth_client field
    auth_client: Optional[DIDWbaAuthHeader] = None

    def __init__(
        self,
        did_document_path: Optional[str] = None,
        private_key_path: Optional[str] = None,
        **data,
    ):
        """
        Initialize ANPTool with DID authentication

        Args:
            did_document_path (str, optional): Path to DID document file. If None, will use default path.
            private_key_path (str, optional): Path to private key file. If None, will use default path.
        """
        super().__init__(**data)

        # Get current script directory
        current_dir = Path(__file__).parent
        # Get project root directory
        base_dir = current_dir.parent

        # Use provided paths or default paths
        if did_document_path is None:
            # Try to get from environment variable first
            did_document_path = os.environ.get("DID_DOCUMENT_PATH")
            if did_document_path is None:
                # Use default path
                did_document_path = str(base_dir / "use_did_test_public/did.json")

        if private_key_path is None:
            # Try to get from environment variable first
            private_key_path = os.environ.get("DID_PRIVATE_KEY_PATH")
            if private_key_path is None:
                # Use default path
                private_key_path = str(
                    base_dir / "use_did_test_public/key-1_private.pem"
                )

        logging.info(
            f"ANPTool initialized - DID path: {did_document_path}, private key path: {private_key_path}"
        )

        self.auth_client = DIDWbaAuthHeader(
            did_document_path=did_document_path, private_key_path=private_key_path
        )

    async def execute(
        self,
        url: str,
        method: str = "GET",
        headers: Dict[str, str] = None,
        params: Dict[str, Any] = None,
        body: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Execute HTTP request to interact with other agents

        Args:
            url (str): URL of the agent description file or API endpoint
            method (str, optional): HTTP method, default is "GET"
            headers (Dict[str, str], optional): HTTP request headers
            params (Dict[str, Any], optional): URL query parameters
            body (Dict[str, Any], optional): Request body for POST/PUT requests

        Returns:
            Dict[str, Any]: Response content
        """

        if headers is None:
            headers = {}
        if params is None:
            params = {}

        logging.info(f"ANP request: method:{method} url:{url} headers:{headers} params:{params} body:{body}")

        # Add basic request headers
        if "Content-Type" not in headers and method in ["POST", "PUT", "PATCH"]:
            headers["Content-Type"] = "application/json"

        # Add DID authentication
        if self.auth_client:
            try:
                auth_headers = self.auth_client.get_auth_header(url)
                headers.update(auth_headers)
            except Exception as e:
                logging.error(f"Failed to get authentication header: {str(e)}")

        async with aiohttp.ClientSession() as session:
            # Prepare request parameters
            processed_params = {}
            if params:
                # Process query parameters to ensure they are properly serialized
                for key, value in params.items():
                    if isinstance(value, (dict, list)):
                        # Serialize complex types to JSON string
                        processed_params[key] = json.dumps(value, ensure_ascii=False)
                    else:
                        # Keep simple types as is
                        processed_params[key] = value
            
            request_kwargs = {
                "url": url,
                "headers": headers,
                "params": processed_params,
            }

            # If there is a request body and the method supports it, add the request body
            if body is not None and method in ["POST", "PUT", "PATCH"]:
                request_kwargs["json"] = body

            # Execute request
            http_method = getattr(session, method.lower())

            try:
                async with http_method(**request_kwargs) as response:
                    logging.info(f"ANP response: status code {response.status}")

                    # Check response status
                    if (
                        response.status == 401
                        and "Authorization" in headers
                        and self.auth_client
                    ):
                        logging.warning(
                            "Authentication failed (401), trying to get authentication again"
                        )
                        # If authentication fails and a token was used, clear the token and retry
                        self.auth_client.clear_token(url)
                        # Get authentication header again
                        headers.update(
                            self.auth_client.get_auth_header(url, force_new=True)
                        )
                        # Execute request again
                        request_kwargs["headers"] = headers
                        async with http_method(**request_kwargs) as retry_response:
                            logging.info(
                                f"ANP retry response: status code {retry_response.status}"
                            )
                            return await self._process_response(retry_response, url)

                    return await self._process_response(response, url)
            except aiohttp.ClientError as e:
                logging.error(f"HTTP request failed: {str(e)}")
                return {"error": f"HTTP request failed: {str(e)}", "status_code": 500}

    async def _process_response(self, response, url):
        """Process HTTP response"""
        # If authentication is successful, update the token
        if response.status == 200 and self.auth_client:
            try:
                self.auth_client.update_token(url, dict(response.headers))
            except Exception as e:
                logging.error(f"Failed to update token: {str(e)}")

        # Get response content type
        content_type = response.headers.get("Content-Type", "").lower()

        # Get response text
        text = await response.text()

        # Process response based on content type
        if "application/json" in content_type:
            # Process JSON response
            try:
                result = json.loads(text)
                logging.info("Successfully parsed JSON response")
            except json.JSONDecodeError:
                logging.warning(
                    "Content-Type declared as JSON but parsing failed, returning raw text"
                )
                result = {"text": text, "format": "text", "content_type": content_type}
        elif "application/yaml" in content_type or "application/x-yaml" in content_type:
            # Process YAML response
            try:
                result = yaml.safe_load(text)
                logging.info("Successfully parsed YAML response")
                result = {
                    "data": result,
                    "format": "yaml",
                    "content_type": content_type,
                }
            except yaml.YAMLError:
                logging.warning(
                    "Content-Type declared as YAML but parsing failed, returning raw text"
                )
                result = {"text": text, "format": "text", "content_type": content_type}
        else:
            # Default to text
            result = {"text": text, "format": "text", "content_type": content_type}

        # Add status code to result
        if isinstance(result, dict):
            result["status_code"] = response.status
        else:
            result = {
                "data": result,
                "status_code": response.status,
                "format": "unknown",
                "content_type": content_type,
            }

        # Add URL to result for tracking
        result["url"] = str(url)

        return result
