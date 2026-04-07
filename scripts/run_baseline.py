from agent.baseline_openai import run

if __name__ == "__main__":
    for level in ["easy", "medium", "hard"]:
        run(level)