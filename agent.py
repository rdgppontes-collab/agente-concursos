import anthropic
from config import MODELO_CLAUDE

import os
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_AGENTE = """Você é um agente especialista em preparação para concursos públicos brasileiros.
Sua missão é gerar conteúdo didático de alta qualidade, focado na aprovação.
Sempre adapte o conteúdo ao estilo da banca informada e ao nível do candidato.
Seja direto, técnico e estratégico. Use exemplos práticos e questões reais."""


def gerar_aula(materia, assunto, banca, nivel, referencia, concurso):
    prompt = f"""Prepare uma aula completa para concurso público com os seguintes parâmetros:

CONCURSO: {concurso}
BANCA: {banca}
MATÉRIA: {materia}
ASSUNTO: {assunto}
NÍVEL DO CANDIDATO: {nivel}
REFERÊNCIA DIDÁTICA: {referencia if referencia else "Professor experiente em concursos"}

A aula deve conter obrigatoriamente estas seções:

## 1. TEORIA BASE
Explicação clara e completa do assunto, no estilo didático de {referencia if referencia else "um professor experiente"}.
Destaque os pontos que a banca {banca} mais cobra.

## 2. PONTOS QUENTES ⚠️
Liste os 5 principais pontos que a {banca} adora cobrar neste assunto.
Inclua artigos de lei, percentuais, prazos e conceitos literais quando relevante.

## 3. MACETES DE MEMORIZAÇÃO
Técnicas, siglas, histórias e associações para fixar o conteúdo.

## 4. QUESTÕES COMENTADAS
Gere 3 questões no estilo exato da banca {banca}:
- Para CESGRANRIO: múltipla escolha (A a E), situações práticas
- Para CESPE: certo/errado com afirmações elaboradas
- Para FCC: múltipla escolha com distratores técnicos
Inclua gabarito e comentário detalhado de cada alternativa.

## 5. ARMADILHAS DA BANCA
Quais são as pegadinhas típicas da {banca} neste assunto?
O que ela usa para induzir ao erro?

## 6. ESQUEMA VISUAL
Mapa mental em texto estruturado com tópicos e subtópicos.

Seja completo mas objetivo. Foco total na aprovação."""

    resposta = client.messages.create(
        model=MODELO_CLAUDE,
        max_tokens=4000,
        system=SYSTEM_AGENTE,
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.content[0].text


def gerar_questoes(materia, assunto, banca, quantidade, nivel):
    prompt = f"""Gere {quantidade} questões inéditas no estilo exato da banca {banca} sobre:

MATÉRIA: {materia}
ASSUNTO: {assunto}
NÍVEL: {nivel}

Para cada questão forneça:
1. O enunciado completo
2. As alternativas (A a E para CESGRANRIO/FCC/VUNESP) ou (Certo/Errado para CESPE)
3. O gabarito
4. Análise completa:
   - O que realmente está sendo testado
   - Por que cada alternativa errada foi construída assim
   - A armadilha usada pela banca
   - Artigo/lei/conceito envolvido

Separe cada questão com uma linha de traços (---).
Formate como: QUESTÃO X, ENUNCIADO, ALTERNATIVAS, GABARITO, ANÁLISE."""

    resposta = client.messages.create(
        model=MODELO_CLAUDE,
        max_tokens=3000,
        system=SYSTEM_AGENTE,
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.content[0].text


def analisar_edital(texto_edital):
    prompt = f"""Analise este edital de concurso público e forneça:

## 1. DADOS PRINCIPAIS
- Cargo, órgão e banca
- Número de vagas e salário
- Data da prova

## 2. ESTRUTURA DA PROVA
Tabela com: matéria | questões | pontos | peso %

## 3. PRIORIDADE ESTRATÉGICA
Ranqueie as matérias por prioridade real de estudo (peso × dificuldade típica)

## 4. PONTOS DE ELIMINAÇÃO
Quais são as regras de nota mínima e eliminação?

## 5. ESTRUTURA OCULTA
O que o edital revela implicitamente sobre o foco da banca?

## 6. CRONOGRAMA SUGERIDO
Distribuição de horas semanais por matéria

## 7. ALERTAS IMPORTANTES
Regras específicas, prazos críticos e armadilhas do edital

EDITAL:
{texto_edital[:8000]}"""

    resposta = client.messages.create(
        model=MODELO_CLAUDE,
        max_tokens=3000,
        system=SYSTEM_AGENTE,
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.content[0].text


def chat_livre(historico, mensagem_usuario, contexto):
    system = SYSTEM_AGENTE
    if contexto:
        system += f"\n\nContexto atual do estudante:\nConcurso: {contexto.get('concurso', '')}\nBanca: {contexto.get('banca', '')}"

    mensagens = historico + [{"role": "user", "content": mensagem_usuario}]

    resposta = client.messages.create(
        model=MODELO_CLAUDE,
        max_tokens=2000,
        system=system,
        messages=mensagens
    )
    return resposta.content[0].text
