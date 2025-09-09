#!/bin/bash
echo "🌤️ 날씨 분석 대시보드 시작..."
source .env
export $(cat .env | xargs)
streamlit run web_dashboard.py --server.port 8501 --server.address 0.0.0.0