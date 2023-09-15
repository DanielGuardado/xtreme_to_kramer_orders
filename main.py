from shipstation import ShipStation
from parse_data import DataParser
from database_manager import DatabaseManager
from data_to_csv import data_to_csv
from ftp_uploader import FTPUploader
from email_helper import send_email, send_file_created_email
import traceback


def main():
    shipstation = ShipStation()
    data_parser = DataParser()

    awaiting_orders_to_add = shipstation.get_abs_orders_info()
    orders_already_added = DatabaseManager().get_orders()
    orders_not_added = [
        order
        for order in awaiting_orders_to_add
        if order["orderNumber"] not in [x[0] for x in orders_already_added]
    ]

    for order in orders_not_added:
        try:
            data_parser.parse_data(order)
        except:
            send_email("Error adding kramer order to csv", traceback.format_exc())
            continue
    if data_parser.parsed_data:
        po_nums = [order["po_number"] for order in data_parser.parsed_data]
        file_path = data_to_csv(data_parser.parsed_data)
        ftp_uploader = FTPUploader.from_config(file_path)

        ftp_uploader.upload_file(file_path)

        db = DatabaseManager()
        for order in data_parser.parsed_data:
            db.insert_order(order)
        send_file_created_email("Kramer America CSV Created", f"PO Numbers: {po_nums}")


if __name__ == "__main__":
    try:
        main()
    except:
        send_email("Error creating kramer america csv", traceback.format_exc())
