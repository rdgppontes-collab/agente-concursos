from flask import Flask, render_template, request, jsonify, send_file
import os
import markdown
from config import MATERIAS, BANCAS, NIVEIS, CONCURSO_ATUAL, BANCA_ATUAL
from storage import (inicializar_storage, salvar_aula, listar_aulas,
                     carregar_aula, carregar_progresso, registrar_questao)
from agent import gerar_aula, gerar_questoes, analisar_edital, chat_livre

app = Flask(__name__)
inicializar_storage()

historico_chat = []


@app.route("/")
def index():
    progresso = carregar_progresso()
    return render_template("index.html",
                           materias=MATERIAS,
                           bancas=BANCAS,
                           niveis=NIVEIS,
                           concurso=CONCURSO_ATUAL,
                           banca=BANCA_ATUAL,
                           progresso=progresso)


@app.route("/gerar-aula", methods=["POST"])
def rota_gerar_aula():
    dados = request.json
    materia = dados.get("materia", "")
    assunto = dados.get("assunto", "")
    banca = dados.get("banca", BANCA_ATUAL)
    nivel = dados.get("nivel", "iniciante")
    referencia = dados.get("referencia", "")
    concurso = dados.get("concurso", CONCURSO_ATUAL)

    if not materia or not assunto:
        return jsonify({"erro": "Matéria e assunto são obrigatórios"}), 400

    try:
        conteudo = gerar_aula(materia, assunto, banca, nivel, referencia, concurso)
        arquivo = salvar_aula(materia, assunto, conteudo, banca)
        conteudo_html = markdown.markdown(conteudo, extensions=["tables", "fenced_code"])
        return jsonify({
            "conteudo": conteudo_html,
            "conteudo_md": conteudo,
            "arquivo": arquivo
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/gerar-questoes", methods=["POST"])
def rota_gerar_questoes():
    dados = request.json
    materia = dados.get("materia", "")
    assunto = dados.get("assunto", "")
    banca = dados.get("banca", BANCA_ATUAL)
    quantidade = dados.get("quantidade", 3)
    nivel = dados.get("nivel", "intermediário")

    if not materia or not assunto:
        return jsonify({"erro": "Matéria e assunto são obrigatórios"}), 400

    try:
        conteudo = gerar_questoes(materia, assunto, banca, quantidade, nivel)
        conteudo_html = markdown.markdown(conteudo, extensions=["tables", "fenced_code"])
        return jsonify({"conteudo": conteudo_html, "conteudo_md": conteudo})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/analisar-edital", methods=["POST"])
def rota_analisar_edital():
    dados = request.json
    texto = dados.get("texto", "")

    if not texto or len(texto) < 100:
        return jsonify({"erro": "Cole o texto do edital (mínimo 100 caracteres)"}), 400

    try:
        analise = analisar_edital(texto)
        analise_html = markdown.markdown(analise, extensions=["tables", "fenced_code"])
        return jsonify({"conteudo": analise_html, "conteudo_md": analise})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/chat", methods=["POST"])
def rota_chat():
    global historico_chat
    dados = request.json
    mensagem = dados.get("mensagem", "")
    progresso = carregar_progresso()

    if not mensagem:
        return jsonify({"erro": "Mensagem vazia"}), 400

    try:
        resposta = chat_livre(historico_chat, mensagem, progresso)
        historico_chat.append({"role": "user", "content": mensagem})
        historico_chat.append({"role": "assistant", "content": resposta})
        if len(historico_chat) > 20:
            historico_chat = historico_chat[-20:]
        resposta_html = markdown.markdown(resposta, extensions=["tables"])
        return jsonify({"resposta": resposta_html, "resposta_md": resposta})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/registrar-resposta", methods=["POST"])
def rota_registrar_resposta():
    dados = request.json
    materia = dados.get("materia", "Geral")
    acertou = dados.get("acertou", False)
    registrar_questao(materia, acertou)
    return jsonify({"ok": True})


@app.route("/historico")
def rota_historico():
    aulas = listar_aulas()
    return jsonify({"aulas": aulas})


@app.route("/aula/<nome_arquivo>")
def rota_ver_aula(nome_arquivo):
    conteudo = carregar_aula(nome_arquivo)
    if conteudo:
        conteudo_html = markdown.markdown(conteudo, extensions=["tables", "fenced_code"])
        return jsonify({"conteudo": conteudo_html, "conteudo_md": conteudo})
    return jsonify({"erro": "Aula não encontrada"}), 404


@app.route("/progresso")
def rota_progresso():
    return jsonify(carregar_progresso())


if __name__ == "__main__":
    print("\n🎓 Agente de Concursos iniciado!")
    print("📱 Acesse no navegador: http://localhost:5000")
    print("🌐 Na rede local: http://SEU_IP:5000\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
