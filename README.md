# 날짜 파싱 MCP 서버

다양한 형식의 날짜 정보를 파싱하고 추출하는 MCP 서버입니다.

## 설치

```bash
pip install -r requirements.txt
```

## 실행

```bash
python server.py
```

## 테스트

```bash
python test_client.py
```

## 기능

### 1. parse_date
- 다양한 형식의 날짜 문자열을 표준 형식으로 변환
- 지원 형식: iso, korean, us, timestamp

### 2. extract_dates  
- 텍스트에서 모든 날짜 정보를 자동 추출
- 다양한 날짜 패턴 인식

## 사용 예시

```python
# 날짜 파싱
parse_date("2024년 3월 15일", format="iso")

# 날짜 추출
extract_dates("회의는 2024-03-15에 있습니다.")
```