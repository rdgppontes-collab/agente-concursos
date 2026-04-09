import os

# Configurações do agente
CONCURSO_ATUAL = "CAIXA ECONÔMICA FEDERAL - Técnico Bancário Novo"
BANCA_ATUAL = "CESGRANRIO"

MATERIAS = [
    "Conhecimentos Bancários",
    "Atendimento Bancário",
    "Língua Portuguesa",
    "Matemática Financeira",
    "Probabilidade e Estatística",
    "Compliance e Ética",
    "Tecnologia da Informação",
    "Comportamentos Digitais",
    "Língua Inglesa",
]

BANCAS = ["CESGRANRIO", "CESPE/CEBRASPE", "FCC", "VUNESP", "FGV"]

NIVEIS = ["iniciante", "intermediário", "avançado"]

MODELO_CLAUDE = "claude-sonnet-4-6"

DADOS_DIR = os.path.join(os.path.dirname(__file__), "dados")
AULAS_DIR = os.path.join(DADOS_DIR, "aulas")
PROGRESSO_FILE = os.path.join(DADOS_DIR, "progresso.json")
