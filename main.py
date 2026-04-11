from fastapi import FastAPI, HTTPException
from env.complaint_env import ComplaintEnv
from env.models import Action
import os
from openai import OpenAI

app = FastAPI()
env = ComplaintEnv("easy")

MODEL = os.environ.get("MODEL_NAME", "gpt-4o-mini")


def get_client():
    """Create LLM client only when env vars are available."""
    api_base = os.environ.get("API_BASE_URL")
    api_key = os.environ.get("API_KEY")
    if api_base and api_key:
        return OpenAI(base_url=api_base, api_key=api_key)
    return None


def classify_complaint(text: str) -> str:
    client = get_client()
    if not client:
        return "medium"  # HF Space fallback (no validator)

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
    return {"message": "API is running successfully"}


@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "status": "reset successful",
        "text": obs.text if obs else None
    }


@app.post("/step")
def step(body: dict):
    text = body.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Missing 'text' in request body")

    priority = classify_complaint(text)
    action = Action(priority=priority)
    obs, reward, done, info = env.step(action)

    return {
        "text": obs.text if obs else None,
        "reward": reward.value if reward else 0,
        "done": done,
        "llm_priority": priority,
        "info": info if info else {}
    }