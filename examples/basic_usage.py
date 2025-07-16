"""
Basic Usage Example for AMS-DB

This example demonstrates the basic usage of AMS-DB components:
- Creating and configuring agents
- Managing conversations
- Working with knowledge bases
"""

import asyncio
from pathlib import Path

from ams_db.core import AgentConfig, PolarsDBHandler, GraphitiRAGFramework


def example_1_basic_agent_config():
    """Example 1: Basic agent configuration"""
    print("🤖 Example 1: Creating and configuring agents")
    print("=" * 50)
    
    # Create a basic agent
    agent = AgentConfig("my_first_agent")
    agent.set_prompt("llmSystem", "You are a helpful AI assistant specialized in Python programming.")
    agent.set_modality_flag("STT_FLAG", True)
    agent.set_modality_flag("LATEX_FLAG", True)
    
    print(f"✅ Created agent: {agent.config['agent_id']}")
    print(f"System prompt: {agent.config['agent_core']['prompts']['llmSystem'][:50]}...")
    print(f"STT enabled: {agent.config['agent_core']['modalityFlags']['STT_FLAG']}")
    
    # Save configuration
    agent.to_json("my_first_agent.json")
    print("✅ Saved agent configuration to my_first_agent.json")
    
    # Load configuration
    new_agent = AgentConfig()
    new_agent.from_json("my_first_agent.json")
    print(f"✅ Loaded agent: {new_agent.config['agent_id']}")
    
    print()


def example_2_database_operations():
    """Example 2: Database operations with PolarsDBHandler"""
    print("🗄️ Example 2: Database operations")
    print("=" * 50)
    
    # Initialize database
    db = PolarsDBHandler("example_database")
    print("✅ Database initialized")
    
    # Create some test agents
    agents_data = [
        {
            "config": {"agent_id": "coding_assistant", "specialization": "programming"},
            "name": "Coding Assistant",
            "description": "Helps with programming tasks",
            "tags": ["coding", "python", "assistant"]
        },
        {
            "config": {"agent_id": "creative_writer", "specialization": "writing"},
            "name": "Creative Writer",
            "description": "Assists with creative writing",
            "tags": ["writing", "creative", "storytelling"]
        }
    ]
    
    # Add agents to database
    agent_ids = []
    for agent_data in agents_data:
        agent_id = db.add_agent_config(
            agent_data["config"],
            agent_data["name"],
            agent_data["description"],
            agent_data["tags"]
        )
        agent_ids.append(agent_id)
        print(f"✅ Added agent: {agent_id}")
    
    # List all agents
    all_agents = db.list_agents()
    print(f"\n📋 Total agents in database: {all_agents.height}")
    for agent in all_agents.to_dicts():
        print(f"  • {agent['agent_id']} - {agent['agent_name']}")
    
    # Add some conversation data
    db.add_conversation_message(
        "coding_assistant", "user", 
        "How do I create a virtual environment in Python?",
        session_id="session_001"
    )
    db.add_conversation_message(
        "coding_assistant", "assistant",
        "You can create a virtual environment using: python -m venv venv_name",
        session_id="session_001"
    )
    
    # Get conversation history
    history = db.get_conversation_history("coding_assistant", "session_001")
    print(f"\n💬 Conversation history: {history.height} messages")
    
    # Add knowledge documents
    kb_id = db.add_knowledge_document(
        "coding_assistant",
        title="Python Virtual Environments Guide",
        content="Virtual environments in Python allow you to create isolated Python environments...",
        content_type="text",
        source="documentation",
        tags=["python", "environment", "guide"]
    )
    print(f"✅ Added knowledge document: {kb_id}")
    
    # Search knowledge base
    search_results = db.search_knowledge_base("coding_assistant", "virtual environment")
    print(f"🔍 Found {search_results.height} knowledge documents matching 'virtual environment'")
    
    # Get database statistics
    stats = db.get_database_stats()
    print(f"\n📊 Database Statistics:")
    print(f"  • Agents: {stats['agent_count']}")
    print(f"  • Conversations: {stats['conversation_count']}")
    print(f"  • Knowledge docs: {stats['knowledge_document_count']}")
    print(f"  • Database size: {stats['database_size_mb']:.2f} MB")
    
    print()


async def example_3_graphiti_integration():
    """Example 3: Graphiti integration (requires Neo4j)"""
    print("🧠 Example 3: Graphiti Knowledge Graph Integration")
    print("=" * 50)
    
    try:
        # Initialize the framework
        # Note: This requires Neo4j to be running
        framework = GraphitiRAGFramework(
            neo4j_uri="bolt://localhost:7687",
            neo4j_user="neo4j",
            neo4j_password="password",
            db_path="example_graphiti_db"
        )
        print("✅ Graphiti framework initialized")
        
        # Create a new agent using the framework
        agent_config = {
            "agent_id": "knowledge_agent",
            "agent_core": {
                "prompts": {
                    "llmSystem": "You are a knowledge management assistant."
                },
                "modalityFlags": {
                    "ACTIVE_AGENT_FLAG": True
                }
            }
        }
        
        agent_id = framework.create_agent(
            agent_config,
            "Knowledge Agent",
            "Agent specialized in knowledge management",
            ["knowledge", "research"]
        )
        print(f"✅ Created agent with Graphiti integration: {agent_id}")
        
        # Load the agent
        framework.load_agent(agent_id)
        print(f"✅ Loaded agent: {framework.current_agent_id}")
        
        # Add knowledge with embedding
        kb_id = await framework.add_knowledge_with_embedding(
            title="Machine Learning Basics",
            content="Machine learning is a method of data analysis that automates analytical model building...",
            content_type="text",
            source="educational_content",
            tags=["ml", "ai", "basics"]
        )
        print(f"✅ Added knowledge with Graphiti embedding: {kb_id}")
        
        # Simulate a conversation turn
        user_input = "What is machine learning?"
        assistant_response = "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from data."
        
        await framework.add_conversation_turn(user_input, assistant_response)
        print("✅ Added conversation turn to both database and knowledge graph")
        
        # Search with context
        search_results = await framework.search_knowledge_with_context(
            "machine learning basics",
            include_graph_context=True
        )
        print(f"🔍 Search results with graph context:")
        print(f"  • Database results: {len(search_results['database_results'])}")
        if search_results['graph_context']:
            print(f"  • Graph context available: {len(search_results['graph_context'])} characters")
        
        # Get system status
        status = framework.get_system_status()
        print(f"\n📊 System Status:")
        print(f"  • Current agent: {status['current_agent']['agent_id']}")
        print(f"  • System ready: {status['system_ready']}")
        print(f"  • Total agents: {status['database_stats']['agent_count']}")
        
    except Exception as e:
        print(f"⚠️ Graphiti integration example failed (Neo4j might not be running): {e}")
        print("💡 To run this example, ensure Neo4j is installed and running")
    
    print()


def example_4_agent_templates():
    """Example 4: Using predefined agent templates"""
    print("📝 Example 4: Agent Templates")
    print("=" * 50)
    
    from ams_db.config import get_template_manager
    
    template_manager = get_template_manager()
    
    # List available templates
    templates = template_manager.list_templates()
    print("Available templates:")
    for name, info in templates.items():
        print(f"  • {name}: {info['name']} - {info['description']}")
    
    # Create agent from template
    speed_chat_agent = template_manager.create_agent_from_template(
        "speed_chat", 
        agent_id="my_speed_chat_bot"
    )
    
    if speed_chat_agent:
        print(f"\n✅ Created agent from template: {speed_chat_agent.config['agent_id']}")
        print(f"System prompt preview: {speed_chat_agent.config['agent_core']['prompts']['llmSystem'][:100]}...")
        
        # Save the agent
        speed_chat_agent.to_json("speed_chat_agent.json")
        print("✅ Saved templated agent configuration")
    
    print()


def cleanup():
    """Clean up example files"""
    print("🧹 Cleaning up example files...")
    files_to_remove = [
        "my_first_agent.json",
        "speed_chat_agent.json"
    ]
    
    for file_path in files_to_remove:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            print(f"  • Removed {file_path}")


async def main():
    """Run all examples"""
    print("🧙‍♂️ AMS-DB Basic Usage Examples")
    print("=" * 60)
    print()
    
    try:
        # Run examples
        example_1_basic_agent_config()
        example_2_database_operations()
        await example_3_graphiti_integration()
        example_4_agent_templates()
        
        print("🎉 All examples completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cleanup()


if __name__ == "__main__":
    asyncio.run(main())
