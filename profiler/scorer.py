def score_violation(violations, threshold = 5):
    """
    Score the violations based on their severity points and return a summary.
    
    Args:
        violations (List[Dict]): List of violations to score.
        threshold (int): The threshold for scoring violations.
    
    Returns:
        Dict: A summary of the scored violations.
    """
    
    return {
        "total_points": sum(v.get("severity_points", 0) for v in violations),
        "issues_count": len(violations),
        "status": "pass" if sum(v.get("severity_points", 0) for v in violations) < threshold else "fail",
        "threshold": threshold
    }
    
