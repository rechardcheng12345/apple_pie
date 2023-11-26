import requests
from utils.utils import _build_authentication_headers
from bitfinnex_funding_credit import main as available_funding
import json

API = "https://api.bitfinex.com/v2"


def format_trade_data(trade_data):
    formatted_trades = []
    trades = json.loads(trade_data)
    status = trades[6]
    text = trades[7]

    formatted_trade = {
        "order_status": status,
        "order_text": text,
    }

    formatted_trades.append(formatted_trade)

    return formatted_trades


def main():
    endpoint = "auth/w/funding/offer/submit"

    result_fund = available_funding()
    data = json.loads(result_fund)[0]
    if float(data["available_balance"]) < 150:
        return "insufficient to create order"
    else:
        payload = {
            "type": "LIMIT",
            "symbol": "fUSD",
            "amount": str(data["available_balance"]),
            "rate": "0.00052",
            "period": 2,
            "flags": 0
        }
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            **_build_authentication_headers(endpoint, payload)
        }

        response = requests.post(f"{API}/{endpoint}", json=payload, headers=headers)
        # data = [
        #     1700901928870, "fon-req", None, None,
        #     [
        #         2704213067, "fUSD", 1700901928862, 1700901928862, 150, 150, "LIMIT", None, None, 0, "ACTIVE", None,
        #         None, None, 0.0005, 2, False, 0, None, False, None
        #     ],
        #     None, "SUCCESS", "Submitting funding offer of 150.0 USD at 0.05000 for 2 days."
        # ]
        json_string = json.dumps(response.text)
        formatted_data = format_trade_data(json_string)
        formatted_json = json.dumps(formatted_data, indent=2)
        return formatted_json


result = main()
print(result)

