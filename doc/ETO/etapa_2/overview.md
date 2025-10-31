# Etapa 2 — ENGINE (início)

**Arquivo:** `/doc/ETO/etapa_2/overview.md` **Objetivo:** iniciar a
implementação do **ENGINE** com base no CODEX, seguindo ECL/ECHO LOOP. **Escopo
mínimo:** esqueleto FastAPI, status/health, correlação `X-Correlation-Id`,
ganchos OTel, DTOs ECL, portas para MEMORY (sem SQL direto). **Critérios de
aceite:** serviço sobe com `/api/v1/status`, healthchecks, correlação visível em
resposta/logs/traces, testes básicos de rota e contrato.

---
