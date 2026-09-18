"""Tracker agent for monitoring ship and port status."""

from typing import Dict, Any
from pydantic_ai import Agent

from ..models.carga import Carga
from ..tools.rastreio import consultar_status_navio, consultar_porto


# Tracker agent for monitoring ship and port status
# Note: Using a mock model for testing, in production use your actual model
rastreador_agent = None  # Will be initialized with actual model in production


async def node_rastreio(carga: Carga) -> Dict[str, Any]:
    """
    Node function for tracking in the pipeline.
    
    Args:
        carga: Cargo to track
        
    Returns:
        Dictionary with tracking status
    """
    # Get ship status
    ship_status = await consultar_status_navio(carga.navio)
    
    # Get port status for origin and destination
    porto_origem_status = await consultar_porto(carga.porto_origem)
    porto_destino_status = await consultar_porto(carga.porto_destino)
    
    # Generate summary
    summary = f"""
    Status de Rastreio para Carga {carga.id}:
    
    Navio: {ship_status['navio']}
    - Posicao: Latitude {ship_status['posicao']['latitude']}, Longitude {ship_status['posicao']['longitude']}
    - Velocidade: {ship_status['velocidade']} nos
    - ETA: {ship_status['eta']}
    - Status: {ship_status['status']}
    - Proximo Porto: {ship_status['proximo_porto']}
    
    Porto de Origem ({carga.porto_origem}):
    - Congestao: {porto_origem_status['congestao']}
    - Tempo de Espera: {porto_origem_status['tempo_espera_dias']} dias
    - Navios em Espera: {porto_origem_status['navios_em_espera']}
    
    Porto de Destino ({carga.porto_destino}):
    - Congestao: {porto_destino_status['congestao']}
    - Tempo de Espera: {porto_destino_status['tempo_espera_dias']} dias
    - Navios em Espera: {porto_destino_status['navios_em_espera']}
    """
    
    return {
        "status_rastreio": summary,
        "ship_status": ship_status,
        "porto_origem_status": porto_origem_status,
        "porto_destino_status": porto_destino_status,
    }
