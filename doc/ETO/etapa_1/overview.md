# Etapa 1 — Fundação Técnica e Arquitetônica (resumo antes de iniciar)

Missão: transformar a filosofia consolidada na Etapa 0 em **base técnica sólida
e rastreável**, definindo esqueleto do sistema, contratos, observabilidade e
schema inicial. Saídas: documentos **part_engine.md**, **part_memory.md**,
**part_space.md** (um por interação), além do acompanhamento vivo em
`/doc/ETO/etapa_1/eto_fase1.md`.

---

**Projeto:** ECHOMIND v2 • **Stack:** FastAPI + PostgreSQL • **Arquitetura:**
ENGINE / MEMORY / SPACE **Objetivo:** estabelecer o alicerce operacional
mínimo-viável, já alinhado ao **ECL** e ao **ECHO LOOP**.

## Escopo

- **ENGINE (FastAPI Core):** roteadores por domínio, camada de casos de uso,
  erros RFC7807.
- **MEMORY (PostgreSQL):** schema base `echo`, `trace`, `pulse`, `anchor`;
  migrações Alembic; repositórios SQLAlchemy 2.0.
- **SPACE (Contexto/Interop):** middleware de correlação (**X-Correlation-Id**),
  autenticação (esqueleto), OpenTelemetry (traces/logs/métricas) e canal de
  eventos (WebSocket/EventStream).

### Critérios de aceite

- Projeto inicial executando com healthcheck e rota de status semanticamente
  rastreável.
- Migração inicial aplicada e reversível; transações idempotentes nos núcleos
  críticos.
- Tracing ponta-a-ponta (requisição → persistência → emissão de **echo/trace**).
- Padrões documentados no trio **part_engine / part_memory / part_space**.

### Entregáveis (progresso incremental)

- `/doc/part_engine.md` • `/doc/part_memory.md` • `/doc/part_space.md`
- `/doc/ETO/etapa_1/eto_fase1.md` (acompanhamento vivo por
  fases/sprints/tarefas)

---
