import pandas as pd
from modules.scoring import compute_score

# 사용자 선택
print("🏠 어떤 사용자 유형에 해당하십니까?")
print("1. 노인\n2. 직장인\n3. 1인가구\n4. 일반 사용자")
choice = input("번호를 입력하세요 (1~4): ").strip()

user_type = {
    "1": "노인",
    "2": "직장인",
    "3": "1인가구"
}.get(choice, "기본")

print(f"\n👤 선택한 사용자 유형: {user_type}\n")

# 데이터 불러오기
df = pd.read_csv("data/미분양_위경도_완료.csv", encoding="utf-8-sig")
df = df.dropna(subset=["위도", "경도"])

# 추천 점수 계산
results = []
for idx, row in df.iterrows():
    lat, lon = row["위도"], row["경도"]
    address = row["시공소재지위치"]
    print(f"\n📍 공실 주소: {address}")
    score = compute_score(lat, lon, user_type, verbose=True)
    results.append({"공실주소": address, "추천점수": score})

# 결과 정렬
df_result = pd.DataFrame(results)
top10 = df_result.sort_values(by="추천점수", ascending=False).head(10)

# 최종 출력
print("\n🏆 사용자 맞춤 추천 Top 10:")
print(top10)

# 엑셀 저장 여부
save = input("\n📁 결과를 엑셀로 저장하시겠습니까? (y/n): ").lower()
if save == "y":
    top10.to_excel("추천_결과.xlsx", index=False)
    print("✅ '추천_결과.xlsx'로 저장 완료!")
else:
    print("❌ 저장하지 않고 종료합니다.")
