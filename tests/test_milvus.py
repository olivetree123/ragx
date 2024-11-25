import requests

with open("./scripts/questions.md", "r", encoding="utf8") as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()
    payload = {"scene_id": 100, "content": line}
    r = requests.post("http://127.0.0.1:8000/chat", json=payload)
    print(r.status_code, '\t', line)
    if not r.ok:
        print(r.text)
