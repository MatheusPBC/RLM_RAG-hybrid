# RLM RAG Hybrid

MCP local para **pesquisa técnica em código com evidência real**.

Este projeto usa:

- **RLM** como orquestrador principal
- **CocoIndex** para retrieval semântico
- **leitura local de arquivos** para confirmar achados antes da resposta final

## O que ele resolve

Em vez de responder só com síntese generativa, o servidor tenta montar respostas mais confiáveis para perguntas como:

- onde isso é usado?
- como esse fluxo funciona?
- quais testes estão mais relacionados?
- qual o impacto provável de mudar este arquivo ou símbolo?

## Para quem é

Útil para devs que usam MCP/OpenCode e querem um assistente de pesquisa técnica que:

- pesquise código de forma semântica
- confirme evidência em arquivos reais
- reduza respostas “plausíveis porém soltas”

## Como funciona

```text
Pergunta -> MCP -> RLM
RLM -> semantic_search (CocoIndex)
RLM -> search_exact / read_file_excerpt
RLM -> síntese final baseada em evidência
```

Comportamento importante:

- a busca semântica entra primeiro para descoberta
- os melhores resultados ganham leitura local automática
- se o RLM ignorar a evidência coletada, o servidor faz um reparo da resposta com base nos achados reais

## Tools MCP disponíveis

| Tool | O que faz |
|---|---|
| `research_codebase` | Pesquisa livre na base e resume os achados mais relevantes |
| `analyze_change_impact` | Faz uma análise técnica do impacto potencial de uma mudança |
| `trace_feature_flow` | Rastreia o fluxo técnico de uma feature, símbolo ou entrypoint |
| `find_related_tests` | Procura testes relacionados ao alvo informado |

## Requisitos

- Python **3.11**
- `uv`
- chave do OpenRouter em `OPENROUTER_API_KEY`
- `cocoindex-code` disponível no ambiente atual **ou** apontado via path de `site-packages`

## Quick start

### 1. Instale as dependências do projeto

```bash
uv sync
```

### 2. Crie seu `.env`

```bash
cp .env.example .env
```

### 3. Configure pelo menos estas variáveis

```bash
export OPENROUTER_API_KEY="your-openrouter-key"
export RLM_RAG_HYBRID_WORKSPACE_ROOT="/absolute/path/to/your/repo-or-workspace"
export RLM_RAG_HYBRID_DEFAULT_REPO="."
```

Se o `cocoindex-code` já estiver instalado fora desse projeto, aponte o `site-packages` dele:

```bash
export RLM_RAG_HYBRID_COCOINDEX_SITE_PACKAGES="/path/to/site-packages"
```

### 4. Rode o servidor MCP

```bash
uv run python -m rlm_rag_hybrid.server
```

## Configuração

| Variável | Obrigatória | Descrição | Default |
|---|---|---|---|
| `OPENROUTER_API_KEY` | Sim | Chave do provider usado pelo RLM | - |
| `RLM_RAG_HYBRID_WORKSPACE_ROOT` | Sim | Raiz do repositório/workspace a pesquisar | diretório atual |
| `RLM_RAG_HYBRID_DEFAULT_REPO` | Não | Escopo padrão das buscas | `.` |
| `RLM_RAG_HYBRID_COCOINDEX_SITE_PACKAGES` | Depende | Path do `site-packages` que contém `cocoindex_code` | vazio |
| `RLM_RAG_HYBRID_RLM_MODEL` | Não | Modelo usado no OpenRouter | `openai/gpt-4o-mini` |
| `RLM_RAG_HYBRID_RLM_MAX_DEPTH` | Não | Profundidade recursiva máxima | `2` |
| `RLM_RAG_HYBRID_RLM_MAX_ITERATIONS` | Não | Iterações máximas do RLM | `8` |
| `RLM_RAG_HYBRID_RLM_TIMEOUT_SECONDS` | Não | Timeout máximo por execução | `45` |
| `RLM_RAG_HYBRID_SEMANTIC_LIMIT` | Não | Limite de resultados semânticos | `8` |
| `RLM_RAG_HYBRID_EXACT_LIMIT` | Não | Limite de resultados de busca exata | `12` |
| `RLM_RAG_HYBRID_LOG_LEVEL` | Não | Nível de log do servidor | `INFO` |

## Exemplo de configuração no OpenCode

```json
{
  "mcp": {
    "rlm-rag-hybrid": {
      "type": "local",
      "command": [
        "uv",
        "run",
        "python",
        "-m",
        "rlm_rag_hybrid.server"
      ],
      "enabled": true,
      "environment": {
        "OPENROUTER_API_KEY": "{env:OPENROUTER_API_KEY}",
        "RLM_RAG_HYBRID_WORKSPACE_ROOT": "{env:RLM_RAG_HYBRID_WORKSPACE_ROOT}",
        "RLM_RAG_HYBRID_DEFAULT_REPO": "{env:RLM_RAG_HYBRID_DEFAULT_REPO}",
        "RLM_RAG_HYBRID_COCOINDEX_SITE_PACKAGES": "{env:RLM_RAG_HYBRID_COCOINDEX_SITE_PACKAGES}"
      }
    }
  }
}
```

## Notas importantes

- o projeto prioriza **evidência concreta** sobre resposta puramente generativa
- a resposta pode incluir dados de:
  - busca semântica
  - busca exata
  - leitura direta de trechos
- o melhor resultado acontece quando o workspace já está bem indexado pelo CocoIndex

## Limites atuais

- depende de `cocoindex_code` disponível no ambiente
- a qualidade final ainda depende do modelo escolhido no OpenRouter
- parte do comportamento é orientada a projetos locais; não há integração remota/GitHub neste MVP
- alguns ambientes podem emitir warnings de terceiros (`dotenv`, Hugging Face, etc.) sem bloquear o uso

## Ideias de uso

- pesquisar uma feature antes de refatorar
- achar testes relevantes antes de mexer em um módulo
- entender fluxos técnicos em codebases grandes
- usar como base para análise de impacto com evidência

## Segurança

- não coloque sua chave no repositório
- use sempre variável de ambiente para `OPENROUTER_API_KEY`
- o servidor só deve apontar para workspaces que você confia
