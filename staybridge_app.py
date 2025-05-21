import streamlit as st
import pandas as pd
from modules.scoring import compute_score

# 파일 로드
@st.cache_data
def load_data():
    df = pd.read_csv("data/\ub2e8일\ubbf8분양_uc704경도_완료.csv", encoding="utf-8-sig")
    df = df.dropna(subset=["위도", "경도"])
    return df

# 사용자 입력
st.set_page_config(page_title="Stay-Bridge 제조 시스템", layout="centered")
st.title("🏡 Stay-Bridge 주거 차원 제안")
st.markdown("""
가장 적합한 공신 주거 참여책을 제안해 드림니다. 하나만 고르세요!
""")

user_type = st.selectbox("해당 사용자 유형을 선택해주세요:", ["노인", "직장인", "1인가구", "기본"])

# 데이터 로드하기
with st.spinner("가져오는 중..."):
    df = load_data()

# 각 공신에 대해 가장 고정된 값을 제공
recommendations = []
seen = set()
for idx, row in df.iterrows():
    address = row["\uc2dc\uacf5\uc18c\uc7ac\uc9c0\uc704\uce58"]
    lat = row["\uc704\ub3c4"]
    lon = row["\uacbd\ub3c4"]
    if address not in seen:
        score = compute_score(lat, lon, user_type)
        same_address_sizes = df[df["\uc2dc\uacf5\uc18c\uc7ac\uc9c0\uc704\uce58"] == address]["\uaddc\ubaa8\ubcc4\uba74\uc801(m\u00b2)"].dropna().unique().tolist()
        recommendations.append({
            "공신 주소": address,
            "구면": same_address_sizes,
            "추천점수": score
        })
        seen.add(address)

# 추천 결과 표시
st.subheader(f"📊 \"{user_type}\" 사용자를 위한 가장 맞지는 공신 Top 10")
result_df = pd.DataFrame(recommendations).sort_values(by="추천점수", ascending=False).head(10)
st.dataframe(result_df)

# 저장 버튼
st.download_button(
    label="파일로 저장 (CSV)",
    data=result_df.to_csv(index=False, encoding="utf-8-sig"),
    file_name="staybridge_recommendation.csv",
    mime="text/csv"
)

st.caption("\u2665 \uc774 \ud504\ub9ac\uc820테이션은 Streamlit을 이용해 \uad6c현되어 \uc788습니다. ")
