#!/usr/bin/env python3
"""
AMS-DB Demonstration Script

This script demonstrates the key features of AMS-DB in action.
"""

import time
from pathlib import Path
from ams_db.core import AgentConfig, PolarsDBHandler
from ams_db.config import get_template_manager


def print_banner():
    """Print the AMS-DB banner"""
    print("🧙‍♂️" + "="*60)
    print("    AMS-DB: Agentic Multimodal Super-alignment Database")
    print("    A Comprehensive Foundation for Multimodal AI Agents")
    print("="*63)
    print()


def demo_agent_configuration():
    """Demonstrate agent configuration capabilities"""
    print("🤖 DEMO 1: Agent Configuration System")
    print("-" * 40)
    
    # Create a custom agent
    agent = AgentConfig("demo_assistant")
    
    # Configure prompts
    agent.set_prompt("llmSystem", 
        "You are a demonstration assistant for AMS-DB. "
        "You help users understand the capabilities of the system."
    )
    agent.set_prompt("llmBooster", 
        "Provide clear, helpful responses about AMS-DB features."
    )
    
    # Configure modalities
    agent.set_modality_flag("STT_FLAG", True)     # Speech-to-text
    agent.set_modality_flag("LATEX_FLAG", True)   # LaTeX support
    agent.set_modality_flag("LLAVA_FLAG", True)   # Vision capabilities
    
    # Configure database paths
    agent.set_database("conversation_history", "demo_conversations.db")
    agent.set_database("knowledge_base", "demo_knowledge.db")
    
    print(f"✅ Created agent: {agent.config['agent_id']}")
    print(f"📝 System prompt: {agent.config['agent_core']['prompts']['llmSystem'][:60]}...")
    print(f"🎤 Speech enabled: {agent.config['agent_core']['modalityFlags']['STT_FLAG']}")
    print(f"👁️ Vision enabled: {agent.config['agent_core']['modalityFlags']['LLAVA_FLAG']}")
    print(f"📊 LaTeX enabled: {agent.config['agent_core']['modalityFlags']['LATEX_FLAG']}")
    
    # Save configuration
    config_file = "demo_assistant_config.json"
    agent.to_json(config_file)
    print(f"💾 Saved configuration to: {config_file}")
    
    return agent


def demo_database_operations(agent_config):
    """Demonstrate database operations"""
    print("\n🗄️ DEMO 2: High-Performance Database Operations")
    print("-" * 40)
    
    # Initialize database
    db = PolarsDBHandler("demo_database")
    print("✅ Database initialized with Polars backend")
    
    # Add the agent to database
    agent_id = db.add_agent_config(
        agent_config.get_config(),
        agent_name="Demo Assistant",
        description="Demonstration agent for AMS-DB capabilities",
        tags=["demo", "assistant", "showcase"]
    )
    print(f"✅ Added agent to database: {agent_id}")
    
    # Add some conversation data
    conversations = [
        {"role": "user", "content": "What is AMS-DB?"},
        {"role": "assistant", "content": "AMS-DB is a comprehensive database foundation for multimodal AI agents!"},
        {"role": "user", "content": "What are its key features?"},
        {"role": "assistant", "content": "Key features include agent configuration, Polars database, Graphiti knowledge graphs, and more!"}
    ]
    
    session_id = "demo_session_001"
    for conv in conversations:
        msg_id = db.add_conversation_message(
            agent_id, conv["role"], conv["content"], session_id
        )
    
    print(f"💬 Added {len(conversations)} conversation messages")
    
    # Add knowledge documents
    knowledge_docs = [
        {
            "title": "AMS-DB Overview",
            "content": "AMS-DB provides a comprehensive foundation for building multimodal AI agents with configuration management, high-performance data storage, and knowledge graph integration.",
            "tags": ["overview", "features"]
        },
        {
            "title": "Agent Configuration",
            "content": "The AgentConfig system allows complete control over agent prompts, modality flags, model settings, and database configurations.",
            "tags": ["configuration", "agents"]
        },
        {
            "title": "Database Performance",
            "content": "Polars-based database handler provides high-performance operations for conversations, knowledge bases, research collections, and agent matrices.",
            "tags": ["database", "performance"]
        }
    ]
    
    for doc in knowledge_docs:
        kb_id = db.add_knowledge_document(
            agent_id, doc["title"], doc["content"], 
            content_type="text", source="demo", tags=doc["tags"]
        )
    
    print(f"📚 Added {len(knowledge_docs)} knowledge documents")
    
    # Demonstrate search
    search_results = db.search_knowledge_base(agent_id, "configuration")
    print(f"🔍 Search for 'configuration': {search_results.height} results found")
    
    # Show statistics
    stats = db.get_database_stats()
    print(f"\n📊 Database Statistics:")
    print(f"   • Agents: {stats['agent_count']}")
    print(f"   • Conversations: {stats['conversation_count']}")
    print(f"   • Knowledge Documents: {stats['knowledge_document_count']}")
    print(f"   • Database Size: {stats['database_size_mb']:.2f} MB")
    
    return db, agent_id


def demo_agent_templates():
    """Demonstrate predefined agent templates"""
    print("\n📝 DEMO 3: Predefined Agent Templates")
    print("-" * 40)
    
    template_manager = get_template_manager()
    
    # List available templates
    templates = template_manager.list_templates()
    print("Available templates:")
    for name, info in templates.items():
        print(f"   • {name}: {info['name']}")
        print(f"     Description: {info['description']}")
        print(f"     Tags: {', '.join(info['tags'])}")
        print()
    
    # Create agent from template
    speed_chat_agent = template_manager.create_agent_from_template(
        "speed_chat",
        agent_id="demo_speed_chat"
    )
    
    if speed_chat_agent:
        print(f"✅ Created Speed Chat agent: {speed_chat_agent.config['agent_id']}")
        
        # Show some configuration details
        system_prompt = speed_chat_agent.config['agent_core']['prompts']['llmSystem']
        print(f"📝 System prompt preview: {system_prompt[:80]}...")
        
        flags = speed_chat_agent.config['agent_core']['modalityFlags']
        enabled_flags = [flag for flag, enabled in flags.items() if enabled]
        print(f"🎛️ Enabled modalities: {', '.join(enabled_flags[:3])}...")
        
        # Save template agent
        speed_chat_agent.to_json("demo_speed_chat_config.json")
        print("💾 Saved template agent configuration")


def demo_export_import():
    """Demonstrate export/import capabilities"""
    print("\n🔄 DEMO 4: Export/Import System")
    print("-" * 40)
    
    # Create a test database with some data
    db = PolarsDBHandler("export_demo_db")
    
    # Add test agent
    test_config = {"agent_id": "export_test", "demo": True}
    agent_id = db.add_agent_config(test_config, "Export Test Agent")
    
    # Add some data
    db.add_conversation_message(agent_id, "user", "Test message")
    db.add_knowledge_document(agent_id, "Test Doc", "Test content")
    
    print("✅ Created test data for export")
    
    # Export agent configuration
    export_success = db.export_agent_config(agent_id, "exported_agent_config.json")
    if export_success:
        print("✅ Exported agent configuration")
    
    # Create database backup
    backup_path = "demo_backup"
    db.export_database_backup(backup_path)
    print(f"✅ Created database backup in: {backup_path}/")
    
    # Show backup contents
    backup_dir = Path(backup_path)
    if backup_dir.exists():
        backup_files = list(backup_dir.glob("*.parquet"))
        print(f"📦 Backup contains {len(backup_files)} data files")


def cleanup_demo_files():
    """Clean up demonstration files"""
    print("\n🧹 Cleaning up demonstration files...")
    
    files_to_remove = [
        "demo_assistant_config.json",
        "demo_speed_chat_config.json", 
        "exported_agent_config.json"
    ]
    
    for file_path in files_to_remove:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            print(f"   • Removed {file_path}")
    
    # Clean up directories
    import shutil
    dirs_to_remove = ["demo_database", "export_demo_db", "demo_backup"]
    for dir_path in dirs_to_remove:
        path = Path(dir_path)
        if path.exists():
            shutil.rmtree(path)
            print(f"   • Removed directory {dir_path}/")


def main():
    """Run the complete demonstration"""
    print_banner()
    
    try:
        print("🎬 Starting AMS-DB Demonstration...")
        print()
        
        # Demo 1: Agent Configuration
        agent_config = demo_agent_configuration()
        time.sleep(1)
        
        # Demo 2: Database Operations
        db, agent_id = demo_database_operations(agent_config)
        time.sleep(1)
        
        # Demo 3: Agent Templates
        demo_agent_templates()
        time.sleep(1)
        
        # Demo 4: Export/Import
        demo_export_import()
        time.sleep(1)
        
        print("\n🎉 DEMONSTRATION COMPLETE!")
        print("-" * 40)
        print("✅ Agent Configuration System - Working")
        print("✅ High-Performance Database - Working") 
        print("✅ Predefined Templates - Working")
        print("✅ Export/Import System - Working")
        print()
        print("🚀 AMS-DB is ready for production use!")
        print("📖 See USAGE.md for detailed documentation")
        print("💡 Check examples/ for more advanced usage")
        
    except KeyboardInterrupt:
        print("\n⚠️ Demonstration interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cleanup_demo_files()
        print("\n🧙‍♂️ Thank you for exploring AMS-DB! ✨")


if __name__ == "__main__":
    main()
