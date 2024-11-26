import requests

with open("./questions.md", "r", encoding="utf8") as f:
    lines = f.readlines()

headers = {"x-project-id": "8718f49a8ca54523ac538dd196ff9b0a"}

for line in lines:
    line = line.strip()
    payload = {"session_id": 1, "content": line}
    r = requests.post("http://127.0.0.1:5610/api/chat/v1",
                      json=payload,
                      headers=headers)
    print(r.status_code, '\t', line)
    if not r.ok:
        print(r.text)
