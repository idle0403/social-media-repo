# 🔗 Notion MCP 연동 설정 가이드

## 1. Notion Integration 생성

### 1-1. Notion 개발자 페이지 접속
- https://www.notion.so/my-integrations 방문
- "New integration" 클릭

### 1-2. Integration 설정
```
Name: Weather Analysis Bot
Associated workspace: [본인의 워크스페이스 선택]
Capabilities: 
  ✅ Read content
  ✅ Update content  
  ✅ Insert content
```

### 1-3. Integration Token 복사
- "Show" 버튼 클릭하여 토큰 복사
- `secret_` 으로 시작하는 토큰

## 2. Notion 데이터베이스 생성

### 2-1. 새 페이지 생성
- Notion에서 새 페이지 생성
- 제목: "날씨 분석 데이터베이스"

### 2-2. 데이터베이스 테이블 생성
```
속성 설정:
- 제목 (Title): 기본 제목 속성
- 지역 (Text): 날씨 조회 지역
- 평균온도 (Number): 평균 기온
- 평균습도 (Number): 평균 습도  
- 분석일시 (Date): 분석 수행 일시
```

### 2-3. Integration 연결
- 데이터베이스 페이지 우상단 "..." 메뉴 클릭
- "Add connections" → 생성한 Integration 선택
- "Confirm" 클릭

### 2-4. 데이터베이스 ID 복사
- 데이터베이스 URL에서 ID 추출
- URL 형태: `https://notion.so/[workspace]/[DATABASE_ID]?v=...`
- DATABASE_ID 부분 복사 (32자리 문자열)

## 3. 환경변수 설정

### 3-1. .env 파일 수정
```bash
# Notion 설정
NOTION_TOKEN=secret_your_integration_token_here
NOTION_DATABASE_ID=your_database_id_here

# 기존 설정들...
OPENWEATHER_API_KEY=your_openweather_api_key
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_CHANNEL=#weather
```

## 4. MCP 클라이언트 설정

### 4-1. Claude Desktop 설정 (macOS)
```bash
# 설정 파일 위치
~/Library/Application Support/Claude/claude_desktop_config.json
```

### 4-2. 설정 파일 내용
```json
{
  "mcpServers": {
    "notion-weather": {
      "command": "python",
      "args": ["/Users/paul/Documents/venv/social-media-repo/notion_weather_server.py"],
      "env": {
        "NOTION_TOKEN": "secret_your_notion_integration_token",
        "OPENWEATHER_API_KEY": "your_openweather_api_key"
      }
    }
  }
}
```

### 4-3. Claude Desktop 재시작
- Claude Desktop 완전 종료
- 다시 실행하여 MCP 서버 연결 확인

## 5. 테스트 및 사용법

### 5-1. Claude에서 테스트
```
Claude에게 다음과 같이 요청:
"서울 날씨를 분석해서 Notion 데이터베이스에 저장해줘"
```

### 5-2. 직접 테스트
```bash
python test_notion_integration.py
```

## 6. 문제 해결

### Integration Token 오류
- Notion Integration 페이지에서 토큰 재생성
- 환경변수 정확성 확인

### 데이터베이스 접근 오류  
- Integration이 데이터베이스에 연결되었는지 확인
- 데이터베이스 ID 정확성 검증

### MCP 연결 오류
- Claude Desktop 설정 파일 경로 확인
- JSON 문법 오류 검사
- Claude Desktop 재시작

## 7. 고급 활용

### 자동화 스케줄링
```bash
# crontab으로 매일 오전 8시 실행
0 8 * * * cd /Users/paul/Documents/venv/social-media-repo && python main_app.py
```

### 다중 지역 분석
```python
locations = ["서울", "부산", "대구", "인천"]
for location in locations:
    await create_weather_page(database_id, location, weather_data)
```