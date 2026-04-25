import yfinance as yf
import json
import os
from datetime import datetime

def get_finance_data():
    # 定義要抓取的標的：美金/台幣, 日幣/台幣, 黃金期貨, 布蘭特原油
    targets = {
        "USD_TWD": "TWD=X",
        "JPY_TWD": "JPYTWD=X",
        "Gold": "GC=F",
        "Oil": "BZ=F"
    }
    
    current_results = {"date": datetime.now().strftime("%Y-%m-%d"), "data": {}}
    
    for name, ticker in targets.items():
        try:
            data = yf.Ticker(ticker)
            # 抓取最近一天的收盤價
            price = data.history(period="1d")['Close'].iloc[-1]
            current_results["data"][name] = round(price, 2)
        except Exception as e:
            print(f"抓取 {name} 失敗: {e}")
            current_results["data"][name] = 0

    return current_results

# 設定檔案路徑 (請確認與你的 index.html 在同個層級或對應路徑)
history_file = 'history.json'
rates_file = 'rates.json'

new_entry = get_finance_data()

# 更新歷史紀錄 history.json
if os.path.exists(history_file):
    with open(history_file, 'r') as f:
        history = json.load(f)
else:
    history = []

# 如果今天還沒紀錄過，就存進去
if not history or history[-1]['date'] != new_entry['date']:
    history.append(new_entry)

# 寫入歷史檔案 (保留最近 30 天)
with open(history_file, 'w') as f:
    json.dump(history[-30:], f, indent=4)

# 同時更新原本的 rates.json 確保即時看板也能動
with open(rates_file, 'w') as f:
    json.dump(new_entry, f, indent=4)

print("數據更新成功！")