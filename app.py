import streamlit as st
import google.generativeai as genai
import yfinance as yf
from datetime import datetime

# 1. 페이지 기본 설정
st.set_page_config(page_title="Golden-Bell AI Pro", layout="wide")

# 2. API 설정 및 모델 연결 (가장 안정적인 -exp 버전 사용)
@st.cache_resource
def setup_ai():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # 현재 가장 확실하게 작동하는 모델명인 'gemini-2.0-flash-exp' 사용
        return genai.GenerativeModel('gemini-2.0-flash-exp')
    except Exception as e:
        st.error(f"⚠️ API 설정 오류: {e}")
        return None

model = setup_ai()

# 3. 주가 정보 수집 함수 (yfinance 활용)
def get_stock_data(ticker_list):
    results = ""
    for ticker in ticker_list:
        try:
            # 한국 시장 종목코드 처리 (숫자 6자리인 경우)
            symbol = f"{ticker}.KS" if ticker.isdigit() else ticker
            stock = yf.Ticker(symbol)
            info = stock.fast_info
            price = info['last_price']
            prev_close = info['regular_market_previous_close']
            diff = ((price - prev_close) / prev_close) * 100
            results += f"\n- {ticker} 현재가: {price:,.0f}원 ({diff:+.2f}%)"
        except:
            continue
    return results

# 4. UI 레이아웃
st.title("🌅 오늘의 단타 모닝브리핑 (정밀 데이터 Ver.)")
st.caption(f"기준일: {datetime.now().strftime('%Y년 %m월 %d일')} | 최신 뉴스 및 실시간 주가 연동")

news_type = st.selectbox("📰 뉴스 유형 선택", 
                         ["🔥 전체 카테고리 통합 풀-브리핑", "정치테마", "기업공시",
