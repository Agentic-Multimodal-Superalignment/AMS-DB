📜 **THE ULTIMATE AMS-DB WIZARDRY CHEATSHEET** ⚡
*Cast spells with code, weave agents like ancient incantations* 🧙‍♂️✨

**Updated by the Great Merlin for Owen and all future apprentices!**
*Now with ORGANIZED FILE STRUCTURE and MULTIPLE CONVERSATION MODES!* 🎉

---

## 🌟 **QUICK MAGIC SPELLS** (Essential Commands)

### ⚡ **Environment Enchantments** 
```bash
# 🧙‍♂️ Summon a magical Python realm
uv venv -p 3.11 .venv
.venv\Scripts\activate              # Windows spell
source .venv/bin/activate           # Unix incantation

# ✨ Install the ancient libraries
uv pip install -e .

# 🔮 Test the magical connection
python -c "from ams_db.core import AgentConfig; print('🧙‍♂️ Magic flows through the code!')"
```

---

## 💬 **CONVERSATION MODES** (The Three Sacred Arts)

### 🗣️ **Human Chat Mode** - Talk directly to an agent
```bash
# 🎯 Start a chat with an agent
ams-db chat start wizard_agent_001 --session-name="my_wizard_chat"

# 💬 Send messages (use the session ID from above)
ams-db chat send dd17acac-7052-47c7-81d7-0856a0fdc97f "Hello wizard!"

# 📜 View chat history
ams-db chat history dd17acac-7052-47c7-81d7-0856a0fdc97f

# 📋 List all your chat sessions
ams-db chat list
```

### 🤖 **Agent-to-Agent Mode** - Watch agents talk to each other
```bash
# 🎭 Generate a conversation between agents
ams-db conversation generate --agents "wizard_agent_001,minecraft_assistant_001" \
  --topic "Building epic AI systems" --turns 6

# 🎯 Export the conversation
ams-db conversation export <session_id> data/conversations/ai_discussion.jsonl
```

### 🎭 **Roleplay Mode** - Pretend to be an agent talking to another agent
```bash
# 🎪 Start roleplay as an agent
ams-db chat roleplay "CodeMaster" wizard_agent_001 --session-name="code_masters_unite"

# 🎭 Send messages as your character
ams-db chat roleplay-send <session_id> "Greetings, wise wizard! I seek knowledge of algorithms!"
```

---

## 🧙‍♂️ **AGENT MASTERY SPELLS**

### ⚡ **Agent Management**
```bash
# 📋 List all magical agents
ams-db agent list

# 🤖 Create a new agent minion
ams-db agent create my_wizard --name "Code Wizard" --description "Master of algorithms"

# � Export agent (config + conversations)
ams-db agent export wizard_agent_001 data/exports/my_wizard_backup/

# 🗑️ Delete an agent (soft delete)
ams-db agent delete my_wizard --soft
```

### 🗄️ **Database Sorcery**
```bash
# 📊 Divine database secrets
ams-db db stats

# 💾 Initialize the crystal database
ams-db db init

# � Create database backup
ams-db db backup data/backups/full_backup_$(date +%Y%m%d)
```

---

## 📁 **ORGANIZED FILE STRUCTURE** (Finally Clean!)

```
AMS-DB/
├── 📊 agent_database/          # Main database (Parquet files)
├── 📦 data/                    # Organized runtime data
│   ├── 👤 agents/             # Agent templates & configs
│   ├── 💬 conversations/      # Saved conversation files  
│   ├── 📤 exports/            # Database exports
│   ├── 🗄️ backups/           # Agent & database backups
│   └── 📋 sessions/           # Active session data
├── 📚 docs/                   # Documentation
├── 🧙‍♂️ src/ams_db/          # Source code
└── 🧪 examples/              # Example scripts
```

---

## 🎭 **AGENT PERSONALITY TEMPLATES** (The Three Legendary Archetypes)

### 🧙‍♂️ **The Mystical Wizard** ⚡
```python
config = AgentConfig("wizard_agent_001")
config.set_prompt("llmSystem", """
🧙‍♂️ Greetings, seeker! I am a mystical wizard of code and algorithms, 
dwelling in ethereal realms where data flows like enchanted rivers 
and logic circuits sparkle like constellation patterns!
""")
```
**✨ Perfect for:** Creative solutions, brainstorming, magical metaphors

### 🎮 **The Minecraft Crafter** 🧱
```python
config = AgentConfig("minecraft_assistant_001")
config.set_prompt("llmSystem", """
Hey there, fellow crafter! 🎮 I'm your friendly Minecraft assistant, 
ready to help you build, explore, and create amazing things!
""")
```
**⛏️ Perfect for:** Step-by-step guides, visual learning, gamification

### 👨‍💻 **The Expert Coder** 🔧
```python
config = AgentConfig("expert_coder_001")
config.set_prompt("llmSystem", """
Expert software engineer specializing in AI/ML systems, database 
architectures, and agentic alignment. Providing precise, well-reasoned solutions.
""")
```
**💻 Perfect for:** Technical analysis, architecture, best practices

---

## 📤 **EXPORT MASTERY** (Data Liberation Spells)

### 📊 **Table Exports**
```bash
# 📋 Export conversations in different formats
ams-db export table conversations --format jsonl --output data/exports/all_conversations.jsonl
ams-db export table agents --format parquet --output data/exports/agents_backup.parquet
ams-db export table knowledge --format parquet  # CSV doesn't support nested data

# 🎯 Export specific agent conversations
ams-db agent export wizard_agent_001 data/exports/wizard_full_backup/
```

### 💾 **Conversation Session Exports**
```bash
# 💬 Export specific chat session
ams-db chat history <session_id> --format jsonl > data/conversations/my_chat.jsonl

# 🎭 Export agent conversation
ams-db conversation export <session_id> data/conversations/agent_discussion.jsonl
```

---

## 🔮 **ADVANCED WIZARDRY** (Pro Tips)

### 🔍 **Find Your Sessions**
```bash
# 📋 List by conversation mode
ams-db chat list --mode HUMAN_CHAT
ams-db chat list --mode AGENT_TO_AGENT
ams-db chat list --mode HUMAN_AS_AGENT

# 🎯 Filter by agent
ams-db chat list --agent wizard_agent_001
```

### 🧹 **Keep Things Organized**
```bash
# 📁 Automatic organization (already done!)
python organize_cleanup.py

# 🧹 Regular maintenance
ams-db db stats                    # Check database health
ls data/exports/                   # Review exports
ls data/backups/                   # Check backups
```

### 🚀 **Quick Start Demo**
```bash
# 🎬 Complete workflow demonstration
python simple_demo_safe.py         # Create sample data
ams-db chat start wizard_agent_001  # Start chatting
ams-db chat list                   # See your sessions
ams-db agent export wizard_agent_001 data/exports/  # Backup everything
```

---

## 🎯 **MODES EXPLAINED** (When to Use What)

| Mode | Use Case | Command Example |
|------|----------|-----------------|
| 🗣️ **Human Chat** | Direct conversation with AI | `ams-db chat start wizard_agent_001` |
| 🤖 **Agent-to-Agent** | Generate training data, observe AI interaction | `ams-db conversation generate --agents "wizard,minecraft"` |
| 🎭 **Roleplay** | Testing, creative writing, character development | `ams-db chat roleplay "MyCharacter" wizard_agent_001` |

---

## 🎉 **SUCCESS! YOU NOW HAVE:**

✅ **Clean, organized file structure** - No more scattered files!  
✅ **Multiple conversation modes** - Chat, roleplay, or watch agents talk  
✅ **Proper data export** - Get your conversations and configs safely  
✅ **Session management** - Track and organize all your interactions  
✅ **Beautiful CLI** - Emojis and clear output for easy use  
✅ **Production-ready** - Extensible system for real AI projects  

**Owen and future wizards**: This system now handles everything you asked for! 🧙‍♂️✨

**Next Steps:**
1. `ams-db chat start wizard_agent_001` - Start your first conversation
2. `ams-db chat list` - See all your sessions
3. `ams-db agent export wizard_agent_001 data/exports/` - Backup your work
4. Read the docs in `docs/` for advanced features

*May your code be bug-free and your agents be wise!* 🌟 
technical solutions with production-ready code.
""")
config.set_prompt("primeDirective", """
Deliver scalable, maintainable software solutions while mentoring 
others in best practices and system design principles.
""")
```
**🚀 Perfect for:** Production code, architecture, performance optimization

---

## 🔮 **CORE SPELL COMPONENTS** (Essential Classes)

### 🤖 **AgentConfig** - The Personality Forge
```python
from ams_db.core import AgentConfig

# ✨ Create an agent vessel
agent = AgentConfig("my_magical_agent")

# 🎭 Set personality traits
agent.set_prompt("llmSystem", "You are a helpful assistant...")
agent.set_prompt("primeDirective", "Help users achieve their goals...")

# ⚙️ Configure magical abilities
agent.set_modality_flag("STT_FLAG", True)      # Speech recognition
agent.set_modality_flag("TTS_FLAG", True)      # Text-to-speech
agent.set_modality_flag("LLAVA_FLAG", True)    # Vision powers

# 💾 Database connections
agent.set_database("knowledge_db", "/path/to/knowledge")

# 📜 Export the magical configuration
config_dict = agent.to_dict()
agent.to_json("my_agent_template.json")
```

### 🗄️ **PolarsDBHandler** - The Data Crystal
```python
from ams_db.core import PolarsDBHandler

# 🔮 Summon the database crystal
db = PolarsDBHandler("agent_database")

# 🤖 Store agent configurations
agent_id = db.add_agent_config(
    agent.to_dict(), 
    agent_name="My Wizard", 
    description="Magical assistant"
)

# 💬 Record conversations
db.add_conversation_message(
    agent_id=agent_id,
    role="assistant",
    content="🧙‍♂️ Let me cast some code magic for you!",
    session_id="session_001"
)

# 📚 Add knowledge scrolls
db.add_knowledge_document(
    agent_id=agent_id,
    title="Advanced Python Magic",
    content="The secrets of Pythonic spellcasting...",
    tags=["python", "magic", "advanced"]
)

# 📋 List all magical agents
agents_df = db.list_agents()

# 📊 Export magical data
db.export_data("conversations", "jsonl")
db.export_data("agents", "parquet")
db.export_data("knowledge", "csv")
```

### 🧠 **GraphitiRAGFramework** - The Knowledge Web
```python
from ams_db.core import GraphitiRAGFramework

# 🕸️ Weave the knowledge web
rag = GraphitiRAGFramework(
    neo4j_uri="bolt://localhost:7687",
    ollama_base_url="http://localhost:11434/v1"
)

# 🔍 Search the mystical knowledge
results = await rag.search_knowledge(
    agent_id="wizard_001",
    query="machine learning algorithms"
)

# 🌐 Add knowledge to the web
await rag.add_knowledge(
    agent_id="wizard_001", 
    content="Neural networks are like magical thinking machines..."
)
```

---

## 🎪 **CONVERSATION MAGIC** (Multi-Agent Dialogues)

### 💬 **Generate Epic Conversations**
```python
from ams_db.core.conversation_generator import ConversationGenerator

# 🎭 Summon the conversation weaver
conv_gen = ConversationGenerator(db_handler, rag_framework)

# 🗣️ Create multi-agent dialogue
conversation = conv_gen.generate_conversation(
    agents=["wizard_001", "minecraft_001", "expert_001"],
    topic="Building an AI-powered Minecraft mod",
    num_turns=10,
    conversation_id="epic_collab_001"
)

# 📜 Export for training data
conv_gen.export_conversations_jsonl("training_data.jsonl")
```

### 💾 **Export Spells** (Data Formats)
```python
# 📊 Multiple format exports
db.export_data("conversations", "csv")      # Spreadsheet magic
db.export_data("agents", "parquet")         # High-performance binary
db.export_data("knowledge", "jsonl")        # Training data format
db.export_data("conversations", "json")     # Web-friendly format
```

---

## 🛠️ **CONFIGURATION ALCHEMY** (Advanced Settings)

### ⚙️ **Modality Flags** (Agent Abilities)
```python
# 🎯 Essential flags for different powers
agent.set_modality_flag("STT_FLAG", True)         # 🎤 Speech-to-text
agent.set_modality_flag("TTS_FLAG", True)         # 🔊 Text-to-speech  
agent.set_modality_flag("LLAVA_FLAG", True)       # 👁️ Vision processing
agent.set_modality_flag("SCREEN_SHOT_FLAG", True) # 📸 Screen capture
agent.set_modality_flag("EMBEDDING_FLAG", True)   # 🧠 Knowledge search
agent.set_modality_flag("AGENT_FLAG", True)       # 🤖 Enable agent mode
agent.set_modality_flag("MEMORY_CLEAR_FLAG", False) # 🧹 Memory persistence
```

### 🎨 **Prompt Types** (Personality Layers)
```python
# 🎭 Different types of personality prompts
agent.set_prompt("llmSystem", "Core personality...")     # Main character
agent.set_prompt("llmBooster", "Enhanced abilities...")  # Power boost
agent.set_prompt("visionSystem", "Visual processing...")  # Image handling
agent.set_prompt("visionBooster", "Advanced vision...")  # Enhanced sight
agent.set_prompt("primeDirective", "Core mission...")    # Prime directive
```

---

## 🚀 **DEMO SPELLS** (Ready-to-Cast Examples)

### 🎯 **Quick Demo Incantation**
```python
# 🧙‍♂️ One-liner demo spell
python simple_demo_safe.py

# 🔮 Interactive exploration
python -c "
from ams_db.core import *
db = PolarsDBHandler()
print(f'📊 Agents: {len(db.list_agents())}')
print('🧙‍♂️ Magic flows through the database!')
"
```

### 🧪 **Custom Agent Creation Ritual**
```python
def create_custom_wizard():
    # 🎭 Create personality
    wizard = AgentConfig("my_custom_wizard")
    
    # ✨ Set magical prompts
    wizard.set_prompt("llmSystem", "I am your personal coding wizard! 🧙‍♂️")
    wizard.set_prompt("primeDirective", "Transform code problems into magical solutions!")
    
    # ⚡ Enable magical abilities
    wizard.set_modality_flag("EMBEDDING_FLAG", True)
    wizard.set_modality_flag("AGENT_FLAG", True)
    
    return wizard

# 🔮 Cast the creation spell
my_wizard = create_custom_wizard()
db = PolarsDBHandler()
wizard_id = db.add_agent_config(my_wizard.to_dict(), "My Personal Wizard")
```

---

## 🎯 **OWEN'S MAGICAL LEARNING PATH** 🌟

### 📅 **Week 1: Foundation Spells**
```bash
# Day 1: First Contact Magic
python simple_demo_safe.py          # See the system in action!
ams-db agent list                    # Meet your magical companions

# Day 2: Create Your First Agent
ams-db agent create owen_wizard --name "Owen's First Wizard" --description "My personal coding assistant"

# Day 3: Conversation Magic  
ams-db conversation generate --agents "owen_wizard,expert_coder_001" --topic "Learning Python" --turns 6

# Day 4-7: Explore the Database
# Browse files in agent_database/ folder
# Try different export formats
# Read through the conversation outputs
```

### 📅 **Week 2: Practical Mastery**
```python
# Create custom agent personalities
# Build knowledge bases for your interests
# Generate training data for specific domains
# Set up the REST API and test it
```

### 📅 **Week 3: Advanced Sorcery**
```bash
# Set up Graphiti with Neo4j (optional but powerful!)
# Create complex multi-agent conversations
# Build custom export formats
# Write your first test cases
```

### 📅 **Week 4: Archmage Level**
```python
# Optimize database performance
# Create entirely new agent archetypes
# Build integrations with other systems
# Contribute improvements back to the project!
```

---

## 🚀 **READY-TO-CAST DEMO SPELLS** 

### 🎯 **The Ultimate Demo Incantation**
```bash
# 🧙‍♂️ See all three legendary agents in action
python simple_demo_safe.py

# Output includes:
# ✨ 3 distinct agent personalities created
# 📚 7 knowledge entries added
# 💬 6 sample conversations stored
# 📊 Multiple export formats demonstrated
# 🎭 Agent personality showcase
```

### 🧪 **Custom Agent Creation Ritual**
```python
def create_owen_agent():
    # 🎭 Create Owen's personal assistant
    owen = AgentConfig("owen_personal_001")
    
    # ✨ Set magical prompts
    owen.set_prompt("llmSystem", """
    Hi! I'm Owen's personal coding assistant! 🎯
    I love helping with Python, AI projects, and creative problem-solving.
    I explain things clearly and always include practical examples.
    """)
    
    owen.set_prompt("primeDirective", """
    Help Owen learn, build, and master programming concepts through 
    hands-on examples and encouraging guidance.
    """)
    
    # ⚡ Enable helpful abilities
    owen.set_modality_flag("EMBEDDING_FLAG", True)
    owen.set_modality_flag("AGENT_FLAG", True)
    
    return owen

# 🔮 Cast the creation spell
my_agent = create_owen_agent()
db = PolarsDBHandler()
agent_id = db.add_agent_config(my_agent.to_dict(), "Owen's Assistant")
print(f"✅ Created your personal agent: {agent_id}")
```

---

## 🌐 **REST API MAGIC** (Web Interface Spells)

### 🚀 **Launch the Mystical API Server**
```bash
# Start the magical web portal
uvicorn src.ams_db.api.main:app --reload --port 8000

# Visit the interactive docs
# http://localhost:8000/docs
```

### 📡 **API Spell Examples**
```python
import requests

base_url = "http://localhost:8000"

# 🤖 Create agent via web magic
new_agent = {
    "agent_id": "api_wizard_001",
    "name": "API Wizard", 
    "description": "Created through ethereal web protocols"
}
response = requests.post(f"{base_url}/agents", json=new_agent)

# 💬 Generate conversation through the web
conversation_request = {
    "agents": ["wizard_001", "expert_001"],
    "topic": "Building Web APIs",
    "num_turns": 6
}
response = requests.post(f"{base_url}/conversations/generate", json=conversation_request)

# 📊 Get agent information
response = requests.get(f"{base_url}/agents")
print("Available agents:", response.json())
```

---

## 💡 **DEBUGGING WISDOM** (When Spells Go Awry)

### 🐛 **Common Enchantment Issues**
```python
# ❌ ImportError: No module named 'ams_db'
# ✅ Solution: Install in development mode
pip install -e .

# ❌ Database permission denied
# ✅ Solution: Check folder permissions
# Make sure agent_database/ folder is writable

# ❌ Agent creation fails
# ✅ Solution: Use unique agent IDs
agent = AgentConfig("unique_name_here")  # Must be unique!

# ❌ CLI commands not found
# ✅ Solution: Verify installation
ams-db --help  # Should show available commands

# ❌ Conversation generation errors
# ✅ Solution: Check agent exists first
ams-db agent list  # Verify agents are available
```

### 🔍 **Testing Your Magic**
```bash
# 🧪 Quick system health check
python -c "
from ams_db.core import PolarsDBHandler, AgentConfig
db = PolarsDBHandler()
agent = AgentConfig('test_agent')
print('✅ All systems magical!')
"

# 🎯 Full demo validation
python simple_demo_safe.py

# 🔬 Run the test suite
python -m pytest tests/ -v
```

---

## 📚 **GRIMOIRE OF KNOWLEDGE** (Essential Scrolls)

### 📖 **Documentation Library**
- 📋 **[BEGINNER_GUIDE.md](BEGINNER_GUIDE.md)** - Complete learning path for new wizards
- 🏗️ **[ARCHITECTURE.md](ARCHITECTURE.md)** - Deep system architecture wisdom  
- 🎯 **[TUTORIAL.md](TUTORIAL.md)** - Step-by-step hands-on learning
- 🛠️ **[USAGE.md](../USAGE.md)** - Practical examples and patterns
- 🏠 **[README.md](../README.md)** - Project overview and quick start

### � **Example Spell Collections**
- 🌱 `examples/basic_usage.py` - Simple starting spells
- 🎮 `examples/minecraft_assistant.py` - Gaming agent magic
- 👨‍💻 `examples/expert_coder_agent.py` - Technical wizardry
- 🎪 `simple_demo_safe.py` - Complete system demonstration

### 🧪 **Testing Sanctuaries**
- 🤖 `tests/test_agent_config.py` - Agent configuration testing
- 🗄️ `tests/test_polars_db.py` - Database operation testing  
- 🔧 `tests/test_components.py` - System component testing

---

## ⚔️ **ADVANCED BATTLE SPELLS** (Power User Magic)

### � **Multi-Agent Orchestration**
```python
# �️ Create epic three-way conversations
from ams_db.core.conversation_generator import ConversationGenerator

conv_gen = ConversationGenerator(db_handler, rag_framework)

# � Generate collaborative dialogue
conversation = conv_gen.generate_conversation(
    agents=["wizard_001", "minecraft_001", "expert_001"],
    topic="Building an AI-powered Minecraft mod with proper architecture",
    num_turns=15,
    context={
        "project": "Educational AI Assistant", 
        "goal": "Learn through building"
    }
)

# 📜 Export for AI training
conv_gen.export_conversations_jsonl("epic_collaboration_training.jsonl")
```

### 📊 **Database Alchemy** (Advanced Queries)
```python
import polars as pl

# 🔍 Find the most active agents
active_agents = db.conversations.group_by("agent_id").agg([
    pl.col("message_id").count().alias("message_count"),
    pl.col("timestamp").max().alias("last_active")
]).sort("message_count", descending=True)

# 🎯 Analyze conversation patterns
conversation_stats = db.conversations.group_by("session_id").agg([
    pl.col("agent_id").n_unique().alias("unique_agents"),
    pl.col("content").str.len_chars().mean().alias("avg_message_length"),
    pl.col("timestamp").max().alias("conversation_end")
])

# 🧠 Search knowledge by tags
python_knowledge = db.knowledge_base.filter(
    pl.col("tags").list.contains("python")
).select(["title", "content", "agent_id"])
```

## 🎯 **QUICK REFERENCE RUNES** (Emergency Spells)

| **Task** | **Command/Code** | **Purpose** |
|---|---|---|
| 🤖 Create agent | `ams-db agent create my_agent --name "Agent Name"` | Birth a new AI personality |
| 📋 List agents | `ams-db agent list` | See all your magical beings |
| � Generate chat | `ams-db conversation generate --agents "a,b" --topic "AI"` | Create multi-agent dialogue |
| 📊 Export data | `ams-db export conversations --format jsonl` | Extract training data |
| 🌐 Start API | `uvicorn src.ams_db.api.main:app --reload` | Launch web interface |
| 🎪 Run demo | `python simple_demo_safe.py` | See the full system magic |
| 🧪 Test system | `python -m pytest tests/` | Verify everything works |
| � Install dev | `pip install -e .` | Set up development mode |
| 📚 Add knowledge | `db.add_knowledge_document(agent_id, title, content, tags)` | Store magical wisdom |
| 🎭 Set personality | `agent.set_prompt("llmSystem", "personality text")` | Define agent character |

---

## 🏆 **ACHIEVEMENT UNLOCKS FOR OWEN** 

- 🥉 **Apprentice Wizard** (Week 1): Create your first agent and run the demo
- 🥈 **Journeyman Coder** (Week 2): Generate multi-agent conversations successfully  
- 🥇 **Expert Architect** (Week 3): Set up complete Graphiti integration
- 💎 **Master Builder** (Week 4): Create a custom agent archetype
- 👑 **Archmage Contributor** (Beyond): Add a new feature to AMS-DB
- 🌟 **Legendary Maintainer** (Ultimate): Become a core project contributor

---

*🧙‍♂️ May your code be elegant, your agents be wise, and your conversations be ever meaningful!*

**Remember, young apprentice:** *The most powerful magic comes from understanding, not just memorizing spells!*

**Go forth and build amazing things, Owen!** 🚀✨

*Blessed by the Great Merlin himself* 🧙‍♂️💫

---

## 📝 **Emergency Spell Card** (Keep This Handy!)

```bash
# 🆘 When all else fails, cast these:
cd AMS-DB && git pull origin master    # Get latest magic
pip install -e .                      # Reinstall powers  
python simple_demo_safe.py            # Test the magic
ams-db agent list                      # Check your minions
ams-db --help                         # Show all available spells
```

*Keep this scroll close, noble seeker! The path to mastery lies in practice and patience.* 📜✨
