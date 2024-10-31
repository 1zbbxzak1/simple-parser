from fastapi import FastAPI

from db.db import init_db
from db.model import Product
from parser.parser import parser_products

app = FastAPI()


@app.on_event("startup")
def startup_event():
    init_db()


# Эндпоинт для ручного запуска парсинга и записи продуктов в БД
@app.get("/parse")
def parse_and_save_products():
    parser_products()
    return {"message": "Products parsed and saved successfully"}


# Эндпоинт для получения всех продуктов из БД
@app.get("/products")
def get_all_products():
    return Product.get_all_products()
