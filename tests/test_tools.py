"""Tests for tool functions."""

import pytest
from decimal import Decimal

from src.xinachain.tools.tributos import calcular_tributos


class TestCalcularTributos:
    """Tests for tax calculation."""
    
    @pytest.mark.asyncio
    async def test_calculo_tributos_smartphone(self):
        """Test tax calculation for smartphone NCM."""
        result = await calcular_tributos(
            ncm="8517.12.00",
            valor_usd=Decimal("100000"),
            frete_usd=Decimal("5000"),
            seguro_usd=Decimal("1000"),
            cotacao_usd_brl=5.0
        )
        
        assert result["valor_usd"] == Decimal("100000")
        assert result["valor_brl"] == Decimal("500000")
        assert result["ii"] > 0
        assert result["total_tributos"] > Decimal("100000")
        assert result["custo_total"] > result["valor_brl"]
    
    @pytest.mark.asyncio
    async def test_calculo_tributos_clothing(self):
        """Test tax calculation for clothing NCM."""
        result = await calcular_tributos(
            ncm="6109.10.00",
            valor_usd=Decimal("50000"),
            frete_usd=Decimal("2500"),
            seguro_usd=Decimal("500"),
            cotacao_usd_brl=5.0
        )
        
        assert result["valor_usd"] == Decimal("50000")
        assert result["valor_brl"] == Decimal("250000")
        assert result["ii"] > 0
        assert result["onus_tributario"] > 0
    
    @pytest.mark.asyncio
    async def test_calculo_tributos_default_ncm(self):
        """Test tax calculation with unknown NCM (uses default rates)."""
        result = await calcular_tributos(
            ncm="9999.99.99",
            valor_usd=Decimal("100000"),
            frete_usd=Decimal("5000"),
            seguro_usd=Decimal("1000"),
            cotacao_usd_brl=5.0
        )
        
        assert result["valor_usd"] == Decimal("100000")
        assert result["valor_brl"] == Decimal("500000")
        assert result["total_tributos"] > 0
    
    @pytest.mark.asyncio
    async def test_calculo_tributos_zero_values(self):
        """Test tax calculation with zero freight and insurance."""
        result = await calcular_tributos(
            ncm="8517.12.00",
            valor_usd=Decimal("100000"),
            frete_usd=Decimal("0"),
            seguro_usd=Decimal("0"),
            cotacao_usd_brl=5.0
        )
        
        assert result["valor_brl"] == Decimal("500000")
        assert result["frete_brl"] == Decimal("0")
        assert result["seguro_brl"] == Decimal("0")
        assert result["total_tributos"] > 0


class TestRastreio:
    """Tests for tracking tools."""
    
    @pytest.mark.asyncio
    async def test_consultar_status_navio(self):
        """Test ship status consultation."""
        from src.xinachain.tools.rastreio import consultar_status_navio
        
        result = await consultar_status_navio("COSCO Shipping")
        
        assert "navio" in result
        assert "posicao" in result
        assert "latitude" in result["posicao"]
        assert "longitude" in result["posicao"]
        assert "velocidade" in result
        assert "eta" in result
        assert "status" in result
    
    @pytest.mark.asyncio
    async def test_consultar_porto(self):
        """Test port status consultation."""
        from src.xinachain.tools.rastreio import consultar_porto
        
        result = await consultar_porto("Santos")
        
        assert "porto" in result
        assert "congestao" in result
        assert "tempo_espera_dias" in result
        assert "navios_em_espera" in result


class TestClima:
    """Tests for weather tools."""
    
    @pytest.mark.asyncio
    async def test_obter_clima_rota(self):
        """Test route weather consultation."""
        from src.xinachain.tools.clima import obter_clima_rota
        
        result = await obter_clima_rota("Shanghai", "Santos")
        
        assert "origem" in result
        assert "destino" in result
        assert "dias_viagem" in result
        assert "condicoes_climaticas" in result
        assert "risco_atraso_dias" in result
        assert "probabilidade_atraso" in result
