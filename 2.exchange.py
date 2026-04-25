import yfinance as yf
import json
from datetime import datetime

def get_finance_data():
    # 定義要抓取的標的：美金/台幣, 美金/日幣, 黃金期貨, 原油期貨
    targets = {
        "USD_TWD": "USDTWD=X",
        "USD_JPY": "JPY=X",
        "Gold": "GC=F",
        "Oil": "CL=F"
    }
    
    results = {"date": datetime.now().strftime("%Y-%m-%d"), "data": {}}
    
    for name, ticker in targets.items():
        data = yf.Ticker(ticker)
        # 抓取最近一天的收盤價
        latest_price = data.history(period="1d")['Close'].iloc[-1]
        results["data"][name] = round(latest_price, 2)
    
    return results

# 讀取並更新歷史檔案 history.json
history_file = 'history.json'
new_entry = get_finance_data()

try:
    with open(history_file, 'r') as f:
        history = json.load(f)
except FileNotFoundError:
    history = []

# 避免重複紀錄同一天
if not history or history[-1]['date'] != new_entry['date']:
    history.append(new_entry)

with open(history_file, 'w') as f:
    json.dump(history[-30:], f, indent=4) # 保留 30 天數據