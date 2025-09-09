#!/usr/bin/env python3
import json
from datetime import datetime
from slack_bot import send_to_slack_formatted
import asyncio

class StandaloneWeatherApp:
    def get_sample_weather(self, location):
        return {
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "forecasts": [
                {"datetime": "2024-01-01 12:00", "temp": 18.5, "humidity": 65, "description": "맑음"},
                {"datetime": "2024-01-01 15:00", "temp": 20.2, "humidity": 60, "description": "구름조금"},
                {"datetime": "2024-01-01 18:00", "temp": 16.8, "humidity": 70, "description": "흐림"}
            ]
        }
    
    def analyze_weather(self, weather_data):
        forecasts = weather_data.get("forecasts", [])
        if forecasts:
            temps = [f["temp"] for f in forecasts]
            humidity = [f["humidity"] for f in forecasts]
            
            return {
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
        return {"error": "분석할 데이터가 없습니다"}
    
    async def run_analysis(self, location):
        print(f"🌤️ {location} 날씨 분석 시작...")
        
        # 1. 샘플 데이터 생성
        weather_data = self.get_sample_weather(location)
        print("✅ 날씨 데이터 수집 완료")
        
        # 2. 데이터 분석
        analysis_data = self.analyze_weather(weather_data)
        print("✅ 데이터 분석 완료")
        
        return {
            "weather_data": weather_data,
            "analysis_data": analysis_data
        }

async def main():
    app = StandaloneWeatherApp()
    result = await app.run_analysis("서울")
    
    print("🎉 분석 완료!")
    print(f"📊 결과: {result['analysis_data']['summary']}")
    print(f"🌡️ 평균 온도: {result['analysis_data']['temperature']['avg']}°C")

if __name__ == "__main__":
    asyncio.run(main())