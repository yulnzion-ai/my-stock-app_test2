import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. 제미나이 2.0 Flash-Lite 설정
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.warning("⚠️ API 키가 설정되지 않았습니다. Streamlit Secrets에 GEMINI_API_KEY를 등록해주세요.")

# 최신 2.0 Flash-Lite 모델 설정
# 가장 확실하고 안정적인 정식 명칭으로 교체합니다.
model = genai.GenerativeModel('gemini-2.0-flash')

# 2. UI 레이아웃 및 스타일
st.set_page_config(page_title="Golden-Bell AI Pro", layout="wide")

# 상단 네비게이션 바 (시각적 요소)
st.markdown("""
    <div style="display: flex; gap: 10px; padding: 10px 0; border-bottom: 1px solid #ddd; margin-bottom: 20px;">
        <button style="background: #2563eb; color: white; border: none; padding: 8px 16px; border-radius: 20px; font-weight: bold;">🌅 모닝브리핑</button>
        <button style="background: #f1f5f9; color: #64748b; border: none; padding: 8px 16px; border-radius: 20px; font-weight: bold;">📍 종목발굴 (준비중)</button>
    </div>
""", unsafe_allow_html=True)

st.title("🌅 오늘의 단타 모닝브리핑")
st.caption(f"기준일: {datetime.now().strftime('%Y년 %m월 %d일')} (실시간 분석 엔진 가동 중)")

# 3. 메뉴 구성 (통합 브리핑 추가)
col1, col2 = st.columns([2, 1])
with col1:
    # 사용자님이 원하신 '한번에 보기' 옵션을 최상단에 배치했습니다.
    news_type = st.selectbox("📰 뉴스 유형 선택", 
                             ["🔥 전체 카테고리 통합 풀-브리핑", "정치테마", "기업공시", "글로벌이슈", "테마급등"])
with col2:
    market = st.radio("🌍 대상 시장", ["한국 (KOSPI/KOSDAQ)"], horizontal=True)

# 4. 분석 실행
if st.button(f"🚀 실시간 정밀 분석 시작", use_container_width=True):
    with st.spinner(f"AI 전문가가 모든 뉴스와 현재가를 검색 중입니다. (전체 분석은 최대 30초 소요)"):
        
        # 통합 분석 시의 특수 지시사항
        if "통합" in news_type:
            prompt_instruction = """
            [명령: 전체 카테고리 통합 분석]
            요약이나 생략 없이, 아래 4가지 카테고리 전체를 각각 독립적으로 정밀 분석하여 보고서를 작성하세요.
            1. 정치테마: 대통령/정부 정책/외교 이슈 및 수혜주
            2. 기업공시: 실적발표/M&A/대규모 계약 및 수혜주
            3. 글로벌이슈: 미 증시 마감 상황/환율/원자재/국제 정세
            4. 테마급등: SNS/커뮤니티 화제 테마 및 수급 집중 종목
            
            [⚠️ 주의사항]
            - 각 카테고리별로 '🔥 1순위, 2순위, 3순위' 종목을 상세히 기술할 것.
            - 절대 내용을 축소하지 말고, 개별 리포트 4개를 합친 분량 그대로 상세히 작성할 것.
            - 반드시 Web Search를 사용하여 실시간 현재가와 최근 24시간 뉴스를 반영할 것.
            """
        else:
            prompt_instruction = f"{news_type} 카테고리에 집중하여 상세 리포트를 작성하세요."

        # 사용자님 제공 RICE 프롬프트 구조 적용
        final_prompt = f"""
        R (Role) - 당신은 10년 경력의 단기 트레이딩 전문가입니다.
        I (Instruction) - {prompt_instruction}
        C (Context) - 장 시작 전 30분~1시간 내 빠른 의사결정이 필요함. 단타 매매 관점.
        E (Example) - 반드시 아래 형식을 각 카테고리마다 반복하여 작성할 것:
        ---
        🔥 [순위]: [뉴스 헤드라인]
        | 항목 | 내용 |
        |------|------|
        | 뉴스 요약 | [내용] |
        | 수혜 종목 | [종목명](코드) |
        | 연결 고리 | [이유] |
        | 현재가/등락 | [실시간 조회 가격] |
        | 예상 영향 | [강도] |
        | 매매 전략 | [시초가/눌림목/관망] |
        | 목표/손절가 | [가격] |
        ---
        📊 테마별 정리 (테이블 형식)
        ⚠️ 주의 종목 (리스크 관리)
        🎯 오늘의 단타 전략 요약
        📅 오늘 주요 일정
        """
        
        try:
            # Gemini 2.0 Flash-Lite 모델 호출
            response = model.generate_content(final_prompt)
            st.markdown("---")
            # AI의 응답을 화면에 출력
            st.markdown(response.text)
        except Exception as e:
            st.error(f"❌ 분석 중 오류가 발생했습니다. (API 키 확인 필요): {e}")

st.divider()
st.info("💡 이 정보는 참고용입니다. 단타는 리스크가 높으니 설정한 손절가를 반드시 준수하세요.")
