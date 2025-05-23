import os
import requests

def search_youtube_videos(query, max_results=5):
    api_key = os.getenv("API_KEY_YOUTUBE")
    print("▶ 유튜브 API 키:", api_key)  # 이게 이제 정상 출력돼야 함

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": api_key,  # ✅ 문자열 API 키
        "maxResults": max_results,
        "type": "video"
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []
    for item in data.get("items", []):
        results.append({
            "title": item["snippet"]["title"],
            "videoId": item["id"]["videoId"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        })

    return results
