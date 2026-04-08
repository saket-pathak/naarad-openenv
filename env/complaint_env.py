import json
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

        #  Base score from grader
        score = grade_prediction(action.priority, correct, current["text"])

        #  Real-world penalty: underestimating critical issues
        if correct == "critical" and action.priority != "critical":
            score *= 0.5

        #  Ensure score is within bounds
        score = max(0.0, min(score, 1.0))

        reward = Reward(value=score)

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