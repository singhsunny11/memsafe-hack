"""
Simplified AI provider using publicly available models that definitely work.
Uses Hugging Face's text generation API with models that are known to be available.
"""

import os
import json
from typing import Optional
import requests


def call_huggingface_simple(prompt: str) -> Optional[str]:
    """
    Call Hugging Face with a model that's definitely available.
    Uses a fallback approach with multiple model options.
    """
    api_token = os.getenv('HUGGINGFACE_API_TOKEN')
    
    if not api_token:
        raise ValueError("HUGGINGFACE_API_TOKEN not set. Get a free token from https://huggingface.co/settings/tokens")
    
    headers = {"Authorization": f"Bearer {api_token}"}
    
    # Format the prompt simply
    formatted_prompt = f"""Analyze this C code for memory safety vulnerabilities. Return ONLY valid JSON:

{prompt}

JSON format:
{{
  "summary": "summary text",
  "safety_score": 50,
  "vulnerabilities": [{{"type": "...", "severity": "Medium", "cwe": 121, "explanation": "...", "insecure_snippet_start_line": 1, "insecure_snippet_end_line": 2, "pattern": "strcpy"}}],
  "suggested_rust": [{{"rust_snippet": "...", "why_safe": "..."}}]
}}"""
    
    # Try models in order of likelihood to work
    models_to_try = [
        "bigscience/bloom-560m",  # Small, usually available
        "gpt2",  # Very common, should work
        "distilgpt2",  # Smaller GPT-2 variant
    ]
    
    for model in models_to_try:
        api_url = f"https://router.huggingface.co/models/{model}"
        payload = {
            "inputs": formatted_prompt,
            "parameters": {
                "max_new_tokens": 1000,
                "temperature": 0.3,
                "return_full_text": False
            },
            "options": {
                "wait_for_model": True
            }
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    if 'generated_text' in result[0]:
                        return result[0]['generated_text']
                elif isinstance(result, dict) and 'generated_text' in result:
                    return result['generated_text']
            elif response.status_code == 503:
                # Model loading, but endpoint exists
                continue  # Try next model
            elif response.status_code != 410:
                # Not a "gone" error, might work with retry
                continue
                
        except Exception:
            continue
    
    # If all fail, raise error
    raise Exception(
        "All Hugging Face models are unavailable. "
        "This might be a temporary issue. Try again in a few minutes, "
        "or check https://huggingface.co/docs/api-inference for status."
    )

