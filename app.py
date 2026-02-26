import streamlit as st
import google.generativeai as genai
import yfinance as yf
from datetime import datetime

# 1. 설정 및 API 연결 (캐싱 처리로 중복 호출 방지)
@st.cache_resource
def setup_ai(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash')

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    model = setup_ai(api_key)
except:
    st.warning("⚠️ API 키를 확인해주세요.")

# 2. UI 레이아웃
st.set_page_config(page_title="Golden-Bell AI Pro", layout="wide")

st.title("🌅 오늘의 단타 모닝브리핑")
st.caption(f"기준일: {datetime.now().strftime('%Y년 %m월 %d일')} | 데이터 모드")

# 뉴스 유형 선택
news_type = st.selectbox("📰 뉴스 유형 선택", 
                         ["🔥 전체 카테고리 통합 풀-브리핑", "정치테마", "기업공시", "글로벌이슈", "테마급등"])

# 3. 분석 버튼 (이 버튼을 누를 때만 할당량을 사용합니다)
if st.button(f"🚀 실시간 정밀 분석 시작", use_container_width=True):
    # 버튼을 누른 순간에만 실행되도록 세션 상태 저장
    st.session_state.run_analysis = True
    
    with st.spinner(f"AI가 데이터를 수집 중입니다. 잠시만 기다려주세요..."):
        final_prompt = f"""
        당신은 전문 트레이더입니다. {news_type}에 대해 웹 검색을 통해 
        오늘자 최신 뉴스와 관련주, 매매 전략을 상세히 보고하세요. 
        절대 요약하지 말고 전체 내용을 풍부하게 작성하세요.
        """
        try:
            response = model.generate_content(final_prompt)
            st.markdown("---")
            st.markdown(response.text)
        except Exception as e:
            if "429" in str(e):
                st.error("⏳ 사용량 초과! 딱 1분만 쉬었다가 다시 눌러주세요.")
            else:
                st.error(f"❌ 에러 발생: {e}")
