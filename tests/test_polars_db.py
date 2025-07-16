"""
Test suite for AMS-DB Polars Database Handler
"""

import pytest
import json
import tempfile
from pathlib import Path

from ams_db.core import PolarsDBHandler


class TestPolarsDBHandler:
    """Test cases for PolarsDBHandler class."""
    
    def setup_method(self):
        """Set up test database."""
        self.temp_dir = tempfile.mkdtemp()
        self.db = PolarsDBHandler(db_path=self.temp_dir)
    
    def teardown_method(self):
        """Clean up test database."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_database_initialization(self):
        """Test database initialization."""
        assert self.db.db_path.exists()
        assert hasattr(self.db, 'agent_matrix')
        assert hasattr(self.db, 'conversations')
        assert hasattr(self.db, 'knowledge_base')
        assert hasattr(self.db, 'research_collection')
        assert hasattr(self.db, 'templates')
    
    def test_add_agent_config(self):
        """Test adding agent configuration."""
        test_config = {
            "agent_id": "test_agent",
            "test_data": "hello world"
        }
        
        agent_id = self.db.add_agent_config(
            test_config, 
            agent_name="Test Agent",
            description="A test agent",
            tags=["test", "demo"]
        )
        
        assert agent_id == "test_agent"
        
        # Verify it was added
        retrieved_config = self.db.get_agent_config(agent_id)
        assert retrieved_config is not None
        assert retrieved_config["agent_id"] == "test_agent"
        assert retrieved_config["test_data"] == "hello world"
    
    def test_list_agents(self):
        """Test listing agents."""
        # Add test agents
        config1 = {"agent_id": "agent1"}
        config2 = {"agent_id": "agent2"}
        
        self.db.add_agent_config(config1, "Agent 1")
        self.db.add_agent_config(config2, "Agent 2")
        
        agents = self.db.list_agents()
        assert agents.height == 2
        
        agent_ids = agents.select("agent_id").to_series().to_list()
        assert "agent1" in agent_ids
        assert "agent2" in agent_ids
    
    def test_update_agent_config(self):
        """Test updating agent configuration."""
        # Add initial config
        original_config = {"agent_id": "update_test", "version": 1}
        agent_id = self.db.add_agent_config(original_config)
        
        # Update config
        updated_config = {"agent_id": "update_test", "version": 2}
        self.db.update_agent_config(agent_id, updated_config)
        
        # Verify update
        retrieved = self.db.get_agent_config(agent_id)
        assert retrieved["version"] == 2
    
    def test_delete_agent(self):
        """Test deleting agents."""
        config = {"agent_id": "delete_test"}
        agent_id = self.db.add_agent_config(config)
        
        # Soft delete
        self.db.delete_agent(agent_id, soft_delete=True)
        active_agents = self.db.list_agents(active_only=True)
        assert active_agents.height == 0
        
        all_agents = self.db.list_agents(active_only=False)
        assert all_agents.height == 1
        
        # Hard delete
        self.db.delete_agent(agent_id, soft_delete=False)
        all_agents = self.db.list_agents(active_only=False)
        assert all_agents.height == 0
    
    def test_conversation_operations(self):
        """Test conversation management."""
        agent_id = "conv_test"
        session_id = "session_123"
        
        # Add messages
        msg1_id = self.db.add_conversation_message(
            agent_id, "user", "Hello", session_id
        )
        msg2_id = self.db.add_conversation_message(
            agent_id, "assistant", "Hi there!", session_id
        )
        
        assert msg1_id is not None
        assert msg2_id is not None
        
        # Get conversation history
        history = self.db.get_conversation_history(agent_id, session_id)
        assert history.height == 2
        
        # Test message content
        messages = history.to_dicts()
        user_msg = next(m for m in messages if m["role"] == "user")
        assert user_msg["content"] == "Hello"
        
        assistant_msg = next(m for m in messages if m["role"] == "assistant")
        assert assistant_msg["content"] == "Hi there!"
    
    def test_knowledge_base_operations(self):
        """Test knowledge base management."""
        agent_id = "kb_test"
        
        # Add knowledge document
        kb_id = self.db.add_knowledge_document(
            agent_id,
            title="Test Document", 
            content="This is test content",
            content_type="text",
            source="test",
            tags=["test", "demo"]
        )
        
        assert kb_id is not None
        
        # Search knowledge base
        results = self.db.search_knowledge_base(agent_id, "test")
        assert results.height >= 1
        
        # Get all documents
        docs = self.db.get_knowledge_documents(agent_id)
        assert docs.height == 1
        
        doc = docs.to_dicts()[0]
        assert doc["title"] == "Test Document"
        assert doc["content"] == "This is test content"
    
    def test_research_operations(self):
        """Test research collection management."""
        agent_id = "research_test"
        
        research_data = {
            "findings": "Important research findings",
            "confidence": 0.95
        }
        
        # Add research result
        research_id = self.db.add_research_result(
            agent_id,
            query="test query",
            results=research_data,
            source_urls=["http://example.com"],
            research_type="web_search"
        )
        
        assert research_id is not None
        
        # Search research collection
        results = self.db.search_research_collection(agent_id, "test")
        assert results.height >= 1
        
        result = results.to_dicts()[0]
        assert result["query"] == "test query"
        assert "findings" in json.loads(result["results"])
    
    def test_template_operations(self):
        """Test template management."""
        # Add template
        template_id = self.db.add_template(
            template_name="test_template",
            template_type="prompt",
            content="You are a helpful assistant",
            description="Test template",
            tags=["test"]
        )
        
        assert template_id is not None
        
        # Get template by ID
        template = self.db.get_template(template_id=template_id)
        assert template is not None
        assert template["template_name"] == "test_template"
        
        # Get template by name
        template_by_name = self.db.get_template(template_name="test_template")
        assert template_by_name is not None
        assert template_by_name["template_id"] == template_id
    
    def test_database_stats(self):
        """Test database statistics."""
        # Add some test data
        self.db.add_agent_config({"agent_id": "stats_test"})
        self.db.add_conversation_message("stats_test", "user", "test")
        self.db.add_knowledge_document("stats_test", "test", "content")
        
        stats = self.db.get_database_stats()
        
        assert "agent_count" in stats
        assert "conversation_count" in stats
        assert "knowledge_document_count" in stats
        assert stats["agent_count"] >= 1
        assert stats["conversation_count"] >= 1
        assert stats["knowledge_document_count"] >= 1


if __name__ == "__main__":
    pytest.main([__file__])
