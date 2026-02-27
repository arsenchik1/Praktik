"""
FastAPI приложение для работы с продуктами iPhone.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="iPhone Products API",
    description="API для CRUD операций с продуктами iPhone",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Тестовые данные
products = [
    {
        "id": 1,
        "title": "iPhone 9",
        "description": "An apple mobile",
        "price": 549,
        "brand": "Apple",
        "category": "smartphones"
    },
    {
        "id": 2,
        "title": "iPhone X",
        "description": "SIM-Free, Model A19211",
        "price": 899,
        "brand": "Apple",
        "category": "smartphones"
    }
]

@app.get("/")
async def root():
    return {
        "message": "iPhone Products API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/api/products")
async def get_products():
    """Получить все продукты iPhone."""
    return {"products": products}

@app.get("/api/products/{product_id}")
async def get_product(product_id: int):
    """Получить продукт по ID."""
    for product in products:
        if product["id"] == product_id:
            return product
    return {"error": "Product not found"}

@app.post("/api/products")
async def create_product(title: str, description: str, price: float):
    """Создать новый продукт."""
    new_product = {
        "id": len(products) + 1,
        "title": title,
        "description": description,
        "price": price,
        "brand": "Apple",
        "category": "smartphones"
    }
    products.append(new_product)
    return new_product

@app.put("/api/products/{product_id}")
async def update_product(product_id: int, title: str = None, price: float = None):
    """Обновить продукт."""
    for product in products:
        if product["id"] == product_id:
            if title:
                product["title"] = title
            if price:
                product["price"] = price
            return product
    return {"error": "Product not found"}

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: int):
    """Удалить продукт."""
    for i, product in enumerate(products):
        if product["id"] == product_id:
            deleted = products.pop(i)
            return {"message": f"Product {deleted['title']} deleted"}
    return {"error": "Product not found"}