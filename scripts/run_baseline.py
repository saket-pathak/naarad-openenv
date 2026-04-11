from agent.baseline_openai import run

#  This is what validator will call
def run_entry():
    for level in ["easy", "medium", "hard"]:
        run(level)


# Optional: still allow local execution
if __name__ == "__main__":
    run_entry()