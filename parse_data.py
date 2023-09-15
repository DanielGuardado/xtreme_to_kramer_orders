from datetime import datetime
from config import state_abbreviations


class DataParser:
    def __init__(self):
        self.parsed_data = []

    def parse_data(self, order):
        for item in order["items"]:
            if "smartliner" not in (item["name"]).lower():
                continue
            order_date = datetime.strptime(
                order["orderDate"][:-1], "%Y-%m-%dT%H:%M:%S.%f"
            )

            formatted_order_date = order_date.strftime("%m/%d/%Y")

            # Check if "shipTo" is available, else use "billTo"
            address_info = order.get("shipTo", order.get("billTo", {}))

            name_parts = address_info["name"].strip().split()
            if len(name_parts) == 1:
                first_name = name_parts[0]
                last_name = ""
            elif len(name_parts) == 2:
                first_name = name_parts[0]
                last_name = name_parts[1]
            else:
                first_name = " ".join(name_parts[:-1])
                last_name = name_parts[-1]

            if address_info.get("street3"):
                address_2 = (
                    address_info["street2"] + " " + address_info["street3"]
                ).strip()
            else:
                address_2 = address_info.get("street2", "").strip()

            # Check state abbreviation
            state = address_info.get("state", "").strip()
            if len(state) > 2:
                state = state_abbreviations.get(
                    state, state
                )  # If not found, retain the original state

            row = {
                "po_number": order["orderNumber"].strip(),
                "po_date": formatted_order_date,
                "sku": item["sku"].strip(),
                "quantity": item["quantity"],
                "first_name": first_name,
                "last_name": last_name,
                "address_1": address_info.get("street1", "").strip(),
                "address_2": address_2,
                "city": address_info.get("city", "").strip(),
                "state": state,
                "zip_code": address_info.get("postalCode", "").strip(),
                "country": address_info.get("country", "").strip(),
                "phone": address_info.get("phone", "").strip(),
            }

            self.parsed_data.append(row)
