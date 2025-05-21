import streamlit as st
import pandas as pd
from modules.scoring import compute_score

# 📁 파일 로드
@st.cache_data
def load_data():
    df = pd.read_csv("data/vacant_locations.csv", encoding="utf-8-sig")  # 영어 파일명 사용
    df = df.dropna(subset=["위도", "경도"])
    return df

# 👤 사용자 입력
st.set_page_config(page_title="Stay-Bridge 주거 차원 제안", layout="centered")
st.title("🏡 Stay-Bridge 주거 차원 제안")

st.markdown("""
가장 적합한 공실 주거 참여책을 제안해 드립니다. 하나만 고르세요!
""")

user_type = st.selectbox("해당 사용자 유형을 선택해주세요:", ["노인", "직장인", "1인가구", "기본"])

# 🧮 데이터 로드
with st.spinner("📊 가져오는 중..."):
    df = load_data()

# 📍 공실에 대해 가중치 값 계산 및 출력
recommendations = []

for _, row in df.iterrows(): 
    score = compute_score(row["위도"], row["경도"], user_type)
    recommendations.append({
        "주소": row["시공소재지위치"],  # ✅ 여기를 정확히 이렇게 고쳐야 합니다
        "추천점수": score
    })


# 🔢 점수 기준 정렬
sorted_recs = sorted(recommendations, key=lambda x: x["추천점수"], reverse=True)

st.subheader("🏆 추천 공실 리스트")

for rec in sorted_recs[:5]:
    st.markdown(f"📍 **공실 주소:** {rec['주소']}")
    st.markdown(f"⭐ **추천 점수:** {rec['추천점수']}점")
    st.markdown("---")
