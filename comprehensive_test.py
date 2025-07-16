#!/usr/bin/env python3
"""
Comprehensive Feature Test for AMS-DB

Tests all major features including JSONL export and conversation generation.
"""

import asyncio
import json
import tempfile
from pathlib import Path

from ams_db.core import AgentConfig, PolarsDBHandler, GraphitiRAGFramework
from ams_db.config import get_template_manager


async def test_jsonl_export():
    """Test JSONL export functionality"""
    print("\n🧪 Testing JSONL Export Features")
    print("=" * 50)
    
    # Initialize components
    db = PolarsDBHandler("test_jsonl_db")
    
    # Create test agent
    agent = AgentConfig("test_jsonl_agent")
    agent.set_prompt("llmSystem", "You are a test agent for JSONL export.")
    agent.set_prompt("llmBooster", "Help with testing JSONL functionality.")
    agent.set_modality_flag("STT_FLAG", True)
    
    agent_id = db.add_agent_config(
        agent.get_config(),
        "JSONL Test Agent",
        "Agent for testing JSONL export"
    )
    
    # Add test conversations
    session_id = "test_session_jsonl"
    db.add_conversation_message(agent_id, "user", "Hello, can you help me test JSONL export?", session_id)
    db.add_conversation_message(agent_id, "assistant", "Of course! I'll help you test the JSONL export functionality.", session_id)
    db.add_conversation_message(agent_id, "user", "What format will the exported data be in?", session_id)
    db.add_conversation_message(agent_id, "assistant", "The data will be exported in JSONL format with message pairs for training.", session_id)
    
    # Test conversation export
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        conversations_file = f.name
    
    success = db.export_conversations_jsonl(agent_id, conversations_file)
    print(f"✅ Conversation export success: {success}")
    
    if success:
        with open(conversations_file, 'r') as f:
            lines = f.readlines()
        print(f"📊 Exported {len(lines)} conversation pairs")
        
        # Show example
        if lines:
            example = json.loads(lines[0])
            print(f"📝 Example format: {list(example.keys())}")
    
    # Test prompt export
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        prompts_file = f.name
    
    success = db.export_prompt_sets_jsonl(prompts_file)
    print(f"✅ Prompt export success: {success}")
    
    if success:
        with open(prompts_file, 'r') as f:
            lines = f.readlines()
        print(f"📊 Exported {len(lines)} prompt examples")
    
    # Cleanup
    Path(conversations_file).unlink(missing_ok=True)
    Path(prompts_file).unlink(missing_ok=True)
    
    return True


async def test_multi_agent_conversation():
    """Test multi-agent conversation generation"""
    print("\n🎭 Testing Multi-Agent Conversation Generation")
    print("=" * 60)
    
    # Initialize components
    db = PolarsDBHandler("test_multiagent_db")
    template_manager = get_template_manager()
    
    # Create multiple agents from templates
    agents = {}
    
    # Speed chat agent
    speed_agent = template_manager.create_agent_from_template("speed_chat", "speed_test")
    if speed_agent:
        agents["speed"] = db.add_agent_config(
            speed_agent.get_config(),
            "Speed Chat Test",
            "Speed chat for testing"
        )
    
    # Minecraft agent
    minecraft_agent = template_manager.create_agent_from_template("minecraft", "minecraft_test")
    if minecraft_agent:
        agents["minecraft"] = db.add_agent_config(
            minecraft_agent.get_config(),
            "Minecraft Test",
            "Minecraft agent for testing"
        )
    
    # Default agent
    default_agent = AgentConfig("default_test")
    default_agent.set_prompt("llmSystem", "You are a helpful AI assistant.")
    agents["default"] = db.add_agent_config(
        default_agent.get_config(),
        "Default Test",
        "Default agent for testing"
    )
    
    print(f"✅ Created {len(agents)} test agents")
    
    # Generate conversations with different scenarios
    scenarios = [
        {
            "topic": "minecraft building strategies",
            "personas": ["AI", "human", "wizardly"],
            "turns": 8
        },
        {
            "topic": "gaming tips and tricks",
            "personas": ["human", "AI"],
            "turns": 6
        },
        {
            "topic": "artificial intelligence discussion",
            "personas": ["AI", "wizardly", "human"],
            "turns": 10
        }
    ]
    
    generated_sessions = []
    
    for i, scenario in enumerate(scenarios, 1):
        agent_list = list(agents.values())[:len(scenario["personas"])]
        
        if len(agent_list) >= 2:
            session_id = db.generate_multi_agent_conversation(
                agent_ids=agent_list,
                topic=scenario["topic"],
                turns=scenario["turns"],
                personas=scenario["personas"]
            )
            
            if session_id:
                generated_sessions.append(session_id)
                print(f"✅ Scenario {i}: Generated session {session_id}")
                print(f"   Topic: {scenario['topic']}")
                print(f"   Agents: {len(agent_list)}, Turns: {scenario['turns']}")
                print(f"   Personas: {', '.join(scenario['personas'])}")
            else:
                print(f"❌ Scenario {i}: Failed to generate conversation")
    
    print(f"\n📊 Generated {len(generated_sessions)} multi-agent conversations")
    
    # Verify conversation data
    for session_id in generated_sessions[:1]:  # Check first session
        conversations = db.conversation_history.filter(
            db.conversation_history["session_id"] == session_id
        )
        print(f"🔍 Session {session_id}: {conversations.height} messages")
        
        # Show example messages
        if conversations.height > 0:
            first_msg = conversations.head(1).to_dicts()[0]
            print(f"   First message: {first_msg['content'][:60]}...")
    
    return len(generated_sessions) > 0


async def test_graphiti_integration():
    """Test Graphiti integration with new features"""
    print("\n🧠 Testing Graphiti Integration")
    print("=" * 40)
    
    try:
        framework = GraphitiRAGFramework("test_graphiti_db")
        
        # Test agent creation
        agent = AgentConfig("graphiti_test")
        agent.set_prompt("llmSystem", "You are a Graphiti integration test agent.")
        
        agent_id = framework.create_agent(
            agent.get_config(),
            "Graphiti Test Agent",
            "Testing Graphiti integration"
        )
        
        print(f"✅ Created agent with Graphiti: {agent_id}")
        
        # Test JSONL export with Graphiti
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            export_file = f.name
        
        success = await framework.export_conversations_jsonl(agent_id, export_file)
        print(f"✅ Graphiti JSONL export: {success}")
        
        # Test multi-agent generation with Graphiti
        session_id = await framework.generate_multi_agent_conversation(
            agent_ids=[agent_id],
            topic="graphiti knowledge graphs",
            turns=4,
            personas=["AI"]
        )
        
        print(f"✅ Graphiti conversation generation: {bool(session_id)}")
        
        # Cleanup
        Path(export_file).unlink(missing_ok=True)
        
        return True
        
    except Exception as e:
        print(f"⚠️ Graphiti not available: {e}")
        return False


async def test_template_system():
    """Test the template system with all predefined agents"""
    print("\n📝 Testing Template System")
    print("=" * 30)
    
    template_manager = get_template_manager()
    
    # List all templates
    templates = template_manager.list_templates()
    print(f"📋 Available templates: {len(templates)}")
    
    for name, info in templates.items():
        print(f"   • {name}: {info['name']}")
        print(f"     Tags: {', '.join(info['tags'])}")
    
    # Test creating agents from each template
    created_agents = []
    
    for template_name in templates.keys():
        try:
            agent = template_manager.create_agent_from_template(
                template_name,
                f"test_{template_name}"
            )
            
            if agent:
                created_agents.append((template_name, agent))
                print(f"✅ Created {template_name} agent")
                
                # Verify agent has required prompts
                prompts = agent.config["agent_core"]["prompts"]
                has_system = bool(prompts.get("llmSystem"))
                print(f"   System prompt: {'✓' if has_system else '✗'}")
                
        except Exception as e:
            print(f"❌ Failed to create {template_name}: {e}")
    
    print(f"\n📊 Successfully created {len(created_agents)} template agents")
    return len(created_agents) == len(templates)


async def main():
    """Run comprehensive feature tests"""
    print("🧪 AMS-DB Comprehensive Feature Testing")
    print("=" * 70)
    
    test_results = {}
    
    try:
        # Test JSONL export
        test_results["jsonl_export"] = await test_jsonl_export()
        
        # Test multi-agent conversations
        test_results["multi_agent"] = await test_multi_agent_conversation()
        
        # Test template system
        test_results["templates"] = await test_template_system()
        
        # Test Graphiti integration
        test_results["graphiti"] = await test_graphiti_integration()
        
        # Summary
        print("\n🏁 Test Results Summary")
        print("=" * 30)
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
            if result:
                passed += 1
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All features working correctly!")
        else:
            print("⚠️ Some features need attention")
            
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
