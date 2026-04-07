def grade_prediction(action, correct):
    levels = ["low", "medium", "high", "critical"]

    if action == correct:
        return 1.0
    elif abs(levels.index(action) - levels.index(correct)) == 1:
        return 0.5
    else:
        return 0.0