"""Report models for executive reporting."""

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from .carga import Carga
from .risco import AnaliseRisco
from .custo import CustoImportacao


class Prioridade(str, Enum):
    """Priority level enumeration."""
    CURTO_PRAZO = "curto_prazo"
    MEDIO_PRAZO = "medio_prazo"
    LONGO_PRAZO = "longo_prazo"


class RelatorioExecutivo(BaseModel):
    """
    Represents an executive report.
    
    Attributes:
        carga: Associated cargo
        analise_risco: Risk analysis
        custo: Import cost calculation
        recomendacao_final: Final recommendation
        prioridade: Priority level
        data_geracao: Report generation date
    """
    carga: Carga = Field(..., description="Associated cargo")
    analise_risco: AnaliseRisco = Field(..., description="Risk analysis")
    custo: CustoImportacao = Field(..., description="Import cost calculation")
    recomendacao_final: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Final recommendation"
    )
    prioridade: Prioridade = Field(..., description="Priority level")
    data_geracao: datetime = Field(
        default_factory=datetime.now,
        description="Report generation date"
    )
