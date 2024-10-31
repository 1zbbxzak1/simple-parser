from db.model import Product


# Создаем базу данных и таблицу, если ее еще нет
def init_db():
    Product.create_table()
