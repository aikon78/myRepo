"""
AI Agent con RAG (Retrieval Augmented Generation)

Questo esempio mostra come creare un agente AI che:
- Utilizza LangChain per orchestrazione
- Implementa RAG per knowledge base personalizzata
- Gestisce memoria conversazionale
- Supporta multiple tools
"""

import os
from typing import List, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader, DirectoryLoader
from loguru import logger

# Carica variabili ambiente
load_dotenv()


class RAGSystem:
    """Sistema RAG per recupero informazioni da knowledge base."""
    
    def __init__(self, knowledge_base_path: str = "data"):
        """
        Inizializza il sistema RAG.
        
        Args:
            knowledge_base_path: Path alla directory con i documenti
        """
        self.knowledge_base_path = knowledge_base_path
        self.embeddings = OpenAIEmbeddings()
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
                logger.warning(f"Nessun documento trovato in {self.knowledge_base_path}")
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
            
            logger.info(f"Knowledge base caricata: {len(chunks)} chunks da {len(documents)} documenti")
            
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
        model: str = "gpt-4",
        temperature: float = 0.7,
        use_rag: bool = True,
        knowledge_base_path: str = "data"
    ):
        """
        Inizializza l'agente AI.
        
        Args:
            model: Modello OpenAI da utilizzare
            temperature: Temperatura per la generazione (0-1)
            use_rag: Se utilizzare il sistema RAG
            knowledge_base_path: Path alla knowledge base
        """
        # Verifica API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY non trovata nel file .env")
        
        # Inizializza LLM
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key
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
            self.rag = RAGSystem(knowledge_base_path)
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
        return [
            Tool(
                name="Calculator",
                func=lambda x: str(eval(x)),
                description="Utile per eseguire calcoli matematici. "
                           "Input deve essere un'espressione matematica valida."
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
        model="gpt-3.5-turbo",  # Usa gpt-4 per risultati migliori
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
