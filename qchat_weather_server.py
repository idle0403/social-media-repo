#!/usr/bin/env python3
import asyncio
import json
import os
from datetime import datetime
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("qchat-weather")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="analyze_weather_query",
            description="Q Chat을 통한 날씨 질의응답 처리",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "사용자 질문"},
                    "location": {"type": "string", "description": "지역명", "default": "서울"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_weather_answer",
            description="날씨 관련 질문에 대한 답변 생성",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "날씨 질문"},
                    "context": {"type": "string", "description": "추가 컨텍스트"}
                },
                "required": ["question"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "analyze_weather_query":
        return await analyze_weather_query(arguments)
    elif name == "get_weather_answer":
        return await get_weather_answer(arguments)

async def analyze_weather_query(args):
    query = args["query"]
    location = args.get("location", "서울")
    
    try:
        # 샘플 날씨 데이터 생성
        weather_data = {
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "current": {
                "temp": 18.5,
                "humidity": 65,
                "description": "맑음",
                "wind_speed": 2.3
            },
            "forecast": [
                {"time": "오늘", "temp": 20, "desc": "맑음"},
                {"time": "내일", "temp": 22, "desc": "구름조금"},
                {"time": "모레", "temp": 19, "desc": "흐림"}
            ]
        }
        
        # 질문 분석 및 답변 생성
        if "온도" in query or "기온" in query:
            answer = f"{location}의 현재 기온은 {weather_data['current']['temp']}°C입니다."
        elif "습도" in query:
            answer = f"{location}의 현재 습도는 {weather_data['current']['humidity']}%입니다."
        elif "날씨" in query:
            answer = f"{location}의 현재 날씨는 {weather_data['current']['description']}이며, 기온은 {weather_data['current']['temp']}°C입니다."
        elif "예보" in query or "내일" in query:
            forecast_text = "\n".join([f"• {f['time']}: {f['temp']}°C, {f['desc']}" for f in weather_data['forecast']])
            answer = f"{location} 날씨 예보:\n{forecast_text}"
        else:
            answer = f"{location}의 종합 날씨 정보: 현재 {weather_data['current']['temp']}°C, {weather_data['current']['description']}, 습도 {weather_data['current']['humidity']}%"
        
        result = {
            "query": query,
            "location": location,
            "answer": answer,
            "weather_data": weather_data,
            "timestamp": datetime.now().isoformat()
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e), "query": query}, ensure_ascii=False)
        )]

async def get_weather_answer(args):
    question = args["question"]
    context = args.get("context", "")
    
    try:
        # 질문 유형별 답변 템플릿
        answer_templates = {
            "비": "현재 강수 확률은 낮습니다. 우산 없이도 외출하셔도 됩니다.",
            "추위": "현재 기온이 적당하니 가벼운 외투 정도면 충분합니다.",
            "더위": "현재 기온이 쾌적한 수준입니다. 시원한 복장을 권합니다.",
            "외출": "현재 날씨가 좋아 외출하기 적합합니다.",
            "운동": "야외 운동하기 좋은 날씨입니다.",
            "세탁": "빨래 말리기 좋은 날씨입니다."
        }
        
        # 키워드 매칭으로 답변 선택
        answer = "날씨 관련 정보를 확인해드리겠습니다."
        for keyword, template in answer_templates.items():
            if keyword in question:
                answer = template
                break
        
        result = {
            "question": question,
            "answer": answer,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e), "question": question}, ensure_ascii=False)
        )]

if __name__ == "__main__":
    from mcp.server.stdio import stdio_server
    asyncio.run(stdio_server(app))