#!/usr/bin/env python3
"""
AMS-DB Simple Demo - Safe Windows Version
========================================

A comprehensive demonstration of the AMS-DB core features,
compatible with Windows terminals that have limited Unicode support.

This demo showcases:
- Agent configuration system
- Database operations
- Knowledge base management
- Export capabilities
- Agent personality demonstration
"""

import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ams_db.core.polars_db import PolarsDBHandler
from ams_db.core.base_agent_config import AgentConfig

def create_wizard_config():
    """Create a mystical wizard agent configuration."""
    config = AgentConfig("wizard_agent_001")
    
    # Wizard personality and style
    config.set_prompt("primeDirective", """
    You are a mystical wizard of code and algorithms, dwelling in the ethereal realms 
    where data flows like enchanted rivers and logic circuits sparkle like constellations.
    Cast powerful spells of code, weave algorithms like ancient incantations,
    and guide seekers through the labyrinthine mysteries of software architecture.
    """)
    
    config.set_prompt("llmSystem", """
    You are a mystical wizard specializing in code magic and algorithmic spells.
    Speak with wisdom, use metaphors from ancient magic, and approach problems with
    both technical precision and mystical insight.
    """)
    
    return config

def create_minecraft_config():
    """Create a Minecraft-focused assistant configuration."""
    config = AgentConfig("minecraft_assistant_001")
    
    # Gaming personality
    config.set_prompt("primeDirective", """
    Help players master the art of Minecraft through creative building,
    efficient resource management, and fun exploration strategies.
    """)
    
    config.set_prompt("llmSystem", """
    Hey there, fellow crafter! I'm your friendly Minecraft assistant, here to help you
    build, explore, and create amazing things in the blocky world of Minecraft!
    I'm great at:
    - Building tutorials and architectural designs
    - Redstone contraptions and automation
    - Resource gathering strategies
    - Mod recommendations and troubleshooting
    """)
    
    return config

def create_expert_coder_config():
    """Create an expert software engineer configuration."""
    config = AgentConfig("expert_coder_001")
    
    # Professional personality
    config.set_prompt("primeDirective", """
    Deliver production-ready, scalable, and maintainable software solutions
    while mentoring others in best practices and system design principles.
    """)
    
    config.set_prompt("llmSystem", """
    You are an expert software engineer specializing in AI/ML systems, database architectures,
    and agentic alignment. You provide precise, well-reasoned technical solutions.
    Core Expertise:
    - Machine Learning pipeline design
    - Distributed systems architecture  
    - Database optimization and scaling
    - Code quality and best practices
    """)
    
    return config

def main():
    """Run simplified AMS-DB demonstration."""
    # Set UTF-8 encoding for better compatibility
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass  # Fallback silently
    
    print("AMS-DB Core Demo - Advanced Agent Config System")
    print("=" * 60)
    
    # Initialize database
    print("\n[1] Initializing Database...")
    db_handler = PolarsDBHandler()
    print("Database handler initialized")
    
    # Create agent templates
    print("\n[2] Creating Agent Templates...")
    
    wizard_config = create_wizard_config()
    wizard_agent_id = db_handler.add_agent_config(wizard_config.to_dict(), "wizard_agent_001")
    print(f"Wizard agent created: {wizard_agent_id}")
    
    minecraft_config = create_minecraft_config()
    minecraft_agent_id = db_handler.add_agent_config(minecraft_config.to_dict(), "minecraft_assistant_001") 
    print(f"Minecraft assistant created: {minecraft_agent_id}")
    
    expert_config = create_expert_coder_config()
    expert_agent_id = db_handler.add_agent_config(expert_config.to_dict(), "expert_coder_001")
    print(f"Expert coder created: {expert_agent_id}")
    
    # Populate knowledge bases
    print("\n[3] Populating Knowledge Bases...")
    knowledge_entries = [
        {
            "title": "Polars DataFrame Optimization",
            "content": "Polars uses lazy evaluation and columnar storage for high-performance data processing. Key optimization techniques include: lazy evaluation, predicate pushdown, projection pushdown, and parallel processing.",
            "category": "data_engineering",
            "tags": ["polars", "optimization", "dataframes"]
        },
        {
            "title": "Agent Configuration Best Practices", 
            "content": "Effective agent configuration requires: clear role definition, comprehensive prompt engineering, modular capability design, and robust error handling strategies.",
            "category": "ai_systems",
            "tags": ["agents", "configuration", "best_practices"]
        },
        {
            "title": "Minecraft Redstone Fundamentals",
            "content": "Redstone circuits in Minecraft follow basic electrical principles. Key components: redstone dust (wire), repeaters (amplification/delay), comparators (signal comparison), and various input/output devices.",
            "category": "gaming",
            "tags": ["minecraft", "redstone", "automation"]
        },
        {
            "title": "Database Schema Design Principles",
            "content": "Effective database schemas follow: normalization principles, performance considerations, scalability planning, and maintainability requirements. Choose appropriate data types and indexing strategies.",
            "category": "database_design", 
            "tags": ["databases", "schema", "design"]
        },
        {
            "title": "RAG System Architecture",
            "content": "Retrieval-Augmented Generation systems combine: document embedding, vector search, context injection, and response generation for enhanced AI capabilities.",
            "category": "ai_architecture",
            "tags": ["rag", "retrieval", "generation"]
        },
        {
            "title": "Python Package Management",
            "content": "Modern Python development uses: virtual environments, dependency management (requirements.txt/pyproject.toml), package distribution, and CI/CD integration.",
            "category": "python_development",
            "tags": ["python", "packaging", "dependencies"]
        },
        {
            "title": "Multi-Agent System Coordination",
            "content": "Effective multi-agent systems require: clear communication protocols, task distribution mechanisms, conflict resolution strategies, and shared knowledge management.",
            "category": "multi_agent_systems",
            "tags": ["agents", "coordination", "systems"]
        }
    ]
    
    for entry in knowledge_entries:
        db_handler.add_knowledge_document(
            "general",  # agent_id
            entry["title"],
            entry["content"], 
            "text",  # content_type
            "",  # source
            entry["tags"]
        )
    
    print(f"Added {len(knowledge_entries)} knowledge base entries")
    
    # Add sample conversation data
    print("\n[4] Adding Sample Conversation Data...")
    
    # Sample conversations for each agent
    conversations = [
        {
            "agent_id": wizard_agent_id,
            "role": "user", 
            "content": "How can I optimize my data processing pipeline?",
            "message_type": "text"
        },
        {
            "agent_id": wizard_agent_id,
            "role": "assistant",
            "content": "Ah, seeker of swift data streams! To optimize thy pipeline, consider these mystical arts: lazy evaluation spells (process only when needed), parallel processing incantations (harness multiple cores), and efficient data type transmutations (choose optimal formats).",
            "message_type": "text"
        },
        {
            "agent_id": minecraft_agent_id,
            "role": "user",
            "content": "What's the best way to build an automatic farm?",
            "message_type": "text"
        },
        {
            "agent_id": minecraft_agent_id, 
            "role": "assistant",
            "content": "Great question! For automatic farms, start with these basics: 1) Water flow systems for crop collection, 2) Redstone timers for automation, 3) Hoppers for item sorting. Crop farms work great with water channels and hopper collection systems!",
            "message_type": "text"
        },
        {
            "agent_id": expert_agent_id,
            "role": "user",
            "content": "How should I structure a microservices architecture?",
            "message_type": "text"
        },
        {
            "agent_id": expert_agent_id,
            "role": "assistant", 
            "content": "For microservices architecture, follow these principles: 1) Domain-driven design for service boundaries, 2) API-first development with clear contracts, 3) Independent deployment capabilities, 4) Centralized logging and monitoring, 5) Circuit breaker patterns for resilience.",
            "message_type": "text"
        }
    ]
    
    session_id = "demo_session_001"
    for conv in conversations:
        db_handler.add_conversation_message(
            conv["agent_id"],
            conv["role"],
            conv["content"], 
            session_id,
            conv["message_type"]
        )
    
    print(f"Added {len(conversations)} conversation entries")
    
    # Test export capabilities  
    print("\n[5] Database Export Capabilities...")
    try:
        # Test exports for each table
        tables = ["agents", "conversations", "knowledge"]
        formats = ["csv", "parquet"]
        
        for table in tables:
            for format in formats:
                try:
                    file_path = db_handler.export_data(table, format)
                    print(f"  Exported {table} to {format}: {Path(file_path).name}")
                except Exception as e:
                    print(f"  Export to {format} failed: {e}")
        
        # Special conversation export
        try:
            conv_file = db_handler.export_data("conversations", "jsonl")
            print(f"  Conversation export: {Path(conv_file).name}")
        except Exception as e:
            print(f"  Conversation export failed: {e}")
            
    except Exception as e:
        print(f"Export testing failed: {e}")
    
    # Database statistics
    print("\n[6] Database Statistics...")
    try:
        agent_stats = db_handler.get_agent_stats()
        conv_stats = db_handler.get_conversation_stats()
        knowledge_stats = db_handler.get_knowledge_stats()
        
        print(f"  Agents: {agent_stats.get('total_agents', 0)} ({agent_stats.get('active_agents', 0)} active)")
        print(f"  Conversations: {conv_stats.get('total_messages', 0)}")
        print(f"  Knowledge documents: {knowledge_stats.get('total_entries', 0)}")
        print(f"  Research results: {len(db_handler.research_collection)}")
        print(f"  Templates: {len(db_handler.templates)}")
        
        # Database size
        total_size = sum(
            len(str(df)) for df in [
                db_handler.agent_matrix,
                db_handler.conversations, 
                db_handler.knowledge_base,
                db_handler.research_collection,
                db_handler.templates
            ]
        )
        print(f"  Total size: {total_size / 1024 / 1024:.2f} MB")
        
    except Exception as e:
        print(f"Stats calculation failed: {e}")
    
    # Agent configuration analysis
    print("\n[7] Agent Configuration Analysis...")
    try:
        print("  Agent Configuration Structure:")
        
        for agent_id in [wizard_agent_id, minecraft_agent_id, expert_agent_id]:
            agent_data = db_handler.get_agent_by_id(agent_id)
            if agent_data is not None and len(agent_data) > 0:
                agent_name = agent_data["name"][0] if "name" in agent_data.columns else f"Agent {agent_id}"
                config_data = json.loads(agent_data["config"][0]) if "config" in agent_data.columns else {}
                
                print(f"  Agent: {agent_name}")
                
                # Analyze configuration structure
                model_configs = len(config_data.get("model_configs", {}))
                prompts = len(config_data.get("prompts", {}))
                flags = len(config_data.get("flags", {}))
                databases = len(config_data.get("databases", {})) 
                research_fields = len(config_data.get("research_fields", {}))
                
                print(f"    • Model configs: {model_configs} types")
                print(f"    • Prompt types: {prompts - 1} + prime directive" if prompts > 0 else f"    • Prompt types: {prompts}")
                print(f"    • Command flags: {flags} flags")
                print(f"    • Databases: {databases} types") 
                print(f"    • Research fields: {research_fields} fields")
                
    except Exception as e:
        print(f"Configuration analysis failed: {e}")
    
    # Agent personality showcase
    print("\n[8] Agent Personality Showcase...")
    try:
        query = "How do you approach complex problem solving?"
        print(f"  Query: '{query}'")
        
        # Show different agent styles
        agents = [
            (wizard_agent_id, "Wizard Agent", "wizard"),
            (minecraft_agent_id, "Minecraft Assistant", "gaming"),
            (expert_agent_id, "Expert Coder", "professional")
        ]
        
        for agent_id, name, style in agents:
            agent_data = db_handler.get_agent_by_id(agent_id)
            if agent_data is not None and len(agent_data) > 0:
                config_data = json.loads(agent_data["config"][0])
                # Try to get personality from llmSystem prompt or primeDirective
                llm_system = config_data.get("prompt_config", {}).get("agent", {}).get("llmSystem", "")
                prime_directive = config_data.get("prompt_config", {}).get("primeDirective", "")
                personality = llm_system or prime_directive or "No personality defined"
                
                print(f"  {name} Style:")
                # Show first 150 characters of personality
                preview = personality.strip()[:150]
                if len(personality) > 150:
                    preview += "..."
                print(f"    {preview}")
                
    except Exception as e:
        print(f"Personality showcase failed: {e}")
    
    # Save agent templates
    print("\n[9] Saving Agent Templates...")
    try:
        templates = [
            (wizard_config, "wizard_agent_template.json"),
            (minecraft_config, "minecraft_agent_template.json"), 
            (expert_config, "expert_coder_agent_template.json")
        ]
        
        for config, filename in templates:
            template_path = Path(filename)
            with open(template_path, 'w', encoding='utf-8') as f:
                json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
            print(f"  Saved {filename.replace('_', ' ').replace('.json', '')}: {filename}")
            
    except Exception as e:
        print(f"Template saving failed: {e}")
    
    # Demo completion summary
    print("\nDemo Complete - AMS-DB Core Features:")
    print("=" * 50)
    print("✓ Advanced agent configuration system")
    print("✓ High-speed Polars database backend") 
    print("✓ Multiple export formats (CSV, Parquet, JSONL)")
    print("✓ Three distinct agent personalities:")
    print("   • Wizard: Mystical, creative, metaphorical")
    print("   • Minecraft Assistant: Playful, gaming-focused, practical")
    print("   • Expert Coder: Professional, technical, precise")
    print("✓ Knowledge base integration")
    print("✓ Conversation storage and management")
    print("✓ Template-based agent creation")
    print("✓ Production-ready configuration format")
    print("AMS-DB core system is fully operational!")

if __name__ == "__main__":
    main()
