# AMS-DB: Agentic Multimodal Super-alignment Database

🧙‍♂️ *A comprehensive database foundation for multimodal agent projects with Graphiti knowledge graphs and Polars high-performance data management.*

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/ams-team/ams-db)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Wizardry](https://img.shields.io/badge/wizardry-✨magical✨-purple.svg)](docs/ULTIMATE_CHEATSHEET.md)

## 🎯 Overview

The AMS: Agentic Multimodal Super-alignment ecosystem uses AMS-DB as its core foundation for storage of knowledge bases and instancing databases for multimodal agent projects. Our custom agent context configuration system allows full control over agent prompt sets, attached models for multimodality, and knowledge bases for expertise in specific topics.

### ✨ **NEW!** Ultimate Wizardry Cheatsheet 
🧙‍♂️ **[📜 VIEW THE ULTIMATE CHEATSHEET](docs/ULTIMATE_CHEATSHEET.md)** - Your complete magical guide to mastering AMS-DB!

**Perfect for Owen and all new contributors** - Everything you need in one mystical scroll! ⚡

**Key Features:**
- 🤖 **Agent Configuration Management** - Complete control over agent prompts, modalities, and behaviors
- � **Multiple Conversation Modes** - Human-to-agent, agent-to-agent, and roleplay modes
- �🗄️ **High-Performance Database** - Polars-based data management with organized file structure
- 🧠 **Knowledge Graph Integration** - Graphiti-powered temporal knowledge graphs for contextual memory
- 📡 **REST API & CLI** - Multiple interfaces for integration and management
- 🔄 **Export/Import System** - Share agent configs, conversation histories, and knowledge bases
- 📝 **Predefined Templates** - Ready-to-use agent configurations for common use cases
- 🎭 **Three Personality Archetypes** - Wizard, Minecraft Assistant, and Expert Coder templates
- 📁 **Organized Data Structure** - Clean separation of agents, conversations, exports, and backups

## 🚀 Quick Start

### ⚡ **[ULTIMATE CHEATSHEET](docs/ULTIMATE_CHEATSHEET.md)** - Skip to the magic! 🧙‍♂️✨
### 📖 **[QUICK START GUIDE](docs/QUICK_START.md)** - Get running in 5 minutes!

### Installation

1. **Create Virtual Environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

2. **Install AMS-DB**
```bash
pip install -e .
```

3. **Initialize Database & Test Magic**
```bash
ams-db db init
python simple_demo_safe.py  # 🎭 See the magic in action!
```

### 🎪 Instant Demo Magic
```bash
# 🧙‍♂️ One command to see everything working
python simple_demo_safe.py
```

This creates 3 magical agents (Wizard 🧙‍♂️, Minecraft Assistant 🎮, Expert Coder 👨‍💻), populates knowledge, generates conversations, and shows exports!

### Basic Usage

**🎭 Three Legendary Agent Personalities:**
- 🧙‍♂️ **Wizard Agent** - Mystical, creative, uses magical metaphors  
- 🎮 **Minecraft Assistant** - Playful, practical, gaming-focused tutorials
- 👨‍💻 **Expert Coder** - Professional, technical, production-ready solutions

**Command Line Magic:**
```bash
# 📋 List all magical agents
ams-db agent list

# 🤖 Create your own agent minion
ams-db agent create my_wizard --name "My Code Wizard" --description "Personal coding assistant"

# 📊 Divine database secrets
ams-db db stats

# 📤 Export mystical training data
ams-db export conversations --format jsonl
```

**Python Sorcery:**
```python
from ams_db.core import AgentConfig, PolarsDBHandler

# 🧙‍♂️ Create a magical agent
agent = AgentConfig("my_wizard")
agent.set_prompt("llmSystem", "🧙‍♂️ I am your coding wizard!")
agent.set_prompt("primeDirective", "Transform problems into magical solutions!")
agent.set_modality_flag("STT_FLAG", True)  # Enable speech magic

# 🔮 Initialize the crystal database
db = PolarsDBHandler("my_magical_database")
agent_id = db.add_agent_config(
    agent.to_dict(),
    agent_name="My Personal Wizard",
    description="🧙‍♂️ Magical coding assistant"
)

# 💬 Start a magical conversation
db.add_conversation_message(agent_id, "user", "How do I cast a Python spell?", "session_001")
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

AMS-DB includes **three legendary agent archetypes** for common use cases:

### �‍♂️ **Wizard Agent** - The Mystical Coder
*"Greetings, seeker! I dwell in ethereal realms where data flows like enchanted rivers..."*
- ✨ **Perfect for**: Creative problem solving, brainstorming, magical metaphors
- 🎯 **Use cases**: Art projects, creative writing, innovative algorithms
- 💫 **Personality**: Mystical, wise, uses magical language and metaphors

### 🎮 **Minecraft Assistant** - The Playful Crafter  
*"Hey there, fellow crafter! Ready to build amazing things in the blocky world?"*
- ⛏️ **Perfect for**: Step-by-step tutorials, visual learning, gamification
- 🎯 **Use cases**: Educational content, gaming guides, hands-on demonstrations
- 🧱 **Personality**: Friendly, enthusiastic, practical tutorial style

### 👨‍💻 **Expert Coder** - The Technical Master
*"Expert software engineer providing precise, production-ready solutions..."*
- 🚀 **Perfect for**: Production code, system architecture, performance optimization
- 🎯 **Use cases**: Software development, code reviews, technical documentation  
- ⚙️ **Personality**: Professional, direct, technically precise

### 🤖 **Create Your Own!**
```python
# 🎭 Forge your own magical personality
custom_agent = AgentConfig("my_unique_agent")
custom_agent.set_prompt("llmSystem", "Your unique personality here...")
custom_agent.set_prompt("primeDirective", "Your core mission...")
```

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

## 📚 Documentation

🧙‍♂️ **Start here:** **[📜 ULTIMATE CHEATSHEET](docs/ULTIMATE_CHEATSHEET.md)** - Everything you need in one magical scroll!

**For Owen and new contributors:**
- 🎓 **[Beginner's Guide](docs/BEGINNER_GUIDE.md)** - Complete learning path from zero to hero
- 🎯 **[Hands-On Tutorial](docs/TUTORIAL.md)** - Step-by-step practical examples  
- 🏗️ **[Architecture Deep Dive](docs/ARCHITECTURE.md)** - System internals and extension points
- �️ **[Usage Guide](USAGE.md)** - Practical examples and API reference

**Examples & Templates:**
- 🎪 `simple_demo_safe.py` - Full system demonstration
- 🎭 `*_template.json` - Ready-to-use agent personalities
- 📁 `examples/` - Practical code examples and patterns

## 🤝 Contributing

**Welcome to the team, Owen!** 🎉

We've built extensive onboarding documentation specifically for new contributors:

1. **Start with the [Ultimate Cheatsheet](docs/ULTIMATE_CHEATSHEET.md)** 🧙‍♂️
2. **Follow the [Beginner's Guide](docs/BEGINNER_GUIDE.md)** 🎓  
3. **Try the [Hands-On Tutorial](docs/TUTORIAL.md)** 🎯
4. **Explore the examples and create your own agents!** 🚀

### Development Setup
```bash
# Clone and enter the magical realm
git clone https://github.com/Agentic-Multimodal-Superalignment/AMS-DB.git
cd AMS-DB

# Set up your wizard environment
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e .

# Test your magical powers
python simple_demo_safe.py
ams-db agent list
```

### Making Contributions
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Write tests** for your changes
4. **Update documentation** to help others understand your magic
5. **Submit a pull request** and share your improvements!

## 🎭 Agent Templates

The system includes **three legendary archetypes** perfect for learning:

| Archetype | Personality | Best For | Example Use |
|---|---|---|---|
| 🧙‍♂️ **Wizard** | Mystical, creative, metaphorical | Brainstorming, creative solutions | *"Cast powerful spells of code..."* |
| 🎮 **Minecraft** | Friendly, tutorial-focused, practical | Step-by-step guides, visual learning | *"Hey fellow crafter, let's build!"* |  
| 👨‍💻 **Expert** | Professional, technical, precise | Production code, architecture | *"Scalable, maintainable solutions..."* |

**Create your own unique personality** by combining different traits and prompts!
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

🎪 **Explore magical examples in the `examples/` directory:**

```bash
# 🌱 Basic wizardry demonstration  
python examples/basic_usage.py

# 🎮 Advanced Minecraft assistant magic
python examples/minecraft_assistant.py

# 👨‍💻 Expert coder agent creation
python examples/expert_coder_agent.py

# 🎭 Full system demonstration (MUST TRY!)
python simple_demo_safe.py
```

## 📚 Documentation Grimoire

🧙‍♂️ **Essential Scrolls of Wisdom:**
- 📜 **[Ultimate Cheatsheet](docs/ULTIMATE_CHEATSHEET.md)** - 🌟 Your magical quick reference
- 🎓 **[Beginner's Guide](docs/BEGINNER_GUIDE.md)** - Complete learning path for newcomers
- 👨‍🏫 **[Hands-On Tutorial](docs/TUTORIAL.md)** - Step-by-step mastery guide  
- 🏗️ **[Architecture Deep Dive](docs/ARCHITECTURE.md)** - System internals and design
- 🛠️ **[Usage Guide](USAGE.md)** - Practical examples and patterns

## 🌐 REST API Magic

Start the mystical API server:
```bash
python -m ams_db.api.main
# ✨ Access the interactive spellbook at: http://localhost:8000/docs
```

**Key Enchantments:**
- `POST /agents/` - 🤖 Create magical agents
- `GET /agents/{id}/conversations/` - 💬 Manage conversations  
- `POST /agents/{id}/knowledge/` - 📚 Add knowledge scrolls
- `GET /system/stats/` - 📊 Divine system statistics

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

## ⚡ **QUICK MAGIC REFERENCE** 

```bash
# 🧙‍♂️ Setup Enchantment
uv venv -p 3.11 .venv && .venv\Scripts\activate && uv pip install -e .

# 🎭 Instant Demo Magic  
python simple_demo_safe.py

# 🔮 Essential CLI Spells
ams-db agent list              # 📋 List all agents
ams-db agent create my_wizard  # 🤖 Create new agent
ams-db db stats               # 📊 Show statistics

# 📜 Master the Ultimate Cheatsheet
📖 docs/ULTIMATE_CHEATSHEET.md
```

**🧙‍♂️ AMS-DB: Building the foundation for intelligent multimodal agents** ✨

*May your code be ever magical and your agents forever wise!* 🪄