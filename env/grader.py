def detect_severity_keywords(text: str) -> int:
    """
    Detect severity level from keywords.
    Returns index based on severity.
    """
    text = text.lower()

    critical_keywords = ["fire", "explosion", "hazard", "accident", "sparking", "emergency"]
    high_keywords = ["water", "electricity", "leakage", "drainage", "garbage"]
    medium_keywords = ["delay", "not working", "issue", "problem"]

    if any(word in text for word in critical_keywords):
        return 3
    elif any(word in text for word in high_keywords):
        return 2
    elif any(word in text for word in medium_keywords):
        return 1
    else:
        return 0


def grade_prediction(predicted: str, actual: str, text: str = "") -> float:
    """
    Advanced grading system:
    - Distance-based scoring
    - Context-aware severity adjustment
    - Penalizes underestimation more than overestimation
    - Prevents trivial constant strategies (judge trap defense)
    """

    priorities = ["low", "medium", "high", "critical"]

    pred_idx = priorities.index(predicted)
    actual_idx = priorities.index(actual)

    distance = abs(pred_idx - actual_idx)

    # 🔹 Base score
    if distance == 0:
        score = 1.0
    elif distance == 1:
        score = 0.7
    elif distance == 2:
        score = 0.3
    else:
        score = 0.0

    # Context-aware adjustment
    if text:
        detected_severity = detect_severity_keywords(text)

        #  Penalize underestimation (very important)
        if pred_idx < detected_severity:
            score *= 0.6

        #  Slight reward for safe overestimation
        elif pred_idx > actual_idx:
            score *= 1.05

    #  Judge Trap Defense: discourage constant "safe" guessing
    if predicted == "high" and actual in ["low", "medium"]:
        score *= 0.8

    #  Clamp final score
    return max(0.0, min(score, 1.0))