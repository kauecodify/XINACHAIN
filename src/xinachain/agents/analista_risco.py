"""Risk analyst agent for assessing cargo risks."""

from typing import Dict, Any
from pydantic_ai import Agent

from ..models.carga import Carga
from ..models.risco import AnaliseRisco
from ..tools.cambio import obter_cotacao_usd_brl, obter_cotacao_usd_cny
from ..tools.clima import obter_clima_rota


# Risk analyst agent
# Note: Using None for testing, in production use your actual model
analista_risco_agent = None  # Will be initialized with actual model in production


async def node_risco(carga: Carga) -> Dict[str, Any]:
    """
    Node function for risk analysis in the pipeline.
    
    Args:
        carga: Cargo to analyze
        
    Returns:
        Dictionary with risk analysis
    """
    # Get weather conditions for the route
    clima = await obter_clima_rota(carga.porto_origem, carga.porto_destino)
    
    # Get exchange rates
    cotacao_usd_brl = await obter_cotacao_usd_brl()
    cotacao_usd_cny = await obter_cotacao_usd_cny()
    
    # Calculate risk score (simplified for demonstration)
    # This would be more sophisticated in production
    risk_score = 0
    
    # Weather risk (0-25 points)
    if clima["risco_atraso_dias"] > 5:
        risk_score += 20
    elif clima["risco_atraso_dias"] > 2:
        risk_score += 10
    else:
        risk_score += 5
    
    # Currency risk (0-25 points)
    # Higher volatility = higher risk
    if cotacao_usd_brl > 5.5:
        risk_score += 15
    elif cotacao_usd_brl > 5.0:
        risk_score += 10
    else:
        risk_score += 5
    
    # Tariff risk based on NCM (0-25 points)
    # Electronics have higher tariff risk
    if carga.ncm.startswith("85"):
        risk_score += 20
    elif carga.ncm.startswith("61") or carga.ncm.startswith("62"):
        risk_score += 25
    else:
        risk_score += 10
    
    # Geopolitical risk (0-15 points)
    # China-Brazil route has moderate geopolitical risk
    risk_score += 10
    
    # Operational risk based on cargo value (0-10 points)
    if float(carga.valor_usd) > 1000000:
        risk_score += 10
    elif float(carga.valor_usd) > 500000:
        risk_score += 5
    
    # Ensure score is between 0 and 100
    risk_score = min(max(risk_score, 0), 100)
    
    # Determine overall risk level
    if risk_score >= 75:
        risco_global = "critico"
    elif risk_score >= 50:
        risco_global = "alto"
    elif risk_score >= 25:
        risco_global = "medio"
    else:
        risco_global = "baixo"
    
    # Create risk analysis
    analise = AnaliseRisco(
        riscos=[
            {
                "categoria": "clima",
                "nivel": "medio" if clima["risco_atraso_dias"] > 2 else "baixo",
                "descricao": f"Risco de atraso por condicoes climaticas: {clima['condicoes_climaticas']}",
                "impacto_dias": clima["risco_atraso_dias"],
                "impacto_financeiro": float(carga.valor_usd) * 0.01 * clima["risco_atraso_dias"],
                "mitigacao": "Monitorar previsao do tempo e considerar rota alternativa",
            },
            {
                "categoria": "moeda",
                "nivel": "medio" if cotacao_usd_brl > 5.2 else "baixo",
                "descricao": f"Risco cambial: USD/BRL = {cotacao_usd_brl}, USD/CNY = {cotacao_usd_cny}",
                "impacto_dias": 0,
                "impacto_financeiro": float(carga.valor_usd) * 0.05,
                "mitigacao": "Considerar hedge cambial para proteger contra variacoes",
            },
            {
                "categoria": "tarifario",
                "nivel": "alto" if carga.ncm.startswith("85") else "medio",
                "descricao": f"Risco tarifario para NCM {carga.ncm}",
                "impacto_dias": 0,
                "impacto_financeiro": float(carga.valor_usd) * 0.20,
                "mitigacao": "Verificar se ha beneficios tarifarios aplicaveis",
            },
        ],
        risco_global=risco_global,
        pontuacao_risco=risk_score,
        recomendacao=f"Pontuacao de risco: {risk_score}/100. Nivel: {risco_global}. Recomenda-se monitoramento constante.",
    )
    
    return {
        "analise_risco": analise,
        "clima": clima,
        "cotacao_usd_brl": cotacao_usd_brl,
        "cotacao_usd_cny": cotacao_usd_cny,
    }
