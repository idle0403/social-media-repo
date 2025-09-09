#!/usr/bin/env python3
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_qchat_server():
    print("🤖 Q Chat 날씨 봇 테스트 시작")
    
    server_params = StdioServerParameters(
        command="python",
        args=["qchat_weather_server.py"]
    )
    
    test_queries = [
        "서울 날씨 어때?",
        "내일 비 와?",
        "외출하기 좋아?",
        "운동하기 좋은 날씨야?",
        "빨래 말리기 좋아?",
        "부산 온도 알려줘"
    ]
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("✅ Q Chat 서버 연결 성공")
                
                # 도구 목록 확인
                tools = await session.list_tools()
                print(f"📋 사용 가능한 도구: {len(tools.tools)}개")
                for tool in tools.tools:
                    print(f"   - {tool.name}: {tool.description}")
                
                print("\n💬 질의응답 테스트:")
                for i, query in enumerate(test_queries, 1):
                    print(f"\n{i}. 질문: {query}")
                    
                    result = await session.call_tool("analyze_weather_query", {
                        "query": query,
                        "location": "서울"
                    })
                    
                    response = json.loads(result.content[0].text)
                    print(f"   답변: {response.get('answer', '답변 없음')}")
                
                print("\n🎯 Q Chat 테스트 완료!")
                
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_qchat_server())