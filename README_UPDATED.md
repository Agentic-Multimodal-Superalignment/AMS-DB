# AMS-DB: Advanced Multi-Agent System Database

A high-performance database and configuration system for multi-agent AI workflows, featuring agent configuration management, conversation/knowledge storage with Graphiti RAG, and ultra-fast Polars database backend.

## 🌟 Key Features

- **Advanced Agent Configuration System**: Unified agent config format matching original prompt sets
- **High-Speed Database**: Polars-powered DataFrame storage with multi-format export
- **Graphiti RAG Integration**: Knowledge graphs and retrieval-augmented generation
- **Multi-Agent Conversations**: Generate and export conversation datasets in JSONL format
- **Three Agent Personalities**: Wizard (mystical), Minecraft Assistant (playful), Expert Coder (technical)
- **Production-Ready APIs**: Both CLI and FastAPI interfaces
- **Multiple Export Formats**: CSV, Parquet, JSONL, JSON support

## 🚀 Quick Start

### Installation

```bash
# Clone and setup
git clone <repository-url>
cd AMS-DB

# Create and activate UV environment
uv venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
uv pip install -e .
```

### Basic Usage

```python
from src.ams_db.core.polars_db import PolarsDBHandler
from src.ams_db.core.graphiti_pipe import GraphitiRAGFramework
from src.ams_db.core.conversation_generator import ConversationGenerator

# Initialize components
db = PolarsDBHandler()
graphiti = GraphitiRAGFramework(db)
generator = ConversationGenerator(db, graphiti)

# Generate multi-agent conversation
conversation = generator.generate_conversation(
    agents=["wizard_agent_001", "expert_coder_001"], 
    topic="AI Safety and Alignment",
    num_turns=8
)

# Export to JSONL for training
generator.export_conversation_jsonl(
    conversation_id=conversation["conversation_id"],
    output_path="training_data.jsonl"
)
```

## 🎭 Agent Personalities

### 🧙‍♂️ Wizard Agent
- **Personality**: Mystical, creative, uses magical metaphors
- **Strengths**: Creative problem-solving, pattern recognition, abstract thinking
- **Use Cases**: Brainstorming, creative coding, innovative approaches

### 🎮 Minecraft Assistant  
- **Personality**: Playful, gaming-focused, practical builder
- **Strengths**: Step-by-step tutorials, visual explanations, hands-on learning
- **Use Cases**: Education, tutorials, practical demonstrations

### 👨‍💻 Expert Coder
- **Personality**: Professional, technical, precise and direct
- **Strengths**: AI/ML systems, database optimization, agentic alignment
- **Use Cases**: Production code, technical architecture, performance optimization

## 📊 Database Architecture

### Core Tables
- **agent_matrix**: Agent configurations and metadata
- **conversation_history**: Multi-agent conversation logs  
- **knowledge_base**: Structured knowledge entries
- **research_collection**: Research results and findings
- **template_files**: Agent template configurations

### Agent Configuration Format
```json
{
  "agent_id": "expert_coder_001",
  "model_config": {
    "largeLanguageModel": {
      "names": ["llama3.1:70b", "qwen2.5:32b"],
      "instances": ["primary", "backup"],
      "model_config_template": {
        "temperature": 0.1,
        "max_tokens": 4096
      }
    }
  },
  "prompt_config": {
    "agent": {
      "llmSystem": "You are an expert software engineer...",
      "llmBooster": "When solving technical problems...",
      "visionSystem": "You are analyzing visual content...",
      "visionBooster": "When analyzing technical visuals..."
    },
    "primeDirective": "Primary Mission: Deliver exceptional..."
  },
  "command_flags": {
    "LLM_SYSTEM_PROMPT_FLAG": true,
    "EMBEDDING_FLAG": true,
    "AGENT_FLAG": true
  },
  "databases": {
    "agent_matrix": "expert_agents.parquet",
    "conversation_history": "expert_conversations.parquet"
  }
}
```

## 🔧 CLI Usage

### Agent Management
```bash
# Create new agent from template
ams-db agent create --template wizard --agent-id my_wizard_001

# List all agents
ams-db agent list

# Show agent details
ams-db agent show my_wizard_001

# Update agent configuration
ams-db agent update my_wizard_001 --config updated_config.json
```

### Conversation Generation
```bash
# Generate single conversation
ams-db conversation generate \
  --agents "wizard_agent_001,expert_coder_001" \
  --topic "Database Optimization" \
  --turns 10 \
  --output conversation.jsonl

# Generate training dataset
ams-db conversation dataset \
  --topics "AI Safety,Database Design,Multi-Agent Systems" \
  --agents "wizard_agent_001,minecraft_assistant_001,expert_coder_001" \
  --turns 8 \
  --output training_dataset.jsonl

# Export existing conversation
ams-db conversation export conv_123 output.jsonl --format jsonl --include-metadata

# List all conversations
ams-db conversation list
```

### Database Operations
```bash
# Show database statistics
ams-db db stats

# Create backup
ams-db db backup backup_20240101.parquet

# Initialize new database
ams-db db init
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/test_agent_config.py -v
pytest tests/test_polars_db.py -v
pytest tests/test_conversation_generator.py -v

# Run with coverage
pytest --cov=src tests/
```

## 📁 Project Structure

```
AMS-DB/
├── src/ams_db/
│   ├── core/
│   │   ├── base_agent_config.py      # Agent configuration management
│   │   ├── polars_db.py              # High-speed database handler
│   │   ├── graphiti_pipe.py          # RAG framework integration
│   │   └── conversation_generator.py  # Multi-agent conversation system
│   ├── cli/
│   │   └── main.py                   # Command-line interface
│   ├── api/
│   │   └── main.py                   # FastAPI REST interface
│   └── utils/
├── examples/
│   ├── wizard_agent.py               # Mystical agent template
│   ├── minecraft_assistant.py       # Gaming-focused agent template
│   ├── expert_coder_agent.py        # Technical expert template
│   └── basic_usage.py               # Usage examples
├── tests/                           # Comprehensive test suite
├── docs/                            # Documentation
└── comprehensive_demo.py            # Full feature demonstration
```

## 🔄 Multi-Agent Conversation Generation

### Generate Training Datasets
```python
# Generate conversations for training
topics = [
    "Machine Learning Architecture",
    "Database Performance Optimization", 
    "Multi-Agent Coordination",
    "AI Safety and Alignment"
]

agent_ids = ["wizard_agent_001", "minecraft_assistant_001", "expert_coder_001"]

dataset_path = generator.generate_training_dataset(
    topic_list=topics,
    agents=agent_ids,
    turns_per_conversation=8,
    output_path="multi_agent_training.jsonl"
)
```

### JSONL Export Format
```json
{"conversation_id": "conv_123", "turn_number": 0, "agent_id": "wizard_agent_001", "message": "🧙‍♂️ Ah, machine learning...", "timestamp": "2024-01-01T12:00:00", "metadata": {"agent_type": "wizard", "word_count": 45}}
{"conversation_id": "conv_123", "turn_number": 1, "agent_id": "expert_coder_001", "message": "From a technical perspective...", "timestamp": "2024-01-01T12:00:01", "metadata": {"agent_type": "expert_coder", "word_count": 52}}
```

## 🎯 Advanced Features

### Knowledge Base Integration
- Automatic knowledge retrieval during conversations
- Category-based knowledge organization
- Metadata-rich knowledge entries
- Cross-agent knowledge sharing

### Export Capabilities
- **CSV**: Tabular data analysis
- **Parquet**: High-performance columnar storage  
- **JSONL**: Machine learning training datasets
- **JSON**: Configuration and API integration

### Performance Optimizations
- Polars DataFrame backend for speed
- Lazy evaluation for large datasets
- Efficient memory management
- Scalable architecture design

## 🔗 Integration Examples

### With Ollama
```python
# Configure for Ollama integration
agent_config.update_config({
    "model_config": {
        "largeLanguageModel": {
            "names": ["llama3.1:70b"],
            "instances": ["ollama_primary"],
            "model_config_template": {
                "base_url": "http://localhost:11434",
                "api_key": None
            }
        }
    }
})
```

### With External RAG Systems  
```python
# Enhanced knowledge integration
knowledge_context = graphiti.search_knowledge(
    agent_id="expert_coder_001",
    query="transformer optimization",
    limit=5
)

# Use in conversation generation
conversation = generator.generate_conversation(
    agents=["expert_coder_001"],
    topic="Model Optimization",
    context={"external_knowledge": knowledge_context}
)
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built for advanced multi-agent AI workflows** 🚀
