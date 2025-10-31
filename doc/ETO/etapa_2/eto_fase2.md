# Fase 1 — Esqueleto do ENGINE

📖 **Resumo** Erguer o app FastAPI modular (rotas por domínio, casos de uso) com
correlação, observabilidade e contratos ECL. Sem lógica de banco direto—apenas
portas para MEMORY e emissão de **Echo/Trace** no SPACE.

🧭 **Introdução** Esta fase transforma o modelo em execução mínima: define DTOs
ECL, status/health, middleware de correlação e instrumentação OTel. A partir
daqui, cada ato do ENGINE é rastreável e compatível com o CODEX.

## Sprint 1 — Bootstrap do ENGINE

### Tarefa 1 — App FastAPI mínimo + status/health + correlação + OTel

**Pt.1**:

Criar o serviço FastAPI com `/api/v1/status`, `/healthz`, `/readyz`, middleware
`X-Correlation-Id`, instrumentação OTel e testes de rota. Preparar portas para
MEMORY (EchoRepo/TraceRepo/PulseSource) sem implementações concretas.
