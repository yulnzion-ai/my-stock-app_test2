import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. 제미나이 2.0 Flash-Lite 설정
# 스트리미트 클라우드의 Secrets에서 키를 가져옵니다.
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.warning("API 키가 설정되지 않았습니다. 앱 설정의 Secrets에 GEMINI_API_KEY를 등록해주세요.")

model = genai.GenerativeModel('gemini-2.0-flash-lite-preview-02-05')

# 2. UI 스타일 설정
st.set_page_config(page_title="Golden-Bell AI Pro", layout="wide")

# 상단 탭 (버튼 클릭 시 색상 변경 로직 포함)
st.markdown("""
    <div style="display: flex; gap: 10px; padding: 10px 0; border-bottom: 1px solid #ddd; margin-bottom: 20px;">
        <button style="background: #2563eb; color: white; border: none; padding: 8px 16px; border-radius: 20px; font-weight: bold;">🌅 모닝브리핑</button>
        <button style="background: #f1f5f9; color: #64748b; border: none; padding: 8px 16px; border-radius: 20px; font-weight: bold;">📍 종목발굴</button>
    </div>
""", unsafe_allow_html=True)

st.title("🌅 오늘의 단타 모닝브리핑")
st.caption(f"기준일: {datetime.now().strftime('%Y년 %m월 %d일')} (실시간 분석)")

# 3. 사용자 선택창
col1, col2 = st.columns(2)
with col1:
    news_type = st.selectbox("📰 뉴스 유형 선택", ["정치테마", "기업공시", "글로벌이슈", "테마급등"])
with col2:
    market = st.radio("🌍 대상 시장", ["한국"], horizontal=True)

# 4. 분석 실행 버튼
if st.button(f"🚀 {news_type} 기반 실시간 AI 분석 시작", use_container_width=True):
    with st.spinner(f"AI 전문가가 최신 뉴스와 실시간 주가를 분석 중입니다..."):
        
        # 뉴스 유형별 동적 조건 (사용자님이 주신 조건들)
        conditions = {
            "정치테마": "대통령/장관/국회의원 발언, 정책 발표, 외교 이슈",
            "기업공시": "실적발표, 대규모 계약, M&A, 유상증자, 자사주 매입",
            "글로벌이슈": "미국 증시, 중국 정책, 환율, 원자재, 지정학 리스크",
            "테마급등": "SNS/커뮤니티 화제, 급등 테마, 거래량 급증"
        }
        
        # 최종 RICE 프롬프트 구성 (사용자님 제공 양식)
        final_prompt = f"""
        R (Role) - 당신은 10년 경력의 단기 트레이딩 전문가입니다.
        I (Instruction) - 분석 조건: 뉴스 유형({news_type}: {conditions[news_type]}), 시장({market}).
        최근 24시간 이내 최신 뉴스와 실시간 주가를 Web Search로 검색하여 분석하세요.
        C (Context) - 장 시작 전 빠른 의사결정이 필요하며 단타 관점입니다.
        E (Example) - 반드시 제공된 출력 형식을 엄수하세요. (뉴스 헤드라인, 수혜종목, 현재가, 전략 등 포함)
        """
        
        try:
            # AI 실행 (Gemini 2.0 Flash-Lite)
            response = model.generate_content(final_prompt)
            st.markdown("---")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"오류 발생: {e}")

st.divider()
st.info("💡 Tip: 이 정보는 참고용입니다. 실제 매매 전 증권사 앱에서 반드시 다시 확인하세요!")