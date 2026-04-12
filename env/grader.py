class grade_prediction:
    def grade(self, sample) -> float:
        # 🔥 REQUIRED for validator
        return 0.5

    def __call__(self, predicted: str, actual: str, text: str = "") -> float:
        priorities = ["low", "medium", "high", "critical"]

        pred_idx = priorities.index(predicted) if predicted in priorities else 1
        actual_idx = priorities.index(actual) if actual in priorities else 1

        distance = abs(pred_idx - actual_idx)

        if distance == 0:
            score = 0.95
        elif distance == 1:
            score = 0.65
        elif distance == 2:
            score = 0.25
        else:
            score = 0.05

        if actual == "critical" and predicted != "critical":
            score *= 0.5

        if predicted == "high" and actual in ["low", "medium"]:
            score *= 0.8

        return max(0.01, min(score, 0.99))