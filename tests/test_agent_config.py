"""
Test suite for AMS-DB Agent Configuration
"""

import pytest
import json
import tempfile
from pathlib import Path

from ams_db.core import AgentConfig


class TestAgentConfig:
    """Test cases for AgentConfig class."""
    
    def test_basic_creation(self):
        """Test basic agent config creation."""
        agent = AgentConfig("test_agent")
        assert agent.config["agent_id"] == "test_agent"
        assert "agent_core" in agent.config
        assert "prompts" in agent.config["agent_core"]
        assert "modalityFlags" in agent.config["agent_core"]
    
    def test_set_prompt(self):
        """Test setting prompts."""
        agent = AgentConfig("test_agent")
        
        test_prompt = "You are a test assistant"
        agent.set_prompt("llmSystem", test_prompt)
        
        assert agent.config["agent_core"]["prompts"]["llmSystem"] == test_prompt
    
    def test_set_modality_flag(self):
        """Test setting modality flags."""
        agent = AgentConfig("test_agent")
        
        agent.set_modality_flag("STT_FLAG", True)
        assert agent.config["agent_core"]["modalityFlags"]["STT_FLAG"] is True
        
        agent.set_modality_flag("STT_FLAG", False)
        assert agent.config["agent_core"]["modalityFlags"]["STT_FLAG"] is False
    
    def test_set_database(self):
        """Test setting database paths."""
        agent = AgentConfig("test_agent")
        
        agent.set_database("conversation_history", "test_conversation.db")
        assert agent.config["agent_core"]["databases"]["conversation_history"] == "test_conversation.db"
    
    def test_update_config(self):
        """Test updating configuration with nested updates."""
        agent = AgentConfig("test_agent")
        
        updates = {
            "model_config": {"temperature": 0.8, "max_tokens": 1000},
            "agent_core": {
                "prompts": {"llmSystem": "Updated system prompt"},
                "modalityFlags": {"TTS_FLAG": True}
            }
        }
        
        agent.update_config(updates)
        
        assert agent.config["model_config"]["temperature"] == 0.8
        assert agent.config["agent_core"]["prompts"]["llmSystem"] == "Updated system prompt"
        assert agent.config["agent_core"]["modalityFlags"]["TTS_FLAG"] is True
    
    def test_json_serialization(self):
        """Test JSON save and load functionality."""
        agent = AgentConfig("test_agent")
        agent.set_prompt("llmSystem", "Test system prompt")
        agent.set_modality_flag("STT_FLAG", True)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            # Save to JSON
            agent.to_json(temp_path)
            
            # Load from JSON
            new_agent = AgentConfig()
            new_agent.from_json(temp_path)
            
            assert new_agent.config["agent_id"] == "test_agent"
            assert new_agent.config["agent_core"]["prompts"]["llmSystem"] == "Test system prompt"
            assert new_agent.config["agent_core"]["modalityFlags"]["STT_FLAG"] is True
            
        finally:
            Path(temp_path).unlink()
    
    def test_dict_operations(self):
        """Test dictionary operations."""
        agent = AgentConfig("test_agent")
        agent.set_prompt("llmSystem", "Test prompt")
        
        # Test to_dict
        config_dict = agent.to_dict()
        assert isinstance(config_dict, dict)
        assert config_dict["agent_id"] == "test_agent"
        
        # Test from_dict
        new_agent = AgentConfig()
        new_agent.from_dict(config_dict)
        assert new_agent.config["agent_id"] == "test_agent"
        assert new_agent.config["agent_core"]["prompts"]["llmSystem"] == "Test prompt"
    
    def test_string_representation(self):
        """Test string representations."""
        agent = AgentConfig("test_agent")
        
        str_repr = str(agent)
        assert isinstance(str_repr, str)
        assert "test_agent" in str_repr
        
        repr_str = repr(agent)
        assert "AgentConfig" in repr_str
        assert "test_agent" in repr_str
    
    def test_invalid_prompt_type(self):
        """Test handling of invalid prompt types."""
        agent = AgentConfig("test_agent")
        
        with pytest.raises(ValueError):
            agent.set_prompt("invalid_prompt_type", "some prompt")
    
    def test_invalid_modality_flag(self):
        """Test handling of invalid modality flags."""
        agent = AgentConfig("test_agent")
        
        with pytest.raises(ValueError):
            agent.set_modality_flag("INVALID_FLAG", True)
    
    def test_invalid_database_name(self):
        """Test handling of invalid database names."""
        agent = AgentConfig("test_agent")
        
        with pytest.raises(ValueError):
            agent.set_database("invalid_db", "some_path.db")


if __name__ == "__main__":
    pytest.main([__file__])
