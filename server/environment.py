from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State
from env.models import Observation, Action
from env.grader import grade_prediction
import json
import os


class ComplaintEnvironment(Environment):
    def __init__(self):
        self.difficulties = ["easy", "medium", "hard"]
        self.all_data = []
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for diff in self.difficulties:
            path = os.path.join(base_dir, "tasks", f"{diff}.json")
            with open(path, "r") as f:
                self.all_data.extend(json.load(f))
        self.index = 0
        self.current = self.all_data[0]
        self._step_count = 0

    def reset(self, seed=None, episode_id=None, **kwargs) -> Observation:
        self.index = 0
        self._step_count = 0
        self.current = self.all_data[self.index]
        return Observation(text=self.current["text"])

    def step(self, action: Action, timeout_s=None, **kwargs):
        correct = self.current["label"]
        score = grade_prediction(action.priority, correct, self.current["text"])

        if correct == "critical" and action.priority != "critical":
            score *= 0.5

        score = max(0.01, min(score, 0.99))
        self._step_count += 1
        self.index += 1
        done = self.index >= len(self.all_data)

        if not done:
            self.current = self.all_data[self.index]
            obs = Observation(text=self.current["text"], done=done, reward=score)
        else:
            obs = Observation(text="", done=True, reward=score)

        # Return Gymnasium-style 4-tuple
        return obs, score, done, {"correct": correct}

    @property
    def state(self) -> State:
        return State(
            episode_id=None,
            step_count=self._step_count
        )