import sqlite3


class Product:
    def __init__(self, category: str, name: str, price: float):
        self.category = category
        self.name = name
        self.price = price

    @classmethod
    def create_table(cls):
        conn = sqlite3.connect("products.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            category TEXT,
                            name TEXT,
                            price FLOAT
                          )''')
        conn.commit()
        conn.close()

    @classmethod
    def save_product(cls, category, name, price):
        conn = sqlite3.connect("products.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (category, name, price) VALUES (?, ?, ?)", (category, name, price))
        conn.commit()
        conn.close()

    @classmethod
    def get_all_products(cls):
        conn = sqlite3.connect("products.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, category, name, price FROM products")
        products = cursor.fetchall()
        conn.close()
        return {
            "products": [{"id": prod_id, "category": category, "name": name, "price": price}
                         for prod_id, category, name, price in products]
        }

    @classmethod
    def exists(cls, name: str, price: float) -> bool:
        conn = sqlite3.connect("products.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM products WHERE name = ? AND price = ?", (name, price))
        result = cursor.fetchone()
        conn.close()
        return result is not None
