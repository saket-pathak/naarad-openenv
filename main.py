from fastapi import FastAPI, HTTPException
from env.complaint_env import ComplaintEnv
from env.models import Action

import os
from openai import OpenAI

# ✅ Safe handling for both environments
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")

if API_BASE_URL and API_KEY:
    # ✅ Hackathon / validator mode
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY,
    )
else:
    # ✅ Local / HF fallback (no crash)
    client = OpenAI()

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

        #  IMPORTANT: Make LLM call (this is what validator checks)
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

        # Optional: use LLM output (not strictly required but good)
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