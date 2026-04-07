from env.complaint_env import ComplaintEnv

def test_env():
    env = ComplaintEnv()
    obs = env.reset()
    assert obs is not None