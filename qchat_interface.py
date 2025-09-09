#!/usr/bin/env python3
import streamlit as st
import asyncio
import json
from datetime import datetime
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

st.set_page_config(
    page_title="🤖 Q Chat 날씨 봇",
    page_icon="🤖",
    layout="wide"
)

# 스타일링
st.markdown("""
<style>
    .chat-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .user-message {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background: #f3e5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #9c27b0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-container"><h1>🤖 Q Chat 날씨 봇</h1><p>자연어로 날씨를 물어보세요!</p></div>', unsafe_allow_html=True)

# 세션 상태 초기화
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

async def get_qchat_response(query, location="서울"):
    server_params = StdioServerParameters(
        command="python",
        args=["qchat_weather_server.py"]
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                result = await session.call_tool("analyze_weather_query", {
                    "query": query,
                    "location": location
                })
                
                return json.loads(result.content[0].text)
    except Exception as e:
        return {"error": str(e), "answer": "죄송합니다. 현재 날씨 정보를 가져올 수 없습니다."}

# 채팅 인터페이스
col1, col2 = st.columns([3, 1])

with col1:
    user_input = st.text_input("💬 날씨에 대해 무엇이든 물어보세요:", placeholder="예: 서울 날씨 어때? 내일 비 와?")

with col2:
    location = st.selectbox("📍 지역", ["서울", "부산", "대구", "인천", "광주", "대전", "울산"])

if st.button("🚀 질문하기", use_container_width=True) and user_input:
    with st.spinner("🤖 답변 생성 중..."):
        response = asyncio.run(get_qchat_response(user_input, location))
        
        # 채팅 히스토리에 추가
        st.session_state.chat_history.append({
            "user": user_input,
            "bot": response.get("answer", "답변을 생성할 수 없습니다."),
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "location": location
        })

# 채팅 히스토리 표시
if st.session_state.chat_history:
    st.subheader("💬 대화 내역")
    
    for i, chat in enumerate(reversed(st.session_state.chat_history[-10:])):  # 최근 10개만 표시
        with st.container():
            st.markdown(f'<div class="user-message"><strong>👤 사용자 ({chat["timestamp"]}):</strong><br/>{chat["user"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="bot-message"><strong>🤖 Q Chat:</strong><br/>{chat["bot"]}</div>', unsafe_allow_html=True)
            
            # 추가 액션 버튼
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"📝 Notion 저장", key=f"notion_{i}"):
                    st.success("✅ Notion에 저장되었습니다!")
            with col2:
                if st.button(f"📤 Slack 전송", key=f"slack_{i}"):
                    st.success("✅ Slack으로 전송되었습니다!")
            with col3:
                if st.button(f"📊 상세 분석", key=f"detail_{i}"):
                    st.info("📈 상세 분석 결과를 확인하세요!")

# 사이드바
with st.sidebar:
    st.header("🔧 설정")
    
    # 자주 묻는 질문
    st.subheader("💡 자주 묻는 질문")
    quick_questions = [
        "오늘 날씨 어때?",
        "내일 비 와?",
        "외출하기 좋아?",
        "운동하기 좋은 날씨야?",
        "빨래 말리기 좋아?",
        "우산 필요해?"
    ]
    
    for question in quick_questions:
        if st.button(question, key=f"quick_{question}"):
            st.session_state.quick_question = question
            st.rerun()
    
    # 히스토리 관리
    st.subheader("📋 히스토리")
    if st.button("🗑️ 대화 내역 삭제"):
        st.session_state.chat_history = []
        st.success("대화 내역이 삭제되었습니다!")
    
    st.write(f"💬 총 대화 수: {len(st.session_state.chat_history)}")

# 빠른 질문 처리
if hasattr(st.session_state, 'quick_question'):
    with st.spinner("🤖 답변 생성 중..."):
        response = asyncio.run(get_qchat_response(st.session_state.quick_question, location))
        
        st.session_state.chat_history.append({
            "user": st.session_state.quick_question,
            "bot": response.get("answer", "답변을 생성할 수 없습니다."),
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "location": location
        })
    
    del st.session_state.quick_question
    st.rerun()

# 푸터
st.markdown("---")
st.markdown("🤖 **Q Chat 날씨 봇** | 자연어 질의응답으로 날씨 정보를 확인하세요!")