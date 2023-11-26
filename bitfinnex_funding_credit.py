import requests
from utils.utils import _build_authentication_headers
import math
from datetime import datetime
import json

API = "https://api.bitfinex.com/v2"


def format_trade_data(trade_data):
    formatted_trades = []
    trades = json.loads(trade_data)
    for trade in trades:
        currency = trade[1]
        total_balance = trade[2],
        unsettled_interest = trade[3],
        available_balance = trade[4]
        rounded_down_value = math.floor(available_balance * 100000) / 100000
        formatted_trade = {
            "currency": currency,
            "total_balance": total_balance,
            "unsettled_interest": unsettled_interest,
            "available_balance": rounded_down_value
        }

        formatted_trades.append(formatted_trade)

    return formatted_trades


def main():
    endpoint = "auth/r/wallets"

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

