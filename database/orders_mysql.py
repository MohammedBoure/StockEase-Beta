import mysql.connector
from datetime import datetime

class OrderDatabase:
    def __init__(self, host="localhost", user="root", password="", database="data_stock"):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()
        self.create_database(database)
        
        self.conn.database = database 
        self.create_tables()

    def create_database(self, database):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        self.conn.commit()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                price DOUBLE NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INT PRIMARY KEY AUTO_INCREMENT,
                date DATETIME NOT NULL,
                total_price DOUBLE NOT NULL,
                consumer VARCHAR(255)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders_data (
                order_id INT,
                product_id INT,
                quantity INT NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                PRIMARY KEY (order_id, product_id)
            )
        ''')
        self.conn.commit()

    def add_order(self, total_price, consumer, products):
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO orders (date, total_price, consumer)
            VALUES (%s, %s, %s)
        ''', (current_date, total_price, consumer))
        order_id = self.cursor.lastrowid

        for product in products:
            self.cursor.execute('''
                SELECT quantity FROM orders_data WHERE order_id = %s AND product_id = %s
            ''', (order_id, product['product_id']))
            existing_product = self.cursor.fetchone()

            if existing_product:
                new_quantity = existing_product[0] + product['quantity']
                self.cursor.execute('''
                    UPDATE orders_data SET quantity = %s WHERE order_id = %s AND product_id = %s
                ''', (new_quantity, order_id, product['product_id']))
            else:
                self.cursor.execute('''
                    INSERT INTO orders_data (order_id, product_id, quantity)
                    VALUES (%s, %s, %s)
                ''', (order_id, product['product_id'], product['quantity']))

        self.conn.commit()
        return order_id

    def delete_order(self, order_id):
        self.cursor.execute('DELETE FROM orders_data WHERE order_id = %s', (order_id,))
        self.cursor.execute('DELETE FROM orders WHERE id = %s', (order_id,))
        self.conn.commit()

    def get_order_details(self, order_id):
        self.cursor.execute('SELECT * FROM orders WHERE id = %s', (order_id,))
        order_info = self.cursor.fetchone()
        if not order_info:
            return None

        self.cursor.execute('SELECT product_id, quantity FROM orders_data WHERE order_id = %s', (order_id,))
        products = self.cursor.fetchall()

        return {'order_info': order_info, 'products': products}

    def get_all_orders(self):
        self.cursor.execute('SELECT * FROM orders')
        return self.cursor.fetchall()

    def drop_tables(self):
        self.cursor.execute('DROP TABLE IF EXISTS orders_data')
        self.cursor.execute('DROP TABLE IF EXISTS orders')
        self.cursor.execute('DROP TABLE IF EXISTS products')
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    import random

    db = OrderDatabase()
    
    for order in db.get_all_orders():
        print(db.get_order_details(order[0]))
    
    db.close()
