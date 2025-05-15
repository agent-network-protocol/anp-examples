# --- 1. Choose a Python base image -----------------------------------------
FROM python:3.11-slim AS app

WORKDIR /app

# Copy the entire project into the container
COPY . .

RUN pip install -r web_app/backend/requirements.txt

# Add the project root to PYTHONPATH to allow imports of modules like 'config' and 'anp_examples'
# ENV PYTHONPATH=/app

# Set the working directory to where the main backend script is located
WORKDIR /app/web_app/backend

# Expose the port the app runs on (assuming 5005 based on README)
EXPOSE 5005

# Define the command to run your application
# This assumes anp_examples_backend.py starts a web server (e.g., Uvicorn/FastAPI)
CMD ["python", "anp_examples_backend.py"]