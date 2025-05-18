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
# ROOT_DIR = Path(__file__).parent.parent.parent
ROOT_DIR = Path(__file__).parent

# Load environment variables from root .env file
load_dotenv(ROOT_DIR / '.env')

# OpenAi
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')


def validate_config():
    """Validate that at least one set of required environment variables is set"""
    required_vars = ["OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL"]

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables for {', '.join(missing_vars)}")
