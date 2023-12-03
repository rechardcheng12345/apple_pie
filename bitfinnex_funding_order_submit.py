import requests
from utils.utils import _build_authentication_headers
from bitfinnex_funding_credit import main as available_funding
from bitfinnex_order_status import main as retrieve_order
from bitfinnex_funding_statistic import main as retrieve_frr
import json
from datetime import datetime, time

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


def check_order_rate(current_frr):
    endpoint = "auth/w/funding/offer/cancel"
    static_diff_rate = 0.015
    order_result = json.loads(retrieve_order())
    if len(order_result) > 0:
        for trade_data in order_result:
            rate = trade_data["rate"]
            trade_id = trade_data["trade_id"]
            if abs(current_frr - rate) < static_diff_rate or abs(rate - current_frr) < static_diff_rate:
                payload = {"id": trade_id}
                request_response(payload,endpoint)


def request_response(payload,endpoint):
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        **_build_authentication_headers(endpoint, payload)
    }
    response = requests.post(f"{API}/{endpoint}", json=payload, headers=headers)
    return response


def main():
    endpoint = "auth/w/funding/offer/submit"
    current_frr = retrieve_frr()
    check_order_rate(current_frr)
    result_fund = available_funding()
    data = json.loads(result_fund)[0]
    if float(data["available_balance"]) < 150:
        return "insufficient to create order"
    else:
        static_rate = 0.051
        current_time = datetime.now().time()
        start_time = time(22, 0)
        end_time = time(2, 0)

        if start_time <= current_time or current_time <= end_time:
            rate = static_rate + 0.005
        else:
            rate = current_frr - 0.001 if current_frr > static_rate else static_rate

        payload = {
            "type": "LIMIT",
            "symbol": "fUSD",
            "amount": str(data["available_balance"]),
            "rate": str(rate / 100),
            "period": 2,
            "flags": 0
        }

        response = request_response(payload,endpoint)
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

