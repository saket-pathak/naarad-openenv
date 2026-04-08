def grade_prediction(predicted: str, actual: str) -> float:
    """
    Advanced grading:
    - Exact match → 1.0
    - Distance-based scoring
    - Critical mistakes penalized more
    """

    priorities = ["low", "medium", "high", "critical"]

    pred_idx = priorities.index(predicted)
    actual_idx = priorities.index(actual)

    distance = abs(pred_idx - actual_idx)

    # Exact match
    if distance == 0:
        return 1.0

    # Close match
    elif distance == 1:
        return 0.7

    # Moderate error
    elif distance == 2:
        return 0.3

    # Severe error (especially missing critical)
    else:
        return 0.0