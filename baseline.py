from env.complaint_env import ComplaintEnv
from env.models import Action
from openai import OpenAI
import os

def run_episode():
    env = ComplaintEnv("easy")
    obs = env.reset()
    done = False

    client = OpenAI(
        base_url=os.environ["API_BASE_URL"],
        api_key=os.environ["API_KEY"]
    )

    while not done:
        #  Safe handling of obs
        text = obs.text if obs else "general complaint"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Classify complaint priority as low, medium, high, or critical."},
                {"role": "user", "content": text}
            ]
        )

        #  Safe handling of response
        content = response.choices[0].message.content
        prediction = (content.strip().lower() if content else "medium")

        if prediction not in ["low", "medium", "high", "critical"]:
            prediction = "medium"

        action = Action(priority=prediction)

        obs, reward, done, info = env.step(action)

    return True


if __name__ == "__main__":
    run_episode()