#!/usr/bin/env python3
"""Test script for the fixed LLM response parsing"""
import os
import asyncio
from pathlib import Path

# Set environment variables
os.environ['NEO4J_URI'] = 'bolt://localhost:7687'
os.environ['NEO4J_USER'] = 'neo4j'
os.environ['NEO4J_PASSWORD'] = 'temppass123'

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.ams_db.core.polars_db import PolarsDBHandler
from src.ams_db.core.graphiti_pipe import GraphitiRAGFramework

async def test_fixed_llm():
    """Test the fixed LLM response parsing"""
    
    # Initialize components
    db_handler = PolarsDBHandler("agent_database")
    
    # Get Neo4j credentials from environment
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD", "temppass123")
    
    # Initialize Graphiti framework
    framework = GraphitiRAGFramework(
        neo4j_uri=neo4j_uri,
        neo4j_user=neo4j_user,
        neo4j_password=neo4j_password,
        db_path="agent_database"
    )
    
    # Test message
    test_message = "Hello wizard, can you explain how your knowledge system works?"
    
    print("🧪 Testing fixed LLM response parsing...")
    print(f"Message: {test_message}")
    print()
    
    try:
        # Generate response using fixed code
        response = await framework.generate_response(
            agent_id="wizard_agent_001",
            user_message=test_message,
            session_id="test_session"
        )
        
        print("✅ SUCCESS! Response received:")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_fixed_llm())
