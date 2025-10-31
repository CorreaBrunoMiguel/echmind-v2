# ECHOMIND v2 — MEMORY (PostgreSQL & Persistência Cognitiva)

## Resumo

MEMORY é o princípio de **retenção** do ECHOMIND v2: transforma experiência em
**estado**. Aqui definimos o **schema inicial** (echo/trace/pulse/anchor),
migrações **Alembic**, repositórios **SQLAlchemy 2.0 (async)**, políticas de
versionamento, idempotência e rastreabilidade — tudo alinhado ao **ECL** e
pulsando no **ECHO LOOP**.

## Componentes Técnicos

- **Banco:** PostgreSQL ≥ 14 (UTC, `statement_timeout` sensato;
  `wal_level=replica` para futuro read-replica).
- **Driver/ORM:** `sqlalchemy[asyncio]` 2.x + `asyncpg`; mapeamento declarativo
  2.x.
- **Migrações:** Alembic (version table `alembic_version`; _revisions_
  semânticas).
- **JSON & Busca:** `jsonb` com índices GIN (`jsonb_path_ops`) para consultas
  semânticas.
- **UUIDs:** `pgcrypto` (`gen_random_uuid()`) habilitado; PKs como `UUID`.
- **Time:** `timestamptz` (UTC); colunas `created_at`, `updated_at`.
- **Idempotência:** chave de idempotência por operação com janela temporal
  configurável.
- **Soft-delete & Versionamento:** colunas `is_deleted`, `version` (optimistic
  locking).
- **Auditoria:** `correlation_id`, `actor` (quem), `origin` (onde), `instance`
  (rota/serviço).

## Modelos e Entidades

### Tabela `anchor`

**Função ECL:** _ponto fixo_ de referência semântica entre ENGINE e MEMORY.
**Colunas (principal):**

- `id UUID PK`, `key TEXT UNIQUE` (ex.: “user:42” ou “doc:ULID”), `kind TEXT`,
- `meta JSONB` (rótulos/atributos), `version INT DEFAULT 1`,
- `created_at timestamptz`, `updated_at timestamptz`,
  `is_deleted BOOLEAN DEFAULT FALSE`. **Índices:** `UNIQUE(key)`, GIN(`meta`),
  BTREE(`kind`, `created_at DESC`).

### Tabela `echo`

**Função ECL:** _emissão observável_ do sistema (evento materializado).
**Colunas (principal):**

- `id UUID PK`, `kind TEXT`, `payload JSONB NOT NULL`,
- `anchor_id UUID FK(anchor) NULL`, `correlation_id UUID`,
  `idempotency_key TEXT NULL`,
- `actor TEXT`, `origin TEXT`,
- `created_at timestamptz DEFAULT now()`. **Regras/Índices:**
- `UNIQUE(idempotency_key)` (ou
  `UNIQUE(idempotency_key) WHERE idempotency_key IS NOT NULL`).
- BTREE(`created_at DESC`), BTREE(`kind`, `created_at DESC`), GIN(`payload`).

### Tabela `trace`

**Função ECL:** _trilha_ do ciclo (debug/observabilidade). **Colunas
(principal):**

- `id UUID PK`, `echo_id UUID FK(echo) NULL`, `span TEXT`, `attrs JSONB`,
- `duration_ms INT`, `correlation_id UUID`,
- `started_at timestamptz`, `ended_at timestamptz`. **Índices:**
  BTREE(`correlation_id`), BTREE(`started_at DESC`), GIN(`attrs`).

### Tabela `pulse`

**Função ECL:** _batida temporal_ do organismo. **Colunas (principal):**

- `id UUID PK`, `ts timestamptz`,
  `sequence BIGINT GENERATED ALWAYS AS IDENTITY`,
- `note TEXT NULL`. **Índices:** BTREE(`ts DESC`), BTREE(`sequence DESC`).

### Tabela `event_outbox` (integração espaço-tempo)

**Padrão:** Outbox para entrega confiável ao **SPACE** (streams/eventos).
**Colunas (principal):**

- `id UUID PK`, `event_type TEXT`, `aggregate_kind TEXT`,
  `aggregate_id UUID NULL`,
- `payload JSONB NOT NULL`, `occurred_at timestamptz`,
- `status TEXT CHECK (status IN ('pending','sent','failed')) DEFAULT 'pending'`,
- `attempts INT DEFAULT 0`, `last_error TEXT NULL`, `sent_at timestamptz NULL`.
  **Índices:** BTREE(`status`, `occurred_at`), GIN(`payload`). **Garantias:**
  transação com o **echo** (mesma TX → atomicidade).

### Convenções Gerais

- **Nomes:** `snake_case`, tabelas no plural (`echo`, `trace`, `pulse`,
  `anchor`).
- **FKs:** `ON DELETE SET NULL` para `echo.anchor_id` (preserva histórico).
- **Políticas multi-tenant (futuro):** coluna `tenant_id` + **RLS** por
  contexto.
- **Políticas de retenção:** `trace` e `event_outbox` com TTL/particionamento
  por mês.

## Integrações

### ENGINE ↔ MEMORY

- **Portas** (interfaces) implementadas aqui:

  - `EchoRepo`: `save(Echo)`, `get(id)`, `list(filter)`,
    `exists_idempotency(key)`
  - `TraceRepo`: `save(Trace)`, `list_by_correlation(corr_id)`
  - `PulseSource`: `now()`, `emit(note?)`
  - `AnchorRepo`: `upsert(key, kind, meta)`, `get_by_key(key)`

- **Transação padrão:** _Unit of Work_ (AsyncSession) por caso de uso; _write_ →
  `commit()`; _read_ → `RO` com `READ COMMITTED`.

### MEMORY ↔ SPACE

- **Outbox dispatcher**: job periódico/BackgroundTask que publica eventos
  `pending` do `event_outbox` no canal de **echo** do SPACE; marca `sent` com
  `sent_at`; _retry_ exponencial (limiar `attempts`).
- **Observabilidade:** cada persistência grava `correlation_id` e atributos ECL;
  integração com OTel por _db spans_.

## Observações

- **Idempotência:** toda operação de criação que aceite `idempotency_key` deve
  validar `UNIQUE` antes de inserir; fallback determinístico.
- **Optimistic Locking:** `version` + `updated_at` nos _anchors_ e entidades de
  leitura frequente.
- **Consistência temporal:** sempre UTC; aplicações convertem para _locale_
  apenas na borda.
- **Desempenho:** índices nos campos de consulta quente; `jsonb` para
  flexibilidade sem cair em _schemaless_ anárquico.
- **Migrações seguras:** _expand → migrate data → contract_ (quando necessário);
  _down_ estável nas primeiras versões.
- **Backups:** base full + WAL; testes de restauração documentados (runbooks).

## Linkagem

- **Etapa 0:** ECL (State, Echo, Trace, Context), ECHO LOOP, léxico
  (Anchor/Field).
- **Etapa 1:**

  - `/doc/part_engine.md` — casos de uso chamando _repos_ (portas).
  - `/doc/part_space.md` — middlewares de correlação, OTel, canais de evento.
  - `/doc/ETO/etapa_1/eto_fase1.md` — execução viva (fases/sprints/tarefas).

---
