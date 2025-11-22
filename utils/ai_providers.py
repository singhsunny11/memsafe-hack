"""
AI Provider abstraction layer - supports multiple free and paid providers.
"""

import os
import json
from typing import Optional, Dict, Any
import requests


def call_huggingface_api(prompt: str, model: str = "mistralai/Mistral-7B-Instruct-v0.2") -> Optional[str]:
    """
    Call Hugging Face Inference API (FREE, no credit card needed).
    
    Get your free API token from: https://huggingface.co/settings/tokens
    
    Note: Some models may be loading on first request (takes 30-60 seconds).
    """
    api_token = os.getenv('HUGGINGFACE_API_TOKEN')
    
    if not api_token:
        raise ValueError("HUGGINGFACE_API_TOKEN not set. Get a free token from https://huggingface.co/settings/tokens")
    
    # Try chat completion API first (newer format)
    # Try old endpoint with wait-for-model header (some models still work here)
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "x-wait-for-model": "true"  # Wait for model to load
    }
    
    # Format prompt based on model type
    if "tinyllama" in model.lower():
        # TinyLlama format
        formatted_prompt = f"""<|user|>
You are a memory-safety analysis assistant. Analyze the following C code and return ONLY valid JSON.

{prompt}

Return ONLY valid JSON with this structure:
{{
  "summary": "One paragraph summary",
  "safety_score": 0-100,
  "vulnerabilities": [{{"type": "...", "severity": "Low|Medium|High|Critical", "cwe": 123, "explanation": "...", "insecure_snippet_start_line": 1, "insecure_snippet_end_line": 2, "pattern": "..."}}],
  "suggested_rust": [{{"rust_snippet": "...", "why_safe": "..."}}]
}}

Return ONLY the JSON, no other text.<|assistant|>
"""
    elif "mistral" in model.lower() or "zephyr" in model.lower():
        # Mistral/Zephyr format
        formatted_prompt = f"""<s>[INST] You are a memory-safety analysis assistant. Analyze the following C code and return ONLY valid JSON.

{prompt}

Return ONLY valid JSON with this structure:
{{
  "summary": "One paragraph summary",
  "safety_score": 0-100,
  "vulnerabilities": [{{"type": "...", "severity": "Low|Medium|High|Critical", "cwe": 123, "explanation": "...", "insecure_snippet_start_line": 1, "insecure_snippet_end_line": 2, "pattern": "..."}}],
  "suggested_rust": [{{"rust_snippet": "...", "why_safe": "..."}}]
}}

Return ONLY the JSON, no other text. [/INST]"""
    elif "phi" in model.lower() or "gemma" in model.lower():
        # Phi/Gemma format (simpler)
        formatted_prompt = f"""You are a memory-safety analysis assistant. Analyze the following C code and return ONLY valid JSON.

{prompt}

Return ONLY valid JSON with this structure:
{{
  "summary": "One paragraph summary",
  "safety_score": 0-100,
  "vulnerabilities": [{{"type": "...", "severity": "Low|Medium|High|Critical", "cwe": 123, "explanation": "...", "insecure_snippet_start_line": 1, "insecure_snippet_end_line": 2, "pattern": "..."}}],
  "suggested_rust": [{{"rust_snippet": "...", "why_safe": "..."}}]
}}

Return ONLY the JSON, no other text."""
    else:
        # Default format
        formatted_prompt = f"""You are a memory-safety analysis assistant. Analyze the following C code and return ONLY valid JSON.

{prompt}

Return ONLY valid JSON with this structure:
{{
  "summary": "One paragraph summary",
  "safety_score": 0-100,
  "vulnerabilities": [{{"type": "...", "severity": "Low|Medium|High|Critical", "cwe": 123, "explanation": "...", "insecure_snippet_start_line": 1, "insecure_snippet_end_line": 2, "pattern": "..."}}],
  "suggested_rust": [{{"rust_snippet": "...", "why_safe": "..."}}]
}}

Return ONLY the JSON, no other text."""
    
    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_new_tokens": 2000,
            "temperature": 0.1,
            "return_full_text": False
        }
    }
    
    try:
        # Try standard inference API first
        response = requests.post(api_url, headers=headers, json=payload, timeout=120)
        
        # If 410, try alternative endpoint or different model format
        if response.status_code == 410:
            # Try with wait parameter (some models need this)
            payload_with_wait = {**payload, "options": {"wait_for_model": True}}
            response = requests.post(api_url, headers=headers, json=payload_with_wait, timeout=180)
        
        # Handle 503 (model loading) and 429 (rate limit) with retry info
        if response.status_code == 503:
            error_info = response.json() if response.content else {}
            estimated_time = error_info.get('estimated_time', 'unknown')
            raise Exception(
                f"Model is loading (this happens on first use). "
                f"Estimated wait time: {estimated_time} seconds. "
                f"Please try again in a minute."
            )
        
        if response.status_code == 429:
            raise Exception(
                "Rate limit exceeded. Please wait a moment and try again. "
                "Free tier has rate limits - consider waiting 30-60 seconds."
            )
        
        if response.status_code == 410:
            raise Exception(
                f"Model '{model}' is no longer available at this endpoint. "
                f"Please try a different model from the dropdown."
            )
        
        response.raise_for_status()
        
        result = response.json()
        
        # Handle different response formats
        if isinstance(result, list) and len(result) > 0:
            if 'generated_text' in result[0]:
                text = result[0]['generated_text']
            elif isinstance(result[0], dict) and 'text' in result[0]:
                text = result[0]['text']
            else:
                text = str(result[0])
        elif isinstance(result, dict):
            if 'generated_text' in result:
                text = result['generated_text']
            elif 'text' in result:
                text = result['text']
            else:
                text = json.dumps(result)
        elif isinstance(result, str):
            text = result
        else:
            text = json.dumps(result)
        
        # Clean up the response (remove instruction tags if present)
        text = text.strip()
        if text.startswith('[INST]'):
            text = text[6:]
        if text.endswith('[/INST]'):
            text = text[:-7]
        text = text.strip()
        
        return text
        
    except requests.exceptions.Timeout:
        raise Exception("Request timed out. The model might be loading. Please try again in a minute.")
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            status_code = e.response.status_code
            try:
                error_detail = e.response.json()
                error_msg = error_detail.get('error', str(e))
            except:
                error_msg = str(e)
            
            if status_code == 410:
                raise Exception(
                    f"Model '{model}' is no longer available. "
                    f"Please select a different model from the dropdown."
                )
            raise Exception(f"Hugging Face API error ({status_code}): {error_msg}")
        raise Exception(f"Hugging Face API error: {str(e)}")


def call_openai_api(prompt: str, model: str = "gpt-4o", api_key: Optional[str] = None) -> str:
    """Call OpenAI API (paid, but has free tier initially)."""
    import openai
    
    if api_key:
        openai.api_key = api_key
    elif not openai.api_key:
        raise ValueError("OpenAI API key not set")
    
    # Try new API style first (v1.0+)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai.api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant specialized in memory safety analysis.'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.0,
            max_tokens=2000,
        )
        return resp.choices[0].message.content
    except (ImportError, AttributeError):
        # Fallback to old API style (v0.x)
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant specialized in memory safety analysis.'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.0,
            max_tokens=2000,
        )
        return resp['choices'][0]['message']['content']


def call_ai_provider(provider: str, prompt: str, model: Optional[str] = None) -> str:
    """
    Unified interface to call different AI providers.
    
    Args:
        provider: 'openai', 'huggingface', or 'local'
        prompt: The prompt to send
        model: Optional model name (provider-specific)
        
    Returns:
        AI response text
    """
    if provider == 'huggingface':
        hf_model = model or "mistralai/Mistral-7B-Instruct-v0.2"
        return call_huggingface_api(prompt, hf_model)
    elif provider == 'openai':
        openai_model = model or "gpt-4o"
        api_key = os.getenv('OPENAI_API_KEY')
        return call_openai_api(prompt, openai_model, api_key)
    else:
        raise ValueError(f"Unknown provider: {provider}")

