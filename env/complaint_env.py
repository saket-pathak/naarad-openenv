import json
import os
from env.models import Observation, Action, Reward
from env.grader import grade_prediction


class ComplaintEnv:
    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty

        with open(f"tasks/{difficulty}.json", "r") as f:
            self.data = json.load(f)

        self.index = 0
        self.actions = ["low", "medium", "high", "critical"]

    def reset(self) -> Observation:
        self.index = 0
        return Observation(text=self.data[self.index]["text"])

    def state(self) -> Observation:
        return Observation(text=self.data[self.index]["text"])

    def step(self, action: Action):
        current = self.data[self.index]
        correct = current["label"]

        score = grade_prediction(action.priority, correct, current["text"])

        # Critical penalty — but never let it touch 0.0
        if correct == "critical" and action.priority != "critical":
            score *= 0.5

        # Strict boundary — never 0.0 or 1.0
        score = max(0.01, min(score, 0.99))  # ✅

        reward = Reward(value=score)

        self.index += 1
        done = self.index >= len(self.data)

        next_obs = None
        if not done:
            next_obs = Observation(text=self.data[self.index]["text"])

        return next_obs, reward, done, {"correct": correct}

    def get_action_space(self):
        return self.actions