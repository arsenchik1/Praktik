"""
Основной файл приложения для конвертации валют.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import uvicorn
from datetime import date

app = FastAPI(
    title="Currency Converter API",
    description="API для конвертации валют",
    version="1.0.0"
)

# Модели данных
class ConversionRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float

class ConversionResponse(BaseModel):
    from_currency: str
    to_currency: str
    amount: float
    result: float
    rate: float
    date: str

# Заглушка с курсами валют
CURRENCIES = {
    "USD": 1.0,
    "EUR": 0.92,
    "RUB": 91.5,
    "GBP": 0.79,
    "JPY": 148.5,
    "CNY": 7.2,
    "KZT": 450.0,
    "TRY": 30.5,
    "CHF": 0.85,
    "CAD": 1.35
}

@app.get("/")
async def root():
    """Корневой эндпоинт с информацией об API."""
    return {
        "message": "Currency Converter API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "GET /api/currencies": "Список доступных валют",
            "GET /api/rates": "Курсы валют",
            "POST /api/convert": "Конвертация валюты"
        }
    }

@app.get("/api/currencies")
async def get_currencies():
    """Получить список доступных валют."""
    return {
        "currencies": list(CURRENCIES.keys()),
        "base": "USD",
        "count": len(CURRENCIES)
    }

@app.get("/api/rates")
async def get_rates(base: str = "USD"):
    """
    Получить курсы валют относительно базовой валюты.
    
    - **base**: базовая валюта (по умолчанию USD)
    """
    base = base.upper()
    
    if base not in CURRENCIES:
        raise HTTPException(
            status_code=400,
            detail=f"Валюта {base} не найдена. Доступные валюты: {list(CURRENCIES.keys())}"
        )
    
    # Рассчитываем курсы относительно базовой валюты
    base_rate = CURRENCIES[base]
    rates = {}
    for currency, rate in CURRENCIES.items():
        if currency != base:
            rates[currency] = round(rate / base_rate, 4)
    
    return {
        "base": base,
        "date": date.today().isoformat(),
        "rates": rates
    }

@app.post("/api/convert", response_model=ConversionResponse)
async def convert_currency(request: ConversionRequest):
    """
    Конвертировать сумму из одной валюты в другую.
    
    Параметры в теле запроса:
    - **from_currency**: исходная валюта (например, USD)
    - **to_currency**: целевая валюта (например, RUB)
    - **amount**: сумма для конвертации
    """
    # Приводим к верхнему регистру
    from_curr = request.from_currency.upper()
    to_curr = request.to_currency.upper()
    
    # Проверяем существование валют
    if from_curr not in CURRENCIES:
        raise HTTPException(
            status_code=400,
            detail=f"Валюта {from_curr} не найдена. Доступные валюты: {list(CURRENCIES.keys())}"
        )
    
    if to_curr not in CURRENCIES:
        raise HTTPException(
            status_code=400,
            detail=f"Валюта {to_curr} не найдена. Доступные валюты: {list(CURRENCIES.keys())}"
        )
    
    if request.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Сумма должна быть больше 0"
        )
    
    # Конвертация через USD как базовую валюту
    amount_in_usd = request.amount / CURRENCIES[from_curr]
    result = amount_in_usd * CURRENCIES[to_curr]
    
    # Курс конвертации
    rate = CURRENCIES[to_curr] / CURRENCIES[from_curr]
    
    return ConversionResponse(
        from_currency=from_curr,
        to_currency=to_curr,
        amount=request.amount,
        result=round(result, 2),
        rate=round(rate, 4),
        date=date.today().isoformat()
    )

@app.get("/api/health")
async def health_check():
    """Проверка работоспособности API."""
    return {"status": "healthy", "timestamp": date.today().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)