import requests
from utils.utils import _build_authentication_headers
from datetime import datetime, timedelta
import json

API = "https://api.bitfinex.com/v2"


def format_trade_data(trade_data):
    formatted_trades = []
    trades = json.loads(trade_data)
    total_funding = 0.0
    for trade in trades:
        trade_id = trade[0]
        symbol = trade[1]
        timestamp_create = trade[3]
        amount = trade[5]
        rate = trade[11]
        period = trade[12]
        mts_opening = trade[13]
        mts_last_payout = trade[14]
        # Convert timestamps to human-readable datetime format
        create_datetime = datetime.fromtimestamp(timestamp_create / 1000.0)
        mts_opening_datetime = datetime.fromtimestamp(mts_opening / 1000.0)

        mts_last_payout_datetime = datetime.fromtimestamp(mts_last_payout / 1000.0) if mts_last_payout is not None else None

        # Calculate the current datetime
        current_datetime = datetime.now()  # You can use datetime.now() if you want the local time
        # Calculate the remaining time
        remaining_time = create_datetime + timedelta(days=period) - current_datetime

        # Extract days, hours, and minutes from the remaining time
        days, remainder = divmod(remaining_time.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)

        formatted_trade = {
            "Trade ID": trade_id,
            "Symbol": symbol,
            "Create Timestamp": create_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "Fund Amount": amount,
            "Rate": rate * 100,
            "Period": period,
            "mts_opening": mts_opening_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "mts_last_payout": mts_last_payout_datetime.strftime("%Y-%m-%d %H:%M:%S") if mts_last_payout_datetime is not None else None,
            "Remaining time": f"{int(days)} days {int(hours)} hours {int(minutes)} minutes"
        }
        total_funding = total_funding + amount
        formatted_trades.append(formatted_trade)

    formatted_trades.append({"total_funding" : total_funding})

    return formatted_trades


def main():
    endpoint = "auth/r/funding/credits/fUSD"

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        **_build_authentication_headers(endpoint)
    }
    response = requests.post(f"{API}/{endpoint}", headers=headers)
    print(response.text)
    formatted_data = format_trade_data(response.text)
    formatted_json = json.dumps(formatted_data, indent=2)
    return formatted_json


result = main()
print(result)

