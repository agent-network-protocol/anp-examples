# ANP Network Explorer

[中文版本](README_cn.md)

### Project Introduction

ANP Network Explorer is an application based on the Agent Network Protocol (ANP) that allows users to interact with intelligent agent networks using natural language. Users can provide agent description URLs, engage in conversations with agents through simple questions, and view the network crawling process in real-time.
![Weather Query Example](images/anp-examples-mainpage.png)

### Project Structure

This project contains the following main components:

- **web_app/**: Web application including frontend and backend implementation
  - **frontend/**: User interface based on HTML/JavaScript
  - **backend/**: Backend server based on FastAPI
  - **static/**: Static resource files

- **anp_examples/**: ANP core functionality implementation
  - **simple_example.py**: Simplified ANP crawling logic implementation
  - **anp_tool.py**: ANP tool class for interacting with agent networks
  - **utils/**: Utility classes and helper functions

- **use_did_test_public/**: DID authentication related files
  - **did.json**: DID document
  - **key-1_private.pem**: Private key file
  - **private_keys.json**: Key configuration

- **examples_code/**: Example code
  - **client.py**: Client example
  - **server.py**: Server example
  - **did_auth_middleware.py**: DID authentication middleware
  - **jwt_config.py**: JWT configuration

### How to Run (For Users)

#### Environment Setup

Before running the project, you need to set up the necessary environment variables. The project provides a `.env.example` file as a template:

1. Copy the `.env.example` file and rename it to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit the `.env` file and fill in your API-KEY, Endpoint, and other actual configuration information.

**Configuration Example:**

```env
# Choose AI service provider (required)
MODEL_PROVIDER=openai  # Options: dashscope / openai

# DashScope (Alibaba Cloud Qwen) Configuration
DASHSCOPE_API_KEY=sk-xxx
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DASHSCOPE_MODEL_NAME=qwen2.5-14b-instruct

# OpenAI Compatible API Configuration  
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.360.cn/v1
OPENAI_MODEL=gpt-4o
```

**Usage Instructions:**
- When choosing `dashscope`, only configure DASHSCOPE related parameters
- When choosing `openai`, only configure OPENAI related parameters
- Get API Key: [Alibaba Cloud Console](https://dashscope.console.aliyun.com/) or your chosen AI service provider

#### Using the Web Application

##### Method 1: Direct Browser Access
You can directly experience the ANP Network Explorer functionality by accessing our web-deployed application.
[Visit: https://service.agent-network-protocol.com/anp-demo/](https://service.agent-network-protocol.com/anp-demo/)
![Weather Query Example](images/anp-examples-web-search-result.png)

##### Method 2: Running with Scripts
You can run the web application locally by following these steps.

1. Install dependencies:
   ```bash
   # Using Poetry
   poetry install
   
   # Or using pip
   pip install -r web_app/backend/requirements.txt
   ```

2. Start the web application:
   
   ```bash
   # Activate Python virtual environment
   poetry shell

   # Or manually activate
   source venv/bin/activate  # Linux/Mac
   # or venv\Scripts\activate  # Windows

   python web_app/backend/anp_examples_backend.py
   ```

3. Open browser and visit: `http://localhost:5005`

4. Enter your question in the input box and provide an agent URL (optional, defaults to `https://agent-search.ai/ad.json`)

5. Click the "Submit Question" button
![Weather Query Example](images/anp-examples-search-agent.png)

6. View results and network crawling process
![Weather Query Example](images/anp-examples-search-result.png)

##### Method 3: Running with Docker
> Run Docker container using `docker compose` command. Make sure you have Docker and Docker Compose installed.
```bash
docker compose up -d
```
Then open browser and visit: `http://localhost:5005`

### How to Develop (For Developers)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/anp-examples.git
   cd anp-examples
   ```

2. Install development dependencies:
   ```bash
   poetry install
   
   # Or using pip
   pip install -r web_app/backend/requirements.txt
   ```

3. Run tests:
   ```bash
   python web_app/backend/anp_examples_backend.py
   ```

4. View logs:
[Complete operation logs](anp-examples.log.md)
