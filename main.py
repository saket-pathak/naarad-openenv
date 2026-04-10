from fastapi import FastAPI, HTTPException
from env.complaint_env import ComplaintEnv
from env.models import Action

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
        act = Action(priority=priority)

        obs, reward, done, info = env.step(act)

        return {
            "text": obs.text if obs else None,
            "reward": reward.value if reward else 0,
            "done": done,
            "info": info if info else {}
        }

    except Exception as e:
        return {"error": str(e)}