import sys
import os
import unittest
import json
import requests
from pathlib import Path

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import request model for type checking
from web_app.backend.hotel_order_api import HotelQueryRequest

# Local server address and port
BASE_URL = "http://localhost:9871"

class TestHotelOrderAPI(unittest.TestCase):
    """Test hotel order API using HTTP requests"""
    
    def test_query_hotel_success(self):
        """Test hotel query API - success scenario"""
        # Construct request data
        request_data = {
            "query": "我想在北京望京附近找一家价格适中的酒店",
            "agent_url": "https://agent-search.ai/ad.json",
            "max_documents": 20
        }
        
        # Send HTTP request
        response = requests.post(
            f"{BASE_URL}/api/travel/hotel/query", 
            json=request_data,
            timeout=3000  # Increase timeout to 30 seconds
        )
        
        # Verify HTTP response status code
        self.assertEqual(response.status_code, 200)
        
        # Parse response content
        data = response.json()
        
        # Verify response structure
        self.assertTrue("summary" in data)
        self.assertTrue("content" in data)
        self.assertTrue(isinstance(data["content"], list))
        
        # Print response content for debugging
        print(f"\nAPI Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
    


# Run tests
if __name__ == "__main__":
    # Print info message
    print("Running tests against API at http://localhost:9871")
    unittest.main()
