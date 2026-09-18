"""CLI for XINACHAIN."""

import asyncio
import click
from datetime import date
from decimal import Decimal
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .models.carga import Carga
from .graph.pipeline import xinachain_pipeline


console = Console()


@click.group()
def cli():
    """XINACHAIN - Multi-agent system for supply chain intelligence."""
    pass


@cli.command()
@click.option(
    "--id",
    "cargo_id",
    default="XINA-2026-001",
    help="Cargo identifier"
)
@click.option(
    "--descricao",
    "cargo_desc",
    default="5G Smartphones - 10,000 units",
    help="Cargo description"
)
@click.option(
    "--ncm",
    "cargo_ncm",
    default="8517.12.00",
    help="NCM code (format: XXXX.XX.XX)"
)
@click.option(
    "--valor-usd",
    "cargo_valor",
    type=float,
    default=1000000.0,
    help="Cargo value in USD"
)
@click.option(
    "--peso-kg",
    "cargo_peso",
    type=float,
    default=5000.0,
    help="Cargo weight in kg"
)
@click.option(
    "--navio",
    "cargo_navio",
    default="COSCO Shipping",
    help="Ship name"
)
@click.option(
    "--origem",
    "cargo_origem",
    default="Shanghai",
    help="Origin port"
)
@click.option(
    "--destino",
    "cargo_destino",
    default="Santos",
    help="Destination port"
)
async def analisar(
    cargo_id: str,
    cargo_desc: str,
    cargo_ncm: str,
    cargo_valor: float,
    cargo_peso: float,
    cargo_navio: str,
    cargo_origem: str,
    cargo_destino: str,
):
    """Analyze a cargo shipment and generate an executive report."""
    console.print(Panel("[bold blue]XINACHAIN[/bold blue] - Analise de Carga", border_style="blue"))
    console.print(f"\nAnalisando carga: {cargo_id}...\n")
    
    # Create cargo object
    carga = Carga(
        id=cargo_id,
        descricao=cargo_desc,
        ncm=cargo_ncm,
        valor_usd=Decimal(str(cargo_valor)),
        peso_kg=cargo_peso,
        navio=cargo_navio,
        porto_origem=cargo_origem,
        porto_destino=cargo_destino,
        data_embarque=date.today(),
        data_chegada_prevista=date.today(),
        status="em_transito",
    )
    
    # Display cargo information
    console.print(Panel("[bold]Informacoes da Carga[/bold]", border_style="green"))
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Campo", style="white")
    table.add_column("Valor", style="yellow")
    
    table.add_row("ID", carga.id)
    table.add_row("Descricao", carga.descricao)
    table.add_row("NCM", carga.ncm)
    table.add_row("Valor (USD)", f"${carga.valor_usd:,.2f}")
    table.add_row("Peso (kg)", f"{carga.peso_kg:,.2f}")
    table.add_row("Navio", carga.navio)
    table.add_row("Origem", carga.porto_origem)
    table.add_row("Destino", carga.porto_destino)
    table.add_row("Status", carga.status)
    
    console.print(table)
    console.print()
    
    # Run pipeline
    try:
        result = await xinachain_pipeline.ainvoke({"carga": carga})
        
        relatorio = result["relatorio"]
        analise_risco = relatorio.analise_risco
        custo = relatorio.custo
        
        # Display risk analysis
        console.print(Panel("[bold]Analise de Risco[/bold]", border_style="red"))
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Campo", style="white")
        table.add_column("Valor", style="yellow")
        
        table.add_row("Risco Global", analise_risco.risco_global.value)
        table.add_row("Pontuacao", f"{analise_risco.pontuacao_risco}/100")
        table.add_row("Recomendacao", analise_risco.recomendacao)
        
        console.print(table)
        console.print()
        
        # Display risks
        console.print(Panel("[bold]Riscos Identificados[/bold]", border_style="magenta"))
        for i, risco in enumerate(analise_risco.riscos, 1):
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Campo", style="white")
            table.add_column("Valor", style="yellow")
            
            table.add_row("#", str(i))
            table.add_row("Categoria", risco.categoria.value)
            table.add_row("Nivel", risco.nivel.value)
            table.add_row("Descricao", risco.descricao)
            table.add_row("Impacto (dias)", str(risco.impacto_dias))
            table.add_row("Impacto (BRL)", f"R$ {risco.impacto_financeiro:,.2f}")
            table.add_row("Mitigacao", risco.mitigacao)
            
            console.print(table)
            console.print()
        
        # Display cost analysis
        console.print(Panel("[bold]Analise de Custos[/bold]", border_style="cyan"))
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Campo", style="white")
        table.add_column("Valor", style="yellow")
        
        table.add_row("Valor (USD)", f"${custo.valor_usd:,.2f}")
        table.add_row("Valor (BRL)", f"R$ {custo.valor_brl:,.2f}")
        table.add_row("Frete (USD)", f"${custo.frete_usd:,.2f}")
        table.add_row("Frete (BRL)", f"R$ {custo.frete_brl:,.2f}")
        table.add_row("Seguro (USD)", f"${custo.seguro_usd:,.2f}")
        table.add_row("Seguro (BRL)", f"R$ {custo.seguro_brl:,.2f}")
        table.add_row("II (BRL)", f"R$ {custo.ii:,.2f}")
        table.add_row("IPI (BRL)", f"R$ {custo.ipi:,.2f}")
        table.add_row("PIS/COFINS (BRL)", f"R$ {custo.pis_cofins:,.2f}")
        table.add_row("ICMS (BRL)", f"R$ {custo.icms:,.2f}")
        table.add_row("Siscomex (BRL)", f"R$ {custo.siscomex:,.2f}")
        table.add_row("Total Tributos (BRL)", f"R$ {custo.total_tributos:,.2f}")
        table.add_row("Custo Total (BRL)", f"R$ {custo.custo_total:,.2f}")
        table.add_row("Onus Tributario", f"{custo.onus_tributario:.2f}%")
        
        console.print(table)
        console.print()
        
        # Display executive report
        console.print(Panel("[bold]Relatorio Executivo[/bold]", border_style="yellow"))
        console.print(f"[bold]Recomendacao Final:[/bold]\n{relatorio.recomendacao_final}\n")
        console.print(f"[bold]Prioridade:[/bold] {relatorio.prioridade.value}")
        console.print(f"[bold]Data Geracao:[/bold] {relatorio.data_geracao}")
        
    except Exception as e:
        console.print(Panel(f"[bold red]Erro ao processar carga:[/bold red] {str(e)}", border_style="red"))
        raise click.ClickException(f"Error processing cargo: {str(e)}")


@cli.command()
def version():
    """Display version information."""
    from . import __version__
    console.print(Panel(f"[bold blue]XINACHAIN[/bold blue] v{__version__}", border_style="blue"))


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    asyncio.run(main())
