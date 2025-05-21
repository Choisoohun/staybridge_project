import streamlit as st
import pandas as pd
from modules.scoring import compute_score

# 📁 파일 로딩 함수
@st.cache_data
def load_data():
    df = pd.read_csv("data/vacant_locations.csv", encoding="utf-8-sig")
    df = df.dropna(subset=["위도", "경도"])
    return df

# 🖥️ 페이지 설정
st.set_page_config(page_title="Stay-Bridge 주거 차원 제안", layout="centered")
st.title("🏡 Stay-Bridge 주거 차원 제안")
st.markdown("가장 적합한 공실 주거 참여책을 제안해 드립니다. 하나만 고르세요!")

# 🧑 사용자 입력
name = st.text_input("이름을 입력하세요")
age = st.number_input("나이를 입력하세요", min_value=0, max_value=120)
job = st.text_input("직업(선택사항)")
user_type = st.selectbox("해당 사용자 유형을 선택해주세요:", ["노인", "직장인", "1인가구", "기본"])

submit_button = st.button("🔍 추천 요청")

# 📄 데이터 불러오기
df = load_data()

if submit_button and user_type.strip():
    recommendations = []
    for _, row in df.iterrows():
        score = compute_score(row["위도"], row["경도"], user_type)
        recommendations.append({
            "주소": row["주소"],
            "면적": row["면적"],
            "추천점수": score
        })

    # 추천점수 높은 순으로 상위 5개만 출력
    top_results = sorted(recommendations, key=lambda x: x["추천점수"], reverse=True)[:5]

    st.markdown("### 🏆 추천 공실 리스트")
    for result in top_results:
        st.markdown(f"📍 **공실 주소:** {result['주소']}")
        st.markdown(f"⭐ **추천 점수:** {result['추천점수']}점")
        st.markdown(f"📐 **면적:** {result['면적']}")
        st.markdown("---")
