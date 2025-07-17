#!/usr/bin/env python3
"""Comprehensive system test to verify all components work together"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ams_db.core.graphiti_pipe import GraphitiRAGFramework
from ams_db.cli.chat_manager import ChatManager

async def test_environment():
    """Test environment variables and basic setup"""
    print("🔍 Testing Environment Setup...")
    
    required_vars = ['NEO4J_URI', 'NEO4J_USER', 'NEO4J_PASSWORD', 'OLLAMA_BASE_URL']
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")
            return False
    return True

async def test_graphiti_framework():
    """Test the GraphitiRAGFramework"""
    print("\n🔍 Testing GraphitiRAGFramework...")
    
    try:
        # Use environment variables
        framework = GraphitiRAGFramework(
            neo4j_uri=os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
            neo4j_user=os.getenv('NEO4J_USER', 'neo4j'),
            neo4j_password=os.getenv('NEO4J_PASSWORD', 'temppass123'),
            ollama_base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434/v1')
        )
        print("✅ Framework initialized")
        
        # Test agent creation (not async)
        agent_config = {
            "id": "test_agent_001",
            "name": "Test Agent",
            "personality": "A helpful test assistant focused on validation",
            "knowledge_areas": ["testing", "validation"]
        }
        
        agent_id = framework.create_agent(agent_config, agent_name="Test Agent")
        if agent_id:
            print(f"✅ Agent created: {agent_id}")
        else:
            print("❌ Agent creation failed")
            return False
            
        # Load the agent
        loaded = await framework.load_agent(agent_id)
        if loaded:
            print("✅ Agent loaded successfully")
        else:
            print("❌ Agent loading failed")
            return False
            
        # Test response generation
        response = await framework.generate_response(
            agent_id=agent_id,
            user_message="Hello, can you confirm you're working?",
            conversation_context="",
            session_id="test_session"
        )
        
        if response and len(response) > 10:
            print(f"✅ Response generated: {response[:100]}...")
            return True
        else:
            print(f"❌ Response generation failed: {response}")
            return False
            
    except Exception as e:
        print(f"❌ GraphitiRAGFramework error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_chat_manager():
    """Test the ChatManager"""
    print("\n🔍 Testing ChatManager...")
    
    try:
        # Need to initialize with PolarsDBHandler
        from ams_db.core.polars_db import PolarsDBHandler
        db_handler = PolarsDBHandler("agent_database")
        chat_manager = ChatManager(db_handler)
        print("✅ ChatManager initialized")
        
        # Test session creation (use start_human_chat)
        session_id, alias = chat_manager.start_human_chat("test_agent_001", "test_session")
        if session_id:
            print(f"✅ Session created: {session_id} (alias: {alias})")
        else:
            print("❌ Session creation failed")
            return False
            
        # Test message sending (is async)
        response = await chat_manager.send_message_to_agent(
            session_id, 
            "test_agent_001", 
            "Please confirm you can receive and respond to messages"
        )
        
        if response and len(response) > 10:
            print(f"✅ Message sent and response received: {response[:100]}...")
            return True
        else:
            print(f"❌ Message sending failed: {response}")
            return False
            
    except Exception as e:
        print(f"❌ ChatManager error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_cli_integration():
    """Test CLI components"""
    print("\n🔍 Testing CLI Integration...")
    
    try:
        # Import CLI components
        from ams_db.cli.main import app
        print("✅ CLI imports successful")
        
        # Test agent listing using PolarsDBHandler
        from ams_db.core.polars_db import PolarsDBHandler
        db = PolarsDBHandler("agent_database")
        agents_df = db.list_agents()
        
        if len(agents_df) > 0:
            print(f"✅ Found {len(agents_df)} agents in database")
        else:
            print("⚠️ No agents found in database")
            
        return True
        
    except Exception as e:
        print(f"❌ CLI integration error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run comprehensive system test"""
    print("🚀 Starting Comprehensive System Test\n")
    
    tests = [
        ("Environment", test_environment),
        ("GraphitiRAGFramework", test_graphiti_framework),
        ("ChatManager", test_chat_manager),
        ("CLI Integration", test_cli_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    print("\n📊 Test Results Summary:")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED - System is fully operational!")
    else:
        print("⚠️ SOME TESTS FAILED - System needs attention")
        
    return all_passed

if __name__ == "__main__":
    asyncio.run(main())
