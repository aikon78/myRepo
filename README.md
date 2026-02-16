# 🤖 AI Agent Development Environment

Ambiente di sviluppo completo per creare agenti di intelligenza artificiale usando GitHub Codespaces.

## 📋 Indice

- [Caratteristiche](#caratteristiche)
- [Quick Start](#quick-start)
- [Guida Completa](#guida-completa)
- [Esempi](#esempi)
- [Struttura del Progetto](#struttura-del-progetto)
- [API Reference](#api-reference)

## ✨ Caratteristiche

- 🚀 **GitHub Codespaces** preconfigurato con tutte le dipendenze
- 🤖 **Multiple implementazioni** di agenti AI (semplice, avanzato, con RAG)
- 📚 **RAG (Retrieval Augmented Generation)** per knowledge base personalizzata
- 🌐 **API REST** con FastAPI
- 💬 **Interfaccia Web** con Streamlit
- 🔧 **Supporto per OpenAI e Anthropic**
- 📊 **Esempi pratici** e documentazione completa

## 🚀 Quick Start

### 1. Apri in Codespace

Clicca sul pulsante "Code" → "Codespaces" → "Create codespace on main"

GitHub installerà automaticamente tutte le dipendenze!

### 2. Configura le API Keys

```bash
# Crea il file .env dalla template
cp .env.example .env

# Modifica .env e aggiungi la tua OpenAI API key
# OPENAI_API_KEY=sk-...
```

Ottieni la tua API key da:
- OpenAI: https://platform.openai.com/api-keys
- Anthropic (opzionale): https://console.anthropic.com/

### 3. Prova l'Agente

**Opzione A - Agente Semplice (Console):**
```bash
python src/simple_agent.py
```

**Opzione B - Agente Avanzato con RAG:**
```bash
python src/agent.py
```

**Opzione C - Interfaccia Web (Streamlit):**
```bash
streamlit run src/streamlit_app.py
```

**Opzione D - API REST (FastAPI):**
```bash
python src/api.py
# Apri http://localhost:8000/docs per la documentazione API
```

## 📖 Guida Completa

Leggi [GUIDA_AI_AGENT.md](GUIDA_AI_AGENT.md) per una guida completa che include:

- 🎯 **Scelta dell'Engine**: Quale modello AI usare (OpenAI, Anthropic, Open Source)
- 🎓 **Training**: Se e quando addestrare un modello
- 🔍 **RAG vs Fine-Tuning**: Quale approccio scegliere
- 💡 **Best Practices**: Prompt engineering, gestione della memoria, tools
- 📚 **Esempi pratici**: Codice pronto all'uso

### Raccomandazioni Rapide

**Engine consigliato**: LangChain + OpenAI GPT-3.5-turbo (o GPT-4)

**Devo addestrare?** NO nella maggior parte dei casi. Usa invece:
1. **Prompt Engineering** (sempre)
2. **RAG** per knowledge base specifica (incluso in questo repo)
3. **Fine-tuning** solo come ultima risorsa

## 📝 Esempi

### Esempio 1: Chat Semplice

```python
from src.simple_agent import SimpleAgent

agent = SimpleAgent(model="gpt-3.5-turbo")
response = agent.chat("Ciao! Come funziona un agente AI?")
print(response)
```

### Esempio 2: Agent con RAG

```python
from src.agent import AIAgent

# L'agente userà automaticamente i documenti in ./data
agent = AIAgent(use_rag=True)
response = agent.chat("Quali prodotti offrite?")
print(response)  # Risponderà basandosi sulla knowledge base
```

### Esempio 3: API REST

```bash
# Avvia il server
python src/api.py

# In un altro terminale, testa l'API
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Ciao!"}'
```

## 📁 Struttura del Progetto

```
myRepo/
├── .devcontainer/
│   └── devcontainer.json      # Configurazione Codespace
├── src/
│   ├── agent.py               # Agente avanzato con LangChain e RAG
│   ├── simple_agent.py        # Agente semplice con OpenAI
│   ├── api.py                 # API REST con FastAPI
│   └── streamlit_app.py       # UI web con Streamlit
├── data/
│   └── knowledge_base.txt     # Knowledge base per RAG
├── tests/
│   └── test_agent.py          # Tests
├── .env.example               # Template per variabili ambiente
├── .gitignore                 # File da ignorare
├── requirements.txt           # Dipendenze Python
├── GUIDA_AI_AGENT.md         # Guida completa (LEGGI QUESTO!)
└── README.md                  # Questo file
```

## 🔧 API Reference

### SimpleAgent

```python
agent = SimpleAgent(
    model="gpt-3.5-turbo",     # Modello OpenAI
    system_prompt="..."         # Prompt di sistema personalizzato
)

response = agent.chat("messaggio")  # Invia messaggio
agent.reset()                       # Reset conversazione
```

### AIAgent (Avanzato)

```python
agent = AIAgent(
    model="gpt-4",              # Modello OpenAI
    temperature=0.7,            # Creatività (0-1)
    use_rag=True,              # Usa RAG
    knowledge_base_path="data"  # Path documenti
)

response = agent.chat("messaggio")  # Invia messaggio
agent.reset_memory()                # Reset memoria
```

## 🧪 Testing

```bash
# Esegui i test
pytest tests/ -v

# Con coverage
pytest tests/ --cov=src --cov-report=html
```

## 📚 Risorse Utili

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🤝 Contribuire

I contributi sono benvenuti! Sentiti libero di aprire issue o pull request.

## 📄 Licenza

MIT

## ❓ Domande Frequenti

**Q: Quale modello devo usare?**  
A: Inizia con `gpt-3.5-turbo` per sviluppo (più economico). Usa `gpt-4` per produzione (più potente).

**Q: Come aggiungo documenti alla knowledge base?**  
A: Aggiungi file .txt nella cartella `data/`. Il sistema RAG li caricherà automaticamente.

**Q: Devo addestrare il modello?**  
A: No! Usa RAG (già configurato) per aggiungere conoscenza specifica. Leggi [GUIDA_AI_AGENT.md](GUIDA_AI_AGENT.md) per dettagli.

**Q: Come faccio deploy in produzione?**  
A: Usa Docker, Heroku, AWS, Azure o Google Cloud. L'API FastAPI è pronta per il deploy.

**Q: Posso usare modelli open source?**  
A: Sì! Modifica il codice per usare Llama, Mistral o altri modelli. Vedi guida per dettagli.

---

Made with ❤️ for AI enthusiasts
