import os
import requests
from typing import List, Optional

#  CONFIG (important)
API_BASE_URL = os.getenv("API_BASE_URL", "https://saketpathak-naarad-openenv.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "simple-agent")

TASK_NAME = "complaint-priority"
BENCHMARK = "naarad-env"

MAX_STEPS = 8
SUCCESS_SCORE_THRESHOLD = 0.5


# LOG FUNCTIONS (STRICT FORMAT)
def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


# SIMPLE AGENT (rule-based for now)
def choose_priority(text: str) -> str:
    text = text.lower()

    if "fire" in text or "emergency" in text:
        return "critical"
    elif "water" in text or "electricity" in text:
        return "high"
    elif "road" in text:
        return "medium"
    else:
        return "low"


#  MAIN LOGIC
def main():
    rewards = []
    steps_taken = 0
    success = False
    score = 0.0

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        # 🔁 RESET
        requests.post(f"{API_BASE_URL}/reset")

        last_text = ""

        for step in range(1, MAX_STEPS + 1):
            try:
                # 🤖 choose action
                action = choose_priority(last_text)

                # ▶️ STEP CALL
                response = requests.post(
                    f"{API_BASE_URL}/step",
                    json={"priority": action}
                )

                data = response.json()

                # 📊 extract values
                text = data.get("text", "")
                reward = float(data.get("reward", 0))
                done = bool(data.get("done", False))
                error = data.get("error", None)

                rewards.append(reward)
                steps_taken = step

                log_step(step, action, reward, done, error)

                last_text = text

                if done:
                    break

            except Exception as e:
                log_step(step, action="error", reward=0.0, done=True, error=str(e))
                break

        #  SCORE CALCULATION
        if rewards:
            score = sum(rewards) / len(rewards)

        success = score >= SUCCESS_SCORE_THRESHOLD

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    main()