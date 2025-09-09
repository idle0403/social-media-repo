#!/usr/bin/env python3
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_date_parser():
    server_params = StdioServerParameters(
        command="python", 
        args=["server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 도구 목록 확인
            tools = await session.list_tools()
            print("사용 가능한 도구:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")
            
            # 날짜 파싱 테스트
            test_dates = [
                "2024년 3월 15일",
                "2024-03-15 14:30:00",
                "March 15, 2024",
                "15/03/2024"
            ]
            
            for date_str in test_dates:
                result = await session.call_tool("parse_date", {
                    "date_string": date_str,
                    "format": "korean"
                })
                print(f"\n입력: {date_str}")
                print(f"결과: {result.content[0].text}")
            
            # 텍스트에서 날짜 추출 테스트
            text = "회의는 2024년 3월 15일에 있고, 마감일은 2024-04-01입니다."
            result = await session.call_tool("extract_dates", {"text": text})
            print(f"\n텍스트 분석: {text}")
            print(f"추출된 날짜: {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(test_date_parser())