import json
import os
from datetime import datetime
from config import DADOS_DIR, AULAS_DIR, PROGRESSO_FILE


def inicializar_storage():
    os.makedirs(AULAS_DIR, exist_ok=True)
    if not os.path.exists(PROGRESSO_FILE):
        dados = {
            "concurso": "",
            "banca": "",
            "aulas": [],
            "questoes_respondidas": 0,
            "questoes_corretas": 0,
            "materias": {}
        }
        salvar_progresso(dados)


def carregar_progresso():
    try:
        with open(PROGRESSO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "concurso": "",
            "banca": "",
            "aulas": [],
            "questoes_respondidas": 0,
            "questoes_corretas": 0,
            "materias": {}
        }


def salvar_progresso(dados):
    with open(PROGRESSO_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def salvar_aula(materia, assunto, conteudo, banca):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"{timestamp}_{materia[:20].replace(' ', '_')}.md"
    caminho = os.path.join(AULAS_DIR, nome_arquivo)

    cabecalho = f"""# {materia} — {assunto}
**Banca:** {banca}  
**Data:** {datetime.now().strftime("%d/%m/%Y %H:%M")}

---

"""
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(cabecalho + conteudo)

    progresso = carregar_progresso()
    progresso["aulas"].append({
        "arquivo": nome_arquivo,
        "materia": materia,
        "assunto": assunto,
        "banca": banca,
        "data": datetime.now().isoformat()
    })

    if materia not in progresso["materias"]:
        progresso["materias"][materia] = {"aulas": 0, "questoes": 0, "acertos": 0}
    progresso["materias"][materia]["aulas"] += 1

    salvar_progresso(progresso)
    return nome_arquivo


def registrar_questao(materia, acertou):
    progresso = carregar_progresso()
    progresso["questoes_respondidas"] += 1
    if acertou:
        progresso["questoes_corretas"] += 1

    if materia not in progresso["materias"]:
        progresso["materias"][materia] = {"aulas": 0, "questoes": 0, "acertos": 0}
    progresso["materias"][materia]["questoes"] += 1
    if acertou:
        progresso["materias"][materia]["acertos"] += 1

    salvar_progresso(progresso)


def listar_aulas():
    progresso = carregar_progresso()
    return progresso.get("aulas", [])


def carregar_aula(nome_arquivo):
    caminho = os.path.join(AULAS_DIR, nome_arquivo)
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    return None
