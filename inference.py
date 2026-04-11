import os
from typing import List, Optional
from openai import OpenAI
from server.environment import ComplaintEnvironment
from env.models import Action

# CONFIG
TASK_NAME = "complaint-priority"
BENCHMARK = "naarad-env"
SUCCESS_SCORE_THRESHOLD = 0.5

# LLM client using validator-injected proxy credentials
api_base = os.environ.get("API_BASE_URL") or ""
api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("API_KEY") or ""

client = OpenAI(
    base_url=api_base if api_base else None,
    api_key=api_key if api_key else "placeholder"
)

MODEL = os.environ.get("MODEL_NAME", "gpt-4o-mini")


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
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


def classify_complaint(text: str) -> str:
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


def run_episode() -> List[float]:
    env = ComplaintEnvironment()
    obs = env.reset()
    rewards = []
    step = 0
    done = False

    while not done and obs is not None:
        step += 1
        try:
            action_str = classify_complaint(obs.text)
            action = Action(priority=action_str)
            obs, reward, done, info = env.step(action)

            reward_val = float(reward) if reward else 0.0
            rewards.append(reward_val)
            log_step(step, action_str, reward_val, done, None)

        except Exception as e:
            log_step(step, "error", 0.0, True, str(e))
            break

    return rewards


def main():
    all_rewards = []
    steps_taken = 0
    success = False
    score = 0.0

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL)

    try:
        rewards = run_episode()
        all_rewards.extend(rewards)
        steps_taken = len(rewards)

        score = sum(all_rewards) / len(all_rewards) if all_rewards else 0.0
        success = score >= SUCCESS_SCORE_THRESHOLD

    finally:
        log_end(
            success=success,
            steps=steps_taken,
            score=score,
            rewards=all_rewards
        )


if __name__ == "__main__":
    main()