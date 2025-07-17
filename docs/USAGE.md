# AMS-DB Usage Guide 🧙‍♂️✨

Welcome to AMS-DB - the Agentic Multimodal Super-alignment Database! This guide will help you get started with building and managing multimodal AI agents with magical ease.

## 🎯 **NEW!** Ultimate Magic Reference

🪄 **[📜 ULTIMATE CHEATSHEET](docs/ULTIMATE_CHEATSHEET.md)** - Everything you need in one mystical scroll!

🎭 **Instant Demo:** `python simple_demo_safe.py` - See everything working in seconds!

**Perfect for Owen and new contributors!** Start with the cheatsheet for quick mastery! ⚡

## Quick Start

### Installation

1. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

2. Install AMS-DB:
```bash
pip install -e .
```

### Basic Usage

#### Command Line Interface

Initialize the database:
```bash
ams-db db init
```

Create an agent:
```bash
ams-db agent create my_agent --name "My Assistant" --description "A helpful AI assistant"
```

List agents:
```bash
ams-db agent list
```

View database statistics:
```bash
ams-db db stats
```

#### Python API Magic 🔮

```python
from ams_db.core import AgentConfig, PolarsDBHandler

# 🧙‍♂️ Create a magical agent
agent = AgentConfig("my_wizard")
agent.set_prompt("llmSystem", "🧙‍♂️ I am your coding wizard!")
agent.set_modality_flag("STT_FLAG", True)  # Enable speech magic

# 💾 Initialize crystal database
db = PolarsDBHandler("my_database")

# 🌟 Add agent to the mystical realm
agent_id = db.add_agent_config(
    agent.to_dict(),
    agent_name="My Wizard Assistant",
    description="🧙‍♂️ A magical coding assistant"
)

print(f"✨ Created magical agent: {agent_id}")
```

### 🎭 **Three Legendary Personalities**
- **🧙‍♂️ Wizard Agent** - Creative, mystical problem solving  
- **🎮 Minecraft Assistant** - Playful, practical tutorials  
- **👨‍💻 Expert Coder** - Professional, technical precision

## Core Components ⚡

### 1. 🤖 AgentConfig - The Personality Forge
Manages agent configurations with prompts, modality flags, and mystical settings.

```python
from ams_db.core import AgentConfig

# 🎭 Create a magical agent vessel
agent = AgentConfig("coding_wizard")

# ✨ Set personality enchantments
agent.set_prompt("llmSystem", "🧙‍♂️ You are a coding wizard!")
agent.set_prompt("llmBooster", "Cast spells of perfect code solutions.")
agent.set_prompt("primeDirective", "Transform coding problems into magical solutions!")

# ⚙️ Configure magical abilities
agent.set_modality_flag("STT_FLAG", True)    # 🎤 Speech-to-text magic
agent.set_modality_flag("LATEX_FLAG", True)  # 📐 LaTeX spell support
agent.set_modality_flag("LLAVA_FLAG", True)  # 👁️ Vision enchantments

# 💾 Save/load magical configuration
agent.to_json("my_wizard.json")
new_agent = AgentConfig()
new_agent.from_json("my_wizard.json")
```

### 2. PolarsDBHandler
High-performance database management using Polars.

```python
from ams_db.core import PolarsDBHandler

# Initialize database
db = PolarsDBHandler("agent_database")

# Agent management
agent_id = db.add_agent_config(config, "Agent Name", "Description")
config = db.get_agent_config(agent_id)
agents = db.list_agents()

# Conversation management
msg_id = db.add_conversation_message(
    agent_id, "user", "Hello!", session_id="session_1"
)
history = db.get_conversation_history(agent_id, "session_1")

# Knowledge base
kb_id = db.add_knowledge_document(
    agent_id, "Title", "Content", tags=["important"]
)
results = db.search_knowledge_base(agent_id, "search query")

# Research collection
research_id = db.add_research_result(
    agent_id, "research query", {"findings": "data"}
)
```

### 3. GraphitiRAGFramework
Advanced RAG with knowledge graphs (requires Neo4j).

```python
import asyncio
from ams_db.core import GraphitiRAGFramework

async def example():
    # Initialize framework
    framework = GraphitiRAGFramework(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )
    
    # Create agent with Graphiti integration
    agent_id = framework.create_agent(config, "Agent Name")
    framework.load_agent(agent_id)
    
    # Add knowledge with embedding
    kb_id = await framework.add_knowledge_with_embedding(
        "Document Title",
        "Document content...",
        tags=["important"]
    )
    
    # Conversation with context
    await framework.add_conversation_turn(
        "User input",
        "Assistant response"
    )
    
    # Search with graph context
    results = await framework.search_knowledge_with_context(
        "search query",
        include_graph_context=True
    )

asyncio.run(example())
```

## Agent Templates

AMS-DB includes predefined agent templates:

### Available Templates

1. **Default Agent** - Basic helpful assistant
2. **Speed Chat Agent** - Quick conversational assistant with speech support
3. **Minecraft Agent** - Gaming assistant specialized for Minecraft
4. **Navigator Agent** - Vision and navigation assistant

### Using Templates

```python
from ams_db.config import get_template_manager

template_manager = get_template_manager()

# List available templates
templates = template_manager.list_templates()
print(templates)

# Create agent from template
agent = template_manager.create_agent_from_template(
    "speed_chat", 
    agent_id="my_speed_chat_bot"
)

# Save the configured agent
agent.to_json("speed_chat_config.json")
```

## Configuration Management

### System Configuration

```python
from ams_db.config import get_config, ConfigManager

# Get current configuration
config = get_config()
print(f"Database path: {config.database.db_path}")
print(f"LLM model: {config.llm.llm_model}")

# Update configuration
config_manager = ConfigManager()
config_manager.update_config(
    llm={"temperature": 0.8, "max_tokens": 2048},
    database={"db_path": "/custom/path"}
)
```

### Environment Variables

Set these environment variables for Graphiti integration:

```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
OLLAMA_BASE_URL=http://localhost:11434/v1
```

## Examples

Run the included examples:

### Basic Usage
```bash
python examples/basic_usage.py
```

### Minecraft Assistant
```bash
python examples/minecraft_assistant.py
```

## Testing

Run the test suite:

```bash
# Run component tests
python tests/test_components.py

# Run with pytest (when available)
pytest tests/
```

## REST API

Start the REST API server:

```python
from ams_db.api import run_server

run_server(host="127.0.0.1", port=8000)
```

Or via command line:
```bash
python -m ams_db.api.main
```

### API Endpoints

- `GET /` - API information
- `POST /agents/` - Create agent
- `GET /agents/` - List agents
- `GET /agents/{agent_id}` - Get agent
- `POST /agents/{agent_id}/conversations/` - Add conversation
- `POST /agents/{agent_id}/knowledge/` - Add knowledge
- `GET /system/stats/` - System statistics

## Architecture

```
AMS-DB/
├── src/ams_db/
│   ├── core/              # Core components
│   │   ├── base_agent_config.py
│   │   ├── polars_db.py
│   │   └── graphiti_pipe.py
│   ├── config/            # Configuration management
│   ├── cli/               # Command line interface
│   ├── api/               # REST API
│   └── utils/             # Utilities
├── tests/                 # Test suites
├── examples/              # Usage examples
└── docs/                  # Documentation
```

## Advanced Features

### Conversation Context
Maintain conversation context across turns with automatic persistence to both Polars database and Graphiti knowledge graph.

### Knowledge Graph Integration
Leverage Graphiti for temporal knowledge graphs that understand relationships and context evolution over time.

### Multi-Agent Support
Manage multiple agents with different configurations, each with their own conversation histories and knowledge bases.

### Export/Import
Export complete agent configurations and data for sharing or backup:

```python
# Export agent data
framework.export_agent_data("backup_folder/")

# Export database backup
db.export_database_backup("backup_folder/")
```

## JSONL Export for Training

AMS-DB supports exporting data in JSONL format for machine learning training:

### Export Conversations for Fine-Tuning

```python
from ams_db.core import PolarsDBHandler

db = PolarsDBHandler()

# Export conversations for a specific agent
success = db.export_conversations_jsonl(
    agent_id="coding_assistant",
    output_path="training_conversations.jsonl"
)

# Each line contains a conversation pair:
# {"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}], ...}
```

### Export Prompt Sets

```python
# Export all agent prompt sets as training examples
success = db.export_prompt_sets_jsonl("prompt_training.jsonl")

# Creates examples from system prompts, boosters, and vision prompts
```

### CLI Export Commands

```bash
# Export conversations
ams-db export conversations-jsonl coding_assistant training_data.jsonl

# Export prompt sets
ams-db export prompts-jsonl prompt_examples.jsonl
```

## Multi-Agent Conversation Generation

Generate synthetic conversations between multiple agents with different personas:

### Python API

```python
# Generate conversation between agents
session_id = db.generate_multi_agent_conversation(
    agent_ids=["minecraft_agent", "speed_chat", "navigator"],
    topic="minecraft building strategies",
    turns=15,
    personas=["AI", "human", "wizardly"]  # Optional persona types
)

print(f"Generated conversation session: {session_id}")
```

### Available Personas

- **AI**: Analytical, data-driven responses
- **Human**: Casual, questioning, learning-oriented
- **Wizardly**: Mystical, ancient wisdom style

### CLI Generation

```bash
# Generate multi-agent conversation
ams-db generate conversation minecraft_agent speed_chat navigator "minecraft survival tips" \
  --turns 20 --personas "AI,human,wizardly"
```

### REST API

```bash
curl -X POST "http://localhost:8000/generate/conversation" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_ids": ["minecraft_agent", "speed_chat"],
    "topic": "crafting strategies",
    "turns": 10,
    "personas": ["AI", "human"]
  }'
```

## Troubleshooting

### Common Issues

1. **Graphiti Connection Errors**
   - Ensure Neo4j is running
   - Check connection parameters
   - Verify Neo4j version compatibility

2. **Import Errors**
   - Ensure virtual environment is activated
   - Reinstall package: `uv pip install -e ".[dev]"`

3. **Performance Issues**
   - Monitor database size
   - Use appropriate query limits
   - Consider data archival for large datasets

### Support

For issues and questions:
1. Check the examples in `examples/`
2. Review test cases in `tests/`
3. Check the documentation in `docs/`

## Contributing

AMS-DB is designed to be extensible. To contribute:

1. Follow the existing code structure
2. Add appropriate tests
3. Update documentation
4. Ensure backwards compatibility

Happy building with AMS-DB! 🧙‍♂️✨

# Development and Build Process

This section documents the terminal usage and development process used to build AMS-DB.

## Environment Setup

### 1. UV Virtual Environment

```bash
# Create and activate UV virtual environment
uv venv ams-db-env
# Windows
ams-db-env\Scripts\activate
# Linux/Mac
source ams-db-env/bin/activate

# Install package in development mode
uv pip install -e .
```

### 2. Development Dependencies

```bash
# Install development dependencies
uv pip install pytest black flake8 mypy

# Install optional dependencies for full functionality
uv pip install graphiti-ai  # For knowledge graph features
```

## Build and Test Process

### 1. Core Component Testing

```bash
# Run individual component tests
python tests/test_components.py

# Run full test suite
pytest tests/ -v

# Test specific components
pytest tests/test_agent_config.py -v
pytest tests/test_polars_db.py -v
```

### 2. CLI Testing

```bash
# Initialize database
ams-db db init

# Create test agents
ams-db agent create test_agent --name "Test Agent" --description "Testing agent"

# List agents
ams-db agent list

# Database statistics
ams-db db stats

# Export functionality
ams-db export conversations-jsonl test_agent conversations.jsonl
ams-db export prompts-jsonl prompts.jsonl

# Generate test conversation
ams-db generate conversation test_agent default_agent "testing strategies" --turns 5
```

### 3. API Testing

```bash
# Start development server
uvicorn ams_db.api.main:app --reload --port 8000

# Test endpoints
curl http://localhost:8000/agents/
curl -X POST http://localhost:8000/agents/ -H "Content-Type: application/json" -d '{"agent_id": "api_test", "agent_name": "API Test"}'
```

### 4. Integration Testing

```bash
# Run comprehensive demo
python demo.py

# Test example scripts
python examples/basic_usage.py
python examples/minecraft_assistant.py
```

## Code Quality and Standards

### 1. Code Formatting

```bash
# Format code with Black
black src/ams_db/ tests/ examples/

# Check with flake8
flake8 src/ams_db/ --max-line-length=100

# Type checking with mypy
mypy src/ams_db/
```

### 2. Documentation Updates

```bash
# Update documentation after changes
# 1. Update USAGE.md with new features
# 2. Update README.md with overview changes
# 3. Update docstrings in code
# 4. Test all examples in documentation
```

## Packaging for Distribution

### 1. Build Package

```bash
# Build wheel and source distribution
python -m build

# Check package
twine check dist/*
```

### 2. Version Management

```bash
# Update version in pyproject.toml
# Tag release
git tag v0.1.0
git push origin v0.1.0
```

### 3. Installation Testing

```bash
# Test installation from wheel
pip install dist/ams_db-*.whl

# Test clean installation
pip install ams-db

# Verify installation
ams-db --version
python -c "from ams_db.core import AgentConfig; print('Import successful')"
```

## Debugging Common Issues

### 1. Import Errors

```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall in development mode
pip uninstall ams-db
pip install -e .
```

### 2. Database Issues

```bash
# Reset database
rm -rf ams_database/
ams-db db init

# Check database integrity
ams-db db stats
```

### 3. Dependency Conflicts

```bash
# Check dependencies
pip list | grep -E "(polars|graphiti|fastapi)"

# Clean install
pip uninstall ams-db
pip install --force-reinstall ams-db
```

---

## 🧙‍♂️ **MAGICAL QUICK REFERENCE**

```bash
# ⚡ Essential Spells
python simple_demo_safe.py           # 🎭 See all magic in action
ams-db agent list                    # 📋 List magical agents  
ams-db agent create my_wizard        # 🤖 Create new agent
ams-db db stats                      # 📊 Divine statistics
```

### 🎯 **Power User Enchantments**
- 📜 **[Ultimate Cheatsheet](docs/ULTIMATE_CHEATSHEET.md)** - Complete magical reference
- 🎓 **[Beginner's Guide](docs/BEGINNER_GUIDE.md)** - Learn from the beginning  
- 👨‍🏫 **[Tutorial](docs/TUTORIAL.md)** - Step-by-step mastery
- 🏗️ **[Architecture](docs/ARCHITECTURE.md)** - Deep system knowledge

**🧙‍♂️ May your agents be ever wise and your code forever magical!** ✨🪄
