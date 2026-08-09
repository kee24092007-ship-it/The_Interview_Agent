import json, urllib.request

base = 'http://127.0.0.1:8000/api/interview'
headers = {'Content-Type': 'application/json'}

def req(data):
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(base, data=body, headers=headers, method='POST')
    with urllib.request.urlopen(req, timeout=10) as resp:
        print('STATUS', resp.status)
        print(resp.read().decode())

sessionId = 'test-session-1'
print('START')
req({'sessionId': sessionId, 'candidate': {'name': 'Alice', 'role': 'Developer'}})
for i, msg in enumerate([
    'I have worked on multiple projects with team collaboration and delivered impact.',
    'I led a product launch and measured results with metrics.',
    'Detailed response with collaboration and results.',
    'Detailed response with collaboration and results.',
    'Detailed response with collaboration and results.',
], start=1):
    print(f'\nTURN {i}')
    req({'sessionId': sessionId, 'message': msg})
