class ProductRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        self.db.execute("""
            SELECT product.id, product.name, product.price, product.quantity, category.name
            FROM product
            JOIN category ON product.id_category = category.id
        """)
        return self.db.fetchall()

    def get_by_category(self, category_id):
        self.db.execute("""
            SELECT product.id, product.name, product.price, product.quantity, category.name
            FROM product
            JOIN category ON product.id_category = category.id
            WHERE category.id = %s
        """, (category_id,))
        return self.db.fetchall()

    def add(self, name, description, price, quantity, category_id):
        self.db.execute("""
            INSERT INTO product (name, description, price, quantity, id_category)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, description, int(price), int(quantity), category_id))
        self.db.commit()

    def update(self, product_id, price, quantity):
        self.db.execute("""
            UPDATE product SET price=%s, quantity=%s WHERE id=%s
        """, (int(price), int(quantity), product_id))
        self.db.commit()

    def delete(self, product_id):
        self.db.execute("DELETE FROM product WHERE id=%s", (product_id,))
        self.db.commit()

    def get_stock(self):
        self.db.execute("SELECT name, quantity FROM product")
        return self.db.fetchall()