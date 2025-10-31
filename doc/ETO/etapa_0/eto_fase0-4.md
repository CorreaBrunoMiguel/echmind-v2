# Fase 0.4 — Síntese Cognitiva

## 📖 Resumo

A mente ganha coesão quando os seus atos, lembranças e contextos dançam no mesmo
compasso. A Síntese Cognitiva fixa esse compasso no **ECHOMIND v2**: ENGINE
(agir), MEMORY (lembrar) e SPACE (manifestar) passam a operar sob um idioma
único (**ECL — Echo Core Language**) e um ciclo invariável (**ECHO LOOP**). Com
isso, a filosofia deixa de pairar: torna-se arquitetura preparada para a
fundação técnica.

---

## 🔁 ECHO LOOP — Ciclo Invariável

1. **Perceber** _(SPACE)_ → capturar o contexto e propagar correlações.
2. **Agir** _(ENGINE)_ → executar o ato consciente (rota, serviço, tarefa).
3. **Reter/Interpretar** _(MEMORY)_ → persistir estado e produzir significado.
4. **Refletir** _(SPACE ⇄ MEMORY)_ → emitir **echo** e atualizar o campo. → O
   ciclo recomeça, alimentado por _pulses_ temporais e _traces_ auditáveis.

**Invariantes do ciclo:** idempotência onde possível, rastreabilidade total,
determinismo nos núcleos críticos, degradação graciosa, contratos semânticos
explícitos.

---

## 🔤 ECL — Echo Core Language (núcleo mínimo)

**Tipos semânticos canônicos**:

- **Act** (ENGINE): ato executável (endpoint/serviço/tarefa).
- **State** (MEMORY): estado persistido (linha, snapshot, versão).
- **Context** (SPACE): metadados de execução (auth, tenant, correlação).
- **Event/Echo** (SPACE): emissão observável do sistema.
- **Trace** (GLOBAL): trilha completa do ciclo (correlation_id + spans).

**Regras de tradução**:

- Todo **Act** gera ao menos um **Echo** e um **Trace**.
- Toda mutação de **State** exige **Anchor** (chave semântica) e **Version**.
- **Context** é obrigatório e propagado ponta-a-ponta (X-Correlation-Id).

---

## 🧩 Identidade Operacional (princípios → engenharia)

- **ENGINE** → _FastAPI Core_ (routers modulares, services, tasks assíncronas).
  Padrões: Application Layer + Use Cases; erros com RFC 7807; testes por caso de
  uso.
- **MEMORY** → _PostgreSQL_ (SQLAlchemy 2.0 + Alembic, Pydantic v2). Padrões:
  versionamento lógico, soft-delete com janelas de retenção, _event outbox_.
- **SPACE** → _Contexto & Interop_ (middlewares, auth, observabilidade, stream).
  Padrões: OpenTelemetry (traces/metrics/logs), WebSocket/EventStream,
  RBAC/ABAC.

---

## 🗺️ Mapeamento semântico → artefatos Etapa 1

- **Echo / Trace / Pulse** → tabelas `echo`, `trace`, `pulse`; views de
  observabilidade.
- **Anchor / Field** → modelos de domínio e índices semânticos (busca e
  correlação).
- **Mirror** → consultas analíticas e materializações para insight operacional.

---

## ✅ Critérios de Conclusão da Etapa 0 (atingidos)

- Linguagem unificada (ECL) definida.
- Ciclo operacional (ECHO LOOP) formalizado.
- Pontes claras da filosofia para a fundação técnica (FastAPI + PostgreSQL +
  Observabilidade).

---

## 🧭 Preparação imediata para a Etapa 1 — Fundação Técnica e Arquitetônica

**Escopo enxuto, sólido e auditável**:

- **Backend (ENGINE):** esqueleto FastAPI, roteamento por _domains_, camadas
  `domain → service → transport`, validação Pydantic v2.
- **Data (MEMORY):** schema inicial (echo/trace/pulse/anchor), migrações
  Alembic, repositórios SQLAlchemy 2.0.
- **Space (Infra/Contexto):** middlewares (correlação, auth), OpenTelemetry,
  logger estruturado, WebSocket/event-stream.

**Documentos-alvo da Etapa 1** (geração progressiva, um por interação):

- `/doc/part_engine.md` • `/doc/part_memory.md` • `/doc/part_space.md` →
  culminando no **ECHO CODEX** consolidado (**Etapa 1.5**).

---
