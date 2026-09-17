# Débitos técnicos — PetMeet

> Registro de pendências conhecidas ao final da N1, para o time que receber o projeto no handoff. Cada item indica o requisito relacionado, o estado atual e o que falta para concluir.

## Resumo

| # | Item | Requisito | Status | Esforço estimado |
|---|------|-----------|--------|-------------------|
| 1 | Apadrinhamento | RF10 / RF11 | Modelo pronto, serviço/rotas pendentes | Médio |
| 2 | Filtros avançados de doações | RF13 | Não iniciado | Baixo |
| 3 | Log de auditoria | RF22 | Modelo pronto, instrumentação pendente | Médio |
| 4 | Observabilidade avançada | RNF06–RNF10 | Não iniciado | Alto |
| 5 | Cache | RNF12 | Não iniciado | Médio |
| 6 | Backup e recuperação automatizados | RNF15–RNF17 | Não iniciado | Alto |
| 7 | Monitoramento de dependências | RNF18–RNF20 | Não iniciado | Médio |

---

## 1. Apadrinhamento (RF10 / RF11)

**Status:** modelo de dados já existe em `app/modelos/apadrinhamento.py`; falta a camada de serviço (`servicos/`) e as rotas (`rotas/`) que expõem essa funcionalidade na API.

**O que falta:**
- Serviço com as regras de negócio de associação padrinho ↔ pet (ex.: um pet pode ter mais de um padrinho? um padrinho pode apadrinhar mais de um pet?).
- Rotas REST para criar, listar, encerrar um apadrinhamento.
- Esquemas Pydantic de entrada/saída.
- Testes cobrindo o fluxo, seguindo o padrão já usado em `testes/test_processo_adocao.py`.

**Risco de não fazer:** a funcionalidade de apadrinhamento — citada no nome do próprio sistema ("adoção **e apadrinhamento**") — fica sem API, mesmo com o modelo pronto no banco.

## 2. Filtros avançados de doações (RF13)

**Status:** não iniciado.

**O que falta:** a rota de consulta de doações existe, mas sem filtros avançados (ex.: por período, por valor, por tipo de doação). Definir com a ONG quais filtros são prioritários antes de implementar.

## 3. Log de auditoria (RF22)

**Status:** modelo `LogAuditoria` já existe; falta instrumentar os serviços para gravar cada alteração relevante (quem alterou, o quê, quando, valores antes/depois).

**O que falta:**
- Decidir quais operações são auditáveis (criação/edição de fichas médicas, finalização de adoção, etc. são as mais sensíveis).
- Instrumentar a camada de `servicos/` para gravar o log sem acoplar essa responsabilidade à lógica de negócio (ex.: decorator, evento, ou chamada explícita centralizada).
- Expor rota de consulta do log (somente para `admin`).

## 4–7. Observabilidade, cache, backup e monitoramento (RNF06–RNF10, RNF12, RNF15–RNF20)

**Status:** não iniciado — arquitetura já preparada, mas a implementação fica a cargo do time de DevOps/infra a partir da base entregue.

**O que já está pronto para apoiar isso:**
- `GET /saude` — healthcheck simples para orquestradores.
- Configuração 100% via variáveis de ambiente (`RNF16`), sem credenciais no código-fonte.
- `Dockerfile` + `docker-compose.yml` prontos para servir de base a um ambiente de produção.

**O que falta:**
- Observabilidade: logging estruturado, métricas e tracing (ex.: OpenTelemetry).
- Cache: identificar rotas de leitura mais custosas (ex.: listagens paginadas) e avaliar Redis ou cache em memória.
- Backup/recuperação automatizados do PostgreSQL.
- Monitoramento de dependências (ex.: Dependabot/Renovate + alertas de vulnerabilidade).

---

## Como usar este documento

Este registro não substitui o código nem a documentação técnica completa (`docs/ARQUITETURA.md`, `docs/MODELO_DE_DADOS.md`). Ele existe para que o time que avaliar a viabilidade de receber o projeto no handoff saiba, em poucos minutos, **o que está pronto, o que está pela metade e o que não foi começado** — e possa estimar o esforço de continuidade com uma base realista.