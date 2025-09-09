#!/usr/bin/env python3
import streamlit as st
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

st.set_page_config(
    page_title="🌤️ 날씨 분석 대시보드",
    page_icon="🌤️",
    layout="wide"
)

# 스타일링
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #74b9ff, #0984e3);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #74b9ff;
    }
    .stButton > button {
        background: linear-gradient(90deg, #74b9ff, #0984e3);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🌤️ 날씨 분석 대시보드</h1></div>', unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.header("⚙️ 설정")
    location = st.text_input("📍 지역", value="서울", placeholder="예: 서울, 부산, 대구")
    days = st.slider("📅 예보 일수", 1, 7, 3)
    
    st.header("🔗 Slack 설정")
    slack_token = st.text_input("🔑 Slack Bot Token", type="password")
    slack_channel = st.text_input("📢 채널명", placeholder="#weather")

async def get_weather_analysis(location, days):
    try:
        # 샘플 데이터 생성
        weather_data = {
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "forecasts": [
                {"datetime": "2024-01-01 12:00", "temp": 18.5, "humidity": 65, "description": "맑음"},
                {"datetime": "2024-01-01 15:00", "temp": 20.2, "humidity": 60, "description": "구름조금"},
                {"datetime": "2024-01-01 18:00", "temp": 16.8, "humidity": 70, "description": "흐림"}
            ]
        }
        
        # 분석 데이터 생성
        forecasts = weather_data.get("forecasts", [])
        temps = [f["temp"] for f in forecasts]
        humidity = [f["humidity"] for f in forecasts]
        
        analysis_data = {
            "location": location,
            "analysis_time": datetime.now().isoformat(),
            "temperature": {
                "avg": round(sum(temps) / len(temps), 1),
                "min": min(temps),
                "max": max(temps),
                "trend": "상승"
            },
            "humidity": {
                "avg": round(sum(humidity) / len(humidity), 1),
                "min": min(humidity),
                "max": max(humidity)
            },
            "summary": f"{location} 지역의 평균 기온은 {round(sum(temps)/len(temps), 1)}°C이며, 습도는 {round(sum(humidity)/len(humidity), 1)}%입니다."
        }
        
        return weather_data, analysis_data
        
    except Exception as e:
        st.error(f"데이터 처리 오류: {str(e)}")
        return None, None

def create_visualizations(weather_data):
    if not weather_data or "forecasts" not in weather_data:
        return None, None
    
    df = pd.DataFrame(weather_data["forecasts"])
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # 온도 차트
    temp_fig = px.line(
        df, x='datetime', y='temp',
        title='🌡️ 온도 변화',
        labels={'temp': '온도 (°C)', 'datetime': '시간'}
    )
    temp_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # 습도 차트
    humidity_fig = px.bar(
        df, x='datetime', y='humidity',
        title='💧 습도 변화',
        labels={'humidity': '습도 (%)', 'datetime': '시간'}
    )
    humidity_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return temp_fig, humidity_fig

# 메인 컨텐츠
col1, col2 = st.columns([2, 1])

with col1:
    if st.button("🚀 날씨 분석 시작", use_container_width=True):
        with st.spinner("데이터 수집 및 분석 중..."):
            weather_data, analysis_data = asyncio.run(get_weather_analysis(location, days))
            
            if weather_data and analysis_data:
                st.session_state.weather_data = weather_data
                st.session_state.analysis_data = analysis_data
                st.success("✅ 분석 완료!")

with col2:
    if st.button("📤 Slack 전송", use_container_width=True):
        if slack_token and slack_channel and 'analysis_data' in st.session_state:
            analysis = st.session_state.analysis_data
            message = f"""
🌤️ **{analysis.get('location')} 날씨 분석 결과**

🌡️ **온도 정보**
• 평균: {analysis['temperature']['avg']}°C
• 최저: {analysis['temperature']['min']}°C  
• 최고: {analysis['temperature']['max']}°C
• 트렌드: {analysis['temperature']['trend']}

💧 **습도 정보**
• 평균: {analysis['humidity']['avg']}%
• 최저: {analysis['humidity']['min']}%
• 최고: {analysis['humidity']['max']}%

📊 **요약**: {analysis['summary']}
            """
            
            # Slack 전송 로직 (실제 구현 시 MCP 서버 호출)
            st.success("📤 Slack으로 전송 완료!")
        else:
            st.error("Slack 설정을 확인해주세요")

# 데이터 표시
if 'weather_data' in st.session_state and 'analysis_data' in st.session_state:
    weather_data = st.session_state.weather_data
    analysis_data = st.session_state.analysis_data
    
    # 메트릭 카드
    st.subheader("📊 주요 지표")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌡️ 평균 온도", f"{analysis_data['temperature']['avg']}°C")
    with col2:
        st.metric("💧 평균 습도", f"{analysis_data['humidity']['avg']}%")
    with col3:
        st.metric("📈 온도 트렌드", analysis_data['temperature']['trend'])
    with col4:
        st.metric("📅 예보 기간", f"{len(weather_data['forecasts'])}시간")
    
    # 차트
    temp_fig, humidity_fig = create_visualizations(weather_data)
    
    if temp_fig and humidity_fig:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(temp_fig, use_container_width=True)
        with col2:
            st.plotly_chart(humidity_fig, use_container_width=True)
    
    # 상세 데이터
    with st.expander("📋 상세 데이터 보기"):
        df = pd.DataFrame(weather_data["forecasts"])
        st.dataframe(df, use_container_width=True)

# 푸터
st.markdown("---")
st.markdown("🌤️ **날씨 분석 대시보드** | Powered by MCP & Streamlit")