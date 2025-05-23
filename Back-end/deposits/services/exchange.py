import os
import requests

OPENEXCHANGE_API_KEY = os.getenv("API_KEY_EXCHANGE")

MAJOR_CURRENCIES = [
    "USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "HKD", "KRW",
    "SGD", "NZD", "SEK", "NOK", "DKK", "INR", "RUB", "BRL", "MXN", "ZAR",
    "TRY", "PLN", "THB", "MYR", "IDR", "VND", "SAR", "AED", "TWD", "CZK"
]

def get_major_exchange_rates():
    url = "https://openexchangerates.org/api/latest.json"
    params = {
        "app_id": OPENEXCHANGE_API_KEY,
        "symbols": ",".join(MAJOR_CURRENCIES)
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "rates" in data:
        return {
            "timestamp": data["timestamp"],
            "base": data["base"],
            "rates": data["rates"]
        }
    else:
        raise ValueError(f"환율 데이터 없음: {data}")

# ✅ USD 기준 실시간 환율 조회
def get_usd_based_rates(symbols=None):
    url = "https://openexchangerates.org/api/latest.json"
    params = {
        "app_id": OPENEXCHANGE_API_KEY
    }

    if symbols:
        params["symbols"] = ",".join(symbols)
    else:
        params["symbols"] = ",".join(MAJOR_CURRENCIES)

    response = requests.get(url, params=params)
    data = response.json()

    if "rates" in data:
        return {
            "timestamp": data["timestamp"],
            "base": data["base"],
            "rates": data["rates"]
        }
    else:
        raise ValueError(f"환율 데이터 없음: {data}")

# ✅ USD → 특정 통화 변환 함수
def convert_currency(to_currency, amount=1.0):
    rates = get_usd_based_rates()["rates"]
    to_currency = to_currency.upper()
    if to_currency in rates:
        return round(rates[to_currency] * amount, 4)
    else:
        raise ValueError(f"{to_currency} 환율 정보 없음")

# ✅ 특정 날짜의 환율 조회 (USD 기준)
def get_historical_rate(date, symbols="KRW"):
    url = f"https://openexchangerates.org/api/historical/{date}.json"
    params = {
        "app_id": OPENEXCHANGE_API_KEY,
        "symbols": symbols
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "rates" in data:
        return {
            "date": date,
            "base": data.get("base"),
            "rates": data["rates"]
        }
    else:
        raise ValueError(f"{date} 기준 환율 데이터 없음: {data}")

# ✅ 지원되는 통화 목록 조회 (상위 30개만 필터링)
def get_supported_currencies():
    url = "https://openexchangerates.org/api/currencies.json"
    response = requests.get(url)
    data = response.json()
    if isinstance(data, dict):
        return {code: name for code, name in data.items() if code in MAJOR_CURRENCIES}
    else:
        raise ValueError("지원 통화 목록 조회 실패")
