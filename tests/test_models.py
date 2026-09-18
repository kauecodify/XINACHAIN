"""Tests for Pydantic models."""

import pytest
from datetime import date
from decimal import Decimal

from src.xinachain.models.carga import Carga
from src.xinachain.models.risco import Risco, AnaliseRisco, RiscoNivel, RiscoCategoria
from src.xinachain.models.custo import CustoImportacao
from src.xinachain.models.relatorio import RelatorioExecutivo, Prioridade


class TestCarga:
    """Tests for Carga model."""
    
    def test_carga_creation(self):
        """Test creating a valid Carga."""
        carga = Carga(
            id="XINA-2026-001",
            descricao="5G Smartphones - 10,000 units",
            ncm="8517.12.00",
            valor_usd=Decimal("1000000.00"),
            peso_kg=5000.0,
            navio="COSCO Shipping",
            porto_origem="Shanghai",
            porto_destino="Santos",
            data_embarque=date(2026, 1, 1),
            data_chegada_prevista=date(2026, 2, 1),
            status="em_transito",
        )
        
        assert carga.id == "XINA-2026-001"
        assert carga.descricao == "5G Smartphones - 10,000 units"
        assert carga.ncm == "8517.12.00"
        assert carga.valor_usd == Decimal("1000000.00")
        assert carga.peso_kg == 5000.0
        assert carga.navio == "COSCO Shipping"
        assert carga.porto_origem == "Shanghai"
        assert carga.porto_destino == "Santos"
        assert carga.status == "em_transito"
    
    def test_carga_invalid_ncm(self):
        """Test that invalid NCM code raises validation error."""
        with pytest.raises(Exception):
            Carga(
                id="XINA-2026-001",
                descricao="Test",
                ncm="invalid",
                valor_usd=Decimal("100.00"),
                peso_kg=100.0,
                navio="Test Ship",
                porto_origem="Port A",
                porto_destino="Port B",
                data_embarque=date(2026, 1, 1),
                data_chegada_prevista=date(2026, 2, 1),
            )
    
    def test_carga_negative_value(self):
        """Test that negative value raises validation error."""
        with pytest.raises(Exception):
            Carga(
                id="XINA-2026-001",
                descricao="Test",
                ncm="8517.12.00",
                valor_usd=Decimal("-100.00"),
                peso_kg=100.0,
                navio="Test Ship",
                porto_origem="Port A",
                porto_destino="Port B",
                data_embarque=date(2026, 1, 1),
                data_chegada_prevista=date(2026, 2, 1),
            )


class TestRisco:
    """Tests for Risco and AnaliseRisco models."""
    
    def test_risco_creation(self):
        """Test creating a valid Risco."""
        risco = Risco(
            categoria=RiscoCategoria.CLIMA,
            nivel=RiscoNivel.MEDIO,
            descricao="Risco de atraso por chuva",
            impacto_dias=5,
            impacto_financeiro=10000.0,
            mitigacao="Monitorar previsao do tempo",
        )
        
        assert risco.categoria == RiscoCategoria.CLIMA
        assert risco.nivel == RiscoNivel.MEDIO
        assert risco.descricao == "Risco de atraso por chuva"
        assert risco.impacto_dias == 5
        assert risco.impacto_financeiro == 10000.0
        assert risco.mitigacao == "Monitorar previsao do tempo"
    
    def test_analise_risco_creation(self):
        """Test creating a valid AnaliseRisco."""
        riscos = [
            Risco(
                categoria=RiscoCategoria.CLIMA,
                nivel=RiscoNivel.MEDIO,
                descricao="Risco de atraso por chuva",
                impacto_dias=5,
                impacto_financeiro=10000.0,
                mitigacao="Monitorar previsao do tempo",
            )
        ]
        
        analise = AnaliseRisco(
            riscos=riscos,
            risco_global=RiscoNivel.MEDIO,
            pontuacao_risco=50,
            recomendacao="Monitorar condicoes climaticas",
        )
        
        assert len(analise.riscos) == 1
        assert analise.risco_global == RiscoNivel.MEDIO
        assert analise.pontuacao_risco == 50
        assert analise.recomendacao == "Monitorar condicoes climaticas"


class TestCustoImportacao:
    """Tests for CustoImportacao model."""
    
    def test_custo_creation(self):
        """Test creating a valid CustoImportacao."""
        custo = CustoImportacao(
            valor_usd=Decimal("100000.00"),
            valor_brl=Decimal("500000.00"),
            frete_usd=Decimal("5000.00"),
            frete_brl=Decimal("25000.00"),
            seguro_usd=Decimal("1000.00"),
            seguro_brl=Decimal("5000.00"),
            ii=Decimal("20000.00"),
            ipi=Decimal("15000.00"),
            pis_cofins=Decimal("9250.00"),
            icms=Decimal("85000.00"),
            siscomex=Decimal("5500.00"),
            total_tributos=Decimal("129750.00"),
            custo_total=Decimal("659750.00"),
            onus_tributario=42.3,
        )
        
        assert custo.valor_usd == Decimal("100000.00")
        assert custo.valor_brl == Decimal("500000.00")
        assert custo.total_tributos == Decimal("129750.00")
        assert custo.custo_total == Decimal("659750.00")
        assert custo.onus_tributario == 42.3


class TestRelatorioExecutivo:
    """Tests for RelatorioExecutivo model."""
    
    def test_relatorio_creation(self):
        """Test creating a valid RelatorioExecutivo."""
        carga = Carga(
            id="XINA-2026-001",
            descricao="5G Smartphones",
            ncm="8517.12.00",
            valor_usd=Decimal("100000.00"),
            peso_kg=5000.0,
            navio="COSCO",
            porto_origem="Shanghai",
            porto_destino="Santos",
            data_embarque=date(2026, 1, 1),
            data_chegada_prevista=date(2026, 2, 1),
        )
        
        riscos = [
            Risco(
                categoria=RiscoCategoria.CLIMA,
                nivel=RiscoNivel.MEDIO,
                descricao="Risco de atraso",
                impacto_dias=3,
                impacto_financeiro=5000.0,
                mitigacao="Monitorar",
            )
        ]
        
        analise = AnaliseRisco(
            riscos=riscos,
            risco_global=RiscoNivel.MEDIO,
            pontuacao_risco=45,
            recomendacao="Monitorar",
        )
        
        custo = CustoImportacao(
            valor_usd=Decimal("100000.00"),
            valor_brl=Decimal("500000.00"),
            frete_usd=Decimal("5000.00"),
            frete_brl=Decimal("25000.00"),
            seguro_usd=Decimal("1000.00"),
            seguro_brl=Decimal("5000.00"),
            ii=Decimal("20000.00"),
            ipi=Decimal("15000.00"),
            pis_cofins=Decimal("9250.00"),
            icms=Decimal("85000.00"),
            siscomex=Decimal("5500.00"),
            total_tributos=Decimal("129750.00"),
            custo_total=Decimal("659750.00"),
            onus_tributario=42.3,
        )
        
        relatorio = RelatorioExecutivo(
            carga=carga,
            analise_risco=analise,
            custo=custo,
            recomendacao_final="Aprovar com monitoramento",
            prioridade=Prioridade.MEDIO_PRAZO,
        )
        
        assert relatorio.carga.id == "XINA-2026-001"
        assert relatorio.analise_risco.pontuacao_risco == 45
        assert relatorio.custo.custo_total == Decimal("659750.00")
        assert relatorio.prioridade == Prioridade.MEDIO_PRAZO
        assert "Aprovar" in relatorio.recomendacao_final
