#!/usr/bin/env python3
"""
Quick test to verify the Message import fix
"""
import os
import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Set environment variables
os.environ['NEO4J_URI'] = 'bolt://localhost:7687'
os.environ['NEO4J_USER'] = 'neo4j'
os.environ['NEO4J_PASSWORD'] = 'temppass123'

async def test_message_import_fix():
    """Test if the Message import fix works"""
    
    print("🧪 Testing Message import fix...")
    
    try:
        # Test 1: Direct import of Message
        try:
            from graphiti_core.prompts.models import Message
            print("✅ Direct import from graphiti_core.prompts.models works")
        except ImportError:
            try:
                from graphiti_core.prompts import Message  
                print("✅ Fallback import from graphiti_core.prompts works")
            except ImportError:
                print("❌ Both Message imports failed")
                return False
        
        # Test 2: Try GraphitiRAGFramework import 
        from ams_db.core.graphiti_pipe import GraphitiRAGFramework
        print("✅ GraphitiRAGFramework imports successfully")
        
        # Test 3: Initialize framework
        framework = GraphitiRAGFramework(
            neo4j_uri='bolt://localhost:7687',
            neo4j_user='neo4j',
            neo4j_password='temppass123'
        )
        print("✅ GraphitiRAGFramework initializes successfully")
        
        # Test 4: Try to generate a response
        print("🔍 Testing response generation...")
        
        # Load wizard agent
        loaded = await framework.load_agent("wizard_agent_001")
        if loaded:
            print("✅ Agent loaded successfully")
        else:
            print("⚠️ Agent loading returned False")
        
        # Generate response
        response = await framework.generate_response(
            agent_id="wizard_agent_001",
            user_message="Hello wizard, can you write a simple Python function?",
            session_id="test_import_fix"
        )
        
        print(f"✅ Response generated successfully!")
        print(f"📝 Response (first 200 chars): {response[:200]}...")
        
        # Check if it's a real LLM response or fallback
        if "I understand you're asking" in response or "setup notice" in response.lower():
            print("⚠️ This appears to be a fallback response")
            return False
        elif len(response) > 100:
            print("✅ This appears to be a real LLM response!")
            return True
        else:
            print("❓ Unclear if this is real LLM or fallback")
            return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_message_import_fix())
    if success:
        print("\n🎉 Message import fix is working! LLM responses are being generated.")
    else:
        print("\n💥 Message import fix needs more work.")
    
    sys.exit(0 if success else 1)
