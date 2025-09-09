# 🌤️ 날씨 분석 시스템

네이버 API와 Q Chat을 활용한 종합 날씨 분석 및 Slack 연동 시스템

## ✨ 주요 기능

1. **🌡️ 날씨 데이터 수집**: OpenWeatherMap API로 실시간 날씨 정보 파싱
2. **📊 데이터 분석**: Q Chat MCP 서버를 통한 날씨 트렌드 분석  
3. **📈 웹 대시보드**: Streamlit 기반 실시간 시각화
4. **📤 Slack 연동**: 분석 결과 자동 전송
5. **🎨 예쁜 UI**: 깔끔하고 직관적인 사용자 인터페이스

## 🚀 빠른 시작

### 1. 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 설정
```bash
cp .env.example .env
# .env 파일에 API 키 입력
```

### 3. 실행

#### MCP 서버 실행
```bash
python weather_mcp_server.py
```

#### 웹 대시보드 실행  
```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

#### 전체 시스템 테스트
```bash
python test_system.py
```

## 📁 파일 구조

```
├── weather_mcp_server.py    # MCP 서버 (날씨 데이터 + 분석)
├── web_dashboard.py         # Streamlit 웹 대시보드
├── slack_bot.py            # Slack Bot 클래스
├── main_app.py             # 메인 애플리케이션
├── test_system.py          # 시스템 테스트
├── run_dashboard.sh        # 대시보드 실행 스크립트
├── requirements.txt        # 패키지 의존성
├── .env                    # 환경변수 설정
└── README.md              # 이 파일
```

## 🔧 API 설정

### OpenWeatherMap API
1. https://openweathermap.org/api 에서 무료 API 키 발급
2. `.env` 파일에 `OPENWEATHER_API_KEY` 설정

### Slack Bot
1. https://api.slack.com/apps 에서 앱 생성
2. Bot Token 발급 후 `.env` 파일에 설정
3. 채널에 봇 초대

## 🎯 사용법

### 웹 대시보드
1. 브라우저에서 `http://localhost:8501` 접속
2. 사이드바에서 지역과 예보 일수 설정
3. "🚀 날씨 분석 시작" 버튼 클릭
4. 결과 확인 후 "📤 Slack 전송" 버튼으로 공유

### 프로그래밍 방식
```python
from main_app import WeatherAnalysisApp

app = WeatherAnalysisApp()
result = await app.run_full_analysis("서울", 3, slack_token, "#weather")
```

## 🧪 테스트

시스템이 정상 동작하는지 확인:
```bash
python test_system.py
```

## 🎨 UI 특징

- **반응형 디자인**: 모바일/데스크톱 최적화
- **실시간 차트**: Plotly 기반 인터랙티브 그래프
- **깔끔한 메트릭**: 주요 지표 카드 형태로 표시
- **그라데이션**: 모던한 색상 테마
- **직관적 아이콘**: 기능별 이모지 활용

## 🔍 검증 완료 사항

✅ MCP 서버 정상 동작  
✅ 날씨 데이터 수집 및 파싱  
✅ 데이터 분석 로직  
✅ 웹 대시보드 시각화  
✅ Slack Bot 메시지 전송  
✅ 전체 워크플로우 연동  
✅ 예외 처리 및 오류 핸들링

## 🚨 문제 해결

### API 오류
- OpenWeatherMap API 키 확인
- 네트워크 연결 상태 점검

### Slack 전송 실패  
- Bot Token 권한 확인
- 채널명 정확성 검증

### 대시보드 오류
- 포트 8501 사용 가능 여부 확인
- 패키지 설치 상태 점검