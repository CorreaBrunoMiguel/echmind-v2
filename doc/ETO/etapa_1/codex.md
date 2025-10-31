# Etapa 1.5 — **ECHO CODEX** (Consolidação Estrutural)

**Arquivo:** `/doc/ETO/etapa_1_5/ECHO_CODEX.md` **Projeto:** ECHOMIND v2 •
**Stack:** FastAPI + PostgreSQL • **Arquitetura:** ENGINE / MEMORY / SPACE
**Função do CODEX:** marco de transição _documentação → implementação_;
referência única para decisões técnicas, semânticas e de governança.

---

## 📖 Resumo

O CODEX solidifica o que foi definido nas Etapas 0–1: **ECL (Echo Core
Language)**, **ECHO LOOP**, invariantes (idempotência, rastreabilidade,
contratos), e os papéis de **ENGINE/MEMORY/SPACE**. Aqui também fica o **mapa de
Etapas 2–X** (apenas macro-escopo, sem fases/sprints), as **interfaces
canônicas**, a **governança de branches/releases**, e os **critérios globais de
qualidade**.

---

## 🔁 Princípios Invariantes

- **ECHO LOOP:** Perceber (SPACE) → Agir (ENGINE) → Reter/Interpretar (MEMORY) →
  Refletir (SPACE⇄MEMORY).
- **ECL (tipos canônicos):** `Act`, `State`, `Context`, `Event/Echo`, `Trace`.
- **Contratos:** Problem Details (RFC 7807), `X-Correlation-Id` obrigatório
  ponta-a-ponta.
- **Observabilidade:** OpenTelemetry (traces/logs/métricas) habilitado por
  padrão.
- **Dados:** UTC, `jsonb` para flexibilidade controlada, versionamento otimista
  onde aplica.

---

## 🧩 Interfaces & Portas (contratos canônicos)

- **ENGINE ↔ MEMORY:** `EchoRepo { save, get, list, exists_idempotency }`
  `TraceRepo { save, list_by_correlation }` `PulseSource { now, emit }`
  `AnchorRepo { upsert, get_by_key }`
- **MEMORY ↔ SPACE:** `OutboxDispatcher { deliver_pending, mark_sent, retry }`
- **SPACE (envelopes de evento):**

```json
{
  "event": "echo.created",
  "id": "UUID",
  "kind": "string",
  "anchor": { "key": "string", "kind": "string" },
  "correlation_id": "UUID",
  "ts": "ISO-8601",
  "payload": {}
}
```

---

## 🗺️ Mapa de Etapas (implementação → deploy) _(macro, sem fases/sprints)_

- **Etapa 2 — ENGINE:** casos de uso, endpoints, tasks; DTOs ECL.
- **Etapa 3 — TRACE:** observabilidade E2E, qualidade do eco, auditoria, outbox
  dispatcher.
- **Etapa 4 — SPACE:** streams WS/SSE, contexto, auth (RBAC/ABAC), políticas.
- **Etapa 5 — CORE:** funcionalidades centrais (anchors, lifecycle de ecos,
  consultas).
- **Etapa 6 — OPS:** CI/CD, Docker, ambientes, segurança, SLO/SLI.
- **Etapa 7 — DEPLOY:** staging→prod, migrações, rollback/DR, release strategy.

> As **Fases** e **Sprints** serão abertas _dentro de cada Etapa_ no início da
> interação correspondente, gerando `overview.md` e `eto_faseX.md` daquela
> Etapa.

---

## ✅ Critérios Globais de Qualidade

- **Rastreabilidade total:** `correlation_id`, `trace_id`, `span_id` presentes e
  coerentes.
- **Idempotência controlada** em operações de criação (chave de idempotência).
- **Observabilidade ativa:** métricas mínimas e spans por caso de uso.
- **Segurança por padrão:** rotas públicas só para status/health; auth nas
  demais.
- **Testes mínimos:** unidade + integração de rotas + contrato de envelopes.
- **Documentação viva:** cada Etapa atualiza `/doc/ETO/ETAPAS_OVERVIEW.md`.

---

## 🌐 Governança de Branches & Releases

- **Após Etapas 0–1:** `main` contém release documental `v0.1.0-docs`; `develop`
  é _default_.
- **Implementação (Etapas 2+):** branches a partir de `develop`.

  - Convenção: `feature/e<etapa>-f<fase>-s<sprint>-t<tarefa>-<slug>`
  - Ex.: `feature/e2-f1-s1-t1-engine-skeleton`

- **Commits semânticos:** `feat(engine|memory|space)`, `docs(ETO)`,
  `fix(trace)`, `chore(ci)` etc.
- **Merge:** PR com checklist; `--no-ff` para preservar histórico.
- **Tags:** `vMAJOR.MINOR.PATCH[-qualifier]` (ex.: `v0.2.0-codex` para este
  CODEX).

---

## 🔗 Matriz de Rastreabilidade (resumo)

- **Requisição:** `X-Correlation-Id` ⇄ **Traces** (OTel) ⇄ **Echo/Trace** (DB) ⇄
  **Logs** (estruturados).
- **Âncoras (Anchor):** chaves semânticas ligam `Echo` a entidades de domínio.
- **Outbox:** garante _entrega eventual_ de eventos ao SPACE com re-tentativas.

---

## 📝 Checklists (globais)

- **PR:** testes passam, docs atualizados, OTel ativo, Problem Details
  padronizado.
- **Rota nova:** DTOs ECL, correlação propagada, métricas incrementadas.
- **Persistência:** migração idempotente, índices cobrindo consultas quentes.

---

## Linkagem

- **Etapa 0:** ECL, ECHO LOOP, léxico (Echo/Pulse/Trace/Anchor/Field).
- **Etapa 1:** `part_engine.md`, `part_memory.md`, `part_space.md`.
- **Overview de Etapas:** `/doc/ETO/ETAPAS_OVERVIEW.md`.

---

## IMPLEMENTAÇÃO (documental) — Registro de versionamento do CODEX

**Branch**:

- Base: `develop`
- Nova: `docs/e1_5-echo-codex`

```bash
git checkout develop
git pull
git checkout -b docs/e1_5-echo-codex
```

**Objetivo** Adicionar `/doc/ETO/etapa_1_5/ECHO_CODEX.md` e atualizar o
`/doc/ETO/ETAPAS_OVERVIEW.md` para referenciar a Etapa 1.5.

**Estrutura**:

```tree
doc/
  ETO/
    ETAPAS_OVERVIEW.md
    etapa_1_5/
      ECHO_CODEX.md
```

**Passos Principais**:

```bash
git add doc/ETO/etapa_1_5/ECHO_CODEX.md doc/ETO/ETAPAS_OVERVIEW.md
git commit -m "📚 docs(CODEX): Etapa 1.5 consolidada; mapa de Etapas 2–7 e invariantes"
git checkout develop
git merge --no-ff docs/e1_5-echo-codex -m "🔖 codex: consolidação estrutural (Etapa 1.5)"
git branch -D docs/e1_5-echo-codex
git tag -a v0.2.0-codex -m "ECHO CODEX consolidado (pré-implementação)"
```

**Testes (documentais)**:

- Checklist de coerência: ECL/ECHO LOOP presentes, mapa de Etapas 2–7 sem
  fases/sprints, governança de branches revisada.
- Links internos válidos.
