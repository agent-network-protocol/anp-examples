"""
A FastAPI server that uses did_auth_middleware as middleware.
"""

import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Import the middleware
from examples_code.did_auth_middleware import did_auth_middleware

# Configure logging
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="ANP Example Server",
    description="An example server using DID authentication middleware",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization"],  # Important: expose Authorization header
)

# Add the middleware
app.middleware("http")(did_auth_middleware)


@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    logger.info("Received request to root endpoint")
    return {"message": "Welcome to ANP Example Server"}


@app.get("/test")
async def test(request: Request):
    """
    Test endpoint that returns 200 OK.
    """
    logger.info("Received test request")
    logger.info(f"Request headers: {request.headers}")

    # Log if the request has an Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header:
        logger.info(f"Authorization header present: {auth_header[:30]}...")
    else:
        logger.info("No Authorization header present")

    response = {"status": "OK", "message": "Test endpoint successful"}
    logger.info(f"Returning response: {response}")
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler.
    """
    logger.error(f"Unhandled exception: {exc}")
    logger.error("Stack trace:", exc_info=True)
    return JSONResponse(status_code=500, content={"message": "Internal server error"})


# 直接运行服务器的代码
if __name__ == "__main__":
    # Run the server
    logger.info("Starting server on 0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
