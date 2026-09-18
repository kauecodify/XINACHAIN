"""Risk models for risk analysis."""

from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional


class RiscoNivel(str, Enum):
    """Risk level enumeration."""
    BAIXO = "baixo"
    MEDIO = "medio"
    ALTO = "alto"
    CRITICO = "critico"


class RiscoCategoria(str, Enum):
    """Risk category enumeration."""
    CLIMA = "clima"
    MOEDA = "moeda"
    TARIFARIO = "tarifario"
    GEOPOLITICO = "geopolitico"
    OPERACIONAL = "operacional"


class Risco(BaseModel):
    """
    Represents a single risk assessment.
    
    Attributes:
        categoria: Risk category
        nivel: Risk level
        descricao: Description of the risk
        impacto_dias: Impact in days
        impacto_financeiro: Financial impact in BRL
        mitigacao: Mitigation suggestion
    """
    categoria: RiscoCategoria = Field(..., description="Risk category")
    nivel: RiscoNivel = Field(..., description="Risk level")
    descricao: str = Field(..., min_length=1, max_length=500, description="Risk description")
    impacto_dias: int = Field(..., ge=0, description="Impact in days")
    impacto_financeiro: float = Field(..., ge=0, description="Financial impact in BRL")
    mitigacao: str = Field(..., min_length=1, max_length=500, description="Mitigation suggestion")


class AnaliseRisco(BaseModel):
    """
    Represents a complete risk analysis.
    
    Attributes:
        riscos: List of identified risks
        risco_global: Overall risk level
        pontuacao_risco: Risk score from 0 to 100
        recomendacao: General recommendation
    """
    riscos: List[Risco] = Field(..., min_length=1, description="List of identified risks")
    risco_global: RiscoNivel = Field(..., description="Overall risk level")
    pontuacao_risco: int = Field(..., ge=0, le=100, description="Risk score from 0 to 100")
    recomendacao: str = Field(..., min_length=1, max_length=1000, description="General recommendation")
