from utils.json_parser import extract_json
'''this file lets the Streamlit UI work even before there is a model'''

def analyze_code_stub(model_output: str):
    """
    Temporary stub until the API key works.
    Takes a string (model output) and parses it.
    """
    data = extract_json(model_output)
    if not data:
        return {
            "error": "Invalid JSON from model",
            "raw_output": model_output
        }

    return data
