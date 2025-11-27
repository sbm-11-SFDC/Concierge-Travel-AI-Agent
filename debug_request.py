import requests, json, sys
COORD = "http://localhost:8005/agent/task"
payload = {"task_id":"T-debug","payload":{"query":"Top attractions in Goa"}}
try:
    r = requests.post(COORD, json=payload, timeout=30)
    print("STATUS:", r.status_code)
    print("HEADERS:", r.headers)
    # print raw body (helps when FastAPI returns HTML traceback)
    print("BODY START\n", r.text[:4000], "\nBODY END")
except Exception as e:
    print("Request failed:", e)
    sys.exit(1)
