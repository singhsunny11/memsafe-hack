def map_severity(vuln_type: str):
    """
    Maps vulnerability type to severity level.
    Returns: "Low", "Medium", "High", or "Critical"
    """
    vuln = vuln_type.lower()

    if "buffer overflow" in vuln or "stack overflow" in vuln:
        return "High"

    if "use-after-free" in vuln:
        return "High"

    if "null pointer" in vuln or "null dereference" in vuln:
        return "Medium"

    if "off-by-one" in vuln or "oob" in vuln:
        return "Medium"

    if "malloc" in vuln or "allocation" in vuln:
        return "Medium"

    return "Low"


def severity_to_score(severity: str) -> int:
    """
    Maps severity level to numeric score.
    Returns: 80 (Low), 60 (Medium), 30 (High), 0 (Critical)
    """
    severity_lower = severity.lower().strip()
    
    if severity_lower == "critical":
        return 0
    elif severity_lower == "high":
        return 30
    elif severity_lower == "medium":
        return 60
    elif severity_lower == "low":
        return 80
    else:
        # Default to Medium if unknown
        return 60


def calculate_safety_score(vulnerabilities: list) -> int:
    """
    Calculates average safety score from a list of vulnerabilities.
    Each vulnerability should have a 'severity' field.
    Returns: 0-100 average score
    """
    if not vulnerabilities:
        return 100  # No vulnerabilities = perfect score
    
    scores = []
    for vuln in vulnerabilities:
        severity = vuln.get('severity', 'Medium')
        score = severity_to_score(severity)
        scores.append(score)
    
    if not scores:
        return 100
    
    return int(sum(scores) / len(scores))

