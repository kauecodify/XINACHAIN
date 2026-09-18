"""Tax calculation tools for Brazilian import taxes."""

from typing import Dict, Any
from decimal import Decimal

# Brazilian tax rates by NCM category (simplified for demonstration)
# In production, this would be a complete database
TAX_RATES = {
    # Electronics
    "8517.12.00": {"ii": 0.20, "ipi": 0.15, "pis_cofins": 0.0925, "icms": 0.17, "siscomex": 0.0055},
    "8517.13.00": {"ii": 0.20, "ipi": 0.15, "pis_cofins": 0.0925, "icms": 0.17, "siscomex": 0.0055},
    "8517.18.00": {"ii": 0.20, "ipi": 0.15, "pis_cofins": 0.0925, "icms": 0.17, "siscomex": 0.0055},
    
    # Clothing
    "6109.10.00": {"ii": 0.35, "ipi": 0.00, "pis_cofins": 0.0925, "icms": 0.17, "siscomex": 0.0055},
    "6203.42.00": {"ii": 0.35, "ipi": 0.00, "pis_cofins": 0.0925, "icms": 0.17, "siscomex": 0.0055},
    
    # Machinery
    "8479.89.00": {"ii": 0.14, "ipi": 0.10, "pis_cofins": 0.0925, "icms": 0.12, "siscomex": 0.0055},
    
    # Default rates for unknown NCM
    "default": {"ii": 0.20, "ipi": 0.10, "pis_cofins": 0.0925, "icms": 0.17, "siscomex": 0.0055},
}


async def calcular_tributos(
    ncm: str,
    valor_usd: Decimal,
    frete_usd: Decimal,
    seguro_usd: Decimal,
    cotacao_usd_brl: float = 5.0
) -> Dict[str, Decimal]:
    """
    Calculate all Brazilian import taxes for a cargo.
    
    Args:
        ncm: NCM code
        valor_usd: Cargo value in USD
        frete_usd: Freight cost in USD
        seguro_usd: Insurance cost in USD
        cotacao_usd_brl: USD to BRL exchange rate
        
    Returns:
        Dictionary with all tax values in BRL
    """
    # Get tax rates for NCM or use default
    rates = TAX_RATES.get(ncm, TAX_RATES["default"])
    
    # Convert all values to BRL
    valor_brl = Decimal(str(valor_usd)) * Decimal(str(cotacao_usd_brl))
    frete_brl = Decimal(str(frete_usd)) * Decimal(str(cotacao_usd_brl))
    seguro_brl = Decimal(str(seguro_usd)) * Decimal(str(cotacao_usd_brl))
    
    # Calculate base for taxes (valor + frete + seguro)
    base_calculo = valor_brl + frete_brl + seguro_brl
    
    # Calculate each tax
    ii = base_calculo * Decimal(str(rates["ii"]))
    ipi = (base_calculo + ii) * Decimal(str(rates["ipi"]))
    pis_cofins = base_calculo * Decimal(str(rates["pis_cofins"]))
    icms = (base_calculo + ii + ipi + pis_cofins) * Decimal(str(rates["icms"]))
    siscomex = valor_brl * Decimal(str(rates["siscomex"]))
    
    # Total taxes
    total_tributos = ii + ipi + pis_cofins + icms + siscomex
    
    # Total cost
    custo_total = valor_brl + frete_brl + seguro_brl + total_tributos
    
    # Tax burden percentage
    onus_tributario = (float(total_tributos) / float(valor_brl)) * 100 if valor_brl > 0 else 0
    
    return {
        "valor_usd": valor_usd,
        "valor_brl": valor_brl,
        "frete_usd": frete_usd,
        "frete_brl": frete_brl,
        "seguro_usd": seguro_usd,
        "seguro_brl": seguro_brl,
        "ii": ii,
        "ipi": ipi,
        "pis_cofins": pis_cofins,
        "icms": icms,
        "siscomex": siscomex,
        "total_tributos": total_tributos,
        "custo_total": custo_total,
        "onus_tributario": round(onus_tributario, 2),
    }
