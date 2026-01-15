import requests
import json

def test_agent_to_agent():
    # Define the green agent URL
    green_agent_url = "http://localhost:9001/"

    # Define the white agent URL
    white_agent_url = "http://localhost:9002"

    # Prepare the JSON-RPC request payload
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",
        "params": {
            "message": {
                "messageId": "test-1",
                "role": "user",
                "parts": [
                    {"kind": "data", "data": {"text": "Hello from green agent"}}
                ],
                "to": "white_agent",
                "from": "green_agent"
            },
            "white_agent_url": white_agent_url
        }
    }

    # Send the request to the green agent
    headers = {"Content-Type": "application/json"}
    response = requests.post(green_agent_url, headers=headers, data=json.dumps(payload))

    # Print the response
    print("Response from green agent:")
    print(response.status_code)
    print(response.json())

if __name__ == "__main__":
    test_agent_to_agent()