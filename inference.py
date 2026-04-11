import os
from typing import List, Optional
from openai import OpenAI
from env.complaint_env import ComplaintEnv
from env.models import Action

# CONFIG
TASK_NAME = "complaint-priority"
BENCHMARK = "naarad-env"
SUCCESS_SCORE_THRESHOLD = 0.5

# LLM client using validator-injected proxy credentials
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

MODEL = os.environ.get("MODEL_NAME", "gpt-4o-mini")


# LOG FUNCTIONS (keep exact same format)
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
    """Call LLM through proxy to classify complaint priority."""
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


def run_episode(difficulty: str) -> List[float]:
    """Run one full episode for a given difficulty level."""
    env = ComplaintEnv(difficulty)
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

            reward_val = reward.value if reward else 0.0
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
        for difficulty in ["easy", "medium", "hard"]:
            rewards = run_episode(difficulty)
            all_rewards.extend(rewards)
            steps_taken += len(rewards)

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