"""Exchange rate tools for currency conversion."""

from typing import Dict, Any
from decimal import Decimal
import httpx
import os

from ..config import settings


async def obter_cotacao_usd_brl() -> float:
    """
    Get USD to BRL exchange rate.
    
    Returns:
        Exchange rate as float
    """
    # Try to get from environment variable first
    if os.environ.get("USD_BRL_RATE"):
        return float(os.environ["USD_BRL_RATE"])
    
    # Try to get from API
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Using a free API for demonstration
            # In production, use a reliable paid API
            response = await client.get(
                "https://economia.awesomeapi.com.br/json/last/USD-BRL"
            )
            data = response.json()
            return float(data["USDBRL"]["bid"])
    except Exception:
        # Fallback to default value from settings
        return settings.default_exchange_rate_usd_brl


async def obter_cotacao_usd_cny() -> float:
    """
    Get USD to CNY exchange rate.
    
    Returns:
        Exchange rate as float
    """
    # Try to get from environment variable first
    if os.environ.get("USD_CNY_RATE"):
        return float(os.environ["USD_CNY_RATE"])
    
    # Try to get from API
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://economia.awesomeapi.com.br/json/last/USD-CNY"
            )
            data = response.json()
            return float(data["USDCNY"]["bid"])
    except Exception:
        # Fallback to default value from settings
        return settings.default_exchange_rate_usd_cny
