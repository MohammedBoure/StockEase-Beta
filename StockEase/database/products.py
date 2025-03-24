import sqlite3

class ProductDatabase:
    def __init__(self, db_name="storage/products.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False) 
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                recommended_quantity INTEGER NOT NULL,
                current_quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                purchase_price REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def add_product(self,id, name, recommended_quantity, current_quantity, price, purchase_price):
        self.cursor.execute("SELECT id FROM products WHERE name = ?", (name,))
        existing_product = self.cursor.fetchone()
        
        if existing_product:
            print("this product alredy exist")
            return False 

        self.cursor.execute('''
            INSERT INTO products (id,name, recommended_quantity, current_quantity, price, purchase_price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (id,name, recommended_quantity, current_quantity, price, purchase_price))
        self.conn.commit()
        return True

    def update_product(self, product_id, name=None, recommended_quantity=None, current_quantity=None, price=None, purchase_price=None):
        query = "UPDATE products SET "
        updates = []
        params = []
        
        if name:
            updates.append("name = ?")
            params.append(name)
        if recommended_quantity is not None:
            updates.append("recommended_quantity = ?")
            params.append(recommended_quantity)
        if current_quantity is not None:
            updates.append("current_quantity = ?")
            params.append(current_quantity)
        if price is not None:
            updates.append("price = ?")
            params.append(price)
        if purchase_price is not None:
            updates.append("purchase_price = ?")
            params.append(purchase_price)
        
        if updates:
            query += ", ".join(updates) + " WHERE id = ?"
            params.append(product_id)
            self.cursor.execute(query, tuple(params))
            self.conn.commit()

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self.conn.commit()

    def clear_table(self):
        self.cursor.execute("DELETE FROM products")
        self.conn.commit()
        
    def get_all_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def get_product_by_id(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        return self.cursor.fetchone()

    def search_product(self, search_term):
        if isinstance(search_term, int) or (isinstance(search_term, str) and search_term.isdigit()):
            search_term = int(search_term)  
            self.cursor.execute("SELECT * FROM products WHERE id = ?", (search_term,))
            result = self.cursor.fetchall()
            if result:
                return result

        if isinstance(search_term, str):
            search_term = search_term.strip()
            self.cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + search_term + '%',))
        
        results = self.cursor.fetchall()
        return results if results else []


    def drop_table(self,table_name="products"):

        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.conn.commit()
        





        
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    import random

    db = ProductDatabase()
    for i in range (1000):
        name = "Product_" + str(random.randint(1, 1000))
        recommended_quantity = random.randint(5, 50)
        current_quantity = random.randint(0, 100)
        price = round(random.uniform(10, 2000), 2)
        purchase_price = round(price * random.uniform(0.6, 0.9), 2)
        id = i + 1
        db.add_product(id, name, recommended_quantity, current_quantity, price, purchase_price)
        

    
    
    """db.create_table()
        
    for i in range(1000):
        name = "Product_" + str(random.randint(1, 1000))
        recommended_quantity = random.randint(5, 50)
        current_quantity = random.randint(0, 100)
        price = round(random.uniform(10, 2000), 2)
        purchase_price = round(price * random.uniform(0.6, 0.9), 2)
        id = i + 1
       

    
        db.add_product(id, name, recommended_quantity, current_quantity, price, purchase_price)
    products=db.get_all_products()
    for i in products:
        print(i)"""
   
    
    db.close()
