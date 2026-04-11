import os
from openai import OpenAI
from env.complaint_env import ComplaintEnv
from env.models import Action

api_base = os.environ.get("API_BASE_URL") or ""
api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("API_KEY") or ""

client = OpenAI(
    base_url=api_base if api_base else None,
    api_key=api_key if api_key else "placeholder"
)


def classify(text: str) -> str:
    response = client.chat.completions.create(
        model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": "Classify the complaint into exactly one of: low, medium, high, critical. Reply with only the single word."
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


def run_episode(difficulty: str) -> float:
    env = ComplaintEnv(difficulty)
    obs = env.reset()
    done = False
    rewards = []

    while not done and obs is not None:
        text = obs.text if obs else "general complaint"
        prediction = classify(text)
        action = Action(priority=prediction)
        obs, reward, done, info = env.step(action)
        if reward:
            rewards.append(reward.value)

    score = sum(rewards) / len(rewards) if rewards else 0.0
    print(f"[{difficulty.upper()}] score={score:.3f}")
    return score


if __name__ == "__main__":
    scores = []
    for diff in ["easy", "medium", "hard"]:
        score = run_episode(diff)
        scores.append(score)
    total = sum(scores) / len(scores)
    print(f"[TOTAL] avg_score={total:.3f}")