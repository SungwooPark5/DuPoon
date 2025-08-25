# 📈 두푼

> 두푼은 다양한 정적 자산 배분 전략을 웹에서 백테스팅하고 결과를 시각화하는 서비스입니다.

<br>

## ⭐ 주요 기능

- **데이터 수집**: 사용자가 지정한 종목을 바탕으로 yfinance 라이브러리를 이용해 자동으로 주가 데이터를 수집합니다.
- **정적 전략 백테스트**: 저장한 종목에 대한 정적인 자산 배분 전략을 지정하고, 백테스트를 실행합니다.
- **전략 저장 및 결과 조회**: 백테스트 결과를 시각화하고, 전략과 백테스트 결과를 저장할 수 있습니다.

<br>

## 🛠️ 기술 스택

### Frontend

![Chart.js]()

### Backend

![Django]()
![Redis]()
![Celery]()

### Database

![PostgreSQL]()
![Docker]()

<br>

## 🚀 설치 및 실행 방법

1. **레포지토리 클론**

   ```bash
   git clone https://github.com/SungwooPark5/DuPoon
   cd DuPoon
   ```

2. **환경 변수 설정**

   ```bash
   cp .env.example .env
   ```

3. **실행**
   ```bash
   docker compose -f docker-compose-asgi.yml up -d
   ```
4. **웹 서비스 접속**
   - 브라우저를 열고 `http://localhost:8000`으로 접속합니다.
