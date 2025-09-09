#!/usr/bin/env python3
import asyncio
import json
import os
from datetime import datetime
from mcp.server import Server
from mcp.types import Tool, TextContent
import aiohttp

app = Server("notion-weather-mcp")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="create_weather_page",
            description="Notion에 날씨 분석 페이지 생성",
            inputSchema={
                "type": "object",
                "properties": {
                    "database_id": {"type": "string", "description": "Notion 데이터베이스 ID"},
                    "location": {"type": "string", "description": "지역명"},
                    "weather_data": {"type": "string", "description": "날씨 분석 데이터"}
                },
                "required": ["database_id", "location", "weather_data"]
            }
        ),
        Tool(
            name="get_weather_and_save",
            description="날씨 데이터 수집 후 Notion에 저장",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "지역명"},
                    "database_id": {"type": "string", "description": "Notion 데이터베이스 ID"}
                },
                "required": ["location", "database_id"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "create_weather_page":
        return await create_weather_page(arguments)
    elif name == "get_weather_and_save":
        return await get_weather_and_save(arguments)

async def create_weather_page(args):
    database_id = args["database_id"]
    location = args["location"]
    weather_data = json.loads(args["weather_data"])
    
    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token:
        return [TextContent(
            type="text",
            text=json.dumps({"error": "NOTION_TOKEN 환경변수가 설정되지 않았습니다"}, ensure_ascii=False)
        )]
    
    try:
        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # Notion 페이지 데이터 구성
        page_data = {
            "parent": {"database_id": database_id},
            "properties": {
                "제목": {
                    "title": [{"text": {"content": f"{location} 날씨 분석 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"}}]
                },
                "지역": {
                    "rich_text": [{"text": {"content": location}}]
                },
                "평균온도": {
                    "number": weather_data.get("temperature", {}).get("avg", 0)
                },
                "평균습도": {
                    "number": weather_data.get("humidity", {}).get("avg", 0)
                },
                "분석일시": {
                    "date": {"start": datetime.now().isoformat()}
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"text": {"content": f"🌤️ {location} 날씨 분석 보고서"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": weather_data.get("summary", "분석 데이터 없음")}}]
                    }
                },
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"text": {"content": f"🌡️ 평균 온도: {weather_data.get('temperature', {}).get('avg', 'N/A')}°C"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "bulleted_list_item", 
                    "bulleted_list_item": {
                        "rich_text": [{"text": {"content": f"💧 평균 습도: {weather_data.get('humidity', {}).get('avg', 'N/A')}%"}}]
                    }
                }
            ]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=page_data) as response:
                if response.status == 200:
                    result = await response.json()
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "success": True,
                            "page_id": result["id"],
                            "url": result["url"],
                            "message": "Notion 페이지가 성공적으로 생성되었습니다"
                        }, ensure_ascii=False, indent=2)
                    )]
                else:
                    error_text = await response.text()
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "success": False,
                            "error": f"Notion API 오류: {response.status}",
                            "details": error_text
                        }, ensure_ascii=False, indent=2)
                    )]
                    
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)
        )]

async def get_weather_and_save(args):
    location = args["location"]
    database_id = args["database_id"]
    
    try:
        # 날씨 데이터 수집 (간단한 더미 데이터)
        weather_analysis = {
            "location": location,
            "temperature": {"avg": 18.5, "min": 15.2, "max": 22.1},
            "humidity": {"avg": 65, "min": 55, "max": 75},
            "summary": f"{location} 지역의 현재 날씨는 온화하며, 평균 기온 18.5°C, 습도 65%입니다."
        }
        
        # Notion에 저장
        result = await create_weather_page({
            "database_id": database_id,
            "location": location,
            "weather_data": json.dumps(weather_analysis)
        })
        
        return result
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)
        )]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server(app) as (read_stream, write_stream):
        await app.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())