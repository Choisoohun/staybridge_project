import streamlit as st
import pandas as pd
from modules.scoring import compute_score

# 파일 로딩
@st.cache_data
def load_data():
    df = pd.read_csv("data/vacant_locations.csv", encoding="utf-8-sig")
    df = df.dropna(subset=["위도", "경도"])
    return df

# UI 구성
st.set_page_config(page_title="Stay-Bridge 주거 차원 제안", layout="centered")
st.title("🏡 Stay-Bridge 주거 차원 제안")
st.markdown("가장 적합한 공실 주거 참여책을 제안해 드립니다. 하나만 고르세요!")

user_type = st.text_input("당신의 생활 유형을 입력하세요 (예: 노인, 직장인, 1인가구 등)")
submit_button = st.button("🔍 추천 요청")

# 데이터 로딩
df = load_data()

if submit_button and user_type.strip():
    recommendations = []

    for _, row in df.iterrows():
        score = compute_score(row["위도"], row["경도"], user_type)
        recommendations.append({
            "주소": row["주소"],
            "면적": row["면적(㎡)"],
            "추천점수": score
        })

    # 상위 5개만 출력
    top_results = sorted(recommendations, key=lambda x: x["추천점수"], reverse=True)[:5]

    st.markdown("### 🏆 추천 공실 리스트")
    for item in top_results:
        st.markdown(f"""
        <div style="padding: 10px 0; border-bottom: 1px solid #444;">
            <p>📍 <b>공실 주소:</b> {item['주소']}</p>
            <p>📐 <b>면적:</b> {item['면적']} ㎡</p>
            <p>⭐ <b>추천 점수:</b> {item['추천점수']}점</p>
        </div>
        """, unsafe_allow_html=True)
