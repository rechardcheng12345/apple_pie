import requests
from utils.utils import _build_authentication_headers
from datetime import datetime, timedelta
import json

API = "https://api.bitfinex.com/v2"


def format_trade_data(trade_data):
    formatted_trades = []
    trades = json.loads(trade_data)
    sorted_data = sorted(trades, key=lambda x: x[3])
    sorted_json = json.dumps(sorted_data)
    total_funding = 0.0
    print(sorted_json)
    result_string = ""
    for trade in sorted_data:
        trade_id = trade[0]
        symbol = trade[1]
        timestamp_create = trade[3]
        amount = trade[5]

        # Convert timestamps to human-readable datetime format
        create_datetime = datetime.fromtimestamp(int(timestamp_create) / 1000.0)

        formatted_trade = {
            "date": create_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "Fund Amount": amount,
        }
        date = create_datetime.strftime("%Y-%m-%d %H:%M:%S")
        fund_amount = amount
        total_funding = total_funding + amount
        formatted_trades.append(formatted_trade)
        result_string += f'{date}  {fund_amount}\n'

    formatted_trades.append({"total_funding" : total_funding})
    result_string += f'"total_funding": {total_funding}\n'
    return result_string


def main():
    endpoint = "auth/r/ledgers/USD/hist"

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        **_build_authentication_headers(endpoint)
    }
    response = requests.post(f"{API}/{endpoint}", headers=headers)
    print(response.text)
    formatted_data = format_trade_data(response.text)
    return formatted_data


result = main()
print(result)


