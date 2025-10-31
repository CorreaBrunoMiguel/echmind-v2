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

perfeito — bora carimbar a Tarefa 2 com testes e um commit limpinho, e já deixo
a próxima Tarefa (T3) pronta no formato **Registro Orion — Pt.1**.

## Comandos rápidos de teste

```bash
# 1) Executar TODOS os testes
poetry run pytest -q

# 2) Só o contrato de ports/stubs/DI (Tarefa 2)
poetry run pytest -q tests/test_ports_contract.py

# 3) Subir o serviço para checagens manuais (em outro terminal)
poetry run uvicorn app.main:app --reload

# 4) Verificações manuais (headers e DI)
curl -i http://localhost:8000/api/v1/status | grep -E "X-Correlation-Id|X-API-Version"
curl -s http://localhost:8000/api/v1/healthz
curl -s http://localhost:8000/api/v1/readyz
curl -s http://localhost:8000/api/v1/dev/di-check | jq .
# (se não tiver jq: apenas remova " | jq .")
```

## Mensagem de commit (Tarefa 2 — geral, com emoji)

```git
✨ feat(engine): ports ECL + stubs + DI (rota /api/v1/dev/di-check)
```

---

### Tarefa 3 — DTOs de Transporte (Pydantic) + Problem Details (RFC7807)

- **ID:** E2-F1-S1-T3
- **Branch base:** develop
- **Branch de trabalho:**
  `feature/e2-f1-s1-t3-transport-schemas-problem-details`
- **Objetivo (one-liner):** Definir schemas Pydantic (ECL) e padronizar erros em
  `application/problem+json` com `X-Correlation-Id`.

**Escopo**:

- Schemas Pydantic: `StatusOut`, `EchoIn`, `EchoOut`, `TraceOut`, `PulseOut`,
  `Problem`
- Mapeador de erros RFC7807 em `app/api/errors.py` (inclui `correlation_id` e
  `instance`)
- Handler de exemplo que dispara `Problem` para teste
- Ajuste de responses para sempre devolver `X-API-Version` e `X-Correlation-Id`

**Critérios de Aceite (verificáveis)**:

- Qualquer exceção mapeada retorna `application/problem+json` com: `type`,
  `title`, `status`, `detail`, `instance`, `correlation_id`
- `GET /api/v1/status` segue válido e inclui cabeçalhos
- Teste valida headers + estrutura completa de `Problem`

**Artefatos/Interfaces**:

- Headers: `X-Correlation-Id`, `X-API-Version`
- Content-Type de erro: `application/problem+json`

**Diretórios/Arquivos (root)**:

- `app/api/schemas.py`
- `app/api/errors.py`
- `tests/test_problem_details.py`

**Commit sugerido**:

- `🛡️ feat(engine): DTOs Pydantic + Problem Details (RFC7807) com correlation id`

**Riscos & rollback**:

- Padronização de erro afetar rotas futuras — mitigado por testes de contrato;
  rollback via revert

**Documentos relacionados**:

- `/doc/ETO/etapa_2/overview.md`
- `/doc/ETO/etapa_2/eto_fase1.md`
- `/doc/ETO/etapa_1_5/ECHO_CODEX.md`

---
