"""
Interfaccia web usando Streamlit per l'agente AI.

Esegui con: streamlit run src/streamlit_app.py
"""

import streamlit as st
import os
from dotenv import load_dotenv

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
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
        index=0
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )
    
    use_rag = st.checkbox("Usa RAG (Knowledge Base)", value=True)
    
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# Verifica API key
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OPENAI_API_KEY non trovata nel file .env")
    st.stop()

# Inizializza chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inizializza agente
if "agent" not in st.session_state or st.session_state.get("model") != model:
    with st.spinner("Inizializzazione agente..."):
        try:
            from src.agent import AIAgent
            st.session_state.agent = AIAgent(
                model=model,
                temperature=temperature,
                use_rag=use_rag
            )
            st.session_state.model = model
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
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Errore: {e}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ using Streamlit")
