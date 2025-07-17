#!/usr/bin/env python3
"""Test the fixed LLM integration"""

import asyncio
import os
import sys
from pathlib import Path

# Set environment variables
os.environ['NEO4J_URI'] = 'bolt://localhost:7687'
os.environ['NEO4J_USER'] = 'neo4j'
os.environ['NEO4J_PASSWORD'] = 'temppass123'
os.environ['OLLAMA_BASE_URL'] = 'http://localhost:11434'

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ams_db.core.graphiti_pipe import GraphitiRAGFramework

async def test_real_llm_response():
    """Test if the LLM is actually being called now"""
    
    print("🧪 Testing REAL LLM Integration...")
    
    # Initialize framework
    framework = GraphitiRAGFramework(
        neo4j_uri='bolt://localhost:7687',
        neo4j_user='neo4j',
        neo4j_password='temppass123',
        ollama_base_url='http://localhost:11434/v1'
    )
    
    # Load the expert coder agent
    await framework.load_agent("expert_coder_001")
    
    # Ask a technical question that should get a real LLM response
    test_message = "Write Python code to handle file I/O exceptions properly. Include try-except blocks and best practices."
    
    print(f"🔍 Question: {test_message}")
    print("🤔 Generating response with actual LLM...")
    
    try:
        response = await framework.generate_response(
            agent_id="expert_coder_001",
            user_message=test_message,
            conversation_context="",
            session_id="test_llm"
        )
        
        print("\n✅ Response received:")
        print("=" * 60)
        print(response)
        print("=" * 60)
        
        # Check if this looks like a real LLM response vs fallback
        if "I'm operating with a sophisticated knowledge management system" in response:
            print("\n❌ Still getting fallback response - LLM not working")
            return False
        elif len(response) > 200 and ("def " in response or "try:" in response or "except" in response):
            print("\n🎉 SUCCESS! This looks like a real LLM-generated code response!")
            return True
        else:
            print("\n⚠️ Got response but unclear if it's from LLM or fallback")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_wizard_response():
    """Test wizard personality with LLM"""
    
    print("\n\n🧙‍♂️ Testing Wizard Agent with LLM...")
    
    framework = GraphitiRAGFramework(
        neo4j_uri='bolt://localhost:7687',
        neo4j_user='neo4j',  
        neo4j_password='temppass123',
        ollama_base_url='http://localhost:11434/v1'
    )
    
    await framework.load_agent("wizard_agent_001")
    
    test_message = "Explain how machine learning works using magical metaphors"
    
    print(f"🔍 Question: {test_message}")
    
    try:
        response = await framework.generate_response(
            agent_id="wizard_agent_001",
            user_message=test_message,
            conversation_context="",
            session_id="test_wizard"
        )
        
        print("\n🧙‍♂️ Wizard Response:")
        print("=" * 60)
        print(response)
        print("=" * 60)
        
        # Check for real wizard-style response
        if "machine learning" in response.lower() and "magical" in response.lower():
            print("\n🎉 SUCCESS! Wizard is giving magical explanations!")
            return True
        else:
            print("\n⚠️ Response doesn't seem wizard-like enough")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

async def main():
    """Run LLM integration tests"""
    print("🚀 TESTING REAL LLM INTEGRATION")
    print("=" * 50)
    
    coder_ok = await test_real_llm_response()
    wizard_ok = await test_wizard_response()
    
    print("\n📊 Results:")
    print(f"Expert Coder LLM: {'✅ PASS' if coder_ok else '❌ FAIL'}")
    print(f"Wizard LLM: {'✅ PASS' if wizard_ok else '❌ FAIL'}")
    
    if coder_ok and wizard_ok:
        print("\n🎉 LLM INTEGRATION IS WORKING!")
        print("Agents are now generating real responses!")
    else:
        print("\n⚠️ LLM integration needs more work")

if __name__ == "__main__":
    asyncio.run(main())
