# 🎓 Agente de Concursos

Agente inteligente para preparação de concursos públicos com aulas, questões e análise de edital.

## Instalação

```bash
# 1. Entre na pasta
cd agente_concursos

# 2. Crie o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure sua chave da API
export ANTHROPIC_API_KEY="sua-chave-aqui"   # Linux/Mac
set ANTHROPIC_API_KEY=sua-chave-aqui        # Windows

# 5. Inicie o agente
python app.py
```

## Acesso

- **No seu PC:** http://localhost:5000
- **No celular (mesmo WiFi):** http://IP_DO_SEU_PC:5000
- **Ver IP:** `ipconfig` (Windows) ou `ifconfig` (Mac/Linux)

## Funcionalidades

| Aba | O que faz |
|---|---|
| Início | Estatísticas e configuração |
| Gerar Aula | Aula completa com teoria, macetes e questões |
| Questões | Simulador no estilo da banca |
| Edital | Análise estratégica do edital |
| Chat | Tire dúvidas livremente |
| Histórico | Todas as aulas salvas |

## Estrutura de arquivos

```
agente_concursos/
├── app.py           # Servidor Flask
├── agent.py         # Lógica do Claude
├── storage.py       # Salvar dados
├── config.py        # Configurações
├── requirements.txt
├── templates/
│   └── index.html   # Interface web
└── dados/
    ├── aulas/       # Aulas em .md
    └── progresso.json
```

## Personalização

Edite `config.py` para ajustar:
- Concurso e banca padrão
- Lista de matérias
- Modelo do Claude
