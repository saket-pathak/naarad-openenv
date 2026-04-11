import os
from openai import OpenAI
from env.complaint_env import ComplaintEnv
from env.models import Action


def get_client():
    """
    Create OpenAI client using LiteLLM proxy (validator)
    or fallback for local/HF
    """
    try:
        return OpenAI(
            base_url=os.environ["API_BASE_URL"],
            api_key=os.environ["API_KEY"]
        )
    except KeyError:
        # fallback (HF/local) → no crash
        return None


def get_action(text):
    client = get_client()

    # ✅ If proxy available → make real call
    if client:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Classify the complaint into one of: low, medium, high, critical."},
                {"role": "user", "content": text}
            ]
        )

        content = response.choices[0].message.content
        prediction = content.strip().lower() if content else "medium"

    else:
        # ✅ HF fallback (no API)
        prediction = "medium"

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