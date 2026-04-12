from fastapi import FastAPI, HTTPException
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


def classify_complaint(text: str) -> str:
    client = get_client()
    if not client:
        return "medium"
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Classify the complaint into exactly one of these priorities: "
                    "low, medium, high, critical. Reply with only the single word."
                )
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


@app.get("/")
def home():
    return {"message": "Naarad OpenEnv is running"}


@app.post("/reset")
def reset(difficulty: str = "easy"):
    obs = envs[difficulty].reset()
    return {"text": obs.text if obs else None}


@app.post("/step")
def step(body: dict):
    difficulty = body.get("difficulty", "easy")
    text = body.get("text", "")

    if not text:
        raise HTTPException(status_code=400, detail="Missing 'text'")

    priority = classify_complaint(text)
    action = Action(priority=priority)
    obs, reward, done, info = envs[difficulty].step(action)

    return {
        "text": obs.text if obs else None,
        "reward": reward.value if reward else 0,
        "done": done,
        "priority": priority,
        "info": info
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/tasks")
def get_tasks():
    return {
        "tasks": [
            {"id": "easy", "name": "Easy Complaint Classification", "grader": "env.grader.grade_prediction"},
            {"id": "medium", "name": "Medium Complaint Classification", "grader": "env.grader.grade_prediction"},
            {"id": "hard", "name": "Hard Complaint Classification", "grader": "env.grader.grade_prediction"}
        ]
    }