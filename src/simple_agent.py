"""
Esempio semplice di agent usando Mistral AI (senza LangChain).

Questo è un approccio più minimale per chi vuole iniziare senza dipendenze complesse.
"""

import os
from typing import List, Dict
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False
from openai import OpenAI

load_dotenv()


class SimpleAgent:
    """Agente AI semplice usando direttamente l'API Mistral."""

    def __init__(self, model: str = "mistral-small-latest", system_prompt: str = None):
        """
        Inizializza l'agente.

        Args:
            model: Modello da utilizzare
            system_prompt: Prompt di sistema personalizzato
        """
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY non trovata nel file .env")

        self.api_key = api_key
        self.base_url = "https://api.mistral.ai/v1"
        self.client = None
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []

        # System prompt di default
        self.system_prompt = system_prompt or """
Sei un assistente AI intelligente e disponibile.
Le tue caratteristiche:
- Rispondi sempre in italiano
- Sei preciso e conciso
- Quando non sai qualcosa, lo ammetti onestamente
- Fornisci esempi pratici quando utile
"""

        # Aggiungi system prompt alla conversazione
        self.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })

    def chat(self, message: str) -> str:
        """
        Invia un messaggio e ricevi una risposta.

        Args:
            message: Messaggio dell'utente

        Returns:
            Risposta dell'agente
        """
        # Aggiungi messaggio utente alla storia
        self.conversation_history.append({
            "role": "user",
            "content": message
        })

        try:
            if self.client is None:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url
                )

            # Chiama API Mistral
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=1000
            )

            # Estrai risposta
            assistant_message = response.choices[0].message.content

            # Aggiungi risposta alla storia
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except Exception as e:
            return f"Errore: {e}"

    def reset(self):
        """Resetta la conversazione."""
        self.conversation_history = [{
            "role": "system",
            "content": self.system_prompt
        }]


def main():
    """Esempio d'uso."""
    agent = SimpleAgent()

    print("🤖 Simple Agent avviato! (scrivi 'exit' per uscire)\n")

    while True:
        user_input = input("Tu: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ['exit', 'quit']:
            print("👋 Arrivederci!")
            break

        response = agent.chat(user_input)
        print(f"\n🤖: {response}\n")


if __name__ == "__main__":
    main()
