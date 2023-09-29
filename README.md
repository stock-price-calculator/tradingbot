<h1 align="center">
  <a href="https://github.com/rong5026/animal_user" title="AwesomeCV Documentation">
    <img alt="AwesomeCV" src="https://github.com/Haehnchen/crypto-trading-bot/assets/77156858/4abd434e-32d8-4856-ad4e-c4a74a803288" width="100%" height="100%" />
  </a>
  <br />
 Kiwoom Auto Trading
</h1>
<p align="center">
  Kiwoom API를 이용한 주식 자동매매 프로그램 입니다.
</p>
<div align="center">
  <img src="https://img.shields.io/badge/React-61DAFB?style=flat&logo=React&logoColor=white"/>

<img src="https://img.shields.io/badge/Electron-47848F?style=flat&logo=Electron&logoColor=white"/>

  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/Flask-000000?style=flat&logo=Flask&logoColor=white"/>

<img src="https://img.shields.io/badge/PyQt5-41CD52?style=flat&logo=Qt&logoColor=white"/>

<img src="https://img.shields.io/badge/Anaconda-44A833?style=flat&logo=anaconda&logoColor=white"/>
  
</div>
<br />

## 📌 개요
- 프로젝트 이름 : 웹 크롤링과 자연어분석을 통한 주식 자동매매 프로그램
- 개발 배경 : 코인뿐만 아니라 주식까지도 자동매매를 제작해보고 싶어 기획하게 되었습니다. 
<br>현재 Mac 환경을 지원해 주는 HTS가 없기에 윈도우에 서버를 두고 맥북으로도 주식매매를 이용할 수 있도록 만들고자 하였습니다.
- 개발 언어 : Python
- 프론트 : React, Electron
- 백엔드 : Flask, 키움증권 API
    
## 🖥️ 프로젝트 소개
- 키움증권 API를 이용하여 주식 자동매매 프로그램을 제작하였습니다.
- 과거 차트 데이터를 통해서 사용자가 직접 백테스팅을 할 수 있는 기능까지 추가하여 자동매매를 실행할 수 있습니다.
- 기존 증권사들의 HTS는 Window 환경에서만 사용가능하고, MAC 사용자들은 사용할 수 없다는 문제점을 해결하기 위해 데스크톱 앱으로 제작하였습니다. 
- 적정주가 계산기 기능을 추가하여 사용자에게 제공합니다.
- 키움증권 모의투자 계좌를 통해 실제매매 진행

## 🕰️ 개발 기간
- 2023.03.27 - 2023.06.10

## 👬 팀 소개
- 홍영환 - <a href="https://github.com/stock-price-calculator/tradingbot">백엔드 (Flask)</a>, 키움증권 API , 백테스팅 , 자동매매 <br>
- 조준희 - <a href="https://github.com/stock-price-calculator/front/tree/junhee">프론트 (React Electron)</a>
- 김현욱 - 적정주가 계산기

## ⚙️ 프로젝트 주요 기능

### 1. 주식 자동매매
- 키움증권 로그인
- 주식 사용자 매도, 매수 (시장가, 지정가)
- 볼린저밴드 값, 익절% 손절%에 따른 자동매매
- 실시간 주식 정보
- 매매기록
- 자동매매 체결 내역

### 2. 백테스팅
- 볼린저밴드를 사용한 백테스팅
- 백테스팅 결과 내역

### 3. 기타기능 
- 주식관련 뉴스
- 증권사 차트 및 부가기능
- 주식 상세정보
- 주식 포트폴리오

### 4. 적정주가 계산기


## 📌 주식 자동매매 페이지

|<img src="https://github.com/stock-price-calculator/tradingbot/assets/77156858/b754f2bc-ebe4-4361-8a69-03c795336574" height="100%" width="700">|<img src="https://github.com/stock-price-calculator/tradingbot/assets/77156858/c5a0d662-c1bb-4e0a-b92e-96215a649267"  height="100%" width="700"> |
|:---:|:---:|
|주문|자동매매|



|<img src="https://github.com/stock-price-calculator/tradingbot/assets/77156858/20b8fb06-8782-4d22-a60d-61ff42a7fb6e" height="100%" width="700" >|<img src="https://github.com/stock-price-calculator/tradingbot/assets/77156858/b8840d03-affb-4055-b6d8-b7b437911caf" height="100%" width="700"> |
|:---:|:---:|
|백테스팅|매매기록 |

|<img src="https://github.com/stock-price-calculator/tradingbot/assets/77156858/2ae2d981-f623-4f4e-8691-15a13c3759cc" height="100%" width="700" >|<img src="https://github.com/stock-price-calculator/tradingbot/assets/77156858/76285f8b-e983-43cb-bd31-bd1d16671ab8" height="100%" width="700"> |<img src="https://github.com/stock-price-calculator/tradingbot/assets/77156858/819f6e25-5133-40d6-916b-46c68388404c" height="100%" width="700" >|
|:---:|:---:|:---:|
|주식 상세정보|주식 차트|주식 뉴스|

 
##  💾 시스템 설계도
<img src="https://github.com/stock-price-calculator/tradingbot/assets/77156858/68209c4f-63fc-4cd3-bf06-ee0bfa0d56bf" height="100%" width="100%" >


## ⚙️ 개발 환경

 국내 증권사 API 사용하려면 32비트 버전 파이썬 인터프리터 사용
- <a href="https://velog.io/@rong5026/%EC%A3%BC%EC%8B%9D%EC%9E%90%EB%8F%99%EB%A7%A4%EB%A7%A4-%ED%82%A4%EC%9B%80%EC%A6%9D%EA%B6%8C-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EA%B0%9C%EB%B0%9C-%ED%99%98%EA%B2%BD%EC%84%A4%EC%A0%95">32비트 환경설정 방법 </a>
<br>


Anaconda Python 버전
- `Python 3.9`

pip 설치목록
- `pandas`
- `pyqt5`
- `matplotlib`
- `pywin32`
- `CORS`
- `Thread`
- `time`
- `numpy`
- `sys`

## 🛠️ 어려웠던점
- 32비트 버전 가상환경 설치
- 키움 api 동기방식 때문에 값 받아오기 어려움.
- 키움 api를 통해 값을 요청할 때 요청을 하면 비동기로 바로 값을 리턴해주는게 아니라 따로 이벤트 요청함수를 연결시켜야 값을 받아옴. 그래서 이벤트 요청을 연속적으로 하면 받아오는 값이 섞이는 경우가 발생함 → flag변수를 통해서 해결 
- Flask와 FastApi에서 Flask를 선택한 이유도 위와같은 이유로 충돌발생 (flaks는 동기방식 기반)
- PyQt5는 비동기 방식으로 무한루프를 돌며 실행됨. 하지만 Kiwoom은 동기방식, 그리고 Flask에서 요청이 들어오고 처리되는 것도 동기방식이라 충돌을 해결하기 어려웠음.
- 자동매매를 돌리려면 쓰레드 한개를 사용해야함. 처음에 메인쓰레드에서 값 요청과 자동매매를 함께 돌리려고 했는데 동기방식이라 쓰레드를 따로 한개 만듬. 그래서 총 메인 Flask에서 한개, 키움증권 1개, 자동매매 1개를 사용.
- 주식시장이 활성화되는 시간 9시 ~ 3시30분 까지만 테스트를 할 수 있다는 불편함.

</hr>

