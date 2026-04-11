from fastapi import FastAPI, HTTPException
from env.complaint_env import ComplaintEnv
from env.models import Action

import os
from openai import OpenAI

# ✅ Try to get injected variables
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")

# ✅ Initialize client properly
if API_BASE_URL and API_KEY:
    # 🔥 Hackathon mode (REQUIRED for validation)
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY,
    )
else:
    # ✅ HF fallback (prevents crash)
    client = OpenAI()  # uses default OpenAI config if available

app = FastAPI()
env = ComplaintEnv("easy")


@app.get("/")
def home():
    return {"message": "API is running successfully"}


@app.post("/reset")
def reset():
    env.reset()
    return {"status": "reset successful"}


@app.post("/step")
def step(action: dict):
    if "priority" not in action:
        raise HTTPException(status_code=400, detail="Missing 'priority'")

    try:
        priority = str(action["priority"])

        # ✅ ALWAYS attempt LLM call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that classifies complaint priority."
                },
                {
                    "role": "user",
                    "content": f"Classify this complaint priority: {priority}"
                }
            ]
        )

        llm_output = response.choices[0].message.content

        act = Action(priority=priority)
        obs, reward, done, info = env.step(act)

        return {
            "text": obs.text if obs else None,
            "reward": reward.value if reward else 0,
            "done": done,
            "info": {
                "llm_response": llm_output,
                **(info if info else {})
            }
        }

    except Exception as e:
        return {"error": str(e)}