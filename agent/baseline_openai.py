import os
from dotenv import load_dotenv
from openai import OpenAI
from env.complaint_env import ComplaintEnv
from env.models import Action

#  LOAD ENV VARIABLES
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_action(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Classify the complaint into one of: low, medium, high, critical."},
            {"role": "user", "content": text}
        ]
    )

    content = response.choices[0].message.content

    #  Safety check
    if content is None:
        return "medium"  # fallback

    return content.strip().lower()


def run(difficulty="easy"):
    env = ComplaintEnv(difficulty)
    obs = env.reset()

    total_score = 0
    done = False

    while not done:
        if obs is None:
            break

        action_str = get_action(obs.text)

        # FIX 1: wrap in Action
        action = Action(priority=action_str)

        obs, reward, done, info = env.step(action)

        # FIX 2: use reward.value
        total_score += reward.value

    print(f"{difficulty.upper()} Score: {total_score:.2f}")


if __name__ == "__main__":
    for level in ["easy", "medium", "hard"]:
        run(level)