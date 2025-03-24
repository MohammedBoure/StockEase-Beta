import mysql.connector

class ProductDatabase:
    def __init__(self, host="localhost", user="root", password="", database="data_stock"):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()
        self.create_database(database)
        
        self.conn.database = database  # Reconnect to the specified database
        self.create_table()

    def create_database(self, database):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        self.conn.commit()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL UNIQUE,
                recommended_quantity INT NOT NULL,
                current_quantity INT NOT NULL,
                price DOUBLE NOT NULL,
                purchase_price DOUBLE NOT NULL
            )
        ''')
        self.conn.commit()

    def add_product(self, id, name, recommended_quantity, current_quantity, price, purchase_price):
        self.cursor.execute("SELECT id FROM products WHERE name = %s", (name,))
        existing_product = self.cursor.fetchone()
        
        if existing_product:
            print("this product already exists")
            return False 

        self.cursor.execute('''
            INSERT INTO products (id, name, recommended_quantity, current_quantity, price, purchase_price)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (id, name, recommended_quantity, current_quantity, price, purchase_price))
        self.conn.commit()
        return True

    def update_product(self, product_id, name=None, recommended_quantity=None, current_quantity=None, price=None, purchase_price=None):
        query = "UPDATE products SET "
        updates = []
        params = []
        
        if name:
            updates.append("name = %s")
            params.append(name)
        if recommended_quantity is not None:
            updates.append("recommended_quantity = %s")
            params.append(recommended_quantity)
        if current_quantity is not None:
            updates.append("current_quantity = %s")
            params.append(current_quantity)
        if price is not None:
            updates.append("price = %s")
            params.append(price)
        if purchase_price is not None:
            updates.append("purchase_price = %s")
            params.append(purchase_price)
        
        if updates:
            query += ", ".join(updates) + " WHERE id = %s"
            params.append(product_id)
            self.cursor.execute(query, tuple(params))
            self.conn.commit()

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        self.conn.commit()

    def clear_table(self):
        self.cursor.execute("DELETE FROM products")
        self.conn.commit()
        
    def get_all_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def get_product_by_id(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        return self.cursor.fetchone()

    def search_product(self, search_term):
        if isinstance(search_term, int) or (isinstance(search_term, str) and search_term.isdigit()):
            search_term = int(search_term)  
            self.cursor.execute("SELECT * FROM products WHERE id = %s", (search_term,))
            result = self.cursor.fetchall()
            if result:
                return result

        if isinstance(search_term, str):
            search_term = search_term.strip()
            self.cursor.execute("SELECT * FROM products WHERE name LIKE %s", ("%" + search_term + "%",))
        
        results = self.cursor.fetchall()
        return results if results else []

    def drop_table(self, table_name="products"):
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.conn.commit()
        
    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    import random
    import uuid 
    db = ProductDatabase()
    
    for _ in range(100):
        name = "Product_" + str(uuid.uuid4())[:8] 
        recommended_quantity = random.randint(5, 50)
        current_quantity = random.randint(0, 100)
        price = round(random.uniform(10, 2000), 2)
        purchase_price = round(price * random.uniform(0.6, 0.9), 2)
        db.add_product(None, name, recommended_quantity, current_quantity, price, purchase_price)
    
    products = db.get_all_products()
    print(products)
    
    db.close()
