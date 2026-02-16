"""
Pagina Streamlit con prompt di richieste pronti all'uso.
"""

import streamlit as st

st.set_page_config(
    page_title="Prompt richieste",
    page_icon=":page_facing_up:",
    layout="wide"
)

st.title("Prompt di richieste")
st.markdown(
    "Usa questi prompt come base per richieste strutturate. "
    "Compila i campi e copia il risultato."
)

CATEGORIES = {
    "Supporto clienti": (
        "Sei un assistente di supporto clienti. Rispondi in italiano con tono {tone}. "
        "Contesto: {context}. Richiesta: {details}. "
        "Formato risposta: {format}."
    ),
    "Analisi e sintesi": (
        "Agisci come analista. Riassumi e analizza: {details}. "
        "Contesto: {context}. Tono: {tone}. "
        "Formato: {format}."
    ),
    "Scrittura contenuti": (
        "Sei un copywriter. Scrivi un testo su: {details}. "
        "Pubblico: {context}. Tono: {tone}. "
        "Formato: {format}."
    ),
    "Sviluppo software": (
        "Sei un ingegnere software. Risolvi la richiesta: {details}. "
        "Stack/contesto: {context}. Stile risposta: {tone}. "
        "Formato output: {format}."
    ),
    "Pianificazione progetto": (
        "Sei un project manager. Crea un piano per: {details}. "
        "Vincoli/contesto: {context}. Tono: {tone}. "
        "Formato: {format}."
    ),
}

with st.sidebar:
    st.header("Impostazioni prompt")
    category = st.selectbox("Categoria", list(CATEGORIES.keys()), index=0)
    tone = st.selectbox(
        "Tono",
        ["professionale", "chiaro e sintetico", "amichevole", "tecnico"],
        index=0
    )
    output_format = st.selectbox(
        "Formato risposta",
        ["bullet points", "passi numerati", "paragrafo breve", "checklist"],
        index=0
    )

context = st.text_input("Contesto / destinatario", "")
details = st.text_area("Dettagli richiesta", "", height=160)

if not details.strip():
    st.info("Inserisci i dettagli della richiesta per generare il prompt.")

prompt_template = CATEGORIES[category]

final_prompt = prompt_template.format(
    tone=tone,
    context=context or "N/A",
    details=details or "N/A",
    format=output_format
)

st.subheader("Prompt generato")
st.code(final_prompt, language="text")

st.markdown(
    "Suggerimento: aggiungi esempi o vincoli specifici per risposte migliori.")
