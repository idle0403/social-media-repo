# 🔗 Notion MCP 연동 완벽 가이드

## 📋 개요
이 가이드는 날씨 분석 시스템을 Notion과 MCP(Model Context Protocol)로 연동하는 방법을 단계별로 설명합니다.

## 🎯 목표
- Notion Integration 생성 및 설정
- MCP 서버 구성
- Claude Desktop과 연동
- 자동 날씨 분석 결과를 Notion에 저장

---

## 1️⃣ Notion Integration 생성

### Step 1: Notion 개발자 페이지 접속
```
1. https://www.notion.so/my-integrations 접속
2. "New integration" 버튼 클릭
```

### Step 2: Integration 기본 설정
```
Name: Weather Analysis MCP
Description: 날씨 분석 결과를 자동으로 Notion에 저장하는 봇
Associated workspace: [본인의 워크스페이스 선택]
```

### Step 3: 권한 설정
```
Capabilities:
✅ Read content
✅ Update content  
✅ Insert content

User Capabilities:
❌ No user information (보안상 비활성화)
```

### Step 4: Integration Token 복사
```
1. "Show" 버튼 클릭
2. secret_로 시작하는 토큰 전체 복사
3. 안전한 곳에 보관 (이후 환경변수로 사용)
```

---

## 2️⃣ Notion 데이터베이스 생성

### Step 1: 새 페이지 생성
```
1. Notion에서 "Add a page" 클릭
2. 페이지 제목: "🌤️ 날씨 분석 데이터베이스"
```

### Step 2: 데이터베이스 테이블 생성
```
1. 페이지 내에서 "/table" 입력
2. "Table - Inline" 선택
3. 다음 속성들 추가:

📝 속성 구성:
- 제목 (Title): 기본 제목 속성 (자동 생성됨)
- 지역 (Text): 날씨 조회 지역명
- 평균온도 (Number): 평균 기온 (°C)
- 평균습도 (Number): 평균 습도 (%)
- 분석일시 (Date): 분석 수행 일시
- 상태 (Select): 완료/진행중/오류 등
```

### Step 3: Integration 연결
```
1. 데이터베이스 페이지 우상단 "..." 메뉴 클릭
2. "Add connections" 선택
3. 앞서 생성한 "Weather Analysis MCP" Integration 선택
4. "Confirm" 클릭
```

### Step 4: 데이터베이스 ID 추출
```
1. 데이터베이스 페이지 URL 복사
2. URL 형태: https://notion.so/workspace/DATABASE_ID?v=VIEW_ID
3. DATABASE_ID 부분만 추출 (32자리 영숫자)
4. 예시: a1b2c3d4e5f6789012345678901234ab
```

---

## 3️⃣ 환경변수 설정

### Step 1: .env 파일 수정
```bash
# 기존 설정들...
OPENWEATHER_API_KEY=your_openweather_api_key
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_CHANNEL=#weather

# 🆕 Notion 설정 추가
NOTION_TOKEN=secret_your_integration_token_here
NOTION_DATABASE_ID=your_database_id_here
```

### Step 2: 환경변수 로드 테스트
```bash
cd /Users/paul/Documents/venv/social-media-repo
source ../bin/activate
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('NOTION_TOKEN:', os.getenv('NOTION_TOKEN')[:20] + '...' if os.getenv('NOTION_TOKEN') else 'NOT SET')
print('NOTION_DATABASE_ID:', os.getenv('NOTION_DATABASE_ID'))
"
```

---

## 4️⃣ MCP 서버 테스트

### Step 1: Notion 연동 테스트
```bash
cd /Users/paul/Documents/venv/social-media-repo
source ../bin/activate
python test_notion_integration.py
```

### Step 2: 예상 출력
```
🧪 Notion MCP 연동 테스트 시작
✅ 환경변수 설정 확인 완료
✅ MCP 서버 연결 성공
📋 사용 가능한 도구: 2개
   - create_weather_page: Notion에 날씨 분석 페이지 생성
   - get_weather_and_save: 날씨 데이터 수집 후 Notion에 저장

🌤️ 날씨 데이터 수집 및 Notion 저장 테스트
✅ Notion 페이지 생성 성공!
   📄 페이지 ID: a1b2c3d4-e5f6-7890-1234-567890123456
   🔗 URL: https://notion.so/...

📝 직접 페이지 생성 테스트
✅ 직접 페이지 생성 성공!
   📄 페이지 ID: b2c3d4e5-f6g7-8901-2345-678901234567

🎯 테스트 완료!
```

---

## 5️⃣ Claude Desktop MCP 설정

### Step 1: 설정 파일 위치 확인
```bash
# macOS
~/Library/Application Support/Claude/claude_desktop_config.json

# Windows
%APPDATA%/Claude/claude_desktop_config.json
```

### Step 2: 설정 파일 생성/수정
```json
{
  "mcpServers": {
    "notion-weather": {
      "command": "python",
      "args": ["/Users/paul/Documents/venv/social-media-repo/notion_weather_server.py"],
      "env": {
        "NOTION_TOKEN": "secret_your_integration_token_here",
        "NOTION_DATABASE_ID": "your_database_id_here",
        "OPENWEATHER_API_KEY": "your_openweather_api_key"
      }
    }
  }
}
```

### Step 3: Claude Desktop 재시작
```
1. Claude Desktop 완전 종료 (Cmd+Q)
2. 다시 실행
3. 새 대화 시작
4. MCP 서버 연결 상태 확인
```

---

## 6️⃣ 사용법 및 테스트

### Claude에서 사용하기
```
Claude에게 다음과 같이 요청:

"서울 날씨를 분석해서 Notion 데이터베이스에 저장해줘"
"부산과 대구의 날씨 정보를 수집해서 Notion에 정리해줘"
"오늘 날씨 분석 결과를 예쁘게 포맷해서 Notion 페이지로 만들어줘"
```

### 직접 테스트
```bash
# 전체 시스템 테스트
python test_notion_integration.py

# 독립형 앱 테스트
python standalone_app.py
```

---

## 7️⃣ 문제 해결

### ❌ "NOTION_TOKEN 환경변수가 설정되지 않았습니다"
```
해결방법:
1. .env 파일에 NOTION_TOKEN 확인
2. secret_로 시작하는지 확인
3. Integration 토큰 재생성
```

### ❌ "Notion API 오류: 401"
```
해결방법:
1. Integration 토큰 유효성 확인
2. Integration이 워크스페이스에 연결되었는지 확인
3. 토큰 권한 재설정
```

### ❌ "Notion API 오류: 404"
```
해결방법:
1. 데이터베이스 ID 정확성 확인
2. Integration이 해당 데이터베이스에 연결되었는지 확인
3. 데이터베이스 권한 재설정
```

### ❌ MCP 서버 연결 실패
```
해결방법:
1. Claude Desktop 설정 파일 경로 확인
2. JSON 문법 오류 검사
3. Python 경로 및 파일 경로 확인
4. Claude Desktop 재시작
```

---

## 8️⃣ 고급 활용

### 자동화 스케줄링
```bash
# crontab으로 매일 오전 8시 실행
0 8 * * * cd /Users/paul/Documents/venv/social-media-repo && python standalone_app.py
```

### 다중 지역 분석
```python
locations = ["서울", "부산", "대구", "인천", "광주"]
for location in locations:
    result = await create_weather_page(database_id, location, weather_data)
```

### 커스텀 템플릿
```python
# notion_weather_server.py에서 페이지 템플릿 수정
"children": [
    {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "rich_text": [{"text": {"content": f"🌤️ {location} 날씨 보고서"}}]
        }
    },
    # 추가 블록들...
]
```

---

## 9️⃣ 보안 고려사항

### API 키 관리
```
✅ DO:
- 환경변수 사용
- .env 파일을 .gitignore에 추가
- 정기적인 토큰 갱신

❌ DON'T:
- 코드에 직접 하드코딩
- 공개 저장소에 업로드
- 불필요한 권한 부여
```

### 접근 권한 최소화
```
Integration 권한:
✅ 필요한 권한만 부여
✅ 특정 페이지/데이터베이스만 연결
❌ 전체 워크스페이스 접근 권한
```

---

## 🎉 완료!

이제 Claude에서 자연어로 날씨 분석을 요청하면 자동으로 Notion 데이터베이스에 예쁘게 정리된 결과가 저장됩니다!

### 다음 단계
1. 웹 대시보드와 Notion 연동
2. Slack 알림과 함께 자동화
3. 더 많은 날씨 데이터 소스 추가
4. 시각화 차트를 Notion에 임베드