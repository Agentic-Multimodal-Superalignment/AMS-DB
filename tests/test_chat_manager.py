#!/usr/bin/env python3
"""Test the fixed chat manager"""
import os
import asyncio

# Set environment variables
os.environ['NEO4J_URI'] = 'bolt://localhost:7687'
os.environ['NEO4J_USER'] = 'neo4j'
os.environ['NEO4J_PASSWORD'] = 'temppass123'

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.ams_db.core.polars_db import PolarsDBHandler
from src.ams_db.cli.chat_manager import ChatManager

async def test_chat_manager():
    """Test the fixed chat manager implementation"""
    
    # Initialize components
    db_handler = PolarsDBHandler("agent_database")
    chat_manager = ChatManager(db_handler)
    
    # Start a chat session
    session_id, alias = chat_manager.start_human_chat("wizard_agent_001", "Test Wizard Chat")
    print(f"✅ Started chat session: {alias} ({session_id})")
    
    # Send a message
    test_message = "Hello wizard, tell me about your knowledge system!"
    print(f"💬 Sending: {test_message}")
    
    try:
        response = await chat_manager.send_message_to_agent(session_id, "wizard_agent_001", test_message)
        print(f"🧙‍♂️ Wizard Response:")
        print(response)
        print("\n✅ Chat test successful!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_chat_manager())
