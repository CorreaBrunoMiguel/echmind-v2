# ECHOMIND v2 — SPACE (Contexto, Observabilidade & Streams)

## Resumo

SPACE é o princípio de **contexto** do ECHOMIND v2 — o palco onde a mente se
manifesta. Define **middlewares** (correlação, auth, CORS, compressão),
**observabilidade** (OpenTelemetry: traces, logs, métricas) e **canais de
evento** (WebSocket/SSE) para materializar **Echo/Trace/Pulse** do ECL no mundo
externo. Tudo que o ENGINE faz e a MEMORY registra é **visível, correlacionável
e auditável** no SPACE.

## Componentes Técnicos

- **Middlewares base**

  - **Correlation**: gera/propaga `X-Correlation-Id` (UUID v4); injeta em
    `request.state.ctx` e resposta.
  - **Trace Context (W3C)**: suporte a `traceparent`/`tracestate`; mapeia para
    OTel spans.
  - **Logging estruturado**: JSON (pydantic encoder), chaves:
    `ts, level, msg, correlation_id, http.method, http.path, status, latency_ms`.
  - **CORS**: whitelist por ambiente; `OPTIONS` rápido (no-trace).
  - **Compression**: GZip/Brotli com limites sensatos.
  - **Rate limit (MVP opcional)**: `slowapi`/token-bucket por `client_id` +
    rota.

- **Auth (esqueleto)**

  - `AuthDependency` injetável (FastAPI `Depends`): suporta **API Key** (MVP) e
    prepara **OAuth2 Bearer** (JWT assinado).
  - **RBAC mínimo**: `system`, `admin`, `reader`; política no nível de rota/uso.
  - **Multi-tenant (futuro)**: `tenant_id` em `Context`; ganchos para **RLS** na
    MEMORY.

- **Observabilidade (OpenTelemetry)**

  - **Traces**: `FastAPIInstrumentor`; spans para request/DB; atributos ECL
    (`echo.id`, `act.kind`, `correlation_id`).
  - **Logs**: export via OTel LoggerProvider → OTLP; correlação
    `trace_id`/`span_id`.
  - **Métricas**: `MeterProvider`; contadores (`http.server.requests`),
    histogramas (`http.server.duration`), _business metrics_ (ecos/min).
  - **Exporters**: OTLP (gRPC/HTTP) para Jaeger/Tempo/OTel Collector/Prometheus.

- **Canais de evento**

  - **WebSocket**: `/api/v1/stream/ws` (tempo real, bidirecional controlado).
  - **SSE**: `/api/v1/stream/sse` (server-sent events; idempotente e leve).
  - **Protocolos de mensagem (envelope ECL)**:

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

- **Health & Status**

  - `/api/v1/status`: `service, version, uptime, correlation_id, pulse_now`.
  - `/api/v1/healthz`: liveness rápido (sem tocar DB).
  - `/api/v1/readyz`: readiness (checa DB/OTLP).

## Modelos e Entidades

- **`RequestContext`**:
  `{ correlation_id: UUID, actor?: str, tenant_id?: str, ip?: str, user_agent?: str }`
- **`EventEnvelope`** (ECL):
  `{ event, id, kind, anchor?, correlation_id, ts, payload }`
- **`Problem`** (RFC 7807):
  `{ type, title, status, detail, instance, correlation_id }`
- **`TelemetryConfig`**:
  `{ service_name, service_version, otlp_endpoint, sampling_ratio }`

## Integrações

- **ENGINE ↔ SPACE**

  - Injeta `RequestContext` em casos de uso; cada **Act** abre um `span`.
  - Mapeia exceções → **Problem Details**; inclui `correlation_id` e `instance`.
  - Após persistência (via MEMORY), publica `echo.created` nos canais (WS/SSE).

- **MEMORY ↔ SPACE**

  - **Outbox dispatcher** lê `event_outbox (pending)` e entrega aos streams;
    confirma `sent` com `sent_at` e re-tentativas exponenciais.
  - Métricas de backpressure: fila do outbox, latência de entrega, taxa de erro.

## Observações

- **Contratos semânticos**: toda resposta carrega `X-Correlation-Id`; logs e
  spans devem refletir o mesmo valor.
- **Backpressure**: WS/SSE com _buffers_ e _drop policies_ configuráveis;
  notificar `client_backpressure` via evento técnico.
- **Privacidade**: **payloads sensíveis não vão para logs**; use chaves-resumo
  (hash/ULID) e _redaction_.
- **Resiliência**: _graceful shutdown_ fecha streams, drena outbox, flush de
  spans/logs.
- **Testabilidade**: testes de contrato dos envelopes e do middleware de
  correlação; _golden files_ para logs.

## Linkagem

- **Etapa 0**: ECL (Context, Echo, Trace, Pulse), **ECHO LOOP**
  (Perceber→Agir→Reter→Refletir).
- **Etapa 1**:

  - `/doc/part_engine.md` (atos que geram ecos),
  - `/doc/part_memory.md` (estado e outbox),
  - `/doc/ETO/etapa_1/eto_fase1.md` (execução viva por fases/sprints/tarefas).

---
