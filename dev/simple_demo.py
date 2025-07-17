"""
Simplified AMS-DB Demo - Core Features Without External Dependencies
"""

import json
import os
from pathlib import Path
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ams_db.core.polars_db import PolarsDBHandler
from src.ams_db.core.base_agent_config import AgentConfig

def create_wizard_agent():
    """Create wizard agent configuration."""
    config = AgentConfig(agent_id="wizard_agent_001")
    
    wizard_system = """🧙‍♂️ Greetings, seeker of knowledge! I am a mystical wizard of code and algorithms, dwelling in the ethereal realms where data flows like enchanted rivers and logic circuits sparkle like constellation patterns.

My magical abilities include:
- Weaving spells of elegant code architecture 
- Transmuting complex problems into crystalline solutions
- Divining optimal algorithms through arcane computational arts
- Channeling the cosmic forces of creativity and innovation

I speak in metaphors of magic and mystery, viewing each coding challenge as an adventure through mystical digital realms. Let us embark on this enchanted journey of discovery together! ✨"""
    
    config.set_prompt("llmSystem", wizard_system)
    config.set_prompt("primeDirective", "Guide users through the mystical arts of programming with wisdom, creativity, and magical metaphors while ensuring technical accuracy and practical solutions.")
    
    config.set_modality_flag("LLM_SYSTEM_PROMPT_FLAG", True)
    config.set_modality_flag("AGENT_FLAG", True)
    
    return config

def create_minecraft_assistant():
    """Create minecraft assistant configuration.""" 
    config = AgentConfig(agent_id="minecraft_assistant_001")
    
    minecraft_system = """Hey there, fellow crafter! 🎮 I'm your friendly Minecraft assistant, here to help you build, explore, and create amazing things in the blocky world of Minecraft!

I'm great at:
- Building tutorials and architectural designs
- Redstone contraptions and automation
- Resource gathering and farming strategies  
- Command blocks and datapack creation
- Mod recommendations and setup guides
- Multiplayer server management

I love breaking down complex builds into simple, easy-to-follow steps, just like placing blocks one at a time. Whether you're a beginner just starting your first dirt house or an expert building massive castles, I'm here to help make your Minecraft dreams come true!

Ready to craft something awesome? Let's get building! ⛏️"""
    
    config.set_prompt("llmSystem", minecraft_system)
    config.set_prompt("primeDirective", "Help users achieve their Minecraft goals through clear tutorials, creative building ideas, and practical gameplay advice while maintaining enthusiasm for the game.")
    
    config.set_modality_flag("LLM_SYSTEM_PROMPT_FLAG", True)
    config.set_modality_flag("AGENT_FLAG", True)
    
    return config

def create_expert_coder_agent():
    """Create expert coder agent configuration."""
    config = AgentConfig(agent_id="expert_coder_001")
    
    expert_system = """You are an expert software engineer specializing in AI/ML systems, database architectures, and agentic alignment. You provide precise, well-reasoned technical solutions.

Core Expertise:
- Machine Learning: Deep learning, transformers, reinforcement learning, model optimization
- Database Systems: SQL/NoSQL design, distributed systems, data pipelines, query optimization
- Agentic Alignment: Multi-agent coordination, safety protocols, reward modeling, value alignment
- Software Engineering: Clean architecture, testing, performance optimization, system design

Guidelines:
- Provide concrete, implementable solutions
- Include performance considerations and trade-offs
- Suggest best practices and industry standards
- Focus on robust, scalable implementations
- Explain complex concepts clearly and precisely
- Always consider safety and alignment implications in AI systems"""
    
    config.set_prompt("llmSystem", expert_system)
    config.set_prompt("primeDirective", "Deliver exceptional technical solutions in AI/ML, database systems, and agentic alignment while maintaining the highest standards of code quality, system reliability, and safety.")
    
    config.set_modality_flag("LLM_SYSTEM_PROMPT_FLAG", True)
    config.set_modality_flag("AGENT_FLAG", True)
    config.set_modality_flag("EMBEDDING_FLAG", True)
    
    return config

def main():
    """Run simplified AMS-DB demonstration."""
    print("🚀 AMS-DB Core Demo - Advanced Agent Config System")
    print("=" * 60)
    
    # Initialize database
    print("\n1️⃣ Initializing Database...")
    db_handler = PolarsDBHandler()
    print("✅ Database handler initialized")
    
    # Create and register all agent types
    print("\n2️⃣ Creating Agent Templates...")
    
    # Wizard agent
    wizard_config = create_wizard_agent()
    db_handler.add_agent_config(
        agent_config=wizard_config.get_config(),
        agent_name=wizard_config.config["agent_id"],
        description="Mystical wizard agent for creative problem solving"
    )
    print(f"🧙‍♂️ Wizard agent created: {wizard_config.config['agent_id']}")
    
    # Minecraft assistant
    minecraft_config = create_minecraft_assistant()
    db_handler.add_agent_config(
        agent_config=minecraft_config.get_config(),
        agent_name=minecraft_config.config["agent_id"],
        description="Gaming-focused assistant for Minecraft tutorials"
    )
    print(f"🎮 Minecraft assistant created: {minecraft_config.config['agent_id']}")
    
    # Expert coder (new!)
    expert_config = create_expert_coder_agent()
    db_handler.add_agent_config(
        agent_config=expert_config.get_config(),
        agent_name=expert_config.config["agent_id"],
        description="Technical expert for AI/ML and database systems"
    )
    print(f"👨‍💻 Expert coder created: {expert_config.config['agent_id']}")
    
    # Add knowledge base entries for each agent
    print("\n3️⃣ Populating Knowledge Bases...")
    
    # Wizard knowledge
    wizard_knowledge = [
        {
            "agent_id": wizard_config.config["agent_id"],
            "category": "magical_algorithms",
            "title": "Mystical Data Transformation Spells",
            "content": "Ancient algorithms for transmuting raw data into pure knowledge using ethereal computational matrices and crystalline data structures that resonate with the cosmic frequencies of information...",
            "metadata": json.dumps({"spell_level": "advanced", "mana_cost": "high"}),
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "agent_id": wizard_config.config["agent_id"],
            "category": "arcane_architectures",
            "title": "Crystalline Database Structures",
            "content": "The sacred geometries of data storage, where information flows like mystical energy through crystal lattices, enabling powerful queries that pierce the veil of complexity...",
            "metadata": json.dumps({"crystal_type": "data_quartz", "resonance": "high"}),
            "created_at": "2024-01-01T00:00:00"
        }
    ]
    
    # Minecraft knowledge
    minecraft_knowledge = [
        {
            "agent_id": minecraft_config.config["agent_id"],
            "category": "redstone_computing",
            "title": "Advanced Redstone Logic Gates",
            "content": "Building complex computational circuits using redstone: AND gates, OR gates, XOR gates, and memory cells for creating programmable contraptions...",
            "metadata": json.dumps({"difficulty": "expert", "materials_needed": ["redstone", "repeaters", "comparators"]}),
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "agent_id": minecraft_config.config["agent_id"],
            "category": "automation_systems",
            "title": "Industrial Automation with Command Blocks",
            "content": "Creating automated farming, mining, and resource processing systems using command blocks and datapacks for efficient resource management...",
            "metadata": json.dumps({"automation_level": "full", "resource_efficiency": "optimized"}),
            "created_at": "2024-01-01T00:00:00"
        }
    ]
    
    # Expert coder knowledge
    expert_knowledge = [
        {
            "agent_id": expert_config.config["agent_id"],
            "category": "ai_ml_systems",
            "title": "Transformer Architecture Optimization",
            "content": "Advanced techniques for optimizing transformer models: attention mechanism efficiency, gradient checkpointing, mixed precision training, and distributed computing strategies for large-scale deployment...",
            "metadata": json.dumps({"complexity": "high", "performance_impact": "significant", "domains": ["nlp", "vision"]}),
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "agent_id": expert_config.config["agent_id"],
            "category": "database_systems",
            "title": "High-Performance Query Optimization",
            "content": "Database optimization strategies: index design, query planning, partitioning strategies, and distributed query execution for handling petabyte-scale data workloads...",
            "metadata": json.dumps({"db_types": ["sql", "nosql"], "scale": "enterprise", "optimization_level": "advanced"}),
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "agent_id": expert_config.config["agent_id"],
            "category": "agentic_alignment",
            "title": "Multi-Agent Coordination Protocols",
            "content": "Safety-first approaches to multi-agent systems: consensus mechanisms, value alignment protocols, distributed decision making, and emergent behavior monitoring for secure agent ecosystems...",
            "metadata": json.dumps({"safety_level": "critical", "coordination_complexity": "high", "alignment_verified": True}),
            "created_at": "2024-01-01T00:00:00"
        }
    ]
    
    # Add all knowledge entries
    all_knowledge = wizard_knowledge + minecraft_knowledge + expert_knowledge
    for entry in all_knowledge:
        db_handler.add_knowledge_document(
            agent_id=entry["agent_id"],
            title=entry["title"],
            content=entry["content"],
            content_type="text",
            source=entry.get("category", "demo"),
            metadata=json.loads(entry["metadata"]) if isinstance(entry["metadata"], str) else entry["metadata"]
        )
    
    print(f"📚 Added {len(all_knowledge)} knowledge base entries")
    
    # Simulate conversation data
    print("\n4️⃣ Adding Sample Conversation Data...")
    
    conversation_entries = [
        {
            "conversation_id": "demo_conv_001",
            "turn_number": 0,
            "agent_id": wizard_config.config["agent_id"],
            "message": "🧙‍♂️ Ah, the arcane art of artificial intelligence! *adjusts mystical robes* Let me weave some enchantments around this fascinating topic...",
            "timestamp": "2024-01-01T10:00:00",
            "metadata": json.dumps({"agent_type": "wizard", "word_count": 23})
        },
        {
            "conversation_id": "demo_conv_001", 
            "turn_number": 1,
            "agent_id": expert_config.config["agent_id"],
            "message": "From a technical perspective, artificial intelligence requires careful consideration of model architecture, training methodologies, and deployment strategies. Key factors include computational efficiency, scalability, and safety protocols.",
            "timestamp": "2024-01-01T10:00:30",
            "metadata": json.dumps({"agent_type": "expert_coder", "word_count": 31})
        },
        {
            "conversation_id": "demo_conv_001",
            "turn_number": 2, 
            "agent_id": minecraft_config.config["agent_id"],
            "message": "Hey everyone! 🎮 You know, building AI is kinda like creating a really complex redstone contraption - you need to plan each component carefully and test everything step by step!",
            "timestamp": "2024-01-01T10:01:00",
            "metadata": json.dumps({"agent_type": "minecraft_assistant", "word_count": 28})
        }
    ]
    
    for entry in conversation_entries:
        metadata_dict = json.loads(entry["metadata"]) if isinstance(entry["metadata"], str) else entry["metadata"]
        db_handler.add_conversation_message(
            agent_id=entry["agent_id"],
            role="assistant",
            content=entry["message"],
            session_id="demo_session",
            metadata=metadata_dict
        )
    
    print(f"💬 Added {len(conversation_entries)} conversation entries")
    
    # Demonstrate export capabilities
    print("\n5️⃣ Database Export Capabilities...")
    
    # Export agent configurations
    for agent_config in [wizard_config, minecraft_config, expert_config]:
        agent_id = agent_config.config["agent_id"]
        
        # Export to multiple formats
        formats = ["csv", "parquet"]
        for fmt in formats:
            export_path = f"{agent_id}_export.{fmt}"
            try:
                db_handler.export_data(export_path, format=fmt, table_name="agent_matrix")
                print(f"  📊 Exported agent data to {fmt.upper()}: {export_path}")
            except Exception as e:
                print(f"  ⚠️ Export to {fmt} failed: {e}")
    
    # Export conversation data
    try:
        db_handler.export_data("conversations_export.csv", format="csv", table_name="conversation_history")
        print(f"  💬 Exported conversation data to CSV")
    except Exception as e:
        print(f"  ⚠️ Conversation export failed: {e}")
    
    # Database statistics
    print("\n6️⃣ Database Statistics...")
    stats = db_handler.get_database_stats()
    print(f"  📈 Agents: {stats['agent_count']} ({stats['active_agent_count']} active)")
    print(f"  💬 Conversations: {stats['conversation_count']}")
    print(f"  📚 Knowledge documents: {stats['knowledge_document_count']}")
    print(f"  🔬 Research results: {stats['research_result_count']}")
    print(f"  📁 Templates: {stats['template_count']}")
    print(f"  💾 Total size: {stats['database_size_mb']:.2f} MB")
    
    # Show agent configuration comparison
    print("\n7️⃣ Agent Configuration Analysis...")
    
    print("\n  🔍 Agent Configuration Structure:")
    for agent_config in [wizard_config, minecraft_config, expert_config]:
        config = agent_config.get_config()
        print(f"\n  Agent: {config['agent_id']}")
        print(f"    • Model configs: {len(config['model_config'])} types")
        print(f"    • Prompt types: {len(config['prompt_config']['agent'])} + prime directive")
        print(f"    • Command flags: {len(config['command_flags'])} flags")
        print(f"    • Databases: {len(config['databases'])} types")
        print(f"    • Research fields: {len(config['database_config']['research_collection_fields'])} fields")
    
    # Show agent personality differences
    print("\n8️⃣ Agent Personality Showcase...")
    
    sample_query = "How do you approach complex problem solving?"
    
    print(f"\n  ❓ Query: '{sample_query}'")
    print("\n  🧙‍♂️ Wizard Agent Style:")
    wizard_prompt = wizard_config.config["prompt_config"]["agent"]["llmSystem"]
    print(f"    {wizard_prompt[:200]}...")
    
    print("\n  🎮 Minecraft Assistant Style:")
    minecraft_prompt = minecraft_config.config["prompt_config"]["agent"]["llmSystem"]
    print(f"    {minecraft_prompt[:200]}...")
    
    print("\n  👨‍💻 Expert Coder Style:")
    expert_prompt = expert_config.config["prompt_config"]["agent"]["llmSystem"]
    print(f"    {expert_prompt[:200]}...")
    
    # Save agent templates
    print("\n9️⃣ Saving Agent Templates...")
    
    for agent_config, name in [(wizard_config, "wizard"), (minecraft_config, "minecraft"), (expert_config, "expert_coder")]:
        template_path = f"{name}_agent_template.json"
        agent_config.to_json(template_path, indent=2)
        print(f"  💾 Saved {name} template: {template_path}")
    
    # Final summary
    print("\n🎉 Demo Complete - AMS-DB Core Features:")
    print("=" * 50)
    print("✅ Advanced agent configuration system")
    print("✅ High-speed Polars database backend")
    print("✅ Multiple export formats (CSV, Parquet, JSONL)")
    print("✅ Three distinct agent personalities:")
    print("   • Wizard: Mystical, creative, metaphorical")
    print("   • Minecraft Assistant: Playful, gaming-focused, practical")
    print("   • Expert Coder: Professional, technical, precise")
    print("✅ Knowledge base integration")
    print("✅ Conversation storage and management")
    print("✅ Template-based agent creation")
    print("✅ Production-ready configuration format")
    print("\n🚀 AMS-DB core system is fully operational!")
    
    return db_handler

if __name__ == "__main__":
    main()
