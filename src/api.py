"""
API REST per l'agente AI usando FastAPI.

Questo permette di esporre l'agente come servizio web.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
from src.agent import AIAgent
from loguru import logger

app = FastAPI(
    title="AI Agent API",
    description="API REST per interagire con l'agente AI",
    version="1.0.0"
)

# Inizializza agente (singleton)
agent: Optional[AIAgent] = None


class ChatRequest(BaseModel):
    """Schema per richiesta chat."""
    message: str
    reset_memory: bool = False


class ChatResponse(BaseModel):
    """Schema per risposta chat."""
    response: str
    success: bool


@app.on_event("startup")
async def startup_event():
    """Inizializza l'agente all'avvio."""
    global agent
    try:
        agent = AIAgent(
            model="gpt-3.5-turbo",
            temperature=0.7,
            use_rag=True
        )
        logger.info("Agente AI inizializzato con successo")
    except Exception as e:
        logger.error(f"Errore nell'inizializzazione dell'agente: {e}")
        raise


@app.get("/")
async def root():
    """Endpoint di health check."""
    return {
        "status": "online",
        "service": "AI Agent API",
        "version": "1.0.0"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint per chattare con l'agente.
    
    Args:
        request: Richiesta con messaggio utente
        
    Returns:
        Risposta dell'agente
    """
    if not agent:
        raise HTTPException(status_code=503, detail="Agente non inizializzato")
    
    try:
        # Reset memoria se richiesto
        if request.reset_memory:
            agent.reset_memory()
        
        # Ottieni risposta
        response = agent.chat(request.message)
        
        return ChatResponse(
            response=response,
            success=True
        )
    
    except Exception as e:
        logger.error(f"Errore nella chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset")
async def reset():
    """Reset della memoria conversazionale."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agente non inizializzato")
    
    try:
        agent.reset_memory()
        return {"status": "success", "message": "Memoria resettata"}
    except Exception as e:
        logger.error(f"Errore nel reset: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
