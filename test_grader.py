import traceback, yaml

d = yaml.safe_load(open('openenv.yaml'))
print('spec_version:', d.get('spec_version'))
print('app:', d.get('app'))
print('Tasks:', len(d.get('tasks', [])))

for t in d.get('tasks', []):
    gpath = t.get('grader', 'MISSING')
    print(f'id={t.get("id")} | grader={gpath}')
    try:
        mod, cls = str(gpath).rsplit(':', 1)
        import importlib
        score = float(getattr(importlib.import_module(mod), cls)().grade(None))
        print(f'  -> {score} {"OK" if 0 < score < 1 else "FAIL"}')
    except Exception as e:
        traceback.print_exc()
        print(f'  -> CRASHED')