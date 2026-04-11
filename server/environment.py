from openenv.core import Environment
from env.models import Observation, Action
from env.grader import grade_prediction
import json


class ComplaintEnvironment(Environment):
    def __init__(self):
        self.difficulties = ["easy", "medium", "hard"]
        self.all_data = []
        for diff in self.difficulties:
            with open(f"tasks/{diff}.json", "r") as f:
                self.all_data.extend(json.load(f))
        self.index = 0
        self.current = self.all_data[0]

    def reset(self, seed=None, episode_id=None, **kwargs) -> Observation:  # ✅ fixed
        self.index = 0
        self.current = self.all_data[self.index]
        return Observation(text=self.current["text"])

    def step(self, action: Action, timeout_s=None, **kwargs) -> Observation:  # ✅ fixed
        correct = self.current["label"]
        score = grade_prediction(action.priority, correct, self.current["text"])

        if correct == "critical" and action.priority != "critical":
            score *= 0.5

        score = max(0.01, min(score, 0.99))

        self.index += 1
        done = self.index >= len(self.all_data)

        if not done:
            self.current = self.all_data[self.index]
            return Observation(text=self.current["text"], done=done, reward=score)
        else:
            return Observation(text="", done=True, reward=score)

    @property
    def state(self):
        return {
            "index": self.index,
            "total": len(self.all_data),
            "current_text": self.current["text"] if self.current else ""
        }