"""Weather tools for route weather conditions."""

from typing import Dict, Any
from datetime import datetime, timedelta
import random


async def obter_clima_rota(origem: str, destino: str) -> Dict[str, Any]:
    """
    Get weather conditions for a shipping route.
    
    Args:
        origem: Origin port
        destino: Destination port
        
    Returns:
        Dictionary with weather conditions and delay risk
    """
    # Simulated data - in production, this would call a real weather API
    weather_conditions = [
        "ensolarado",
        "nublado",
        "chuvoso",
        "tempestade",
        "nevoeiro",
        "ventania",
    ]
    
    wind_speeds = ["baixo", "moderado", "forte", "muito_forte"]
    wave_heights = ["calmo", "leve", "moderado", "agitado", "perigoso"]
    
    # Generate random weather data for the route
    dias_viagem = random.randint(15, 45)
    
    return {
        "origem": origem,
        "destino": destino,
        "dias_viagem": dias_viagem,
        "condicoes_climaticas": random.sample(weather_conditions, k=min(3, len(weather_conditions))),
        "velocidade_vento": random.choice(wind_speeds),
        "altura_ondas": random.choice(wave_heights),
        "temperatura_media": round(random.uniform(15, 35), 1),
        "umidade_media": round(random.uniform(50, 95), 1),
        "risco_atraso_dias": random.randint(0, 7),
        "probabilidade_atraso": round(random.uniform(0, 0.5), 2),
        "recomendacao": random.choice([
            "Condicoes favoraveis para navegacao",
            "Monitorar condicoes climaticas",
            "Considerar rota alternativa",
            "Atenção especial necessaria",
        ]),
    }
