# AMS-DB: Agentic Multimodal Super-alignment Database

🧙‍♂️ *A comprehensive database foundation for multimodal agent projects with Graphiti knowledge graphs and Polars high-performance data management.*

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/Agentic-Multimodal-Superalignment/AMS-DB)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Wizardry](https://img.shields.io/badge/wizardry-✨magical✨-purple.svg)](docs/ULTIMATE_CHEATSHEET.md)

## 🎯 Overview

AMS-DB is the core foundation for the Agentic Multimodal Super-alignment ecosystem, providing storage for knowledge bases and instancing databases for multimodal agent projects. Our custom agent configuration system gives you complete control over agent prompts, modalities, and knowledge bases.

### ✨ **Quick Start Guide**
🧙‍♂️ **[📜 ULTIMATE CHEATSHEET](docs/ULTIMATE_CHEATSHEET.md)** - Everything you need in one magical scroll!

**Key Features:**
- 🤖 **Agent Configuration Management** - Complete control over agent prompts, modalities, and behaviors
- 💬 **Multiple Conversation Modes** - Human-to-agent, agent-to-agent, and roleplay modes
- 🗄️ **High-Performance Database** - Polars-based data management with organized file structure
- 🧠 **Knowledge Graph Integration** - Graphiti-powered temporal knowledge graphs for contextual memory
- 📡 **REST API & CLI** - Multiple interfaces for integration and management
- 🔄 **Export/Import System** - Share agent configs, conversation histories, and knowledge bases
- 📝 **Predefined Templates** - Ready-to-use agent configurations for common use cases
- 🎭 **Three Personality Archetypes** - Wizard, Minecraft Assistant, and Expert Coder templates
- 📁 **Organized Data Structure** - Clean separation of agents, conversations, exports, and backups

## 🚀 Quick Start

### ⚡ System Status: **FULLY OPERATIONAL** ✅
**Latest Validation:** July 17, 2025 - All components tested and working  
**[View Complete Status Report](docs/SYSTEM_STATUS.md)**

### Installation & Setup
```bash
# 1. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 2. Install AMS-DB
pip install -e .

# 3. Test the system
python tests/test_final_validation.py
```

### Start Chatting Immediately
```bash
# 🧙‍♂️ Chat with the wizard
python -m ams_db.cli.main chat start wizard_agent_001
python -m ams_db.cli.main chat send wiz1 "Tell me about your magical powers!"

# 🎮 Chat with Minecraft assistant  
python -m ams_db.cli.main chat start minecraft_assistant_001
python -m ams_db.cli.main chat send mc1 "How do I build a castle?"

# 👨‍💻 Get coding help from expert
python -m ams_db.cli.main chat start expert_coder_001  
python -m ams_db.cli.main chat send code1 "Best practices for Python error handling?"
```

### 📚 Essential Documentation
- ⚡ **[ULTIMATE CHEATSHEET](docs/ULTIMATE_CHEATSHEET.md)** - 🌟 Your magical quick reference
- 🎯 **[WORKING CLI COMMANDS](docs/WORKING_CLI_COMMANDS.md)** - Tested & ready commands
- 📖 **[QUICK START GUIDE](docs/QUICK_START.md)** - Get running in 5 minutes
- 🎓 **[BEGINNER'S GUIDE](docs/BEGINNER_GUIDE.md)** - Complete learning path
- 👨‍🏫 **[HANDS-ON TUTORIAL](docs/TUTORIAL.md)** - Step-by-step mastery guide

## 🎭 Agent Templates

AMS-DB includes **three legendary agent archetypes** for immediate use:

### 🧙‍♂️ **Wizard Agent** - The Mystical Coder
*"Greetings, seeker! I dwell in ethereal realms where data flows like enchanted rivers..."*
- ✨ **Perfect for**: Creative problem solving, brainstorming, magical metaphors
- 💫 **Personality**: Mystical, wise, uses magical language and metaphors

### 🎮 **Minecraft Assistant** - The Playful Crafter  
*"Hey there, fellow crafter! Ready to build amazing things in the blocky world?"*
- ⛏️ **Perfect for**: Step-by-step tutorials, visual learning, gamification
- 🧱 **Personality**: Friendly, enthusiastic, practical tutorial style

### 👨‍💻 **Expert Coder** - The Technical Master
*"Expert software engineer providing precise, production-ready solutions..."*
- 🚀 **Perfect for**: Production code, system architecture, performance optimization
- ⚙️ **Personality**: Professional, direct, technically precise

### 🤖 **Create Your Own!**
```python
# 🎭 Forge your own magical personality
custom_agent = AgentConfig("my_unique_agent")
custom_agent.set_prompt("llmSystem", "Your unique personality here...")
custom_agent.set_prompt("primeDirective", "Your core mission...")
```

## ⚡ Core Components

### 1. Agent Configuration System
```python
from ams_db.core import AgentConfig

agent = AgentConfig("coding_assistant")
agent.set_prompt("llmSystem", "You are a coding assistant.")
agent.set_modality_flag("LLAVA_FLAG", True)  # Enable vision
agent.save_to_json("my_config.json")
```

### 2. High-Performance Database
```python
from ams_db.core import PolarsDBHandler

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
from ams_db.core import GraphitiRAGFramework

framework = GraphitiRAGFramework()
await framework.load_agent(agent_id)

# Add contextual knowledge
await framework.add_knowledge_with_embedding("Title", "Content")

# Context-aware search
results = await framework.search_knowledge_with_context("query")
```

## 🏗️ Architecture

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

## � Examples & Demos

Explore magical examples in the project directories:

```bash
# 🌱 Basic wizardry demonstration  
python examples/basic_usage.py

# 🎮 Advanced Minecraft assistant magic
python examples/minecraft_assistant.py

# 👨‍💻 Expert coder agent creation
python examples/expert_coder_agent.py

# 🎭 Full system demonstration (MUST TRY!)
python dev/simple_demo_safe.py
```

## 🌐 REST API

Start the API server:
```bash
python -m ams_db.api.main
# ✨ Access interactive docs at: http://localhost:8000/docs
```

**Key Endpoints:**
- `POST /agents/` - 🤖 Create agents
- `GET /agents/{id}/conversations/` - 💬 Manage conversations  
- `POST /agents/{id}/knowledge/` - 📚 Add knowledge
- `GET /system/stats/` - 📊 System statistics

## 🛠️ Development

### Project Structure
```
AMS-DB/
├── src/ams_db/           # 🧙‍♂️ Core source code
│   ├── core/             # Core components
│   ├── config/           # Configuration management
│   ├── cli/              # Command line interface
│   ├── api/              # REST API
│   └── utils/            # Utilities
├── tests/                # 🧪 Test suites
├── examples/             # 📚 Usage examples
├── dev/                  # 🎪 Demo files and development tools
├── docs/                 # 📖 Documentation
├── data/                 # 🗄️ Data storage and templates
└── pyproject.toml        # Project configuration
```

### Running Tests
```bash
# Quick validation
python tests/test_final_validation.py

# Component tests
python tests/test_components.py

# Run all tests
pytest tests/
```

## 🤝 Contributing

### Development Setup
```bash
# Clone the magical realm
git clone https://github.com/Agentic-Multimodal-Superalignment/AMS-DB.git
cd AMS-DB

# Set up environment
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e .

# Test your powers
python dev/simple_demo_safe.py
```

### Contributing Guidelines
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Write tests** for your changes
4. **Update documentation** accordingly
5. **Submit a pull request**

## 📖 Documentation

**Essential Guides:**
- 📜 **[ULTIMATE CHEATSHEET](docs/ULTIMATE_CHEATSHEET.md)** - Complete quick reference
- 🎓 **[BEGINNER'S GUIDE](docs/BEGINNER_GUIDE.md)** - Learning path from zero to hero
- 👨‍🏫 **[HANDS-ON TUTORIAL](docs/TUTORIAL.md)** - Step-by-step practical guide
- 🏗️ **[ARCHITECTURE](docs/ARCHITECTURE.md)** - System internals and design
- 🛠️ **[USAGE GUIDE](docs/USAGE.md)** - Practical examples and API reference

## ⚡ Quick Magic Reference

```bash
# 🧙‍♂️ Setup Enchantment
python -m venv .venv && .venv\Scripts\activate && pip install -e .

# 🎭 Instant Demo Magic  
python dev/simple_demo_safe.py

# 🔮 Essential CLI Spells
python -m ams_db.cli.main agent list              # 📋 List all agents
python -m ams_db.cli.main chat start wizard_agent_001  # 🤖 Start chatting
python -m ams_db.cli.main db stats               # 📊 Show statistics
```

## Configuration

Set environment variables for full functionality:
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**🧙‍♂️ AMS-DB: Building the foundation for intelligent multimodal agents** ✨

*May your code be ever magical and your agents forever wise!* 🪄