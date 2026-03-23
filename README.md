# RLM RAG Hybrid

MCP local para pesquisa técnica híbrida, onde:

- **RLM** é o orquestrador principal
- **CocoIndex** faz o retrieval semântico
- **leitura local** confirma evidência real

## O que ele faz

Expõe 4 tools MCP:

- `research_codebase`
- `analyze_change_impact`
- `trace_feature_flow`
- `find_related_tests`

## Arquitetura

```text
Pergunta -> MCP -> RLM
RLM -> semantic_search (CocoIndex)
RLM -> search_exact / read_file_excerpt
RLM -> síntese final com evidência
```

## Requisitos

- Python 3.11
- chave do OpenRouter em `OPENROUTER_API_KEY`
- `cocoindex-code` disponível no ambiente

## Instalação

```bash
uv sync
cp .env.example .env
```

Se o `cocoindex-code` já estiver instalado em outro ambiente global, você pode apontar:

```bash
export RLM_RAG_HYBRID_COCOINDEX_SITE_PACKAGES="/path/to/site-packages"
```

## Rodando

```bash
uv run python -m rlm_rag_hybrid.server
```

## Variáveis principais

- `OPENROUTER_API_KEY`
- `RLM_RAG_HYBRID_WORKSPACE_ROOT`
- `RLM_RAG_HYBRID_DEFAULT_REPO`
- `RLM_RAG_HYBRID_RLM_MODEL`
- `RLM_RAG_HYBRID_COCOINDEX_SITE_PACKAGES`

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

## Observações

- O projeto prioriza **evidência concreta** sobre resposta puramente generativa.
- Quando o RLM ignora a evidência coletada, o servidor faz **reparo de resposta** baseado nos achados reais.
- O retrieval inicial lê automaticamente os melhores trechos para enriquecer a resposta.
