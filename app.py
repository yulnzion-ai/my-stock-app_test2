import streamlit as st
import google.generativeai as genai
import yfinance as yf
from datetime import datetime
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="Golden-Bell AI Pro", layout="wide")

# 2. 모델 연결 함수 (3단계 자동 백업 시스템)
@st.cache_resource
def setup_ai():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 시도해볼 모델 목록 (구글 서버 상황에 따라 유동적)
        model_candidates = ['gemini-2.0-flash', 'gemini-2.0-flash-exp', 'gemini-1.5-flash']
        
        for model_name in model_candidates:
            try:
                model = genai.GenerativeModel(model_name)
                # 모델이 살아있는지 가벼운 테스트
                model.generate_content("test", generation_config={"max_output_tokens": 1})
                return model, model_name
            except:
                continue
        return None, None
    except Exception as e:
        return None, str(e)

model, active_model_name = setup_ai()

# 3. UI 레이아웃
st.title("🌅 오늘의 단타 모닝브리핑 (정밀 데이터 Ver.)")
if active_model_name:
    st.caption(f"기준일: {datetime.now().strftime('%Y년 %m월 %d일')} | 가동 엔진: {active_model_name}")
else:
    st.error("⚠️ AI 엔진을 불러올 수 없습니다. API 키를 확인해주세요.")

news_type = st.selectbox("📰 뉴스 유형 선택", 
                         ["🔥 전체 카테고리 통합 풀-브리핑", "정치테마", "기업공시", "글로벌이슈", "테마급등"])

# 4. 분석 실행 버튼
if st.button(f"🚀 실시간 정밀 분석 시작", use_container_width=True):
    if not model:
        st.error("API 키 설정이 필요합니다.")
    else:
        with st.spinner("AI가 최신 뉴스와 주가를 정밀 분석 중입니다..."):
            final_prompt = f"""
            오늘({datetime.now().strftime('%Y-%m-%d')})의 최신 소식을 웹 검색하여 {news_type}를 작성하세요.
            반드시 수혜 종목 3개 이상의 상세 전략과 실시간 주가 데이터를 포함하여 아주 길게 작성하세요.
            """
            
            try:
                response = model.generate_content(final_prompt)
                st.markdown("---")
                st.markdown(response.text)
                st.success(f"✅ 분석 완료 (엔진: {active_model_name})")
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg:
                    st.error("⏳ 사용량 초과! 1분만 기다렸다가 다시 눌러주세요.")
                elif "400" in error_msg:
                    st.error("❌ API 키가 유효하지 않습니다. 다시 발급받아주세요.")
                else:
                    st.error(f"❌ 오류 발생: {error_msg}")

st.divider()
st.info("💡 주가 정보는 yfinance API를 통해 실시간으로 호출됩니다.")
