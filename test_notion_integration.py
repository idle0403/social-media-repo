#!/usr/bin/env python3
import asyncio
import json
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_notion_integration():
    print("🧪 Notion MCP 연동 테스트 시작")
    
    # 환경변수 확인
    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    if not notion_token:
        print("❌ NOTION_TOKEN 환경변수가 설정되지 않았습니다")
        return
    
    if not database_id:
        print("❌ NOTION_DATABASE_ID 환경변수가 설정되지 않았습니다")
        return
    
    print("✅ 환경변수 설정 확인 완료")
    
    # MCP 서버 연결 테스트
    server_params = StdioServerParameters(
        command="python",
        args=["notion_weather_server.py"]
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("✅ MCP 서버 연결 성공")
                
                # 도구 목록 확인
                tools = await session.list_tools()
                print(f"📋 사용 가능한 도구: {len(tools.tools)}개")
                for tool in tools.tools:
                    print(f"   - {tool.name}: {tool.description}")
                
                # 테스트 1: 날씨 데이터 수집 및 Notion 저장
                print("\n🌤️ 날씨 데이터 수집 및 Notion 저장 테스트")
                result = await session.call_tool("get_weather_and_save", {
                    "location": "서울",
                    "database_id": database_id
                })
                
                response_data = json.loads(result.content[0].text)
                if response_data.get("success"):
                    print("✅ Notion 페이지 생성 성공!")
                    print(f"   📄 페이지 ID: {response_data.get('page_id')}")
                    print(f"   🔗 URL: {response_data.get('url')}")
                else:
                    print(f"❌ 실패: {response_data.get('error')}")
                
                # 테스트 2: 직접 페이지 생성
                print("\n📝 직접 페이지 생성 테스트")
                sample_weather_data = {
                    "location": "부산",
                    "temperature": {"avg": 20.5, "min": 18.0, "max": 23.0},
                    "humidity": {"avg": 70, "min": 65, "max": 75},
                    "summary": "부산 지역의 날씨는 온화하며 습도가 다소 높습니다."
                }
                
                result = await session.call_tool("create_weather_page", {
                    "database_id": database_id,
                    "location": "부산",
                    "weather_data": json.dumps(sample_weather_data)
                })
                
                response_data = json.loads(result.content[0].text)
                if response_data.get("success"):
                    print("✅ 직접 페이지 생성 성공!")
                    print(f"   📄 페이지 ID: {response_data.get('page_id')}")
                else:
                    print(f"❌ 실패: {response_data.get('error')}")
                
    except Exception as e:
        print(f"❌ 연결 오류: {str(e)}")
        print("\n🔧 문제 해결 방법:")
        print("1. NOTION_TOKEN 환경변수 확인")
        print("2. NOTION_DATABASE_ID 환경변수 확인") 
        print("3. Notion Integration 권한 확인")
        print("4. 데이터베이스에 Integration 연결 확인")
    
    print("\n🎯 테스트 완료!")

if __name__ == "__main__":
    # 환경변수 로드
    from dotenv import load_dotenv
    load_dotenv()
    
    asyncio.run(test_notion_integration())