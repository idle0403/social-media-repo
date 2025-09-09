#!/usr/bin/env python3
import asyncio
import json
import os
from datetime import datetime
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from slack_bot import send_to_slack_formatted

class WeatherAnalysisApp:
    def __init__(self):
        self.mcp_server_params = StdioServerParameters(
            command="python", 
            args=["simple_weather_server.py"]
        )
    
    async def get_weather_data(self, location, days=3):
        async with stdio_client(self.mcp_server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                result = await session.call_tool("get_sample_weather", {
                    "location": location
                })
                
                return json.loads(result.content[0].text)
    
    async def analyze_weather(self, weather_data):
        # 간단한 분석 로직
        forecasts = weather_data.get("forecasts", [])
        if forecasts:
            temps = [f["temp"] for f in forecasts]
            humidity = [f["humidity"] for f in forecasts]
            
            analysis = {
                "location": weather_data.get("location"),
                "temperature": {
                    "avg": round(sum(temps) / len(temps), 1),
                    "min": min(temps),
                    "max": max(temps)
                },
                "humidity": {
                    "avg": round(sum(humidity) / len(humidity), 1)
                },
                "summary": f"{weather_data.get('location')} 지역 평균 기온 {round(sum(temps)/len(temps), 1)}°C"
            }
            return analysis
        else:
            return {"error": "분석할 데이터가 없습니다"}
    
    async def send_to_slack(self, token, channel, analysis_data):
        return await send_to_slack_formatted(token, channel, analysis_data)
    
    async def run_full_analysis(self, location, days, slack_token=None, slack_channel=None):
        print(f"🌤️ {location} 날씨 분석 시작...")
        
        # 1. 날씨 데이터 수집
        weather_data = await self.get_weather_data(location, days)
        if "error" in weather_data:
            return {"error": weather_data["error"]}
        
        print("✅ 날씨 데이터 수집 완료")
        
        # 2. 데이터 분석
        analysis_data = await self.analyze_weather(weather_data)
        if "error" in analysis_data:
            return {"error": analysis_data["error"]}
        
        print("✅ 데이터 분석 완료")
        
        # 3. Slack 전송 (선택사항)
        slack_result = None
        if slack_token and slack_channel:
            slack_result = await self.send_to_slack(slack_token, slack_channel, analysis_data)
            if slack_result["success"]:
                print("✅ Slack 전송 완료")
            else:
                print(f"❌ Slack 전송 실패: {slack_result['error']}")
        
        return {
            "weather_data": weather_data,
            "analysis_data": analysis_data,
            "slack_result": slack_result
        }

async def main():
    app = WeatherAnalysisApp()
    
    # 환경변수에서 설정 읽기
    location = os.getenv("WEATHER_LOCATION", "서울")
    days = int(os.getenv("WEATHER_DAYS", "3"))
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    slack_channel = os.getenv("SLACK_CHANNEL")
    
    result = await app.run_full_analysis(location, days, slack_token, slack_channel)
    
    if "error" in result:
        print(f"❌ 오류: {result['error']}")
    else:
        print("🎉 전체 분석 완료!")
        print(f"📊 분석 결과: {result['analysis_data']['summary']}")

if __name__ == "__main__":
    asyncio.run(main())