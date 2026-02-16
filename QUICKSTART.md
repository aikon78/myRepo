# 🚀 Quick Start - Come Iniziare in 5 Minuti

## Passo 1: Apri il Codespace (1 minuto)

1. Vai su GitHub nella repository `aikon78/myRepo`
2. Clicca sul pulsante verde **"Code"**
3. Seleziona la tab **"Codespaces"**
4. Clicca su **"Create codespace"** per creare un nuovo Codespace

GitHub creerà automaticamente un ambiente di sviluppo completo nel cloud! ☁️

Il Codespace include:
- ✅ Python 3.11
- ✅ Tutte le librerie AI (LangChain, OpenAI, etc.)
- ✅ VS Code nel browser
- ✅ GitHub Copilot attivato
- ✅ Tutto pronto per sviluppare!

## Passo 2: Configura la tua API Key (2 minuti)

Nel terminale del Codespace, esegui:

```bash
# Crea il file .env dalla template
cp .env.example .env

# Apri il file .env
code .env
```

Modifica il file `.env` e sostituisci `your-openai-api-key-here` con la tua vera API key di OpenAI.

### Come ottenere una API key OpenAI:

1. Vai su https://platform.openai.com/
2. Registrati o fai login
3. Vai su https://platform.openai.com/api-keys
4. Clicca "Create new secret key"
5. Copia la chiave (inizia con `sk-...`)
6. Incollala nel file `.env`

**Costo**: OpenAI offre $5 di credito gratuito per provare. GPT-3.5-turbo costa circa $0.002 per 1000 token (molto economico!).

## Passo 3: Verifica la Configurazione (30 secondi)

```bash
python check_setup.py
```

Dovresti vedere tutti check verdi ✅

Se vedi problemi, il script ti dirà cosa fare!

## Passo 4: Prova il tuo primo Agente AI! (1 minuto)

### Opzione A - Agente Semplice (Consigliata per iniziare)

```bash
python src/simple_agent.py
```

Scrivi qualcosa come:
```
Tu: Ciao! Spiegami cosa fai
Tu: Dimmi 3 idee per un'app AI
Tu: exit
```

### Opzione B - Interfaccia Web (Più carina!)

```bash
streamlit run src/streamlit_app.py
```

Il Codespace aprirà automaticamente una tab del browser con la UI! 🎉

### Opzione C - Agente Avanzato con RAG

```bash
python src/agent.py
```

Prova a chiedere: "Quali prodotti offrite?" - L'agente risponderà usando la knowledge base in `data/knowledge_base.txt`!

## 🎯 Cosa Fare Dopo

### 1. Personalizza la Knowledge Base

Modifica `data/knowledge_base.txt` con le tue informazioni:
- Informazioni sulla tua azienda
- FAQ
- Documentazione prodotti
- Qualsiasi informazione specifica

L'agente userà automaticamente questi dati per rispondere!

### 2. Modifica il System Prompt

Apri `src/simple_agent.py` e cambia il `system_prompt`:

```python
system_prompt = """
Sei [IL TUO ASSISTENTE].
Le tue caratteristiche:
- [CARATTERISTICA 1]
- [CARATTERISTICA 2]
"""
```

Riavvia l'agente e vedrai la differenza!

### 3. Sperimenta con i Modelli

Nel codice, prova a cambiare:
- `gpt-3.5-turbo` → economico e veloce
- `gpt-4` → più intelligente ma più costoso
- `gpt-4-turbo-preview` → GPT-4 più veloce

### 4. Aggiungi Nuovi Tools

Apri `src/agent.py` e aggiungi tools personalizzati nella funzione `_create_custom_tools()`:

```python
Tool(
    name="MioTool",
    func=lambda x: "risultato",
    description="Cosa fa questo tool"
)
```

### 5. Crea un'API

```bash
# Avvia il server API
python src/api.py

# In un altro terminale, testa
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Ciao!"}'
```

Apri http://localhost:8000/docs per la documentazione interattiva!

## 📚 Risorse per Imparare di Più

1. **Leggi la Guida Completa**: [GUIDA_AI_AGENT.md](GUIDA_AI_AGENT.md)
   - Quale engine scegliere
   - Quando addestrare (spoiler: quasi mai!)
   - RAG vs Fine-tuning
   - Best practices

2. **Esplora il Codice**:
   - `src/simple_agent.py` - Esempio base
   - `src/agent.py` - Esempio avanzato
   - `src/api.py` - REST API
   - `src/streamlit_app.py` - Web UI

3. **Documentazione Ufficiale**:
   - [LangChain](https://python.langchain.com/)
   - [OpenAI](https://platform.openai.com/docs/)
   - [FastAPI](https://fastapi.tiangolo.com/)

## ❓ Problemi Comuni

### "ImportError: No module named 'openai'"

```bash
pip install -r requirements.txt
```

### "OpenAI API key not found"

Hai creato il file `.env`? Controlla che sia nella directory principale e contenga:
```
OPENAI_API_KEY=sk-tua-chiave-qui
```

### "Rate limit exceeded"

Stai usando troppi token. Aspetta un minuto o aggiungi credito al tuo account OpenAI.

### Il Codespace è lento

Controlla la configurazione della macchina. Puoi upgradare a una macchina più potente nelle impostazioni del Codespace.

## 🎉 Sei Pronto!

Ora hai tutto ciò che serve per:
- ✅ Creare agenti AI conversazionali
- ✅ Usare RAG per knowledge base personalizzata
- ✅ Costruire API e interfacce web
- ✅ Sperimentare con diversi modelli
- ✅ Sviluppare in modo professionale

**Prossimo passo**: Inizia a sperimentare e costruisci il TUO agente AI! 🚀

---

💡 **Suggerimento**: Usa GitHub Copilot (già incluso nel Codespace) per aiutarti a scrivere codice. Prova a scrivere un commento come `# crea una funzione che...` e Copilot ti suggerirà il codice!
