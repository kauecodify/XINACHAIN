"""Carga model for shipment data."""

from decimal import Decimal
from datetime import date
from pydantic import BaseModel, Field
from typing import Optional


class Carga(BaseModel):
    """
    Represents a cargo shipment with all necessary details.
    
    Attributes:
        id: Unique identifier for the cargo
        descricao: Description of the cargo
        ncm: NCM code (Brazilian customs classification)
        valor_usd: Value of the cargo in USD
        peso_kg: Weight of the cargo in kilograms
        navio: Name of the ship
        porto_origem: Port of origin
        porto_destino: Destination port
        data_embarque: Embarkation date
        data_chegada_prevista: Expected arrival date
        status: Current status of the cargo
    """
    id: str = Field(..., min_length=1, max_length=50, description="Unique cargo identifier")
    descricao: str = Field(..., min_length=1, max_length=500, description="Cargo description")
    ncm: str = Field(
        ...,
        pattern=r"^\d{4}\.\d{2}\.\d{2}$",
        description="NCM code in format XXXX.XX.XX"
    )
    valor_usd: Decimal = Field(..., gt=0, le=Decimal("10000000"), description="Cargo value in USD")
    peso_kg: float = Field(..., gt=0, description="Cargo weight in kg")
    navio: str = Field(..., min_length=1, max_length=100, description="Ship name")
    porto_origem: str = Field(..., min_length=1, max_length=100, description="Origin port")
    porto_destino: str = Field(..., min_length=1, max_length=100, description="Destination port")
    data_embarque: date = Field(..., description="Embarkation date")
    data_chegada_prevista: date = Field(..., description="Expected arrival date")
    status: str = Field(
        default="em_transito",
        min_length=1,
        max_length=50,
        description="Current cargo status"
    )
