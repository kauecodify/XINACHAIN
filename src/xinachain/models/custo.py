"""Cost models for import cost calculation."""

from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Dict


class CustoImportacao(BaseModel):
    """
    Represents the complete import cost calculation.
    
    Attributes:
        valor_usd: Original value in USD
        valor_brl: Converted value in BRL
        frete_usd: Freight cost in USD
        frete_brl: Freight cost in BRL
        seguro_usd: Insurance cost in USD
        seguro_brl: Insurance cost in BRL
        ii: Import tax (II) in BRL
        ipi: IPI tax in BRL
        pis_cofins: PIS/COFINS tax in BRL
        icms: ICMS tax in BRL
        siscomex: Siscomex fee in BRL
        total_tributos: Total taxes in BRL
        custo_total: Total cost in BRL
        onus_tributario: Tax burden percentage
    """
    valor_usd: Decimal = Field(..., gt=0, description="Original value in USD")
    valor_brl: Decimal = Field(..., gt=0, description="Converted value in BRL")
    frete_usd: Decimal = Field(..., ge=0, description="Freight cost in USD")
    frete_brl: Decimal = Field(..., ge=0, description="Freight cost in BRL")
    seguro_usd: Decimal = Field(..., ge=0, description="Insurance cost in USD")
    seguro_brl: Decimal = Field(..., ge=0, description="Insurance cost in BRL")
    ii: Decimal = Field(..., ge=0, description="Import tax (II) in BRL")
    ipi: Decimal = Field(..., ge=0, description="IPI tax in BRL")
    pis_cofins: Decimal = Field(..., ge=0, description="PIS/COFINS tax in BRL")
    icms: Decimal = Field(..., ge=0, description="ICMS tax in BRL")
    siscomex: Decimal = Field(..., ge=0, description="Siscomex fee in BRL")
    total_tributos: Decimal = Field(..., ge=0, description="Total taxes in BRL")
    custo_total: Decimal = Field(..., gt=0, description="Total cost in BRL")
    onus_tributario: float = Field(..., ge=0, le=100, description="Tax burden percentage")
