# ECHOMIND v2 — ENGINE (FastAPI Core)

## Resumo

ENGINE é o princípio de **movimento** do ECHOMIND v2: transforma intenção em
execução. Aqui definimos o esqueleto do app **FastAPI** orientado a casos de
uso, contratos explícitos (ECL), erros padronizados (RFC 7807) e telemetria
acoplada ao ciclo **ECHO LOOP**. O ENGINE fala com a MEMORY por portas de
repositório e manifesta seus atos no SPACE por eventos/echo e traces.

## Componentes Técnicos

- **Linguagem/Runtime:** Python ≥ 3.11
- **Framework Web:** FastAPI (async-first) + Uvicorn (ASGI)
- **Validação/DTOs:** Pydantic v2 (BaseModel, `model_config`)
- **Padrões de Camada:** `domain → usecase/service → transport (api/router)`
- **Erros:** Problem Details (RFC 7807) como `application/problem+json`
- **Observabilidade:** OpenTelemetry (traces/logs/métricas) com
  `X-Correlation-Id` propagado
- **Tarefas assíncronas:** `BackgroundTasks` (MVP) — expansível p/ Celery/RQ
- **Testes:** pytest + httpx AsyncClient (integração de rotas)
- **Configuração:** 12-Factor via env (`APP_ENV`, `APP_NAME`, `OTEL_EXPORTER_*`,
  etc.)
- **Empacotamento:** Poetry (lock determinístico)
- **Estrutura sugerida (MVP):**

  ```tree
  app/
    core/            # config, logging, telemetry (hooks do SPACE)
    domain/          # entidades e contratos ECL (sem infra)
    usecases/        # casos de uso orquestrando domain + portas
    adapters/        # portas → implementações (ex.: repos da MEMORY)
    api/
      v1/routers/    # status, echo, trace, pulse
      deps.py        # deps comuns (auth, correlation, repos)
      errors.py      # mapeamento RFC7807
      schemas.py     # DTOs Pydantic (ECL)
    main.py          # criação da app e montagem de routers
  ```

## Modelos e Entidades

**Léxico ECL aplicado ao ENGINE (DTOs mínimos):**

- `StatusOut`: `service`, `version`, `uptime`, `correlation_id`, `pulse_now`
- `EchoIn`: `kind`, `payload` (JSON), `anchor` (string opcional)
- `EchoOut`: `id`, `kind`, `created_at`, `correlation_id`
- `TraceOut`: `id`, `span`, `echo_id?`, `started_at`, `duration_ms`
- `PulseOut`: `ts`, `sequence`
- `Problem`: `type`, `title`, `status`, `detail`, `instance`, `correlation_id`

**Entidades de domínio (sem infra):**

- `Act` (ato) — abstrai execução de caso de uso
- `Context` — metadados (tenant, auth, correlation)
- **Contratos (ports)**:

  - `EchoRepo` (gravar/consultar ecos)
  - `TraceRepo` (consultar rastros)
  - `PulseSource` (emitir/consultar pulso atual)

> Nota: As implementações concretas destas portas residem na MEMORY
> (SQLAlchemy/PostgreSQL), plugadas via `adapters/`.

## Integrações

- **Com MEMORY**: via interfaces `EchoRepo`, `TraceRepo`, `PulseSource`. ENGINE
  não conhece SQL; apenas contratos.
- **Com SPACE**: middlewares de correlação, autenticação (esqueleto), CORS e
  emissor de eventos (WebSocket/EventStream).
- **Observabilidade (OTel)**: cada `Act` abre `span` com atributos ECL
  (`act.kind`, `echo.id?`, `correlation_id`).
- **Erros**: exceções mapeadas para `Problem Details` com `correlation_id` e
  `instance` (rota).
- **Eventos**: após `Echo` persistido (via MEMORY), ENGINE emite **echo** no
  SPACE (canal `echo.stream`).

## Observações

- **Invariantes**: idempotência quando aplicável; rastreabilidade total;
  contratos estáveis; degradação graciosa.
- **Segurança**: dependências de auth (RBAC/ABAC) preparadas; rotas públicas
  apenas para health/status.
- **Versão de API**: prefixo `/api/v1` e cabeçalho `X-API-Version` no response.
- **Boundary DDD**: ENGINE nunca acessa infra de banco diretamente; tudo por
  portas.

## Linkagem

- **Etapa 0**: ECL, ECHO LOOP, léxico (`Echo`, `Pulse`, `Trace`, `Anchor`,
  `Field`).
- **Etapa 1** (relacionados):

  - `/doc/part_memory.md` — schema, repositórios e migrações (implementações das
    portas)
  - `/doc/part_space.md` — middlewares, OTel, canais de evento e políticas de
    contexto
  - `/doc/ETO/etapa_1/eto_fase1.md` — acompanhamento vivo
    (fases/sprints/tarefas)

---
