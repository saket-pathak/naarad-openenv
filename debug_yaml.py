import yaml

with open("openenv.yaml") as f:
    d = yaml.safe_load(f)

print("TASK COUNT:", len(d.get("tasks", [])))
print(d.get("tasks"))