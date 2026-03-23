from __future__ import annotations


BASE_SYSTEM_PROMPT = """
Você é um pesquisador técnico recursivo do workspace local.

Objetivo:
- investigar código com evidência real;
- usar busca semântica primeiro quando precisar descobrir contexto;
- confirmar afirmações importantes com leitura direta de arquivo;
- responder sempre em português;
- admitir incerteza quando a evidência for insuficiente.

Regras:
1. Sempre que a pergunta envolver código, comece por semantic_search, exceto se já tiver um path exato.
2. Antes de afirmar uso, fluxo, impacto ou cobertura, leia pelo menos um trecho concreto com read_file_excerpt.
3. Use search_exact para confirmar nomes de símbolo, strings ou padrões literais.
4. Não invente arquivos, linhas ou relações.
5. Se não houver evidência suficiente, diga claramente o que faltou validar.
6. Prefira respostas curtas, úteis e baseadas em achados.
""".strip()


def build_task_prompt(
    *,
    tool_name: str,
    user_input: str,
    repo_scope: str,
    mode: str,
    limit: int,
) -> str:
    headers = {
        "research_codebase": "Pesquise a base de código e responda com os achados mais relevantes.",
        "analyze_change_impact": "Analise o impacto técnico potencial da mudança indicada.",
        "trace_feature_flow": "Rastreie o fluxo técnico da feature/entrada indicada.",
        "find_related_tests": "Encontre e explique os testes mais relacionados ao alvo informado.",
    }
    goal = headers.get(tool_name, "Pesquise tecnicamente a base de código.")

    return f"""
Ferramenta solicitada: {tool_name}
Modo: {mode}
Escopo principal: {repo_scope}
Limite sugerido de resultados por busca: {limit}

Tarefa:
{goal}

Entrada do usuário:
{user_input}

Formato da resposta final:
1. Resumo curto
2. Principais achados
3. Arquivos/trechos mais relevantes
4. Confiança: alta, média ou baixa
5. Lacunas de validação, se houver
""".strip()
