import requests
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_place_count(lat, lon, place_type="hospital", radius=1000):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": radius,
        "type": place_type,
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return len(data.get("results", []))

# 사용자 유형별 가중치
USER_WEIGHTS = {
    "노인": {"hospital": 30, "subway_station": 10, "convenience_store": 10},
    "직장인": {"hospital": 10, "subway_station": 30, "convenience_store": 10},
    "1인가구": {"hospital": 10, "subway_station": 10, "convenience_store": 30},
    "기본": {"hospital": 20, "subway_station": 20, "convenience_store": 10}
}

def compute_score(lat, lon, user_type="기본", verbose=False):
    weights = USER_WEIGHTS.get(user_type, USER_WEIGHTS["기본"])
    score = 0
    log = []

    # 병원
    hospital_count = get_place_count(lat, lon, "hospital")
    hospital_score = weights["hospital"] if hospital_count >= 1 else 0
    score += hospital_score
    log.append(f"🏥 병원 개수: {hospital_count} → {hospital_score}점")

    # 지하철
    subway_count = get_place_count(lat, lon, "subway_station")
    subway_score = weights["subway_station"] if subway_count >= 1 else 0
    score += subway_score
    log.append(f"🚇 지하철역 개수: {subway_count} → {subway_score}점")

    # 편의점
    cvs_count = get_place_count(lat, lon, "convenience_store")
    cvs_score = weights["convenience_store"] if cvs_count >= 3 else 0
    score += cvs_score
    log.append(f"🏪 편의점 개수: {cvs_count} → {cvs_score}점")

    # 로그 출력
    if verbose:
        print("\n[공실 후보 위치]")
        print(f"위도: {lat}, 경도: {lon}")
        for line in log:
            print(line)
        print(f"🧮 총점: {score}점\n" + "-" * 40)

    return score