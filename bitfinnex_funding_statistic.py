import requests
from utils.utils import _build_authentication_headers
from datetime import datetime, timedelta
import json

API = "https://api.bitfinex.com/v2"


def format_trade_data(trade_data):
    formatted_trades = []
    trades = json.loads(trade_data)
    for trade in trades:
        trade_id = trade[0]
        symbol = trade[1]
        amount = trade[4]

        formatted_trade = {
            "Trade ID": trade_id,
            "Symbol": symbol,
            "Buy Price": amount,
        }

        formatted_trades.append(formatted_trade)

    return formatted_trades


def main():
    symbol = "fUSD"
    current_time = datetime.now()
    three_minutes_ago = current_time - timedelta(minutes=5)
    start_epoch_time = int(three_minutes_ago.timestamp()) * 1000
    end_epoch_time = int(current_time.timestamp()) * 1000
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
    }
    # print(f"Current Time: {value}")
    # print(f"Time 3 minutes ago: {three_minutes_ago}")
    # print(f"Epoch Time: {start_epoch_time}")
    # endpoint = f"funding/stats/{symbol}/hist?start={start_epoch_time}&end={end_epoch_time}"
    endpoint = f"funding/stats/{symbol}/hist?limit=1"
    response = requests.get(f"{API}/{endpoint}", headers=headers)
    print(response.text)
    result_value = json.loads(response.text)
    rate = float(result_value[0][3]) * 100 * 365
    print(rate)
    return rate
    # formatted_data = format_trade_data(response.text)
    # formatted_json = json.dumps(formatted_data, indent=2)
    # return formatted_json


result = main()
print(result)

