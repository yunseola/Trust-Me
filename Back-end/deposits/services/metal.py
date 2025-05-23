import os
import requests

def fetch_gold_or_silver_data(metal="XAU"):
    base_url = f"https://www.goldapi.io/api/{metal}/USD"
    headers = {
        "x-access-token": os.getenv("API_KEY_METAL"),
        "Content-Type": "application/json"
    }

    response = requests.get(base_url, headers=headers)
    data = response.json()

    return {
        "metal": metal,
        "open": data.get("open_price"),
        "high": data.get("high_price"),
        "low": data.get("low_price")
    }
