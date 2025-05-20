# AgentConnect: https://github.com/agent-network-protocol/AgentConnect
# Author: Yu Chen
# Website: https://agent-network-protocol.com/
#
# This project is open-sourced under the MIT License. For details, please see the LICENSE file.

import json
from typing import Any


def robust_json_parse(raw_args: str) -> Any:
    """
    Ultra-robust JSON parser that handles:
    - Standard JSON
    - Quote-wrapped JSON
    - Missing braces/quotes
    - Partially wrapped strings
    - Any combination of the above

    Args:
        raw_args: Input string that may contain malformed JSON

    Returns:
        Parsed Python object

    Raises:
        ValueError: When JSON cannot be repaired
    """

    json_data = _json_parse(raw_args)
    if isinstance(json_data, str):
        # Try to parse again after removing any trailing comma
        json_data = _json_parse(json_data)

    return json_data

def _json_parse(raw_args: str) -> Any:
    """
    Parses JSON string robustly, handling common errors such as missing braces/quotes,
    """
    if not isinstance(raw_args, str):
        raw_args = str(raw_args).strip()

    raw_args = raw_args.replace('\\"', '"')  # Handle escaped quotes
    raw_args = raw_args.replace('\"', '"')  # Handle escaped quotes

    # Case 1: Try direct parse first (for valid JSON)
    try:
        return json.loads(raw_args)
    except json.JSONDecodeError:
        pass

    # Case 2: Handle quote-wrapped or partially wrapped cases
    modified = raw_args
    was_quoted = False

    # Remove outer quotes if they exist (complete or partial)
    if modified.startswith('"'):
        was_quoted = True
        modified = modified[1:]
        if modified.endswith('"'):
            modified = modified[:-1]

    # Case 2a: Try parsing after removing outer quotes
    try:
        return json.loads(modified)
    except json.JSONDecodeError as e:
        # Case 2b: Try repairing structure
        try:
            return _repair_and_parse(modified, was_quoted)
        except ValueError:
            # Case 3: Final attempt with original string
            try:
                return _repair_and_parse(raw_args, False)
            except ValueError as e:
                raise ValueError(f"Failed to parse JSON: {raw_args}") from e


def _repair_and_parse(json_str: str, was_quoted: bool) -> Any:
    """Handles JSON repair and final parsing attempt"""
    # Balance braces
    if json_str.count('{') > json_str.count('}'):
        json_str = json_str.rstrip() + '}'

    # Balance quotes if we removed outer quotes
    if was_quoted and json_str.count('"') % 2 != 0:
        json_str += '"'

    # Remove any trailing comma
    json_str = json_str.rstrip().rstrip(',')

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError("Repair failed") from e


if __name__ == '__main__':
    res = robust_json_parse('{"key": "value"}')      # Standard
    print(res)
    res = robust_json_parse('"{\\"key\\": \\"value\\"}"')  # Wrapped
    print(res)
    res = robust_json_parse('{"key": "value"')       # Missing }
    print(res)
    res = robust_json_parse('"{"key": "value"')      # Partial wrap
    print(res)
    res = robust_json_parse('"{')                    # Extreme case
    print(res)