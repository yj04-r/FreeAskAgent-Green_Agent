import json
import asyncio
import os
from tau_bench.envs.vln.env import load_vln_data
from a2a.utils import new_agent_text_message
from a2a.types import Message
import aiohttp

# 确保环境变量 VLN_DATA_PATH 已正确设置
os.environ["VLN_DATA_PATH"] = "C:\\Users\\18563\\Desktop\\agentify-example-tau-bench-main\\tau-bench\\tau_bench\\envs\\vln\\data\\VLNData.json"

async def test_green_agent():
    # 加载 VLN 数据
    vln_data = load_vln_data()

    # 构造任务配置
    env_config = {
        "env": "vln_env",
        "task_ids": [0],  # 假设任务索引为 0
    }

    # 构造 JSON-RPC 请求
    request_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",
        "params": {
            "message": {
                "messageId": "test_message_1",
                "role": "user",
                "parts": [
                    f"<white_agent_url>http://localhost:9002</white_agent_url>\n<env_config>{json.dumps(env_config)}</env_config>"
                ],
                "to": "green_agent",
                "from_": "tester",
            }
        },
    }

    # 发送请求到 Green Agent
    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:9001", json=request_payload) as response:
            result = await response.json()
            print("Green Agent Response:", json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(test_green_agent())