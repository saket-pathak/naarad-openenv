import os
from openai import OpenAI
from env.complaint_env import ComplaintEnv
from env.models import Action

# Initialize client using proxy env vars (no silent fallback)
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

MODEL = os.environ.get("MODEL_NAME", "gpt-4o-mini")  # use env var if provided


def get_action(text):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Classify the complaint into exactly one of these priorities: low, medium, high, critical. Reply with only the single word."
            },
            {"role": "user", "content": text}
        ],
        max_tokens=10,
        temperature=0
    )

    content = response.choices[0].message.content
    prediction = content.strip().lower() if content else "medium"

    if prediction not in ["low", "medium", "high", "critical"]:
        prediction = "medium"

    return prediction


def run(difficulty="easy"):
    env = ComplaintEnv(difficulty)
    obs = env.reset()

    total_score = 0
    done = False

    while not done:
        if obs is None:
            break

        action_str = get_action(obs.text)
        action = Action(priority=action_str)

        obs, reward, done, info = env.step(action)
        total_score += reward.value

    print(f"{difficulty.upper()} Score: {total_score:.2f}")


if __name__ == "__main__":
    for level in ["easy", "medium", "hard"]:
        run(level)