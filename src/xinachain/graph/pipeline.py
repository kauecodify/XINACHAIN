"""LangGraph pipeline for XINACHAIN."""

from typing import Dict, Any, TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from ..models.carga import Carga
from ..models.risco import AnaliseRisco
from ..models.custo import CustoImportacao
from ..models.relatorio import RelatorioExecutivo
from ..agents.rastreador import node_rastreio
from ..agents.analista_risco import node_risco
from ..agents.calculista import node_custo
from ..agents.relator import node_relatorio


class XinaState(TypedDict, total=False):
    """State for the XINACHAIN pipeline."""
    carga: Optional[Carga]
    status_rastreio: Optional[str]
    analise_risco: Optional[AnaliseRisco]
    custo: Optional[CustoImportacao]
    relatorio: Optional[RelatorioExecutivo]


def build_xinachain_graph() -> Any:
    """
    Build the XINACHAIN pipeline graph.
    
    Returns:
        Compiled LangGraph graph
    """
    # Create the graph
    graph = StateGraph(XinaState)
    
    # Add nodes
    graph.add_node("rastreio", node_rastreio)
    graph.add_node("risco", node_risco)
    graph.add_node("custo", node_custo)
    graph.add_node("relatorio", node_relatorio)
    
    # Add edges
    graph.add_edge(START, "rastreio")
    graph.add_edge("rastreio", "risco")
    graph.add_edge("risco", "custo")
    graph.add_edge("custo", "relatorio")
    graph.add_edge("relatorio", END)
    
    # Compile the graph
    return graph.compile()


# Create the pipeline
xinachain_pipeline = build_xinachain_graph()
