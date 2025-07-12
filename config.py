# AgentConnect: https://github.com/agent-network-protocol/AgentConnect
# Author: GaoWei Chang
# Email: chgaowei@gmail.com
# Website: https://agent-network-protocol.com/
#
# This project is open-sourced under the MIT License. For details, please see the LICENSE file.

# Configuration file for tests
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the project root directory (assuming tests folder is directly under root)
#ROOT_DIR = Path(__file__).parent.parent.parent
ROOT_DIR = Path(__file__).parent

print('ROOT_DIR is ' + str(ROOT_DIR))

# Load environment variables from root .env file
load_dotenv(ROOT_DIR / '.env')

# OpenRouter - DeepSeek API configurations
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
DASHSCOPE_BASE_URL = os.getenv('DASHSCOPE_BASE_URL')
DASHSCOPE_MODEL_NAME = os.getenv('DASHSCOPE_MODEL_NAME')

model_provider = os.getenv("MODEL_PROVIDER", "openai").lower()

# OpenAi
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
OPENAI_BASE_URL=os.getenv('OPENAI_BASE_URL')
OPENAI_MODEL=os.getenv('OPENAI_MODEL')



def validate_config():
    """Validate that at least one set of required environment variables is set"""

    print('model_provider is ' + model_provider)

    if model_provider == "dashscope":
        required_vars = ["DASHSCOPE_API_KEY", "DASHSCOPE_BASE_URL", "DASHSCOPE_MODEL_NAME"]
    elif model_provider == "openai":
        required_vars = ["OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL"]
    else:
        raise ValueError(f"Unsupported MODEL_PROVIDER: {model_provider}")

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables for {model_provider}: {', '.join(missing_vars)}")