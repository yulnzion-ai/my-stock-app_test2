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
                         ["🔥 전체 카테고리 통합 풀-브리핑", "정치테마", "기업공시", "글로벌이슈", "테마급등"])

# 5. 분석 실행 버튼
if st.button(f"🚀 실시간 정밀 분석 시작", use_container_width=True):
    if not model:
        st.error("API 키가 올바르지 않습니다. Secrets 설정을 확인해주세요.")
    else:
        with st.spinner("AI가 최신 뉴스와 실시간 주가를 분석 중입니다. 잠시만 기다려주세요..."):
            
            # 프롬프트: '실시간 검색'과 '상세 브리핑' 강조
            final_prompt = f"""
            당신은 최고의 주식 분석가입니다. 
            오늘({datetime.now().strftime('%Y-%m-%d')})의 최신 소식을 웹 검색하여 {news_type}를 작성하세요.
            
            [필수 포함 내용]
            1. 관련 뉴스 헤드라인과 핵심 요약
            2. 가장 유망한 수혜 종목 3개 이상 (종목코드 6자리 포함)
            3. 각 종목별 구체적인 시나리오와 매매 전략
            4. 분석한 종목의 실제 주가와 등락률을 '실시간 데이터' 기반으로 언급할 것
            
            절대 요약하지 말고, 사용자가 바로 매매에 참고할 수 있도록 아주 상세하고 길게 작성하세요.
            """
            
            try:
                # AI 분석 결과 출력
                response = model.generate_content(final_prompt)
                st.markdown("---")
                st.markdown(response.text)
                st.success("✅ 분석이 완료되었습니다!")
                
            except Exception as e:
                if "429" in str(e):
                    st.error("⏳ 구글 서버 사용량 초과입니다. 약 1~2분 뒤에 다시 시도해주세요.")
                    st.info("팁: 계속 발생한다면 다른 구글 계정으로 API 키를 발급받아 교체하는 것이 가장 좋습니다.")
                elif "404" in str(e):
                    st.error("❌ 모델 연결 오류: 모델명을 'gemini-2.0-flash-exp'로 확인했으나 구글 서버에서 거부되었습니다.")
                else:
                    st.error(f"❌ 오류 발생: {e}")

st.divider()
st.info("💡 주가 정보는 yfinance API를 통해 실시간으로 호출됩니다. (일부 종목 15분 지연 가능)")
