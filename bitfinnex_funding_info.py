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
        amount = trade[4]

        formatted_trade = {
            "Trade ID": trade_id,
            "Symbol": symbol,
            "Buy Price": amount,
        }

        formatted_trades.append(formatted_trade)

    return formatted_trades


def main():
    endpoint = "auth/r/info/funding/fUSD"

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        **_build_authentication_headers(endpoint)
    }
    response = requests.post(f"{API}/{endpoint}", headers=headers)
    print(response.text)
    # formatted_data = format_trade_data(response.text)
    # formatted_json = json.dumps(formatted_data, indent=2)
    # return formatted_json
    return ""


result = main()
print(result)

