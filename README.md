# AMS-DB: Agentic Multimodal Super-alignment Database

🧙‍♂️ *A comprehensive database foundation for multimodal agent projects with Graphiti knowledge graphs and Polars high-performance data management.*

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/ams-team/ams-db)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Overview

The AMS: Agentic Multimodal Super-alignment ecosystem uses AMS-DB as its core foundation for storage of knowledge bases and instancing databases for multimodal agent projects. Our custom agent context configuration system allows full control over agent prompt sets, attached models for multimodality, and knowledge bases for expertise in specific topics.

**Key Features:**
- 🤖 **Agent Configuration Management** - Complete control over agent prompts, modalities, and behaviors
- 🗄️ **High-Performance Database** - Polars-based data management for conversations, knowledge, and research
- 🧠 **Knowledge Graph Integration** - Graphiti-powered temporal knowledge graphs for contextual memory
- 📡 **REST API & CLI** - Multiple interfaces for integration and management
- 🔄 **Export/Import System** - Share agent configs, conversation histories, and knowledge bases
- 📝 **Predefined Templates** - Ready-to-use agent configurations for common use cases

## Quick Start

### Installation

1. **Create Virtual Environment**
```bash
uv venv -p 3.11 .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

2. **Install AMS-DB**
```bash
uv pip install -e ".[dev]"
```

3. **Initialize Database**
```bash
ams-db db init
```

### Basic Usage

**Command Line:**
```bash
# Create an agent
ams-db agent create my_agent --name "My Assistant" --description "A helpful AI assistant"

# List agents
ams-db agent list

# View statistics
ams-db db stats
```

**Python API:**
```python
from ams_db.core import AgentConfig, PolarsDBHandler

# Create and configure an agent
agent = AgentConfig("my_agent")
agent.set_prompt("llmSystem", "You are a helpful AI assistant.")
agent.set_modality_flag("STT_FLAG", True)  # Enable speech-to-text

# Initialize database and add agent
db = PolarsDBHandler("my_database")
agent_id = db.add_agent_config(
    agent.get_config(),
    agent_name="My Assistant"
)
```

## Architecture

```
AMS-DB Components:
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   AgentConfig       │    │   PolarsDBHandler   │    │ GraphitiRAGFramework│
│                     │    │                     │    │                     │
│ • Prompt Management │    │ • Conversation Data │    │ • Knowledge Graphs  │
│ • Modality Flags    │◄──►│ • Knowledge Base    │◄──►│ • Temporal Context  │
│ • Model Settings    │    │ • Research Results  │    │ • Graph Search      │
│ • Export/Import     │    │ • Agent Matrices    │    │ • Memory Persistence│
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
           │                           │                           │
           └─────────────┬─────────────┴─────────────┬─────────────┘
                         │                           │
               ┌─────────▼──────────┐      ┌─────────▼──────────┐
               │     CLI Tools      │      │     REST API       │
               │                    │      │                    │
               │ • Agent Management │      │ • Web Interface    │
               │ • DB Operations    │      │ • Integration      │
               │ • Knowledge Tools  │      │ • Remote Access    │
               └────────────────────┘      └────────────────────┘
```

## Agent Templates

AMS-DB includes predefined agent templates for common use cases:

### 🤖 **Default Agent**
Basic helpful assistant with standard capabilities.

### ⚡ **Speed Chat Agent**
Quick conversational assistant optimized for:
- Speech-to-text interaction
- Rapid response times
- LaTeX math support
- Conversational flow

### 🎮 **Minecraft Agent**
Gaming assistant specialized for:
- Real-time gameplay guidance
- Mob identification and threats
- Crafting and building advice
- Screenshot analysis

### 🧭 **Navigator Agent**
Vision and navigation assistant featuring:
- Image recognition capabilities
- Spatial understanding
- Multi-modal input processing
- Real-time guidance

## Core Components

### 1. Agent Configuration System
```python
agent = AgentConfig("coding_assistant")
agent.set_prompt("llmSystem", "You are a coding assistant.")
agent.set_modality_flag("LLAVA_FLAG", True)  # Enable vision
agent.save_to_json("my_config.json")
```

### 2. High-Performance Database
```python
db = PolarsDBHandler("agent_database")

# Manage conversations
db.add_conversation_message(agent_id, "user", "Hello!")
history = db.get_conversation_history(agent_id)

# Knowledge management
db.add_knowledge_document(agent_id, "Title", "Content")
results = db.search_knowledge_base(agent_id, "query")
```

### 3. Knowledge Graph Integration
```python
framework = GraphitiRAGFramework()
framework.load_agent(agent_id)

# Add contextual knowledge
await framework.add_knowledge_with_embedding("Title", "Content")

# Conversation with persistent memory
await framework.add_conversation_turn("User input", "Response")

# Context-aware search
results = await framework.search_knowledge_with_context("query")
```

## Advanced Features

### 📊 **Export/Import System**
- **JSONL Training Data**: Export conversations and prompts for machine learning
- **Multiple Formats**: JSON, Parquet, CSV support
- **Complete Backups**: Full agent configurations and data
- **Training Sets**: Formatted data for fine-tuning models

### 🎭 **Multi-Agent Conversation Generation**
- **Synthetic Conversations**: Generate training data between multiple agents
- **Persona Support**: AI, Human, and Wizardly conversation styles
- **Topic-Based Generation**: Conversations around specific topics
- **Configurable Parameters**: Adjustable turns and agent participation

### 🔄 **Training Data Pipeline**
- **Conversation Pairs**: User-assistant message pairs for fine-tuning
- **Prompt Examples**: System prompt training examples
- **Multi-Modal Data**: Vision and text conversation exports
- **Metadata Inclusion**: Session IDs, timestamps, and persona information

### 🌐 **Multi-Interface Support**
- Command Line Interface (CLI)
- REST API with FastAPI
- Direct Python API
- Configuration management

### 🧠 **Intelligent Memory**
- Temporal knowledge graphs
- Context-aware retrieval
- Relationship understanding
- Memory persistence

## Examples

Explore comprehensive examples in the `examples/` directory:

```bash
# Basic usage demonstration
python examples/basic_usage.py

# Advanced Minecraft assistant
python examples/minecraft_assistant.py
```

## REST API

Start the API server:
```bash
python -m ams_db.api.main
```

Access the interactive docs at: `http://localhost:8000/docs`

Key endpoints:
- `POST /agents/` - Create agents
- `GET /agents/{id}/conversations/` - Manage conversations
- `POST /agents/{id}/knowledge/` - Add knowledge
- `GET /system/stats/` - System statistics

## Development

### Project Structure
```
AMS-DB/
├── src/ams_db/           # Source code
│   ├── core/             # Core components
│   ├── config/           # Configuration management
│   ├── cli/              # Command line interface
│   ├── api/              # REST API
│   └── utils/            # Utilities
├── tests/                # Test suites
├── examples/             # Usage examples
├── docs/                 # Documentation
└── pyproject.toml        # Project configuration
```

### Testing
```bash
# Run component tests
python tests/test_components.py

# Run full test suite
pytest tests/
```

### Configuration

Set environment variables for full functionality:
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

## Contributing

We welcome contributions! Please:
1. Follow the existing code structure
2. Add appropriate tests
3. Update documentation
4. Ensure backwards compatibility

## License

MIT License - see [LICENSE](LICENSE) for details.

## Documentation

- **[Usage Guide](USAGE.md)** - Comprehensive usage documentation
- **[API Documentation](docs/)** - Detailed API reference
- **[Examples](examples/)** - Practical usage examples
- **[Graphiti Docs](docs/graphiti_docs/)** - Knowledge graph integration
- **[Polars Docs](docs/polars_docs/)** - High-performance data management

---

**AMS-DB: Building the foundation for intelligent multimodal agents** 🧙‍♂️✨