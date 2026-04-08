import json
from turtle import done

from numpy import diff
from env.models import Observation, Action, Reward
from env.grader import grade_prediction


class ComplaintEnv:
    def __init__(self, difficulty="easy"):
        """
        Initialize environment with difficulty level.
        Loads dataset from tasks folder.
        """
        self.difficulty = difficulty

        with open(f"tasks/{difficulty}.json", "r") as f:
            self.data = json.load(f)

        self.index = 0
        self.actions = ["low", "medium", "high", "critical"]

    def reset(self) -> Observation:
        """
        Reset environment to initial state.
        """
        self.index = 0
        return Observation(text=self.data[self.index]["text"])

    def state(self) -> Observation:
        """
        Return current observation.
        """
        return Observation(text=self.data[self.index]["text"])

    def step(self, action: Action):
        """
        Take an action and return:
        (next_observation, reward, done, info)
        """
        current = self.data[self.index]
        correct = current["label"]

    # 🔥 Advanced reward shaping
        levels = ["low", "medium", "high", "critical"]

        action_idx = levels.index(action.priority)
        correct_idx = levels.index(correct)

        diff = abs(action_idx - correct_idx)

        if diff == 0:
            score = 1.0
        elif diff == 1:
            score = 0.5
        else:
            score = 0.0

    # 🔥 Penalty for very wrong prediction
        if diff >= 2:
            score -= 0.2

        reward = Reward(value=max(score, 0.0))

    # Move to next state
        self.index += 1
        done = self.index >= len(self.data)

        next_obs = None
        if not done:
            next_obs = Observation(text=self.data[self.index]["text"])

        return next_obs, reward, done, {"correct": correct}

    def get_action_space(self):
        """
        Returns available actions.
        """
        return self.actions