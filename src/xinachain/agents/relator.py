"""Reporter agent for generating executive reports."""

from typing import Dict, Any
from pydantic_ai import Agent

from ..models.carga import Carga
from ..models.risco import AnaliseRisco
from ..models.custo import CustoImportacao
from ..models.relatorio import RelatorioExecutivo, Prioridade
from datetime import datetime


# Reporter agent
# Note: Using None for testing, in production use your actual model
relator_agent = None  # Will be initialized with actual model in production


async def node_relatorio(
    carga: Carga,
    analise_risco: AnaliseRisco,
    custo: CustoImportacao
) -> Dict[str, Any]:
    """
    Node function for report generation in the pipeline.
    
    Args:
        carga: Cargo data
        analise_risco: Risk analysis data
        custo: Cost calculation data
        
    Returns:
        Dictionary with executive report
    """
    # Determine priority based on risk score and cost
    if analise_risco.pontuacao_risco >= 75 or custo.onus_tributario > 60:
        prioridade = Prioridade.CURTO_PRAZO
    elif analise_risco.pontuacao_risco >= 50 or custo.onus_tributario > 40:
        prioridade = Prioridade.MEDIO_PRAZO
    else:
        prioridade = Prioridade.LONGO_PRAZO
    
    # Generate final recommendation
    recomendacao_final = f"""
    Analise da carga {carga.id} ({carga.descricao}):
    
    Risco Global: {analise_risco.risco_global.value}
    Pontuacao de Risco: {analise_risco.pontuacao_risco}/100
    
    Custo Total: R$ {custo.custo_total:,.2f}
    Onus Tributario: {custo.onus_tributario:.1f}%
    
    Principais Riscos:
    {chr(10).join([f'- {risco.descricao} ({risco.nivel.value})' for risco in analise_risco.riscos])}
    
    Recomendacao: {analise_risco.recomendacao}
    
    Prioridade: {prioridade.value}
    """
    
    # Create report
    relatorio = RelatorioExecutivo(
        carga=carga,
        analise_risco=analise_risco,
        custo=custo,
        recomendacao_final=recomendacao_final,
        prioridade=prioridade,
        data_geracao=datetime.now(),
    )
    
    return {
        "relatorio": relatorio,
    }
