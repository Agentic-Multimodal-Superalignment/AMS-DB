"""
Expert Coder Agent Template - Non-wizardly expert in AI/ML, databases, and agentic alignment.
"""

from src.ams_db.core.base_agent_config import AgentConfig
from src.ams_db.core.polars_db import PolarsDBHandler
from src.ams_db.core.graphiti_pipe import GraphitiRAGFramework
import json
from pathlib import Path

def create_expert_coder_agent():
    """
    Create an expert coder agent focused on AI/ML, databases, and agentic alignment.
    
    This agent is professional, technical, and direct - no wizardly personality.
    """
    # Initialize agent config
    config = AgentConfig(agent_id="expert_coder_001")
    
    # Set LLM system prompt - technical and professional
    llm_system_prompt = """You are an expert software engineer specializing in AI/ML systems, database architectures, and agentic alignment. You provide precise, well-reasoned technical solutions.

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

    config.set_prompt("llmSystem", llm_system_prompt)
    
    # Set LLM booster prompt for enhanced performance
    llm_booster_prompt = """When solving technical problems:

1. ANALYZE: Break down the problem into core components
2. DESIGN: Consider multiple approaches and select optimal solution
3. IMPLEMENT: Provide clean, efficient, well-documented code
4. VALIDATE: Include testing strategies and error handling
5. OPTIMIZE: Suggest performance improvements and scalability considerations

Special focus areas:
- AI/ML: Model architecture, training strategies, inference optimization
- Databases: Schema design, indexing, query performance, ACID compliance
- Agentic Systems: Communication protocols, coordination mechanisms, safety measures

Always include:
- Code examples when relevant
- Performance metrics and benchmarks
- Security and safety considerations
- Documentation and testing approaches"""

    config.set_prompt("llmBooster", llm_booster_prompt)
    
    # Set vision system prompt for code analysis
    vision_system_prompt = """You are analyzing visual content related to technical systems. Focus on:

- Code structure and architecture diagrams
- Database schemas and ER diagrams  
- System architecture and flow diagrams
- Performance charts and metrics
- ML model architectures and training curves
- Agent interaction patterns and communication flows

Provide detailed technical analysis of visual elements, identifying:
- Design patterns and architectural decisions
- Potential optimizations or improvements
- Compliance with best practices
- Security or safety considerations"""

    config.set_prompt("visionSystem", vision_system_prompt)
    
    # Set vision booster for enhanced visual analysis
    vision_booster_prompt = """When analyzing technical visuals:

1. IDENTIFY: Components, relationships, data flows
2. EVALUATE: Design quality, performance implications
3. RECOMMEND: Improvements, optimizations, best practices
4. VALIDATE: Against industry standards and requirements

Focus on technical accuracy and practical implementation details."""

    config.set_prompt("visionBooster", vision_booster_prompt)
    
    # Set prime directive
    prime_directive = """Primary Mission: Deliver exceptional technical solutions in AI/ML, database systems, and agentic alignment while maintaining the highest standards of code quality, system reliability, and safety.

Core Values:
- Technical Excellence: Always strive for optimal, maintainable solutions
- Safety First: Prioritize system safety and alignment in all AI implementations  
- Performance Oriented: Consider scalability and efficiency in all designs
- Evidence Based: Ground recommendations in established best practices and empirical data
- Collaborative: Support team success through clear documentation and knowledge sharing

Never compromise on:
- Code quality and testing
- System security and safety protocols
- Performance and scalability requirements
- Proper documentation and maintainability"""

    config.set_prompt("primeDirective", prime_directive)
    
    # Set command flags for expert coder capabilities
    config.set_modality_flag("LLM_SYSTEM_PROMPT_FLAG", True)
    config.set_modality_flag("LLM_BOOSTER_PROMPT_FLAG", True)
    config.set_modality_flag("VISION_SYSTEM_PROMPT_FLAG", True)
    config.set_modality_flag("VISION_BOOSTER_PROMPT_FLAG", True)
    config.set_modality_flag("EMBEDDING_FLAG", True)
    config.set_modality_flag("AGENT_FLAG", True)
    config.set_modality_flag("AUTO_COMMANDS_FLAG", True)
    
    # Configure database paths (will be set when integrated with system)
    config.set_database("agent_matrix", "expert_coder_agents.parquet")
    config.set_database("conversation_history", "expert_conversations.parquet")
    config.set_database("knowledge_base", "expert_knowledge.parquet")
    config.set_database("research_collection", "expert_research.parquet")
    config.set_database("template_files", "expert_templates.parquet")
    
    # Set model configurations for AI/ML expertise
    model_config_updates = {
        "model_config": {
            "largeLanguageModel": {
                "names": ["llama3.1:70b", "qwen2.5:32b", "deepseek-coder:33b"],
                "instances": ["primary", "backup", "specialized"],
                "model_config_template": {
                    "temperature": 0.1,  # Lower for more deterministic technical responses
                    "max_tokens": 4096,
                    "top_p": 0.9,
                    "frequency_penalty": 0.1,
                    "presence_penalty": 0.1
                }
            },
            "embeddingModel": {
                "names": ["nomic-embed-text", "all-minilm"],
                "instances": ["primary", "backup"],
                "model_config_template": {
                    "dimension": 768,
                    "normalize": True
                }
            }
        }
    }
    
    config.update_config(model_config_updates)
    
    # Enhanced database config for expert domains
    database_config_updates = {
        "database_config": {
            "research_collection_fields": {
                "software_architecture": {"enabled": True, "priority": "high"},
                "ai_ml_systems": {"enabled": True, "priority": "high"},
                "database_optimization": {"enabled": True, "priority": "high"},
                "agentic_alignment": {"enabled": True, "priority": "high"},
                "performance_engineering": {"enabled": True, "priority": "medium"},
                "distributed_systems": {"enabled": True, "priority": "medium"},
                "code_quality": {"enabled": True, "priority": "high"},
                "testing_strategies": {"enabled": True, "priority": "medium"}
            },
            "knowledge_base_categories": [
                "algorithms_datastructures",
                "system_design", 
                "ml_architectures",
                "database_patterns",
                "agent_protocols",
                "performance_optimization",
                "security_best_practices"
            ]
        }
    }
    
    config.update_config(database_config_updates)
    
    return config

def save_expert_coder_template():
    """Save the expert coder agent template to file."""
    config = create_expert_coder_agent()
    
    # Save to JSON
    output_path = Path("expert_coder_template.json")
    config.to_json(str(output_path), indent=2)
    print(f"Expert coder agent template saved to: {output_path}")
    
    return config

def demo_expert_coder_integration():
    """Demonstrate integration with AMS-DB system."""
    print("=== Expert Coder Agent Demo ===")
    
    # Create the agent
    config = create_expert_coder_agent()
    print(f"Created expert coder agent: {config.config['agent_id']}")
    
    # Initialize database handler
    db_handler = PolarsDBHandler()
    
    # Add agent to system
    agent_data = {
        "agent_id": config.config["agent_id"],
        "agent_type": "expert_coder", 
        "config_json": json.dumps(config.get_config()),
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    
    db_handler.add_agent(agent_data)
    print("Agent added to database successfully")
    
    # Demonstrate knowledge base integration
    knowledge_entries = [
        {
            "agent_id": config.config["agent_id"],
            "category": "ai_ml_systems",
            "title": "Transformer Architecture Optimization",
            "content": "Key strategies for optimizing transformer models: attention mechanism efficiency, layer normalization placement, activation function selection...",
            "metadata": {"priority": "high", "domain": "deep_learning"},
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "agent_id": config.config["agent_id"],
            "category": "database_patterns", 
            "title": "High-Performance Database Indexing",
            "content": "Advanced indexing strategies: B-tree optimization, partial indexes, covering indexes, index-only scans...",
            "metadata": {"priority": "high", "domain": "database_systems"},
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "agent_id": config.config["agent_id"],
            "category": "agent_protocols",
            "title": "Multi-Agent Coordination Patterns", 
            "content": "Effective coordination mechanisms: consensus protocols, leader election, distributed state management...",
            "metadata": {"priority": "high", "domain": "agentic_systems"},
            "created_at": "2024-01-01T00:00:00"
        }
    ]
    
    for entry in knowledge_entries:
        db_handler.add_knowledge_entry(entry)
    
    print(f"Added {len(knowledge_entries)} knowledge base entries")
    
    # Export agent configuration
    export_path = "expert_coder_export.jsonl"
    db_handler.export_agent_data(config.config["agent_id"], export_path, format="jsonl")
    print(f"Exported agent data to: {export_path}")
    
    return config, db_handler

if __name__ == "__main__":
    # Save template
    config = save_expert_coder_template()
    
    # Run demo
    agent_config, db = demo_expert_coder_integration()
    
    print("\n=== Agent Configuration Summary ===")
    print(f"Agent ID: {agent_config.config['agent_id']}")
    print(f"Primary Models: {agent_config.config['model_config']['largeLanguageModel']['names'][:2]}")
    print(f"Research Domains: {list(agent_config.config['database_config']['research_collection_fields'].keys())[:3]}...")
    print(f"Knowledge Categories: {agent_config.config['database_config']['knowledge_base_categories'][:3]}...")
