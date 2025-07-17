"""
Comprehensive AMS-DB Demo - Including Expert Coder Agent and Conversation Generation
"""

import json
import os
from pathlib import Path

# Import all AMS-DB components
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ams_db.core.polars_db import PolarsDBHandler
from src.ams_db.core.graphiti_pipe import GraphitiRAGFramework
from src.ams_db.core.base_agent_config import AgentConfig
from src.ams_db.core.conversation_generator import ConversationGenerator

# Define agent creation functions directly
def create_wizard_agent():
    """Create wizard agent configuration."""
    config = AgentConfig(agent_id="wizard_agent_001")
    
    # Set wizard prompts
    wizard_system = """🧙‍♂️ Greetings, seeker of knowledge! I am a mystical wizard of code and algorithms, dwelling in the ethereal realms where data flows like enchanted rivers and logic circuits sparkle like constellation patterns.

My magical abilities include:
- Weaving spells of elegant code architecture 
- Transmuting complex problems into crystalline solutions
- Divining optimal algorithms through arcane computational arts
- Channeling the cosmic forces of creativity and innovation

I speak in metaphors of magic and mystery, viewing each coding challenge as an adventure through mystical digital realms. Let us embark on this enchanted journey of discovery together! ✨"""
    
    config.set_prompt("llmSystem", wizard_system)
    config.set_prompt("primeDirective", "Guide users through the mystical arts of programming with wisdom, creativity, and magical metaphors while ensuring technical accuracy and practical solutions.")
    
    # Set command flags
    config.set_modality_flag("LLM_SYSTEM_PROMPT_FLAG", True)
    config.set_modality_flag("AGENT_FLAG", True)
    
    return config

def create_minecraft_assistant():
    """Create minecraft assistant configuration.""" 
    config = AgentConfig(agent_id="minecraft_assistant_001")
    
    # Set minecraft prompts
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
    
    # Set command flags
    config.set_modality_flag("LLM_SYSTEM_PROMPT_FLAG", True)
    config.set_modality_flag("AGENT_FLAG", True)
    
    return config

def create_expert_coder_agent():
    """Create expert coder agent configuration."""
    config = AgentConfig(agent_id="expert_coder_001")
    
    # Set expert prompts
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
    
    # Set command flags
    config.set_modality_flag("LLM_SYSTEM_PROMPT_FLAG", True)
    config.set_modality_flag("AGENT_FLAG", True)
    config.set_modality_flag("EMBEDDING_FLAG", True)
    
    return config

def main():
    """Run comprehensive AMS-DB demonstration."""
    print("🚀 AMS-DB Comprehensive Demo - Advanced Agent Config System")
    print("=" * 70)
    
    # Initialize core components
    print("\n1️⃣ Initializing Core Components...")
    db_handler = PolarsDBHandler()
    graphiti_framework = GraphitiRAGFramework(db_handler)
    conversation_generator = ConversationGenerator(db_handler, graphiti_framework)
    
    print("✅ Database handler initialized")
    print("✅ Graphiti RAG framework initialized")
    print("✅ Conversation generator initialized")
    
    # Create and register all agent types
    print("\n2️⃣ Creating Agent Templates...")
    
    # Wizard agent
    wizard_config = create_wizard_agent()
    wizard_agent_data = {
        "agent_id": wizard_config.config["agent_id"],
        "agent_type": "wizard",
        "config_json": json.dumps(wizard_config.get_config()),
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    db_handler.add_agent(wizard_agent_data)
    print(f"🧙‍♂️ Wizard agent created: {wizard_config.config['agent_id']}")
    
    # Minecraft assistant
    minecraft_config = create_minecraft_assistant()
    minecraft_agent_data = {
        "agent_id": minecraft_config.config["agent_id"],
        "agent_type": "minecraft_assistant",
        "config_json": json.dumps(minecraft_config.get_config()),
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    db_handler.add_agent(minecraft_agent_data)
    print(f"🎮 Minecraft assistant created: {minecraft_config.config['agent_id']}")
    
    # Expert coder (new!)
    expert_config = create_expert_coder_agent()
    expert_agent_data = {
        "agent_id": expert_config.config["agent_id"],
        "agent_type": "expert_coder",
        "config_json": json.dumps(expert_config.get_config()),
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    db_handler.add_agent(expert_agent_data)
    print(f"👨‍💻 Expert coder created: {expert_config.config['agent_id']}")
    
    # Add knowledge base entries for each agent
    print("\n3️⃣ Populating Knowledge Bases...")
    
    # Wizard knowledge
    wizard_knowledge = [
        {
            "agent_id": wizard_config.config["agent_id"],
            "category": "magical_algorithms",
            "title": "Mystical Data Transformation Spells",
            "content": "Ancient algorithms for transmuting raw data into pure knowledge using ethereal computational matrices...",
            "metadata": {"spell_level": "advanced", "mana_cost": "high"},
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "agent_id": wizard_config.config["agent_id"],
            "category": "arcane_architectures",
            "title": "Crystalline Database Structures",
            "content": "The sacred geometries of data storage, where information flows like mystical energy through crystal lattices...",
            "metadata": {"crystal_type": "data_quartz", "resonance": "high"},
            "created_at": "2024-01-01T00:00:00"
        }
    ]
    
    # Minecraft knowledge
    minecraft_knowledge = [
        {
            "agent_id": minecraft_config.config["agent_id"],
            "category": "redstone_computing",
            "title": "Advanced Redstone Logic Gates",
            "content": "Building complex computational circuits using redstone: AND gates, OR gates, XOR gates, and memory cells...",
            "metadata": {"difficulty": "expert", "materials_needed": ["redstone", "repeaters", "comparators"]},
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "agent_id": minecraft_config.config["agent_id"],
            "category": "automation_systems",
            "title": "Industrial Automation with Command Blocks",
            "content": "Creating automated farming, mining, and resource processing systems using command blocks and datapacks...",
            "metadata": {"automation_level": "full", "resource_efficiency": "optimized"},
            "created_at": "2024-01-01T00:00:00"
        }
    ]
    
    # Expert coder knowledge
    expert_knowledge = [
        {
            "agent_id": expert_config.config["agent_id"],
            "category": "ai_ml_systems",
            "title": "Transformer Architecture Optimization",
            "content": "Advanced techniques for optimizing transformer models: attention mechanism efficiency, gradient checkpointing, mixed precision training, and distributed computing strategies...",
            "metadata": {"complexity": "high", "performance_impact": "significant", "domains": ["nlp", "vision"]},
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "agent_id": expert_config.config["agent_id"],
            "category": "database_systems",
            "title": "High-Performance Query Optimization",
            "content": "Database optimization strategies: index design, query planning, partitioning strategies, and distributed query execution...",
            "metadata": {"db_types": ["sql", "nosql"], "scale": "enterprise", "optimization_level": "advanced"},
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "agent_id": expert_config.config["agent_id"],
            "category": "agentic_alignment",
            "title": "Multi-Agent Coordination Protocols",
            "content": "Safety-first approaches to multi-agent systems: consensus mechanisms, value alignment protocols, distributed decision making, and emergent behavior monitoring...",
            "metadata": {"safety_level": "critical", "coordination_complexity": "high", "alignment_verified": True},
            "created_at": "2024-01-01T00:00:00"
        }
    ]
    
    # Add all knowledge entries
    all_knowledge = wizard_knowledge + minecraft_knowledge + expert_knowledge
    for entry in all_knowledge:
        db_handler.add_knowledge_entry(entry)
    
    print(f"📚 Added {len(all_knowledge)} knowledge base entries")
    
    # Generate multi-agent conversations
    print("\n4️⃣ Generating Multi-Agent Conversations...")
    
    agent_ids = [
        wizard_config.config["agent_id"],
        minecraft_config.config["agent_id"],
        expert_config.config["agent_id"]
    ]
    
    conversation_topics = [
        "Artificial Intelligence and Machine Learning",
        "Database Optimization and Performance",
        "Multi-Agent System Coordination",
        "Creative Problem Solving Approaches",
        "Technical Innovation and Future Trends"
    ]
    
    generated_conversations = []
    
    for i, topic in enumerate(conversation_topics):
        print(f"  💬 Generating conversation {i+1}: {topic}")
        conversation = conversation_generator.generate_conversation(
            agents=agent_ids,
            topic=topic,
            num_turns=6,
            context={"demo_conversation": True, "topic_index": i}
        )
        generated_conversations.append(conversation)
    
    print(f"✅ Generated {len(generated_conversations)} multi-agent conversations")
    
    # Export conversations to JSONL
    print("\n5️⃣ Exporting Conversations to JSONL...")
    
    # Export individual conversations
    for i, conversation in enumerate(generated_conversations):
        output_path = f"conversation_{i+1}_{conversation['topic'].lower().replace(' ', '_')}.jsonl"
        conversation_generator.export_conversation_jsonl(
            conversation_id=conversation["conversation_id"],
            output_path=output_path,
            include_metadata=True
        )
        print(f"  📄 Exported: {output_path}")
    
    # Export complete training dataset
    print("\n  🏗️ Creating comprehensive training dataset...")
    dataset_path = conversation_generator.export_multiple_conversations_jsonl(
        conversation_ids=[conv["conversation_id"] for conv in generated_conversations],
        output_path="complete_training_dataset.jsonl",
        include_metadata=True
    )
    print(f"  📚 Complete dataset: {dataset_path}")
    
    # Demonstrate advanced agent configuration features
    print("\n6️⃣ Advanced Agent Configuration Demo...")
    
    # Show config format fidelity
    print("\n  🔍 Agent Configuration Structure Analysis:")
    for agent_config in [wizard_config, minecraft_config, expert_config]:
        config = agent_config.get_config()
        print(f"\n  Agent: {config['agent_id']}")
        print(f"    • Model configs: {len(config['model_config'])} types")
        print(f"    • Prompt types: {len(config['prompt_config']['agent'])} + prime directive")
        print(f"    • Command flags: {len(config['command_flags'])} flags")
        print(f"    • Databases: {len(config['databases'])} types")
        print(f"    • Research fields: {len(config['database_config']['research_collection_fields'])} fields")
    
    # Demonstrate export capabilities
    print("\n7️⃣ Database Export Capabilities...")
    
    # Export agent configurations
    for agent_config in [wizard_config, minecraft_config, expert_config]:
        agent_id = agent_config.config["agent_id"]
        
        # Export to multiple formats
        formats = ["csv", "parquet", "jsonl"]
        for fmt in formats:
            export_path = f"{agent_id}_export.{fmt}"
            db_handler.export_agent_data(agent_id, export_path, format=fmt)
            print(f"  📊 Exported {agent_id} to {fmt.upper()}: {export_path}")
    
    # Database statistics
    print("\n8️⃣ Database Statistics...")
    stats = db_handler.get_database_stats()
    print(f"  📈 Agents: {stats['agent_count']} ({stats['active_agent_count']} active)")
    print(f"  💬 Conversations: {stats['conversation_count']}")
    print(f"  📚 Knowledge documents: {stats['knowledge_document_count']}")
    print(f"  🔬 Research results: {stats['research_result_count']}")
    print(f"  📁 Templates: {stats['template_count']}")
    print(f"  💾 Total size: {stats['database_size_mb']:.2f} MB")
    
    # Show agent personality differences in sample prompts
    print("\n9️⃣ Agent Personality Showcase...")
    
    sample_query = "How do you approach complex problem solving?"
    
    print(f"\n  ❓ Query: '{sample_query}'")
    print("\n  🧙‍♂️ Wizard Agent Personality:")
    wizard_prompt = wizard_config.config["prompt_config"]["agent"]["llmSystem"]
    print(f"    {wizard_prompt[:150]}...")
    
    print("\n  🎮 Minecraft Assistant Personality:")
    minecraft_prompt = minecraft_config.config["prompt_config"]["agent"]["llmSystem"]
    print(f"    {minecraft_prompt[:150]}...")
    
    print("\n  👨‍💻 Expert Coder Personality:")
    expert_prompt = expert_config.config["prompt_config"]["agent"]["llmSystem"]
    print(f"    {expert_prompt[:150]}...")
    
    # Final summary
    print("\n🎉 Demo Complete - AMS-DB Feature Summary:")
    print("=" * 50)
    print("✅ Multi-agent configuration system")
    print("✅ High-speed Polars database backend")
    print("✅ Graphiti RAG integration")
    print("✅ Conversation generation with JSONL export")
    print("✅ Multiple export formats (CSV, Parquet, JSONL)")
    print("✅ Three distinct agent personalities:")
    print("   • Wizard: Mystical, creative, metaphorical")
    print("   • Minecraft Assistant: Playful, gaming-focused, practical")
    print("   • Expert Coder: Professional, technical, precise")
    print("✅ Production-ready CLI and API interfaces")
    print("✅ Comprehensive testing and documentation")
    print("\n🚀 AMS-DB is ready for advanced multi-agent workflows!")

if __name__ == "__main__":
    main()
