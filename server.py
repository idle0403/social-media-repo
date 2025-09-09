#!/usr/bin/env python3
import asyncio
import json
from datetime import datetime, timezone
from dateutil import parser
import re
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("date-parser")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="parse_date",
            description="다양한 형식의 날짜 문자열을 파싱하여 표준 형식으로 변환",
            inputSchema={
                "type": "object",
                "properties": {
                    "date_string": {
                        "type": "string",
                        "description": "파싱할 날짜 문자열"
                    },
                    "format": {
                        "type": "string", 
                        "description": "출력 형식 (iso, korean, us, timestamp)",
                        "default": "iso"
                    }
                },
                "required": ["date_string"]
            }
        ),
        Tool(
            name="extract_dates",
            description="텍스트에서 모든 날짜 정보를 추출",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "날짜를 추출할 텍스트"
                    }
                },
                "required": ["text"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "parse_date":
        return await parse_date(arguments)
    elif name == "extract_dates":
        return await extract_dates(arguments)

async def parse_date(args):
    date_string = args["date_string"]
    output_format = args.get("format", "iso")
    
    try:
        # dateutil로 파싱
        parsed_date = parser.parse(date_string, fuzzy=True)
        
        # 출력 형식 선택
        if output_format == "iso":
            result = parsed_date.isoformat()
        elif output_format == "korean":
            result = parsed_date.strftime("%Y년 %m월 %d일 %H시 %M분")
        elif output_format == "us":
            result = parsed_date.strftime("%m/%d/%Y %I:%M %p")
        elif output_format == "timestamp":
            result = str(int(parsed_date.timestamp()))
        else:
            result = parsed_date.isoformat()
            
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": True,
                "original": date_string,
                "parsed": result,
                "datetime_obj": parsed_date.isoformat()
            }, ensure_ascii=False, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text", 
            text=json.dumps({
                "success": False,
                "error": str(e),
                "original": date_string
            }, ensure_ascii=False, indent=2)
        )]

async def extract_dates(args):
    text = args["text"]
    
    # 다양한 날짜 패턴
    patterns = [
        r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',  # 2024-01-01, 2024/01/01
        r'\d{1,2}[-/]\d{1,2}[-/]\d{4}',  # 01-01-2024, 01/01/2024
        r'\d{4}년\s*\d{1,2}월\s*\d{1,2}일',  # 2024년 1월 1일
        r'\d{1,2}월\s*\d{1,2}일',  # 1월 1일
        r'\d{4}\.\d{1,2}\.\d{1,2}',  # 2024.01.01
    ]
    
    found_dates = []
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                parsed = parser.parse(match, fuzzy=True)
                found_dates.append({
                    "original": match,
                    "parsed": parsed.isoformat(),
                    "position": text.find(match)
                })
            except:
                continue
    
    return [TextContent(
        type="text",
        text=json.dumps({
            "found_dates": found_dates,
            "count": len(found_dates)
        }, ensure_ascii=False, indent=2)
    )]

if __name__ == "__main__":
    import mcp.server.stdio
    mcp.server.stdio.run_server(app)