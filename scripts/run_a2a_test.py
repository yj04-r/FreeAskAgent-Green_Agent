import urllib.request, json, sys

def get(url):
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as r:
            print(f"GET {url} -> {r.status}")
            print(r.read().decode())
    except Exception as e:
        print(f"GET {url} failed:", e)


def post(url, data):
    try:
        body = json.dumps(data).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"POST {url} -> {r.status}")
            print(r.read().decode())
    except Exception as e:
        print(f"POST {url} failed:", e)


if __name__ == '__main__':
    agentcard = 'http://localhost:9001/.well-known/agent-card.json'
    rpc = 'http://localhost:9001/'

    print('=== Fetch agent-card ===')
    get(agentcard)

    print('\n=== Send message/send JSON-RPC ===')
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",
        "params": {
            "message": {
                "type": "message",
                "messageId": "test-1",
                "role": "user",
                "parts": [{"kind": "data", "data": {"text": "Hello from test client"}}],
                "to": "agent",
                "from": "tester"
            }
        }
    }
    post(rpc, payload)
