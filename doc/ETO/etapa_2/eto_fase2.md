# Fase 1 — Esqueleto do ENGINE

## 🔧 Rituais da Fase (fixos)

- **Branch base:** `develop`
- **Nome de feature:** `feature/e2-f1-s<sprint>-t<tarefa>-<slug>`
- **Commits semânticos:** `feat(engine)`, `docs(ETO)`, `chore(ci)`, `fix(trace)`
- **Checklist de PR:** testes verdes • headers presentes • spans OTel gerados •
  doc desta fase atualizado
- **DoD (Definition of Done):** critérios de aceite atendidos **+** comandos de
  verificação executáveis registrados

## Sprint 1

### Tarefa 1

- **ID:** E2-F1-S1-T1
- **Branch base:** develop
- **Branch de trabalho:** `feature/e2-f1-s1-t1-engine-skeleton`
- **Objetivo (one-liner):** Subir serviço FastAPI com status/health, correlação
  (X-Correlation-Id) e OTel.

**Escopo**:

- Endpoints `/api/v1/status`, `/api/v1/healthz`, `/api/v1/readyz`
- Middleware de correlação + header `X-API-Version`
- Instrumentação OpenTelemetry (pronto para OTLP)
- Testes de rota (pytest + httpx)

**Critérios de Aceite (verificáveis)**:

- `/api/v1/status` inclui `correlation_id` (body) **e** header
  `X-Correlation-Id`
- Todas as respostas têm `X-API-Version`
- `healthz` e `readyz` retornam `200` com `{ok}` / `{ready}`
- Pelo menos 2 spans OTel por requisição (server + handler)

**Comandos de verificação**:

```bash
poetry run pytest -q
curl -i http://localhost:8000/api/v1/status | grep -E "X-Correlation-Id|X-API-Version"
curl -s http://localhost:8000/api/v1/healthz
curl -s http://localhost:8000/api/v1/readyz
```

**Artefatos/Interfaces**:

- Headers: `X-Correlation-Id`, `X-API-Version`
- Observabilidade: OTLP export habilitável

**Diretórios/Arquivos (root)**:

- `app/core/{config.py,telemetry.py,correlation.py}`
- `app/api/v1/routers/status.py`
- `app/main.py`, `tests/test_status.py`, `.env.example`, `pyproject.toml`

**Commit sugerido**:

- `feat(engine): esqueleto FastAPI + status/health + X-Correlation-Id + OTel`

**Riscos & rollback**:

- Sem dependência de DB; rollback via revert do merge

**Documentos relacionados**:

- `/doc/ETO/etapa_2/overview.md`
- `/doc/ETO/etapa_2/eto_fase1.md`

---

### Tarefa 2

- **ID:** E2-F1-S1-T2
- **Branch base:** develop
- **Branch de trabalho:** `feature/e2-f1-s1-t2-ports-and-stubs`
- **Objetivo (one-liner):** Definir ports ECL do ENGINE, criar stubs e pontos de
  injeção (DI) sem tocar DB.

**Escopo**:

- Ports em `app/domain/ports.py` (EchoRepo, TraceRepo, PulseSource, AnchorRepo)
- Tipos leves em `app/domain/models.py` (Echo, Trace, Pulse, Anchor, Context)
- Stubs em `app/adapters/stubs/*` (levantam `NotImplementedError`)
- DI em `app/api/deps.py` (`get_*` retornando stubs)
- Teste de contrato import/assinatura/exceção

**Critérios de Aceite (verificáveis)**:

- Imports e assinaturas dos ports estáveis
- Injeção dos stubs via `Depends` em rota de exemplo
- Teste valida `NotImplementedError` padronizado nos stubs

**Comandos de verificação**:

```bash
poetry run pytest -q tests/test_ports_contract.py
python -c "import app.domain.ports as p; print([a for a in dir(p) if a.endswith('Repo') or a.endswith('Source')])"
```

**Artefatos/Interfaces**:

- Ports: `EchoRepo`, `TraceRepo`, `PulseSource`, `AnchorRepo`
- Contexto: `Context` com `correlation_id` e metadados

**Diretórios/Arquivos (root)**:

- `app/domain/{ports.py,models.py}`
- `app/adapters/stubs/`
- `app/api/deps.py`
- `tests/test_ports_contract.py`

**Commit sugerido**:

- `feat(engine): ports ECL + stubs + DI prontos para integração`

**Riscos & rollback**:

- Quebra de contrato futura — mitigado por testes de assinatura; rollback via
  revert

**Documentos relacionados**:

- `/doc/ETO/etapa_2/overview.md`
- `/doc/ETO/etapa_2/eto_fase1.md`
- `/doc/ETO/etapa_1_5/ECHO_CODEX.md`

---

## 🧩 Matriz ECL (Sprint 1)

- **Act (ENGINE):** handlers `status/health`
- **State (MEMORY):** n/a (definição de ports na T2; sem persistência)
- **Context (SPACE):** `X-Correlation-Id` (+ `X-API-Version`)
- **Event/Echo:** preparado (emissão futura via outbox)
- **Trace:** spans OTel ativos na T1

---
