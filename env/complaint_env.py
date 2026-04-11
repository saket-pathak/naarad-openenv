import json
import os
from openai import OpenAI
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

        # 🔥 Initialize client ONCE
        try:
            self.client = OpenAI(
                base_url=os.environ["API_BASE_URL"],
                api_key=os.environ["API_KEY"]
            )
            print("✅ OpenAI client initialized (proxy mode)")
        except KeyError as e:
            print("⚠️ Missing env variable:", e)
            self.client = None  # HF fallback

    def reset(self) -> Observation:
        self.index = 0
        return Observation(text=self.data[self.index]["text"])

    def state(self) -> Observation:
        return Observation(text=self.data[self.index]["text"])

    def step(self, action: Action):
        """
        Take an action and return:
        (next_observation, reward, done, info)
        """

        print("🔁 STEP CALLED")

        current = self.data[self.index]

        # 🔥 FORCE LLM PROXY CALL (CRITICAL)
        if self.client:
            try:
                print("🔍 LLM CALL STARTED")

                response = self.client.chat.completions.create(
                    model="gpt-4o",  # 🔥 important change
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a complaint classification system."
                        },
                        {
                            "role": "user",
                            "content": f"Classify priority of this complaint: {current['text']}"
                        }
                    ],
                    max_tokens=10
                )

                print("✅ LLM CALL SUCCESS")

            except Exception as e:
                print("❌ LLM CALL FAILED:", e)
        else:
            print("⚠️ CLIENT NOT INITIALIZED")

        # ---------------- EXISTING LOGIC ---------------- #

        correct = current["label"]

        score = grade_prediction(action.priority, correct, current["text"])

        if correct == "critical" and action.priority != "critical":
            score *= 0.5

        score = max(0.0, min(score, 1.0))

        reward = Reward(value=score)

        self.index += 1
        done = self.index >= len(self.data)

        next_obs = None
        if not done:
            next_obs = Observation(text=self.data[self.index]["text"])

        return next_obs, reward, done, {"correct": correct}

    def get_action_space(self):
        return self.actions