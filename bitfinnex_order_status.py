import requests
from utils.utils import _build_authentication_headers
from datetime import datetime
import json

API = "https://api.bitfinex.com/v2"


def format_trade_data(trade_data):
    formatted_trades = []
    trades = json.loads(trade_data)
    for trade in trades:
        trade_id = trade[0]
        symbol = trade[1]
        timestamp_create = trade[2]
        amount = trade[4]
        rate = trade[14]
        period = trade[15]

        # Convert timestamps to human-readable datetime format
        create_datetime = datetime.fromtimestamp(timestamp_create / 1000.0)

        formatted_trade = {
            "trade_id": trade_id,
            "symbol": symbol,
            "create_timestamp": create_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "order_price": amount,
            "rate": rate * 100,
            "period": period
        }

        formatted_trades.append(formatted_trade)

    return formatted_trades


def main():
    endpoint = "auth/r/funding/offers/fUSD"

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        **_build_authentication_headers(endpoint)
    }
    response = requests.post(f"{API}/{endpoint}", headers=headers)

    formatted_data = format_trade_data(response.text)
    formatted_json = json.dumps(formatted_data, indent=2)
    return formatted_json


result = main()
print(result)

