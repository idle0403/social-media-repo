# 🌤️ 날씨 분석 시스템

MCP(Model Context Protocol)를 활용한 종합 날씨 분석 및 자동화 시스템

## 🏗️ 시스템 아키텍처

```mermaid
graph TB
    subgraph "🌐 External APIs"
        OW[OpenWeatherMap API]
        SLACK[Slack API]
        NOTION[Notion API]
    end
    
    subgraph "🤖 MCP Servers"
        WS[Weather MCP Server]
        NS[Notion MCP Server]
    end
    
    subgraph "💻 Applications"
        WD[Web Dashboard<br/>Streamlit]
        SA[Standalone App]
        MA[Main App]
    end
    
    subgraph "🤖 AI Integration"
        QCHAT[Q Chat Interface]
        QS[Q Chat Server]
    end
    
    subgraph "📊 Data Flow"
        WS --> |날씨 데이터| WD
        WS --> |분석 결과| SA
        NS --> |Notion 저장| CLAUDE
        WD --> |시각화| USER[👤 사용자]
        SA --> |Slack 전송| SLACK
        QCHAT --> |질의응답| QS
        QS --> |MCP 연동| WS
        QS --> |MCP 연동| NS
    end
    
    OW --> WS
    SLACK --> SA
    NOTION --> NS
    
    style WS fill:#e1f5fe
    style NS fill:#f3e5f5
    style WD fill:#e8f5e8
    style QCHAT fill:#fff3e0
    style QS fill:#e3f2fd
```

## 🔄 Q Chat 워크플로우

```mermaid
sequenceDiagram
    participant U as 👤 사용자
    participant Q as 🤖 Q Chat
    participant M as 🔧 MCP Server
    participant W as 🌐 Weather API
    participant N as 📝 Notion
    participant S as 💬 Slack
    
    U->>Q: "서울 날씨 어때?"
    Q->>M: 질의 분석 요청
    M->>W: 날씨 데이터 수집
    W-->>M: 실시간 날씨 정보
    M->>M: 질문 유형 분석
    M-->>Q: 맞춤형 답변 생성
    Q-->>U: "서울 현재 18°C, 맑음입니다"
    
    opt 추가 요청
        U->>Q: "이 정보 Notion에 저장해줘"
        Q->>M: 저장 요청
        M->>N: 구조화된 데이터 저장
        N-->>M: 저장 완료
        M-->>Q: 저장 결과
        Q-->>U: "✅ Notion에 저장했습니다"
    end
    
    opt 공유 요청
        U->>Q: "팀에게 공유해줘"
        Q->>M: 공유 요청
        M->>S: 포맷된 메시지 전송
        S-->>U: 📱 팀 알림
    end
```

## ✨ 주요 기능

### 🔧 핵심 컴포넌트
1. **🌡️ 날씨 데이터 수집**: OpenWeatherMap API 연동
2. **📊 실시간 분석**: 온도, 습도, 트렌드 자동 계산
3. **📝 Notion 자동 저장**: MCP를 통한 실시간 문서화
4. **📈 웹 대시보드**: Streamlit 기반 인터랙티브 시각화
5. **💬 Slack 연동**: 예쁜 포맷으로 결과 공유
6. **🤖 AI 통합**: Claude Desktop MCP 지원

### 🎯 사용 시나리오
- **개인**: 일상 날씨 모니터링 및 기록
- **팀**: 날씨 기반 업무 계획 수립
- **연구**: 날씨 데이터 수집 및 분석
- **자동화**: 정기적인 날씨 보고서 생성

## 🚀 빠른 시작

### 1️⃣ 환경 설정
```bash
# 가상환경 활성화
source /Users/paul/Documents/venv/bin/activate

# 패키지 설치
cd social-media-repo
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일에서 API 키들 설정
```

### 2️⃣ 실행 방법

#### 🖥️ 웹 대시보드 (추천)
```bash
streamlit run web_dashboard.py
# 브라우저에서 http://localhost:8501 접속
```

#### 🤖 Claude Desktop MCP 연동
```bash
# 1. Claude Desktop 설정 파일 수정
~/Library/Application Support/Claude/claude_desktop_config.json

# 2. MCP 서버 설정 추가 (NOTION_MCP_SETUP.md 참고)
# 3. Claude Desktop 재시작
# 4. Claude에서 "서울 날씨 분석해서 Notion에 저장해줘" 요청
```

#### 📱 독립형 앱
```bash
python standalone_app.py
```

## 📁 프로젝트 구조

```
social-media-repo/
├── 🤖 MCP Servers
│   ├── weather_mcp_server.py      # 날씨 데이터 수집 및 분석
│   ├── notion_weather_server.py   # Notion API 연동
│   └── simple_weather_server.py   # 테스트용 간단 서버
│
├── 💻 Applications  
│   ├── web_dashboard.py           # Streamlit 웹 대시보드
│   ├── standalone_app.py          # 독립형 실행 앱
│   └── main_app.py               # 통합 메인 앱
│
├── 🔧 Utilities
│   ├── slack_bot.py              # Slack 메시지 전송
│   └── test_*.py                 # 각종 테스트 스크립트
│
├── ⚙️ Configuration
│   ├── mcp_config.json           # MCP 서버 설정
│   ├── .env                      # 환경변수
│   └── requirements.txt          # 패키지 의존성
│
└── 📚 Documentation
    ├── README.md                 # 이 파일
    ├── NOTION_MCP_SETUP.md       # Notion 연동 가이드
    └── setup_notion_integration.md
```

## 🔧 API 설정 가이드

### 🌤️ OpenWeatherMap API
```bash
# 1. https://openweathermap.org/api 접속
# 2. 무료 계정 생성 후 API 키 발급
# 3. .env 파일에 추가
OPENWEATHER_API_KEY=your_api_key_here
```

### 💬 Slack Bot 설정
```bash
# 1. https://api.slack.com/apps 에서 새 앱 생성
# 2. Bot Token Scopes 설정: chat:write, channels:read
# 3. 워크스페이스에 설치 후 토큰 복사
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_CHANNEL=#weather
```

### 📝 Notion Integration
```bash
# 1. https://www.notion.so/my-integrations 에서 Integration 생성
# 2. 데이터베이스 생성 및 Integration 연결
# 3. 토큰과 데이터베이스 ID 설정
NOTION_TOKEN=secret_your_integration_token
NOTION_DATABASE_ID=your_database_id
```

## 🎯 사용법

### 🖥️ 웹 대시보드 사용법
```mermaid
flowchart LR
    A[🌐 브라우저 접속<br/>localhost:8501] --> B[📍 지역 선택<br/>서울, 부산, 대구...]
    B --> C[📅 예보 일수 설정<br/>1-7일]
    C --> D[🚀 분석 시작 버튼]
    D --> E[📊 결과 확인<br/>차트 & 메트릭]
    E --> F[📤 Slack 전송]
    E --> G[📝 Notion 저장]
```

### 🤖 Claude Desktop 사용법
```
💬 Claude에게 자연어로 요청:

"서울 날씨를 분석해서 Notion에 저장해줘"
"부산과 대구의 날씨 비교 분석 결과를 정리해줘"
"오늘 날씨 데이터를 예쁘게 포맷해서 Slack으로 보내줘"
"이번 주 날씨 트렌드를 분석해서 보고서 만들어줘"
```

### 💻 프로그래밍 방식
```python
# 독립형 앱 사용
from standalone_app import StandaloneWeatherApp

app = StandaloneWeatherApp()
result = await app.run_analysis("서울")
print(result['analysis_data']['summary'])
```

## 🧪 테스트 및 검증

### 🔍 전체 시스템 테스트
```bash
# 독립형 앱 테스트
python standalone_app.py

# Notion 연동 테스트  
python test_notion_integration.py

# 웹 대시보드 테스트
streamlit run web_dashboard.py
```

### ✅ 검증 체크리스트
- [ ] 환경변수 설정 완료
- [ ] 패키지 설치 완료
- [ ] 웹 대시보드 정상 실행
- [ ] Notion Integration 연결
- [ ] Claude Desktop MCP 설정
- [ ] Slack Bot 권한 설정

## 🎨 UI/UX 특징

### 📱 웹 대시보드
- **반응형 디자인**: 모바일/태블릿/데스크톱 최적화
- **실시간 차트**: Plotly 기반 인터랙티브 시각화
- **메트릭 카드**: 주요 지표를 카드 형태로 직관적 표시
- **그라데이션 테마**: 모던하고 깔끔한 색상 디자인
- **이모지 아이콘**: 기능별 직관적 아이콘 활용

### 🤖 Claude 연동
- **자연어 인터페이스**: 복잡한 명령어 없이 대화형 요청
- **실시간 피드백**: 작업 진행 상황 실시간 업데이트
- **컨텍스트 유지**: 이전 대화 내용 기반 연속 작업

### 📝 Notion 출력
- **구조화된 페이지**: 제목, 메타데이터, 본문 자동 구성
- **시각적 블록**: 이모지와 서식을 활용한 가독성 향상
- **데이터베이스 연동**: 검색, 필터링, 정렬 가능한 구조화된 데이터

## ✅ 검증 완료 사항

### 🔧 기술적 검증
- ✅ MCP 프로토콜 정상 동작
- ✅ 날씨 API 연동 및 데이터 파싱
- ✅ 실시간 데이터 분석 로직
- ✅ Streamlit 웹 대시보드 시각화
- ✅ Notion API 연동 및 페이지 생성
- ✅ Slack Bot 메시지 전송
- ✅ Claude Desktop MCP 연동

### 🎯 기능적 검증
- ✅ 다중 지역 날씨 분석
- ✅ 트렌드 분석 및 통계 계산
- ✅ 자동 문서화 및 보고서 생성
- ✅ 실시간 알림 및 공유
- ✅ 예외 처리 및 오류 복구
- ✅ 사용자 친화적 인터페이스

## 🚨 문제 해결 가이드

### 🔧 일반적인 문제

#### Q Chat 서버 연결 실패
```bash
# 해결방법
1. Q Chat 서버 실행 상태 확인
2. MCP 서버 포트 충돌 검사
3. Python 경로 및 파일 경로 확인
4. 서버 재시작
```

#### API 인증 오류
```bash
# OpenWeatherMap
- API 키 유효성 확인
- 요청 한도 초과 여부 점검

# Notion
- Integration 토큰 확인 (secret_로 시작)
- 데이터베이스 연결 권한 확인

# Slack
- Bot Token 권한 (chat:write) 확인
- 채널 접근 권한 확인
```

#### 웹 대시보드 오류
```bash
# 포트 충돌
streamlit run web_dashboard.py --server.port 8502

# 패키지 오류
pip install -r requirements.txt --force-reinstall
```

### 🆘 고급 디버깅
```bash
# 로그 확인
python -c "import logging; logging.basicConfig(level=logging.DEBUG)"

# 환경변수 확인
env | grep -E '(NOTION|SLACK|OPENWEATHER)'

# Q Chat 서버 직접 테스트
python qchat_weather_server.py

# Q Chat 인터페이스 테스트
python test_qchat.py
```

## 🚀 다음 단계

### 🔮 향후 개발 계획
- [ ] **실시간 알림**: 날씨 변화 시 자동 알림
- [ ] **머신러닝**: 날씨 예측 모델 통합
- [ ] **다중 API**: 여러 날씨 서비스 통합
- [ ] **모바일 앱**: React Native 기반 앱 개발
- [ ] **대시보드 확장**: 더 많은 시각화 옵션

### 🤝 기여하기
```bash
# 1. Fork this repository
# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Commit changes
git commit -m 'Add amazing feature'

# 4. Push to branch
git push origin feature/amazing-feature

# 5. Open Pull Request
```

---

**🌤️ 이제 AI와 대화하듯 날씨를 분석하고 자동으로 문서화할 수 있습니다!**

*Made with ❤️ using MCP, Claude, Notion, and Streamlit*