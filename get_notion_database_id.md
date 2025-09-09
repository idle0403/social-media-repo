# 📝 Notion 데이터베이스 ID 확인 방법

## 🔍 방법 1: URL에서 직접 추출

### Step 1: 데이터베이스 페이지 열기
1. Notion에서 데이터베이스가 있는 페이지로 이동
2. 브라우저 주소창의 URL 확인

### Step 2: URL 구조 이해
```
https://www.notion.so/workspace/DATABASE_ID?v=VIEW_ID&pvs=4
                              ^^^^^^^^^^^^^^^^
                              이 부분이 데이터베이스 ID
```

### Step 3: ID 추출
- URL에서 32자리 영숫자 문자열 찾기
- 하이픈(-)이 포함된 경우 제거
- 예시: `a1b2c3d4e5f6789012345678901234ab`

## 🔍 방법 2: 공유 링크 사용

### Step 1: 데이터베이스 공유
1. 데이터베이스 우상단 "Share" 버튼 클릭
2. "Copy link" 선택

### Step 2: 링크에서 ID 추출
```
https://notion.so/DATABASE_ID?v=VIEW_ID
                  ^^^^^^^^^^^^^^^^
                  이 부분이 데이터베이스 ID
```

## 🔍 방법 3: 개발자 도구 사용

### Step 1: 개발자 도구 열기
1. 데이터베이스 페이지에서 F12 키 누르기
2. Network 탭 선택

### Step 2: API 요청 확인
1. 페이지 새로고침
2. `query` 또는 `database` 관련 요청 찾기
3. 요청 URL에서 데이터베이스 ID 확인

## ✅ 실제 예시

### 예시 URL:
```
https://www.notion.so/myworkspace/12345678901234567890123456789012?v=abcdef...
```

### 추출된 ID:
```
12345678901234567890123456789012
```

## 🛠️ 자동 확인 스크립트

아래 명령어로 현재 설정된 ID 확인:
```bash
cd /Users/paul/Documents/venv/social-media-repo
source ../bin/activate
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
db_id = os.getenv('NOTION_DATABASE_ID')
print(f'현재 설정된 데이터베이스 ID: {db_id}')
print(f'ID 길이: {len(db_id) if db_id else 0}자리')
print('✅ 올바른 형식' if db_id and len(db_id) == 32 else '❌ 잘못된 형식')
"
```

## 📋 체크리스트

- [ ] URL에서 32자리 ID 추출 완료
- [ ] 하이픈(-) 제거 확인
- [ ] .env 파일에 NOTION_DATABASE_ID 설정
- [ ] Integration이 해당 데이터베이스에 연결됨
- [ ] 테스트 스크립트로 연결 확인

## 🚨 주의사항

1. **데이터베이스 vs 페이지**: 일반 페이지 ID가 아닌 데이터베이스 ID여야 함
2. **권한 확인**: Integration이 해당 데이터베이스에 연결되어 있어야 함
3. **형식 확인**: 정확히 32자리 영숫자여야 함