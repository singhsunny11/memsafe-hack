import json
import re
from typing import Optional, Dict, Any


def extract_json(text: str) -> Optional[Dict[Any, Any]]:
    """
    Extract and parse JSON from a model response with robust fallback.
    
    Strategy:
    1. Try direct JSON parsing
    2. Try extracting JSON block with regex (handles markdown code blocks)
    3. Try extracting JSON from code fences (```json ... ```)
    4. Return None if all attempts fail
    
    Args:
        text: Raw model response text
        
    Returns:
        Parsed JSON dict or None if parsing fails
    """
    if not text or not text.strip():
        return None
    
    # Strategy 1: Direct JSON parse
    try:
        return json.loads(text.strip())
    except (json.JSONDecodeError, ValueError):
        pass
    
    # Strategy 2: Extract JSON from markdown code blocks (```json ... ```)
    json_block_pattern = r"```(?:json)?\s*(\{.*?\})\s*```"
    match = re.search(json_block_pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        try:
            return json.loads(match.group(1))
        except (json.JSONDecodeError, ValueError):
            pass
    
    # Strategy 3: Extract first {...} block (nested braces supported)
    # This regex tries to match balanced braces
    brace_count = 0
    start_idx = -1
    for i, char in enumerate(text):
        if char == '{':
            if start_idx == -1:
                start_idx = i
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0 and start_idx != -1:
                json_str = text[start_idx:i+1]
                try:
                    return json.loads(json_str)
                except (json.JSONDecodeError, ValueError):
                    # Reset and continue searching
                    start_idx = -1
                    brace_count = 0
    
    # Strategy 4: Simple regex fallback (may not handle nested braces well)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except (json.JSONDecodeError, ValueError):
            pass
    
    return None
