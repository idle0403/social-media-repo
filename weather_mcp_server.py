#!/usr/bin/env python3
import asyncio
import json
import aiohttp
import os
from datetime import datetime
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("weather-analyzer")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_weather_data",
            description="네이버 API로 날씨 데이터 수집 및 파싱",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "지역명"},
                    "days": {"type": "integer", "description": "예보 일수", "default": 3}
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="analyze_weather_trend",
            description="날씨 데이터 트렌드 분석",
            inputSchema={
                "type": "object", 
                "properties": {
                    "weather_data": {"type": "string", "description": "분석할 날씨 데이터"}
                },
                "required": ["weather_data"]
            }
        ),
        Tool(
            name="send_to_slack",
            description="분석 결과를 Slack으로 전송",
            inputSchema={
                "type": "object",
                "properties": {
                    "token": {"type": "string", "description": "Slack Bot Token"},
                    "channel": {"type": "string", "description": "채널명"},
                    "message": {"type": "string", "description": "전송할 메시지"}
                },
                "required": ["token", "channel", "message"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_weather_data":
        return await get_weather_data(arguments)
    elif name == "analyze_weather_trend":
        return await analyze_weather_trend(arguments)
    elif name == "send_to_slack":
        return await send_to_slack(arguments)

async def get_weather_data(args):
    location = args["location"]
    days = args.get("days", 3)
    
    try:
        # OpenWeatherMap API 사용 (무료)
        api_key = os.getenv("OPENWEATHER_API_KEY", "demo_key")
        url = f"http://api.openweathermap.org/data/2.5/forecast"
        
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric",
            "lang": "kr",
            "cnt": days * 8  # 3시간 간격
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # 데이터 정리
                    weather_info = {
                        "location": location,
                        "timestamp": datetime.now().isoformat(),
                        "forecasts": []
                    }
                    
                    for item in data.get("list", []):
                        weather_info["forecasts"].append({
                            "datetime": item["dt_txt"],
                            "temp": item["main"]["temp"],
                            "humidity": item["main"]["humidity"],
                            "description": item["weather"][0]["description"],
                            "wind_speed": item["wind"]["speed"]
                        })
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps(weather_info, ensure_ascii=False, indent=2)
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=json.dumps({"error": f"API 오류: {response.status}"}, ensure_ascii=False)
                    )]
                    
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, ensure_ascii=False)
        )]

async def analyze_weather_trend(args):
    weather_data = json.loads(args["weather_data"])
    
    try:
        forecasts = weather_data.get("forecasts", [])
        
        if not forecasts:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "분석할 데이터가 없습니다"}, ensure_ascii=False)
            )]
        
        # 기본 통계 계산
        temps = [f["temp"] for f in forecasts]
        humidity = [f["humidity"] for f in forecasts]
        
        analysis = {
            "location": weather_data.get("location"),
            "analysis_time": datetime.now().isoformat(),
            "temperature": {
                "avg": round(sum(temps) / len(temps), 1),
                "min": min(temps),
                "max": max(temps),
                "trend": "상승" if temps[-1] > temps[0] else "하강"
            },
            "humidity": {
                "avg": round(sum(humidity) / len(humidity), 1),
                "min": min(humidity),
                "max": max(humidity)
            },
            "summary": f"{weather_data.get('location')} 지역의 평균 기온은 {round(sum(temps)/len(temps), 1)}°C이며, 습도는 {round(sum(humidity)/len(humidity), 1)}%입니다."
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(analysis, ensure_ascii=False, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, ensure_ascii=False)
        )]

async def send_to_slack(args):
    token = args["token"]
    channel = args["channel"]
    message = args["message"]
    
    try:
        url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "channel": channel,
            "text": message,
            "username": "날씨봇",
            "icon_emoji": ":sunny:"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                result = await response.json()
                
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "success": result.get("ok", False),
                        "message": "전송 완료" if result.get("ok") else result.get("error", "전송 실패")
                    }, ensure_ascii=False, indent=2)
                )]
                
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, ensure_ascii=False)
        )]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server(app) as (read_stream, write_stream):
        await app.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())