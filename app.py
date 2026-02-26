import streamlit as st
import google.generativeai as genai
import yfinance as yf
from datetime import datetime

# 1. 페이지 기본 설정
st.set_page_config(page_title="Golden-Bell AI Pro", layout="wide")

# 2. 모델 연결 함수 (구글 서버 상황에 맞춰 3개 모델 자동 시도)
def load_ai_model():
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            return None, "Secrets에 GEMINI_API_KEY가 설정되지 않았습니다."
        
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 시도할 모델 리스트 (최신순)
        # 2.0 시리즈가 거부될 경우를 대비해 가장 안정적인 1.5 버전을 마지막에 배치
        models_to_try = ['gemini-2.0-flash', 'gemini-2.0-flash-exp', 'gemini-1.5-flash']
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                # 모델이 정상인지 아주 짧은 테스트 호출
                model.generate_content("hi", generation_config={"max_output_tokens": 1})
                return model, model_name
            except:
                continue
                
        return None, "모든 Gemini 모델 명칭이 거부되었습니다. API 키 활성화 상태를 확인해주세요."
    except Exception as e:
        return None, str(e)

# 모델 로드 (캐싱 없이 매번 시도하여 상태 반영)
model, status = load_ai_model()

# 3. UI 레이아웃
st.title("🌅 오늘의 단타 모닝브리핑 (최종 안정화 Ver.)")

if model:
    st.success(f"✅ AI 엔진 가동 중: {status}")
else:
    st.error(f"❌ AI 엔진 연결 실패: {status}")
    st.info("💡 해결 방법: 1. API Studio에서 새 키 발급 -> 2. Streamlit Secrets 업데이트 -> 3. 5분 뒤 새로고침")

news_type = st.selectbox("📰 뉴스 유형 선택", 
                         ["🔥 전체 카테고리 통합 풀-브리핑", "정치테마", "기업공시", "글로벌이슈", "테마급등"])

# 4. 분석 실행
if st.button(f"🚀 실시간 정밀 분석 시작", use_container_width=True):
    if not model:
        st.error("엔진이 연결되지 않아 분석을 시작할 수 없습니다.")
    else:
        with st.spinner("최신 데이터를 가져오는 중입니다..."):
            prompt = f"오늘({datetime.now().strftime('%Y-%m-%d')}) {news_type} 관련 뉴스 헤드라인과 수혜주, 매매 전략을 아주 상세히 리포트해줘."
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"분석 중 오류 발생: {e}")

st.divider()
st.info("💡 주가 정보는 yfinance API를 통해 호출됩니다.")
