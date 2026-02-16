"""
Tests per l'agente AI.
"""

import pytest
from unittest.mock import Mock, patch
import os


def test_simple_agent_initialization():
    """Test inizializzazione agente semplice."""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        from src.simple_agent import SimpleAgent
        
        agent = SimpleAgent()
        assert agent.model == "gpt-3.5-turbo"
        assert len(agent.conversation_history) == 1
        assert agent.conversation_history[0]["role"] == "system"


def test_simple_agent_missing_api_key():
    """Test che l'agente fallisce senza API key."""
    with patch.dict(os.environ, {}, clear=True):
        from src.simple_agent import SimpleAgent
        
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            SimpleAgent()


def test_rag_system_initialization():
    """Test inizializzazione sistema RAG."""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        from src.agent import RAGSystem
        
        # Test con directory vuota
        rag = RAGSystem(knowledge_base_path="./tests")
        assert rag.knowledge_base_path == "./tests"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
