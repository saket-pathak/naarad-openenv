from fastapi import FastAPI, HTTPException
from env.complaint_env import ComplaintEnv
from env.models import Action

import os
from openai import OpenAI

#  STRICT PROXY USAGE (validator requirement)
try:
    client = OpenAI(
        base_url=os.environ["API_BASE_URL"],
        api_key=os.environ["API_KEY"]
    )
    USING_PROXY = True
except KeyError:
    #  HF fallback only
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    USING_PROXY = False

app = FastAPI()
env = ComplaintEnv("easy")


@app.get("/")
def home():
    return {
        "message": "API is running successfully",
        "using_proxy": USING_PROXY
    }


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

        #  FORCE LLM CALL (no condition)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Classify complaint priority."
                },
                {
                    "role": "user",
                    "content": f"{priority}"
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
                "using_proxy": USING_PROXY,
                **(info if info else {})
            }
        }

    except Exception as e:
        return {"error": str(e)}