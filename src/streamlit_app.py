"""
Interfaccia web usando Streamlit per l'agente AI.

Esegui con: streamlit run src/streamlit_app.py
"""

import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Assicura che il progetto sia importabile quando lo script gira da /src
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Carica variabili ambiente
load_dotenv()

# Configura pagina
st.set_page_config(
    page_title="AI Agent Chat",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 AI Agent Chat")
st.markdown("Chatta con il tuo agente AI personalizzato")

# Sidebar per configurazioni
with st.sidebar:
    st.header("⚙️ Configurazioni")

    model = st.selectbox(
        "Modello",
        ["mistral-small-latest", "mistral-medium-latest", "mistral-large-latest"],
        index=0
    )

    temperature = st.slider(
        "Temperatura",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    use_rag = st.checkbox("Usa RAG (Knowledge Base)", value=True)

    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        if "agent" in st.session_state:
            try:
                st.session_state.agent.reset_memory()
            except Exception:
                pass
        st.rerun()

    if st.button("🔄 Ricarica Knowledge Base"):
        if not use_rag:
            st.sidebar.warning("Abilita RAG per ricaricare la knowledge base.")
        elif "agent" in st.session_state and hasattr(st.session_state.agent, "rag"):
            with st.spinner("Ricarico knowledge base..."):
                try:
                    st.session_state.agent.rag.reload()
                    st.sidebar.success("Knowledge base ricaricata.")
                except Exception as e:
                    st.sidebar.error(f"Errore nel reload: {e}")
        else:
            st.sidebar.warning("Agente non pronto, riprova tra poco.")


# Verifica API key
if not os.getenv("MISTRAL_API_KEY"):
    st.error("⚠️ MISTRAL_API_KEY non trovata nel file .env")
    st.stop()

# Inizializza chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inizializza agente
current_config = {
    "model": model,
    "temperature": temperature,
    "use_rag": use_rag
}

if (
    "agent" not in st.session_state
    or st.session_state.get("agent_config") != current_config
):
    with st.spinner("Inizializzazione agente..."):
        try:
            from src.agent import AIAgent
            st.session_state.agent = AIAgent(
                model=model,
                temperature=temperature,
                use_rag=use_rag
            )
            st.session_state.agent_config = current_config
        except Exception as e:
            st.error(f"Errore nell'inizializzazione: {e}")
            st.stop()

# Mostra messaggi esistenti
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utente
if prompt := st.chat_input("Scrivi il tuo messaggio..."):
    # Aggiungi messaggio utente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Ottieni risposta agente
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = st.session_state.agent.chat(prompt)
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Errore: {e}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("© 2026 AI Agent Chat")
