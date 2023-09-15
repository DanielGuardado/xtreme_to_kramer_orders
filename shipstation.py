import requests
from config import shipstation_auth, state_abbreviations


class ShipStation:
    def get_abs_orders_info(self):
        url = "http://ssapi.shipstation.com/orders?orderStatus=awaiting_shipment&page=1"
        json = requests.get(url, auth=shipstation_auth).json()
        orders_to_add = []
        for order in json["orders"]:
            for item in order["items"]:
                if "smartliner" in (item["name"]).lower():
                    orders_to_add.append(order)
        return orders_to_add
