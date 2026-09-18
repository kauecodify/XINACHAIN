"""Cost calculator agent for import cost calculation."""

from typing import Dict, Any
from decimal import Decimal
from pydantic_ai import Agent

from ..models.carga import Carga
from ..models.custo import CustoImportacao
from ..tools.cambio import obter_cotacao_usd_brl
from ..tools.tributos import calcular_tributos


# Cost calculator agent
# Note: Using None for testing, in production use your actual model
calculista_agent = None  # Will be initialized with actual model in production


async def node_custo(carga: Carga) -> Dict[str, Any]:
    """
    Node function for cost calculation in the pipeline.
    
    Args:
        carga: Cargo to calculate costs for
        
    Returns:
        Dictionary with cost calculation
    """
    # Get exchange rate
    cotacao_usd_brl = await obter_cotacao_usd_brl()
    
    # Calculate freight and insurance (simplified for demonstration)
    # In production, these would be actual values from the cargo
    frete_usd = Decimal(str(float(carga.valor_usd) * 0.05))  # 5% of cargo value
    seguro_usd = Decimal(str(float(carga.valor_usd) * 0.01))  # 1% of cargo value
    
    # Calculate taxes
    tributos = await calcular_tributos(
        ncm=carga.ncm,
        valor_usd=carga.valor_usd,
        frete_usd=frete_usd,
        seguro_usd=seguro_usd,
        cotacao_usd_brl=cotacao_usd_brl,
    )
    
    # Create cost object
    custo = CustoImportacao(
        valor_usd=carga.valor_usd,
        valor_brl=tributos["valor_brl"],
        frete_usd=frete_usd,
        frete_brl=tributos["frete_brl"],
        seguro_usd=seguro_usd,
        seguro_brl=tributos["seguro_brl"],
        ii=tributos["ii"],
        ipi=tributos["ipi"],
        pis_cofins=tributos["pis_cofins"],
        icms=tributos["icms"],
        siscomex=tributos["siscomex"],
        total_tributos=tributos["total_tributos"],
        custo_total=tributos["custo_total"],
        onus_tributario=tributos["onus_tributario"],
    )
    
    return {
        "custo": custo,
        "cotacao_usd_brl": cotacao_usd_brl,
        "frete_usd": frete_usd,
        "seguro_usd": seguro_usd,
    }
