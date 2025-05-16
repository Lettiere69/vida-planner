import datetime
import streamlit as st
import json
import os
from twilio.rest import Client

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

# --- FUNÇÃO PARA ENVIAR WHATSAPP ---
def enviar_agenda_whatsapp(agenda, telefone_destino):
    account_sid = "SEU_ACCOUNT_SID"
    auth_token = "SEU_AUTH_TOKEN"
    client = Client(account_sid, auth_token)

    mensagem = "📋 *Sua agenda do dia:*\n\n"
    for item in agenda:
        mensagem += f"• {item}\n"

    client.messages.create(
        from_="whatsapp:+14155238886",
        to=f"whatsapp:{telefone_destino}",
        body=mensagem
    )

# Controle de treino de corrida sequencial
treinos_corrida = [
    "Corrida leve 3km - aquecimento de 5 min andando + corrida leve focando na respiração. Tente manter pace abaixo de 6:30.",
    "Intervalado: aquecimento 5 min leve + 4x400m em ritmo forte (80-85%) com 200m caminhada entre os tiros. Finalize com desaquecimento leve.",
    "Rodagem contínua 4km - mantenha ritmo constante, foco na cadência e respiração diafragmática.",
    "Treino progressivo 3km - inicie leve, aumente o ritmo a cada km. Último km em ritmo forte.",
    "Longão 5km - mantenha ritmo confortável. Foco é resistência e constância. Não acelere muito.",
    "Tiros curtos: aquecimento 1km + 6x300m com intensidade alta (quase sprint), 1min de descanso parado entre cada.",
    "Corrida leve 3.5km - atenção na postura (tronco ereto, braços relaxados), ritmo controlado.",
    "Rodagem 5km simulando prova - use o tênis que usaria em corrida oficial. Tente ritmo constante e superação leve."
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

    with open(arquivo_progresso, "w") as f:
        json.dump(progresso, f)

    # Enviar WhatsApp após gerar agenda
    try:
        enviar_agenda_whatsapp(agenda, "+5586988248770")
        st.success("📤 Agenda enviada para seu WhatsApp com sucesso!")
    except Exception as e:
        st.error(f"Erro ao enviar WhatsApp: {e}")

    return agenda
