# Guida allo Sviluppo di Agenti AI

## Panoramica

Questa guida ti aiuterà a scegliere l'engine giusto per il tuo agente AI e a capire se e come addestrarlo.

## 1. Scelta dell'Engine AI

### Opzioni Principali

#### A. **OpenAI GPT (Consigliato per iniziare)**
- **Modelli**: GPT-4, GPT-3.5-turbo
- **Vantaggi**: 
  - Eccellente comprensione del linguaggio naturale
  - Ampia documentazione e comunità
  - Nessun addestramento necessario (pre-addestrato)
  - API facile da usare
- **Casi d'uso**: Chatbot, assistenti virtuali, analisi di testo
- **Costo**: Pay-per-use (API)

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Ciao!"}]
)
```

#### B. **Anthropic Claude**
- **Modelli**: Claude 3 (Opus, Sonnet, Haiku)
- **Vantaggi**:
  - Eccellente per conversazioni lunghe
  - Buona sicurezza e allineamento
  - Context window molto ampio
- **Casi d'uso**: Analisi di documenti, assistenza complessa
- **Costo**: Pay-per-use (API)

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Ciao!"}]
)
```

#### C. **LangChain (Framework - Consigliato)**
- **Tipo**: Framework per costruire applicazioni con LLM
- **Vantaggi**:
  - Supporta multipli provider (OpenAI, Anthropic, ecc.)
  - Tools per RAG (Retrieval Augmented Generation)
  - Gestione della memoria e catene complesse
  - Integrazioni con vector databases
- **Ideale per**: Agenti complessi con memoria, tool usage, RAG

```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

chat = ChatOpenAI(temperature=0)
response = chat([HumanMessage(content="Ciao!")])
```

#### D. **Modelli Open Source (Llama, Mistral)**
- **Vantaggi**:
  - Completamente gratuiti
  - Possono essere hostati localmente
  - Privacy completa dei dati
- **Svantaggi**:
  - Richiedono hardware potente (GPU)
  - Performance inferiore ai modelli commerciali
  - Necessitano configurazione complessa

## 2. Devo Addestrare il Modello?

### Risposta Breve: **Probabilmente NO**

La maggior parte dei casi d'uso NON richiede addestramento. Ecco le alternative:

### A. **Prompt Engineering (Approccio Consigliato)**
Nessun addestramento necessario, solo prompt ben strutturati.

```python
system_prompt = """
Sei un assistente esperto in [dominio specifico].
Le tue responsabilità sono:
1. [Compito 1]
2. [Compito 2]

Regole:
- Rispondi sempre in italiano
- Sii conciso ma completo
"""

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "domanda utente"}
]
```

### B. **RAG - Retrieval Augmented Generation (Molto Consigliato)**
Fornisci conoscenza specifica senza addestramento.

**Vantaggi**:
- Nessun costo di addestramento
- Facilmente aggiornabile
- Informazioni sempre attuali
- Più economico del fine-tuning

**Come funziona**:
1. Carica i tuoi documenti
2. Crea embeddings
3. Salva in un vector database
4. Recupera informazioni rilevanti al momento della query
5. Passa le informazioni al LLM

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

# Carica documenti
loader = TextLoader('knowledge_base.txt')
documents = loader.load()

# Split in chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

# Crea embeddings e salva in vector DB
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embeddings)

# Query
results = vectorstore.similarity_search("la mia domanda")
```

### C. **Fine-Tuning (Solo se necessario)**

**Quando considerarlo**:
- Hai un dominio molto specifico
- Hai migliaia di esempi di alta qualità
- Il prompt engineering non è sufficiente
- Hai budget per l'addestramento

**Costi e Requisiti**:
- Minimo 50-100 esempi (meglio 500+)
- Costo variabile (OpenAI: ~$0.008 per 1K tokens)
- Tempo: ore/giorni
- Validazione richiesta

**Processo**:
```python
from openai import OpenAI

client = OpenAI()

# 1. Prepara dataset in formato JSONL
# {"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}

# 2. Upload file
file = client.files.create(
    file=open("training_data.jsonl", "rb"),
    purpose="fine-tune"
)

# 3. Crea fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=file.id,
    model="gpt-3.5-turbo"
)
```

## 3. Architettura Consigliata per Iniziare

### Setup Base con LangChain + RAG

```
my-ai-agent/
├── .devcontainer/          # Codespace configuration
├── data/                   # Knowledge base documents
│   └── knowledge_base.txt
├── src/
│   ├── agent.py           # Main agent logic
│   ├── rag.py             # RAG implementation
│   └── utils.py           # Utility functions
├── tests/
│   └── test_agent.py
├── .env.example
├── requirements.txt
└── README.md
```

### Esempio Agent Completo

```python
# src/agent.py
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from rag import RAGSystem

class AIAgent:
    def __init__(self, api_key):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model="gpt-4",
            openai_api_key=api_key
        )
        
        self.rag = RAGSystem(api_key)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        tools = [
            Tool(
                name="KnowledgeBase",
                func=self.rag.search,
                description="Cerca nella base di conoscenza"
            )
        ]
        
        self.agent = initialize_agent(
            tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )
    
    def chat(self, message):
        return self.agent.run(message)
```

## 4. Prossimi Passi

1. **Setup immediato**:
   ```bash
   # Crea .env file
   echo "OPENAI_API_KEY=your-key-here" > .env
   
   # Installa dipendenze
   pip install -r requirements.txt
   
   # Testa l'agent
   python src/agent.py
   ```

2. **Inizia con Prompt Engineering**:
   - Sperimenta con diversi system prompts
   - Testa con vari scenari
   - Itera e migliora

3. **Aggiungi RAG se necessario**:
   - Carica i tuoi documenti
   - Configura il vector database
   - Integra con l'agent

4. **Fine-Tuning solo come ultima risorsa**:
   - Solo dopo aver esaurito altre opzioni
   - Con dataset di qualità
   - Con budget adeguato

## 5. Risorse Utili

- **LangChain Docs**: https://python.langchain.com/
- **OpenAI API Reference**: https://platform.openai.com/docs/
- **Anthropic Claude**: https://docs.anthropic.com/
- **Vector Databases**: ChromaDB, Pinecone, Weaviate
- **Esempi**: https://github.com/langchain-ai/langchain/tree/master/templates

## Conclusione

**Raccomandazione finale**:
- **Engine**: LangChain + OpenAI GPT-4 (o GPT-3.5-turbo per costi minori)
- **Approccio**: Prompt Engineering + RAG
- **Addestramento**: Non necessario per il 90% dei casi

Inizia semplice, itera rapidamente, e scala solo quando necessario!
