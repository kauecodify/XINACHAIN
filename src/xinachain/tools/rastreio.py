"""Tracking tools for ship and port status."""

from typing import Dict, Any
from datetime import datetime, timedelta
import random
from decimal import Decimal


async def consultar_status_navio(navio: str) -> Dict[str, Any]:
    """
    Consult ship status, position, speed, and ETA.
    
    Args:
        navio: Name of the ship
        
    Returns:
        Dictionary with ship status information
    """
    # Simulated data - in production, this would call a real API
    portos = ["Shanghai", "Ningbo", "Shenzhen", "Hong Kong", "Santos", "Rio de Janeiro"]
    
    return {
        "navio": navio,
        "posicao": {
            "latitude": round(random.uniform(-90, 90), 6),
            "longitude": round(random.uniform(-180, 180), 6),
        },
        "velocidade": round(random.uniform(10, 25), 2),
        "eta": (datetime.now() + timedelta(days=random.randint(5, 30))).strftime("%Y-%m-%d"),
        "status": random.choice(["em_transito", "atracado", "em_esperado"]),
        "proximo_porto": random.choice(portos),
    }


async def consultar_porto(porto: str) -> Dict[str, Any]:
    """
    Consult port congestion and waiting time.
    
    Args:
        porto: Name of the port
        
    Returns:
        Dictionary with port congestion information
    """
    # Simulated data - in production, this would call a real API
    return {
        "porto": porto,
        "congestao": random.choice(["baixa", "media", "alta", "critica"]),
        "tempo_espera_dias": random.randint(0, 14),
        "navios_em_espera": random.randint(0, 50),
        "capacidade_operacional": random.uniform(0.5, 1.0),
    }
