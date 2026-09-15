<img width="100" height="100" alt="image" src="https://github.com/user-attachments/assets/1de207e9-2ba9-46e6-ad7d-a01526f5a1ec" />


# XINACHAIN

Multi-agent system for supply chain intelligence between China and Brazil. It monitors cargo, assesses risks, calculates import costs, and generates executive reports automatically.

---

## Overview

XinaChain is a Python application that orchestrates multiple autonomous agents to analyze an international shipment. Each agent is specialized in one stage of the process and uses external tools to obtain real or simulated data. The final output is a structured and validated executive report.

The application demonstrates in practice:

- Use of PydanticAI for agents with data validation.
- Orchestration with LangGraph in a sequential pipeline.
- Integration with local LLMs via Ollama or external APIs.
- Tools for currency exchange, taxes, weather, and tracking.
- Pydantic models for input and output contracts.

---

## Application Architecture

```
+-------------+     +----------------+     +----------------+     +-------------+
|  CLI/API    | --> |  LangGraph     | --> |  Agents        | --> |  External   |
|  (input)    |     |  Pipeline      |     |  (PydanticAI)  |     |  Tools      |
+-------------+     +----------------+     +----------------+     +-------------+
                                                      |
                                                      v
                                            +----------------+
                                            |  Pydantic      |
                                            |  Models        |
                                            +----------------+
                                                      |
                                                      v
                                            +----------------+
                                            |  Executive     |
                                            |  Report        |
                                            +----------------+
```

The application is divided into five layers:

1. **Input**: CLI receives a validated `Carga` object.
2. **Orchestration**: LangGraph executes the agents sequentially.
3. **Agents**: each agent uses PydanticAI and specific tools.
4. **Tools**: external functions for currency, taxes, weather, and tracking.
5. **Output**: executive report validated by a Pydantic model.

---

## Execution Flow

The pipeline is defined as a state graph. The `XinaState` carries data between nodes.

```
START
  |
  v
[tracking] --> [risk] --> [cost] --> [report] --> END
```

Each node executes an agent and updates the state:

1. **tracking**: queries ship status and port congestion.
2. **risk**: assesses weather, currency, tariff, and geopolitical risks.
3. **cost**: calculates import taxes (II, IPI, PIS/COFINS, ICMS, Siscomex).
4. **report**: generates an executive report with recommendation and priority.

The state is typed with `TypedDict`:

```python
class XinaState(TypedDict, total=False):
    carga: Carga
    status_rastreio: str
    analise_risco: AnaliseRisco
    custo: CustoImportacao
    relatorio: RelatorioExecutivo
```

---

## Components

### Data Models

All contracts are defined with Pydantic. This ensures type, limit, and format validation.

- `Carga`: id, description, NCM, USD value, weight, ports, dates, status.
- `Risco`: category, level, impact in days and financial, mitigation.
- `AnaliseRisco`: list of risks, overall risk, score from 0 to 100.
- `CustoImportacao`: BRL values, taxes, total cost, tax burden.
- `RelatorioExecutivo`: cargo, risk analysis, cost, recommendation, priority.

Validation example:

```python
class Carga(BaseModel):
    ncm: str = Field(pattern=r"^\d{4}\.\d{2}\.\d{2}$")
    valor_usd: float = Field(gt=0, le=10_000_000)
    peso_kg: float = Field(gt=0)
```

### Tools

Tools are asynchronous functions that agents can invoke.

- `consultar_status_navio(navio)`: returns position, speed, and ETA.
- `consultar_porto(porto)`: returns congestion and waiting time.
- `obter_cotacao_usd_brl()`: fetches USD/BRL exchange rate.
- `obter_cotacao_usd_cny()`: fetches USD/CNY exchange rate.
- `calcular_tributos(ncm, valor, frete, seguro)`: calculates II, IPI, PIS/COFINS, ICMS, Siscomex.
- `obter_clima_rota(origem, destino)`: returns weather conditions and delay risk.

### Agents

Each agent is an instance of `pydantic_ai.Agent` with `deps_type` and `output_type` defined.

| Agent | Input | Output | Tools |
|--------|---------|-------|-------------|
| Tracker | Carga | str | status_navio, status_porto |
| Risk Analyst | Carga | AnaliseRisco | cotacao_dolar, clima_rota |
| Cost Calculator | Carga | CustoImportacao | cotacao, tributos |
| Reporter | Consolidated text | RelatorioExecutivo | — |

Definition example:

```python
analista_risco = Agent(
    model="openai:gpt-4o-mini",
    deps_type=Carga,
    output_type=AnaliseRisco,
    system_prompt="Assess risks for China-Brazil cargo."
)
```

### LangGraph Pipeline

The pipeline is built with `StateGraph` and compiled.

```python
def build_xinachain_graph():
    g = StateGraph(XinaState)
    g.add_node("rastreio", node_rastreio)
    g.add_node("risco", node_risco)
    g.add_node("custo", node_custo)
    g.add_node("relatorio", node_relatorio)
    g.add_edge(START, "rastreio")
    g.add_edge("rastreio", "risco")
    g.add_edge("risco", "custo")
    g.add_edge("custo", "relatorio")
    g.add_edge("relatorio", END)
    return g.compile()
```

### CLI

The CLI uses `rich` to display the final report.

```python
async def analisar(carga: Carga):
    result = await xinachain_pipeline.ainvoke({"carga": carga})
    rel = result["relatorio"]
    console.print(Panel(f"Recommendation: {rel.recomendacao_final}"))
```

---

## Directory Structure

```
xinachain/
├── pyproject.toml
├── README.md
├── .env.example
├── src/
│   └── xinachain/
│       ├── __init__.py
│       ├── config.py
│       ├── models/
│       │   ├── carga.py
│       │   ├── risco.py
│       │   ├── custo.py
│       │   └── relatorio.py
│       ├── tools/
│       │   ├── rastreio.py
│       │   ├── cambio.py
│       │   ├── tributos.py
│       │   └── clima.py
│       ├── agents/
│       │   ├── rastreador.py
│       │   ├── analista_risco.py
│       │   ├── calculista.py
│       │   └── relator.py
│       ├── graph/
│       │   └── pipeline.py
│       └── cli.py
└── tests/
    └── test_agents.py
```

---

## How to Run

1. Install dependencies:

```bash
pip install -e .
```

2. Start Ollama and download the model (optional, if using a local LLM):

```bash
ollama pull gpt-oss:20b
ollama serve
```

3. Configure the `.env` file (optional):

```bash
cp .env.example .env
```

4. Run the application:

```bash
xinachain
```

5. Run the tests:

```bash
pytest tests/ -v
```

---

## Example Output

```
Analysis of cargo XINA-2026-001
Description: 5G Smartphones - 10,000 units
Overall risk: medium
Risk score: 45
Total cost: R$ 8,750,000.00
Tax burden: 42.3%
Recommendation: Monitor congestion at the Port of Santos and consider an alternative route via Paranaguá.
Priority: short_term
```

---

## Tests

Tests cover model validation, tax calculation, and pipeline integrity.

```bash
pytest tests/ -v
```

Test example:

```python
def test_calculo_tributos_smartphone():
    r = calcular_tributos("8517.12.00", Decimal("100000"), Decimal("5000"), Decimal("1000"))
    assert r["ii"] > 0
    assert r["total"] > Decimal("100000")
```

---

## Final Considerations

XinaChain demonstrates how to build a real multi-agent application with PydanticAI and LangGraph. The architecture is modular, testable, and extensible. New agents, tools, or models can be added without changing the system core.

To adapt the application to other domains, simply replace the Pydantic models, tools, and agent prompts, while keeping the orchestration pipeline.
