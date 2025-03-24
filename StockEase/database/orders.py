import sqlite3
from datetime import datetime

class OrderDatabase:
    def __init__(self, db_name="storage/orders.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                total_price REAL NOT NULL,
                consumer TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders_data (
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (product_id) REFERENCES products(id),
                PRIMARY KEY (order_id, product_id)
            )
        ''')
        self.conn.commit()

    def add_order(self, total_price, consumer, products):
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO orders (date, total_price, consumer)
            VALUES (?, ?, ?)
        ''', (current_date, total_price, consumer))
        order_id = self.cursor.lastrowid

        for product in products:
            self.cursor.execute('''
                INSERT INTO orders_data (order_id, product_id, quantity)
                VALUES (?, ?, ?)
            ''', (order_id, product['product_id'], product['quantity']))

        self.conn.commit()
        return order_id

    def delete_order(self, order_id):
        self.cursor.execute('''
            DELETE FROM orders_data WHERE order_id = ?
        ''', (order_id,))
        
        self.cursor.execute('''
            DELETE FROM orders WHERE id = ?
        ''', (order_id,))
        self.conn.commit()

    def get_order_details(self, order_id):
        self.cursor.execute('''
            SELECT * FROM orders WHERE id = ?
        ''', (order_id,))
        order_info = self.cursor.fetchone()

        if not order_info:
            return None

        self.cursor.execute('''
            SELECT product_id, quantity FROM orders_data WHERE order_id = ?
        ''', (order_id,))
        products = self.cursor.fetchall()

        return {
            'order_info': order_info,
            'products': products
        }

    def get_all_orders(self):
        self.cursor.execute('SELECT * FROM orders')
        return self.cursor.fetchall()

    def drop_tables(self):
        self.cursor.execute('DROP TABLE IF EXISTS orders_data')
        self.cursor.execute('DROP TABLE IF EXISTS orders')
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = OrderDatabase()

    total_price = 150.75
    consumer = "John Doe"
    products = [
        {"product_id": 1, "quantity": 2},  # Product ID 1, Quantity 2
        {"product_id": 2, "quantity": 1},  # Product ID 2, Quantity 1
    ]
    order_id = db.add_order(total_price, consumer, products)

    order_details = db.get_order_details(order_id)
    print("Order Details:", order_details)
    
    for i in db.get_all_orders():

        print(db.get_order_details(i[0]))
    
    db.close()