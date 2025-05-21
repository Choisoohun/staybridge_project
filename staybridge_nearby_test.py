import requests
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_nearby_place_count(lat, lon, place_type="hospital", radius=1000):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": radius,
        "type": place_type,
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    results = data.get("results", [])
    print(f"✅ {place_type} 검색 결과: {len(results)}개")
    for i, place in enumerate(results[:5], start=1):
        print(f"{i}. {place['name']}")
    return len(results)

# 테스트용 좌표 (예: 안산시 단원구 공실)
lat = 37.321413
lon = 126.830841

get_nearby_place_count(lat, lon, place_type="hospital", radius=1000)
