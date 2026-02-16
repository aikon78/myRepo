"""
AI Agent con RAG (Retrieval Augmented Generation)

Questo esempio mostra come creare un agente AI che:
- Utilizza LangChain per orchestrazione
- Implementa RAG per knowledge base personalizzata
- Gestisce memoria conversazionale
- Supporta multiple tools

Provider predefinito: Mistral AI.
"""

import os
from typing import List, Optional
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from loguru import logger

# Carica variabili ambiente
load_dotenv()


class RAGSystem:
    """Sistema RAG per recupero informazioni da knowledge base."""

    def __init__(
        self,
        knowledge_base_path: str = "data",
        api_key: Optional[str] = None,
        base_url: str = "https://api.mistral.ai/v1"
    ):
        """
        Inizializza il sistema RAG.

        Args:
            knowledge_base_path: Path alla directory con i documenti
        """
        if not api_key:
            api_key = os.getenv("MISTRAL_API_KEY")

        self.knowledge_base_path = knowledge_base_path
        self.embeddings = OpenAIEmbeddings(
            model="mistral-embed",
            openai_api_key=api_key,
            openai_api_base=base_url
        )
        self.vectorstore = None
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Carica i documenti e crea il vector store."""
        try:
            # Carica documenti
            loader = DirectoryLoader(
                self.knowledge_base_path,
                glob="**/*.txt",
                loader_cls=TextLoader
            )
            documents = loader.load()

            if not documents:
                logger.warning(
                    f"Nessun documento trovato in {self.knowledge_base_path}")
                return

            # Split in chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_documents(documents)

            # Crea vector store
            self.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory="./chroma_db"
            )

            logger.info(
                f"Knowledge base caricata: {len(chunks)} chunks da {len(documents)} documenti")

        except Exception as e:
            logger.error(f"Errore nel caricamento della knowledge base: {e}")

    def search(self, query: str, k: int = 3) -> str:
        """
        Cerca informazioni rilevanti nella knowledge base.

        Args:
            query: Query di ricerca
            k: Numero di risultati da restituire

        Returns:
            Testo concatenato dei risultati più rilevanti
        """
        if not self.vectorstore:
            return "Knowledge base non disponibile."

        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return "\n\n".join([doc.page_content for doc in results])
        except Exception as e:
            logger.error(f"Errore nella ricerca: {e}")
            return f"Errore nella ricerca: {e}"


class AIAgent:
    """Agente AI principale con capacità di conversazione e accesso a tools."""

    def __init__(
        self,
        model: str = "mistral-small-latest",
        temperature: float = 0.7,
        use_rag: bool = True,
        knowledge_base_path: str = "data"
    ):
        """
        Inizializza l'agente AI.

        Args:
            model: Modello Mistral da utilizzare
            temperature: Temperatura per la generazione (0-1)
            use_rag: Se utilizzare il sistema RAG
            knowledge_base_path: Path alla knowledge base
        """
        # Verifica API key
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY non trovata nel file .env")

        base_url = "https://api.mistral.ai/v1"

        # Inizializza LLM
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=api_key,
            openai_api_base=base_url
        )

        # Inizializza memoria
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Inizializza tools
        tools = []

        # Aggiungi RAG se abilitato
        if use_rag:
            self.rag = RAGSystem(
                knowledge_base_path=knowledge_base_path,
                api_key=api_key,
                base_url=base_url
            )
            tools.append(
                Tool(
                    name="KnowledgeBase",
                    func=self.rag.search,
                    description="Utile per cercare informazioni nella knowledge base aziendale. "
                    "Usa questo quando l'utente fa domande su informazioni specifiche "
                    "o su argomenti che potrebbero essere nella documentazione."
                )
            )

        # Aggiungi altri tools personalizzati
        tools.extend(self._create_custom_tools())

        # Inizializza agent
        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )

        logger.info(f"Agente AI inizializzato con {len(tools)} tools")

    def _create_custom_tools(self) -> List[Tool]:
        """
        Crea tools personalizzati per l'agente.

        Returns:
            Lista di tools
        """
        def safe_calculate(expression: str) -> str:
            """Calcola in modo sicuro espressioni matematiche."""
            try:
                # Rimuovi spazi
                expression = expression.strip()
                # Usa un approccio più sicuro limitando il namespace
                allowed_names = {
                    'abs': abs, 'round': round, 'min': min, 'max': max,
                    'sum': sum, 'pow': pow
                }
                # Valuta solo con funzioni matematiche sicure
                result = eval(expression, {"__builtins__": {}}, allowed_names)
                return str(result)
            except Exception as e:
                return f"Errore nel calcolo: {e}"

        return [
            Tool(
                name="Calculator",
                func=safe_calculate,
                description="Utile per eseguire calcoli matematici semplici. "
                "Input deve essere un'espressione matematica valida (es: 2+2, 10*5, pow(2,3))."
            ),
            # Aggiungi altri tools qui secondo le tue necessità
        ]

    def chat(self, message: str) -> str:
        """
        Invia un messaggio all'agente e ricevi una risposta.

        Args:
            message: Messaggio dell'utente

        Returns:
            Risposta dell'agente
        """
        try:
            response = self.agent.run(message)
            return response
        except Exception as e:
            logger.error(f"Errore nella conversazione: {e}")
            return f"Mi dispiace, si è verificato un errore: {e}"

    def reset_memory(self):
        """Resetta la memoria conversazionale."""
        self.memory.clear()
        logger.info("Memoria conversazionale resettata")


def main():
    """Esempio di utilizzo dell'agente."""

    # Inizializza agente
    agent = AIAgent(
        model="mistral-small-latest",
        temperature=0.7,
        use_rag=True
    )

    print("🤖 Agente AI avviato! (scrivi 'exit' per uscire, 'reset' per resettare la memoria)\n")

    # Loop conversazionale
    while True:
        try:
            user_input = input("Tu: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'esci']:
                print("👋 Arrivederci!")
                break

            if user_input.lower() == 'reset':
                agent.reset_memory()
                print("✅ Memoria resettata!\n")
                continue

            # Ottieni risposta
            response = agent.chat(user_input)
            print(f"\n🤖 Agent: {response}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Arrivederci!")
            break
        except Exception as e:
            logger.error(f"Errore: {e}")
            print(f"❌ Errore: {e}\n")


if __name__ == "__main__":
    main()
