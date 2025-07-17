#!/usr/bin/env python3
"""Test the fixed chat system with wizard agent"""
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
from src.ams_db.cli.chat_manager import ChatManager

async def test_chat_system():
    """Test the full chat system"""
    
    # Initialize components
    db_handler = PolarsDBHandler("agent_database")
    chat_manager = ChatManager(db_handler)
    
    # Start a chat session with wizard
    session_id, alias = chat_manager.start_human_chat(
        agent_id="wizard_agent_001",
        session_name="Test Wizard Chat",
        topic="Knowledge system discussion"
    )
    
    print(f"🎭 Started chat session: {alias} (ID: {session_id})")
    
    # Test messages
    test_messages = [
        "Hello wizard, how does your knowledge system work?",
        "Can you tell me about knowledge graphs?",
        "What makes your system magical?"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Message {i} ---")
        print(f"👤 User: {message}")
        
        try:
            # Send message to agent
            response = await chat_manager.send_message_to_agent(session_id, "wizard_agent_001", message)
            print(f"🧙‍♂️ Wizard: {response[:200]}{'...' if len(response) > 200 else ''}")
            
            # Update session activity
            chat_manager.update_session_activity(alias)
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Show session info
    session = chat_manager.get_session_by_alias(alias)
    print(f"\n📊 Session Summary:")
    print(f"   • Alias: {alias}")
    print(f"   • Messages: {session.message_count}")
    print(f"   • Mode: {session.mode}")
    print(f"   • Topic: {session.topic}")

if __name__ == "__main__":
    asyncio.run(test_chat_system())
