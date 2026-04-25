import requests
import json

# 調用 API 獲取匯率 (以美金為基底)
response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
data = response.json()

# 將結果存成 JSON 供前端讀取
with open("rates.json", "w") as f:
    json.dump(data, f)