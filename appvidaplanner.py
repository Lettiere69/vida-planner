import datetime
import streamlit as st

# --- PROTEÇÃO POR SENHA ---
st.set_page_config(page_title="VidaPlanner", layout="centered")
senha = st.text_input("Digite a senha para acessar:", type="password")

senha_correta = "vidaplanner2024"
if senha != senha_correta:
    st.warning("Acesso negado. Digite a senha correta.")
    st.stop()

# --- CONFIGURAÇÕES BÁSICAS ---
horario_acordar = "06:45"
horario_trabalho_inicio = "08:00"
horario_trabalho_fim = "18:00"
dias_semana = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]

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
treino_index = st.session_state.get("treino_index", 0)

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
    dia = dia.lower()
    agenda = []

    agenda.append("06:45 - Acordar")

    if dia in ["segunda", "terça", "quarta", "quinta", "sexta"]:
        agenda.append("08:00 - 18:00 | Trabalho")

        if dia == "quarta":
            agenda.append("18:00 - 19:00 | Chegar em casa, banho e lanche")
            agenda.extend(eventos_fixos.get("quarta", []))
        else:
            agenda.append("18:00 - 18:30 | Chegar em casa, banho e lanche")
            if vai_correr:
                treino = treinos_corrida[st.session_state.treino_index % len(treinos_corrida)]
                agenda.append(f"18:30 - 19:30 | Corrida - {treino}")
                st.session_state.treino_index += 1
            else:
                agenda.append("18:30 - 19:30 | Musculação")
            agenda.append("20:00 - 21:00 | Jogo para desestressar")
            agenda.append("21:00 - 22:00 | Tempo livre ou leitura (opcional)")
            agenda.append("22:30 - Dormir 💤")

    elif dia == "sábado":
        agenda.append("Manhã livre")
        agenda.extend(eventos_fixos.get("sábado", []))
        if vai_correr:
            treino = treinos_corrida[st.session_state.treino_index % len(treinos_corrida)]
            agenda.append(f"18:30 - 19:30 | Corrida - {treino}")
            st.session_state.treino_index += 1
        else:
            agenda.append("18:30 - 19:30 | Musculação")
        agenda.append("20:00 - 21:30 | Lazer / Jogo")
        agenda.append("22:30 - Dormir 💤")

    elif dia == "domingo":
        agenda.append("Manhã livre / descanso")
        if vai_correr:
            treino = treinos_corrida[st.session_state.treino_index % len(treinos_corrida)]
            agenda.append(f"15:00 - 16:00 | Corrida - {treino}")
            st.session_state.treino_index += 1
        else:
            agenda.append("15:00 - 16:00 | Musculação ou descanso")
        agenda.append("17:00 - 18:00 | Revisar a semana / planejar")
        agenda.append("19:00 - 20:00 | Tempo livre ou leitura")
        agenda.append("22:00 - Dormir 💤")

    if dia in eventos_personalizados:
        agenda.extend(eventos_personalizados[dia])

    return agenda

# --- INTERFACE STREAMLIT ---
st.title("VidaPlanner – Planejador Diário")

dia_escolhido = st.selectbox("Escolha o dia da semana para gerar a agenda:", dias_semana)
vai_correr = st.radio("Hoje você vai correr ou fazer musculação?", ["Correr", "Musculação"]) == "Correr"

if st.button("Gerar Agenda"):
    agenda = gerar_agenda(dia_escolhido, vai_correr)
    st.subheader(f"Agenda sugerida para {dia_escolhido.capitalize()}:")

    nova_agenda = []
    for i, item in enumerate(agenda):
        novo_item = st.text_input(f"Item {i+1}", item)
        nova_agenda.append(novo_item)

    if st.button("Aprovar e Salvar Agenda"):
        nome_arquivo = f"agenda_{dia_escolhido}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(f"Agenda para {dia_escolhido.capitalize()}\n")
            f.write("="*30 + "\n")
            for item in nova_agenda:
                f.write(f"{item}\n")
        st.success(f"Agenda salva como '{nome_arquivo}'")
