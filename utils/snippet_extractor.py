from typing import Optional


def extract_snippet_from_lines(code: str, start_line: Optional[int], end_line: Optional[int]) -> str:
    """
    Extracts lines from the original C code using 1-based line numbers.
    
    Args:
        code: Original C source code
        start_line: 1-based starting line number (None if not provided)
        end_line: 1-based ending line number (None if not provided)
        
    Returns:
        Extracted code snippet or empty string if invalid
    """
    if not code:
        return ""
    
    if start_line is None or end_line is None:
        return ""
    
    lines = code.split("\n")
    total_lines = len(lines)
    
    # Validate line numbers
    if start_line < 1 or end_line < start_line:
        return ""
    
    if start_line > total_lines:
        return ""
    
    # Clamp end_line to available lines
    end_line = min(end_line, total_lines)
    
    # Convert 1-based to 0-based indices
    return "\n".join(lines[start_line-1:end_line])


def fallback_extract_snippet_from_pattern(code: str, pattern: str) -> str:
    """
    Fallback extraction using pattern matching.
    Searches for lines containing the pattern and returns a context window.
    
    Args:
        code: Original C source code
        pattern: Substring to search for in the code
        
    Returns:
        Extracted code snippet with context or empty string if not found
    """
    if not code or not pattern or not pattern.strip():
        return ""
    
    lines = code.split("\n")
    pattern_clean = pattern.strip()
    
    # Find all matching lines
    matching_indices = []
    for i, line in enumerate(lines):
        if pattern_clean in line:
            matching_indices.append(i)
    
    if not matching_indices:
        return ""
    
    # Return first match with context (2 lines before and after)
    first_match = matching_indices[0]
    start_idx = max(0, first_match - 2)
    end_idx = min(len(lines), first_match + 3)
    
    return "\n".join(lines[start_idx:end_idx])
