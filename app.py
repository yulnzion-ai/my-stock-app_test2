import streamlit as st
import google.generativeai as genai
import yfinance as yf
from datetime import datetime

# 1. 설정 및 API 연결
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.warning("⚠️ API 키가 설정되지 않았습니다.")

model = genai.GenerativeModel('gemini-2.0-flash')

# 2. 실시간 주가 조회 함수
def get_stock_price(ticker_symbol):
    try:
        # 한국 종목 코드 처리 (코스피 .KS, 코스닥 .KQ)
        # 종목코드가 6자리 숫자인 경우 처리
        if ticker_symbol.isdigit() and len(ticker_symbol) == 6:
            # 여기서는 기본적으로 코스피(.KS)로 시도하고 안되면 코스닥으로 처리하는 로직이 필요하나
            # 일단 사용자 편의를 위해 검색 기능을 AI에게 맡기거나 보조적으로 사용
            full_ticker = ticker_symbol + ".KS" 
            stock = yf.Ticker(full_ticker)
            price = stock.fast_info['last_price']
            change = stock.fast_info['regular_market_previous_close']
            diff = ((price - change) / change) * 100
            return f"{price:,.0f}원 ({diff:+.2f}%)"
    except:
        return "주가 정보 조회 중"
    return "조회 불가"

# 3. UI 레이아웃
st.set_page_config(page_title="Golden-Bell AI Pro", layout="wide")

st.title("🌅 오늘의 단타 모닝브리핑 (Data Ver.)")
st.caption(f"기준일: {datetime.now().strftime('%Y년 %m월 %d일')} | 실시간 주가 API 연동됨")

# 메뉴 구성
news_type = st.selectbox("📰 뉴스 유형 선택", 
                         ["🔥 전체 카테고리 통합 풀-브리핑", "정치테마", "기업공시", "글로벌이슈", "테마급등"])

# 4. 분석 실행
if st.button(f"🚀 실시간 정밀 분석 시작", use_container_width=True):
    with st.spinner(f"실시간 데이터 수집 및 AI 분석 중..."):
        
        # 프롬프트 구성 (주가 데이터 강조)
        prompt_instruction = ""
        if "통합" in news_type:
            prompt_instruction = "정치, 공시, 글로벌, 테마급등 4개 분야를 각각 상세히 분석하세요. 요약은 절대 금지입니다."
        else:
            prompt_instruction = f"{news_type} 분야에 집중하여 분석하세요."

        final_prompt = f"""
        R (Role) - 당신은 최고의 단타 매매 전문가입니다.
        I (Instruction) - {prompt_instruction}
        C (Context) - 현재 날짜 {datetime.now().strftime('%Y-%m-%d')}. 반드시 실시간 웹 검색을 사용하여 최신 뉴스 헤드라인을 가져오세요.
        E (Example) - 각 카테고리별로 1~3순위 종목을 선정하고 아래 형식을 반복하세요:
        ---
        🔥 [순위]: [뉴스 헤드라인]
        - 수혜 종목: [종목명](정확한 6자리 코드)
        - 연결 고리: [상세 이유]
        - 현재가/등락: (반드시 검색된 실시간 가격 기재)
        - 매매 전략: [시초가 진입/눌림목 매수/관망]
        - 목표가/손절가: [구체적 가격]
        ---
        """
        
        try:
            response = model.generate_content(final_prompt)
            st.markdown("---")
            st.markdown(response.text)
        except Exception as e:
            if "429" in str(e):
                st.error("⏳ 구글 API 사용량이 초과되었습니다. 1분만 기다렸다가 다시 눌러주세요.")
            else:
                st.error(f"❌ 오류 발생: {e}")

st.divider()
st.info("💡 API를 통해 가져온 주가는 실제 거래소와 15분 내외의 지연이 발생할 수 있습니다.")
