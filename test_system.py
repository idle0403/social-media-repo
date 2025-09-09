#!/usr/bin/env python3
import asyncio
import json
from main_app import WeatherAnalysisApp

async def test_weather_system():
    print("🧪 날씨 분석 시스템 테스트 시작")
    
    app = WeatherAnalysisApp()
    
    # 테스트 1: 날씨 데이터 수집
    print("\n1️⃣ 날씨 데이터 수집 테스트")
    try:
        weather_data = await app.get_weather_data("서울", 2)
        if "error" in weather_data:
            print(f"❌ 실패: {weather_data['error']}")
        else:
            print("✅ 성공: 날씨 데이터 수집 완료")
            print(f"   📍 위치: {weather_data.get('location')}")
            print(f"   📊 예보 개수: {len(weather_data.get('forecasts', []))}")
    except Exception as e:
        print(f"❌ 예외 발생: {str(e)}")
    
    # 테스트 2: 데이터 분석
    print("\n2️⃣ 데이터 분석 테스트")
    try:
        # 샘플 데이터로 테스트
        sample_data = {
            "location": "서울",
            "forecasts": [
                {"temp": 15.5, "humidity": 60, "description": "맑음"},
                {"temp": 18.2, "humidity": 55, "description": "구름조금"},
                {"temp": 20.1, "humidity": 50, "description": "맑음"}
            ]
        }
        
        analysis = await app.analyze_weather(sample_data)
        if "error" in analysis:
            print(f"❌ 실패: {analysis['error']}")
        else:
            print("✅ 성공: 데이터 분석 완료")
            print(f"   🌡️ 평균 온도: {analysis['temperature']['avg']}°C")
            print(f"   💧 평균 습도: {analysis['humidity']['avg']}%")
    except Exception as e:
        print(f"❌ 예외 발생: {str(e)}")
    
    # 테스트 3: 전체 워크플로우
    print("\n3️⃣ 전체 워크플로우 테스트")
    try:
        result = await app.run_full_analysis("서울", 2)
        if "error" in result:
            print(f"❌ 실패: {result['error']}")
        else:
            print("✅ 성공: 전체 워크플로우 완료")
            print(f"   📋 요약: {result['analysis_data']['summary']}")
    except Exception as e:
        print(f"❌ 예외 발생: {str(e)}")
    
    print("\n🎯 테스트 완료!")

if __name__ == "__main__":
    asyncio.run(test_weather_system())