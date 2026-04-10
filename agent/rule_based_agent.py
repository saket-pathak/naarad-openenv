from env.complaint_env import ComplaintEnv
from env.models import Action


def rule_based_predict(text):
    """
    Simple rule-based logic for classification
    """
    text = text.lower()

    if any(word in text for word in ["fire", "accident", "emergency"]):
        return "critical"
    elif any(word in text for word in ["water", "electricity", "power"]):
        return "high"
    elif any(word in text for word in ["not working", "delay", "issue"]):
        return "medium"
    else:
        return "low"


def run(difficulty="easy"):
    env = ComplaintEnv(difficulty)
    obs = env.reset()

    total_score = 0
    done = False

    while not done:
        if obs is None:
            break

        action_str = rule_based_predict(obs.text)

        action = Action(priority=action_str)

        obs, reward, done, info = env.step(action)

        total_score += reward.value

    return total_score


if __name__ == "__main__":
    for level in ["easy", "medium", "hard"]:
        run(level)