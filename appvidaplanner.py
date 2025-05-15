import datetime
import streamlit as st
import json
import os

# --- PROTEÇÃO POR SENHA COM MEMÓRIA DE SESSÃO ---
st.set_page_config(page_title="VidaPlanner", layout="wide")

if "acesso_liberado" not in st.session_state:
    st.session_state.acesso_liberado = False

if not st.session_state.acesso_liberado:
    st.markdown("""<h2 style='text-align: center;'>🔒 VidaPlanner</h2>""", unsafe_allow_html=True)
    senha = st.text_input("Digite a senha para acessar:", type="password")
    senha_correta = "vidaplanner2024"
    if senha == senha_correta:
        st.session_state.acesso_liberado = True
        st.rerun()
    else:
        st.warning("Acesso negado. Digite a senha correta.")
        st.stop()

# --- CONFIGURAÇÕES BÁSICAS ---
horario_acordar = "06:45"
horario_trabalho_inicio = "08:00"
horario_trabalho_fim = "18:00"
dias_semana = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]

# --- SALVAR PROGRESSO DE TREINOS ---
arquivo_progresso = "progresso_treino.json"
if os.path.exists(arquivo_progresso):
    with open(arquivo_progresso, "r") as f:
        progresso = json.load(f)
else:
    progresso = {"treino_index": 0}

# Controle de treino de corrida sequencial
treinos_corrida = [
    "Corrida leve 3km - foco em manter o pace abaixo de 6:30",
    "Treino intervalado: 4x400m rápido + 200m caminhada",
    "Rodagem 4km - respiração controlada",
    "Progressivo 3km (aumentar o ritmo a cada km)",
    "Longão 5km ritmo constante",
    "Treino de tiros: 6x300m forte + 1min descanso",
    "Corrida leve 3.5km - foco em postura",
    "Rodagem 5km - simulação leve de prova"
]

# Eventos fixos e personalizados
eventos_fixos = {
    "quarta": ["19:00 - 00:00 | Centro Espírita"],
    "sábado": ["14:30 - 18:00 | Centro Espírita"]
}
eventos_personalizados = {
    "segunda": ["20:00 - 21:00 | Reunião com mentor"],
    "domingo": ["10:00 - 11:00 | Estudo do Evangelho"]
}

# --- FUNÇÃO PRINCIPAL ---
def gerar_agenda(dia, vai_correr):
    agenda = ["06:45 - Acordar"]
    dia = dia.lower()

    if dia in ["segunda", "terça", "quarta", "quinta", "sexta"]:
        agenda.append("08:00 - 18:00 | Trabalho")
        if dia == "quarta":
            agenda.append("18:00 - 19:00 | Chegar em casa, banho e lanche")
            agenda.extend(eventos_fixos.get("quarta", []))
        else:
            agenda.append("18:00 - 18:30 | Chegar em casa, banho e lanche")
            if vai_correr:
                treino = treinos_corrida[progresso["treino_index"] % len(treinos_corrida)]
                agenda.append(f"18:30 - 19:30 | Corrida - {treino}")
                progresso["treino_index"] += 1
            else:
                agenda.append("18:30 - 19:30 | Musculação")
            agenda.extend([
                "20:00 - 21:00 | Jogo para desestressar",
                "21:00 - 22:00 | Tempo livre ou leitura (opcional)",
                "22:30 - Dormir 💤"
            ])

    elif dia == "sábado":
        agenda.append("Manhã livre")
        agenda.extend(eventos_fixos.get("sábado", []))
        if vai_correr:
            treino = treinos_corrida[progresso["treino_index"] % len(treinos_corrida)]
            agenda.append(f"18:30 - 19:30 | Corrida - {treino}")
            progresso["treino_index"] += 1
        else:
            agenda.append("18:30 - 19:30 | Musculação")
        agenda.extend(["20:00 - 21:30 | Lazer / Jogo", "22:30 - Dormir 💤"])

    elif dia == "domingo":
        agenda.append("Manhã livre / descanso")
        if vai_correr:
            treino = treinos_corrida[progresso["treino_index"] % len(treinos_corrida)]
            agenda.append(f"15:00 - 16:00 | Corrida - {treino}")
            progresso["treino_index"] += 1
        else:
            agenda.append("15:00 - 16:00 | Musculação ou descanso")
        agenda.extend([
            "17:00 - 18:00 | Revisar a semana / planejar",
            "19:00 - 20:00 | Tempo livre ou leitura",
            "22:00 - Dormir 💤"
        ])

    if dia in eventos_personalizados:
        agenda.extend(eventos_personalizados[dia])

    return agenda

# --- INTERFACE STREAMLIT ---
st.markdown("""<h1 style='color:#4fc3f7;'>📅 VidaPlanner – Planejador Diário com IA</h1>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    dia_escolhido = st.selectbox("Escolha o dia da semana:", dias_semana)
with col2:
    vai_correr = st.radio("Atividade principal hoje:", ["Correr", "Musculação"]) == "Correr"

if st.button("Gerar Agenda"):
    agenda = gerar_agenda(dia_escolhido, vai_correr)
    with open(arquivo_progresso, "w") as f:
        json.dump(progresso, f)

    st.success(f"Agenda gerada para {dia_escolhido.capitalize()} 🎯")
    st.subheader("✍️ Edite os horários e compromissos do seu dia:")

    nova_agenda = []
    for i, item in enumerate(agenda):
        novo_item = st.text_input(label=f"🕒 {item.split('|')[0].strip()} -", value=item)
        nova_agenda.append(novo_item)

    if st.button("✅ Aprovar e Salvar Agenda"):
        nome_arquivo = f"agenda_{dia_escolhido}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(f"Agenda para {dia_escolhido.capitalize()}\n")
            f.write("="*30 + "\n")
            for item in nova_agenda:
                f.write(f"{item}\n")
        st.success(f"Agenda salva como '{nome_arquivo}'")
