import os
import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# Add project root directory to system path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from anp_examples.simple_example import simple_crawl
from anp_examples.utils.log_base import setup_logging
from web_app.backend.models import QueryRequest, QueryResponse

# Set up logging
setup_logging()

# Get project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize FastAPI app
app = FastAPI(
    title="Agent Network Search API",
    description="Agent Network Search API based on ANP protocol",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Get DID paths
did_document_path = str(ROOT_DIR / "use_did_test_public/did.json")
private_key_path = str(ROOT_DIR / "use_did_test_public/key-1_private.pem")


@app.get("/")
async def read_root():
    """API root endpoint"""
    return {"message": "Agent Network Search API service is running"}


@app.post("/api/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Process query request"""
    try:
        # Use agent URL provided by user or default URL
        initial_url = request.agent_url if request.agent_url else "https://agent-search.ai/ad.json"
        
        # Call simple_crawl function
        result = await simple_crawl(
            user_input=request.query,
            task_type="general",
            did_document_path=did_document_path,
            private_key_path=private_key_path,
            max_documents=10,  # Crawl up to 10 documents
            initial_url=initial_url,
        )
        
        return result
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


if __name__ == "__main__":
    # Start uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=9871)
