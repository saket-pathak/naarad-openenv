from fastapi import FastAPI
from pydantic import BaseModel
from env.complaint_env import ComplaintEnv
from env.models import Action
import os
from openai import OpenAI

app = FastAPI()

envs = {
    "easy": ComplaintEnv("easy"),
    "medium": ComplaintEnv("medium"),
    "hard": ComplaintEnv("hard")
}

MODEL = os.environ.get("MODEL_NAME", "gpt-4o-mini")


def get_client():
    api_base = os.environ.get("API_BASE_URL")
    api_key = (
        os.environ.get("HF_TOKEN") or
        os.environ.get("OPENAI_API_KEY") or
        os.environ.get("API_KEY")
    )
    if api_base and api_key:
        return OpenAI(base_url=api_base, api_key=api_key)
    return None


def classify(text: str) -> str:
    client = get_client()
    if not client:
        return "medium"
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Classify the complaint into exactly one of: low, medium, high, critical. Reply with only the single word."},
            {"role": "user", "content": text}
        ],
        max_tokens=10,
        temperature=0
    )
    content = response.choices[0].message.content
    prediction = content.strip().lower() if content else "medium"
    return prediction if prediction in ["low", "medium", "high", "critical"] else "medium"


class ResetRequest(BaseModel):
    difficulty: str = "easy"


class StepRequest(BaseModel):
    text: str
    difficulty: str = "easy"


@app.get("/")
def root():
    return {"status": "ok", "env": "naarad-openenv"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/reset")
def reset(req: ResetRequest):
    obs = envs[req.difficulty].reset()
    return {"text": obs.text if obs else None, "difficulty": req.difficulty}


@app.post("/step")
def step(req: StepRequest):
    priority = classify(req.text)
    action = Action(priority=priority)
    obs, reward, done, info = envs[req.difficulty].step(action)
    return {
        "observation": {"text": obs.text if obs else None},
        "reward": reward.value if reward else 0,
        "done": done,
        "info": info
    }


@app.get("/state")
def state():
    return {"tasks": list(envs.keys())}


@app.get("/tasks")
def tasks():
    return {
        "tasks": [
            {"id": "easy", "description": "Simple complaint classification", "difficulty": "easy"},
            {"id": "medium", "description": "Moderate complaint classification", "difficulty": "medium"},
            {"id": "hard", "description": "Complex complaint classification", "difficulty": "hard"}
        ]
    }