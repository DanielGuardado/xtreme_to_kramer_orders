import sqlite3


class DatabaseManager:
    def __init__(self, db_name="Orders.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

        # Create KramerOrders table if it doesn't exist
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS KramerOrders (
            id INTEGER PRIMARY KEY,
            po_number TEXT,
            po_date TEXT,
            sku TEXT,
            quantity INTEGER,
            first_name TEXT,
            last_name TEXT,
            address_1 TEXT,
            address_2 TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            country TEXT,
            phone TEXT
        )
        """
        )
        self.connection.commit()

    def insert_order(self, order_data):
        columns = ", ".join(order_data.keys())
        placeholders = ", ".join("?" * len(order_data))
        query = f"INSERT INTO KramerOrders ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, tuple(order_data.values()))
        self.connection.commit()

    def get_orders(self):
        query = "SELECT po_number FROM KramerOrders"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()
