#!/usr/bin/env python3
import asyncio
import json
from datetime import datetime
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("simple-weather")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_sample_weather",
            description="샘플 날씨 데이터 생성",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "지역명"}
                },
                "required": ["location"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_sample_weather":
        location = arguments["location"]
        
        # 샘플 데이터 생성
        sample_data = {
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "forecasts": [
                {"datetime": "2024-01-01 12:00", "temp": 18.5, "humidity": 65, "description": "맑음"},
                {"datetime": "2024-01-01 15:00", "temp": 20.2, "humidity": 60, "description": "구름조금"},
                {"datetime": "2024-01-01 18:00", "temp": 16.8, "humidity": 70, "description": "흐림"}
            ]
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(sample_data, ensure_ascii=False, indent=2)
        )]

if __name__ == "__main__":
    import mcp.server.stdio
    asyncio.run(mcp.server.stdio.stdio_server(app))