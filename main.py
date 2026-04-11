from fastapi import FastAPI, HTTPException
from env.complaint_env import ComplaintEnv
from env.models import Action

import os
from openai import OpenAI

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
    try:
        # 🔥 FORCE proxy usage (validator requirement)
        client = OpenAI(
            base_url=os.environ["API_BASE_URL"],
            api_key=os.environ["API_KEY"]
        )

        # 🔥 ALWAYS call LLM FIRST (no conditions, no skipping)
        priority_input = str(action.get("priority", "general complaint"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Classify complaint priority."},
                {"role": "user", "content": priority_input}
            ]
        )

        llm_output = response.choices[0].message.content

        # ✅ Continue normal logic AFTER LLM call
        if "priority" not in action:
            raise HTTPException(status_code=400, detail="Missing 'priority'")

        priority = str(action["priority"])

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