import os
from openai import OpenAI
from env.complaint_env import ComplaintEnv
from env.models import Action

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_action(text):
    """
    Uses OpenAI model to predict priority
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Classify the complaint into one of: low, medium, high, critical."},
            {"role": "user", "content": text}
        ]
    )

    return response.choices[0].message.content.strip().lower()


def run(difficulty="easy"):
    env = ComplaintEnv(difficulty)
    obs = env.reset()

    total_score = 0
    done = False

    while not done:
        action_str = get_action(obs.text)

        # FIX 1: wrap in Action
        action = Action(priority=action_str)

        obs, reward, done, info = env.step(action)

        # FIX 2: use reward.value
        total_score += reward.value

    print(f"{difficulty.upper()} Score:", total_score)


if __name__ == "__main__":
    for level in ["easy", "medium", "hard"]:
        run(level)