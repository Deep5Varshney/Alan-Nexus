import requests

url = "http://localhost:8000/api/nexus/voice"

print("--- TEST 1: Technical Code Query ---")
req1 = {
    "user_input": "Can you explain how async await works in Python?",
    "session_id": "session_demo_101",
    "context": {"source": "hackathon_test"}
}
res1 = requests.post(url, json=req1)
print("Status:", res1.status_code)
print("Response:", res1.json())
print("\n")

print("--- TEST 2: Dynamic UI Navigation Action ---")
req2 = {
    "user_input": "Open the project settings and switch theme to dark mode",
    "session_id": "session_demo_101",
    "context": {"source": "hackathon_test"}
}
res2 = requests.post(url, json=req2)
print("Status:", res2.status_code)
print("Response:", res2.json())