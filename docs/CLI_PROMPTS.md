# AMS-DB CLI Commands & Chat Prompts 🧙‍♂️

## ✅ System Status Verified ✅
**All components tested and working correctly:**
- ✅ Database: Connected and operational
- ✅ Neo4j: Running on localhost:7687 
- ✅ Ollama: Running with 67+ models available
- ✅ Agents: Configured and responding properly
- ✅ Chat Manager: Creating sessions and handling messages
- ✅ Knowledge Base: Integrated and accessible
- ✅ Graphiti: Providing context and search capabilities

## 🚀 Essential CLI Commands

### 📋 Agent Management
```bash
# List all agents
python -m src.ams_db.cli.main agent list

# Create a new agent
python -m src.ams_db.cli.main agent create my_agent --name "My Agent" --description "Cool agent"

# Get agent info
python -m src.ams_db.cli.main agent info wizard_agent_001

# Export agent configuration
python -m src.ams_db.cli.main agent export wizard_agent_001 wizard_config.json
```

### 💬 Chat Commands
```bash
# Start a chat session
python -m src.ams_db.cli.main chat start wizard_agent_001

# Send message to chat session (replace 'wiz14' with your session alias)
python -m src.ams_db.cli.main chat send wiz14 "Tell me about machine learning"

# List all chat sessions
python -m src.ams_db.cli.main chat list

# Get chat history
python -m src.ams_db.cli.main chat history wiz14
```

### 📚 Knowledge Management
```bash
# Add knowledge document from file
python -m src.ams_db.cli.main knowledge add wizard_agent_001 "ML Basics" knowledge.txt --tags "ml,basics"

# Search knowledge base
python -m src.ams_db.cli.main knowledge search wizard_agent_001 "neural networks"

# List knowledge documents
python -m src.ams_db.cli.main knowledge list-docs wizard_agent_001
```

### 📊 Database Operations
```bash
# Initialize database
python -m src.ams_db.cli.main db init

# Show database statistics
python -m src.ams_db.cli.main db stats

# Export data
python -m src.ams_db.cli.main export table agents --format csv
python -m src.ams_db.cli.main export table conversations --format jsonl
```

## 🎭 Available Agents

### 🧙‍♂️ Wizard Agent (`wizard_agent_001`)
**Personality:** Mystical, creative, uses magical metaphors for technical concepts
**Best for:** Creative problem solving, learning concepts through magical analogies
**Example chat:**
```bash
python -m src.ams_db.cli.main chat start wizard_agent_001
python -m src.ams_db.cli.main chat send <session_alias> "Explain neural networks like magic spells"
```

### 🎮 Minecraft Assistant (`minecraft_assistant_001`)
**Personality:** Playful, practical, gaming-focused tutorials
**Best for:** Learning through building analogies, step-by-step tutorials
**Example chat:**
```bash
python -m src.ams_db.cli.main chat start minecraft_assistant_001
python -m src.ams_db.cli.main chat send <session_alias> "How do I build a REST API like building a redstone contraption?"
```

### 👨‍💻 Expert Coder (`expert_coder_001`)
**Personality:** Professional, technical, production-ready solutions
**Best for:** Code reviews, architecture decisions, technical implementations
**Example chat:**
```bash
python -m src.ams_db.cli.main chat start expert_coder_001
python -m src.ams_db.cli.main chat send <session_alias> "Design a scalable microservices architecture"
```

## 🔥 Quick Chat Session Workflow

### 1. Start a Session
```bash
python -m src.ams_db.cli.main chat start wizard_agent_001
# Returns: ✅ Session created: wiz15 (a04b5e0e...)
```

### 2. Send Messages
```bash
# Use the session alias returned above (e.g., wiz15)
python -m src.ams_db.cli.main chat send wiz15 "What is machine learning?"
python -m src.ams_db.cli.main chat send wiz15 "Explain it like I'm learning magic"
python -m src.ams_db.cli.main chat send wiz15 "Give me a practical example"
```

### 3. View Chat History
```bash
python -m src.ams_db.cli.main chat history wiz15
```

## 🧪 Testing Commands

### Quick System Test
```bash
# Run comprehensive system test
python test_comprehensive_system.py

# Run final validation test
python test_final_validation.py

# Test chat manager directly
python test_chat_manager.py
```

### Demo Scripts
```bash
# Safe demo (recommended)
python simple_demo_safe.py

# Basic demo
python demo_basic.py

# Comprehensive demo
python comprehensive_demo.py
```

## 🔧 Environment Setup

Make sure your environment variables are set (these are automatically configured):
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=temppass123
```

## 🎯 Common Use Cases

### Learning Session
```bash
# Start with wizard for creative explanations
python -m src.ams_db.cli.main chat start wizard_agent_001
python -m src.ams_db.cli.main chat send <alias> "Explain quantum computing using magical analogies"

# Switch to expert for technical details
python -m src.ams_db.cli.main chat start expert_coder_001
python -m src.ams_db.cli.main chat send <alias> "Give me the technical implementation details for quantum algorithms"
```

### Project Planning
```bash
# Get creative ideas from wizard
python -m src.ams_db.cli.main chat send <wizard_alias> "How would you approach building an AI chatbot?"

# Get practical building steps from Minecraft assistant
python -m src.ams_db.cli.main chat send <minecraft_alias> "Break down chatbot development like building a castle"

# Get technical architecture from expert
python -m src.ams_db.cli.main chat send <expert_alias> "Design the technical architecture for this chatbot"
```

### Knowledge Building
```bash
# Add knowledge documents
echo "Neural networks are computational models inspired by biological neural networks" > ml_basics.txt
python -m src.ams_db.cli.main knowledge add wizard_agent_001 "ML Fundamentals" ml_basics.txt --tags "ml,basics,neural-networks"

# Test knowledge integration
python -m src.ams_db.cli.main chat send <alias> "What do you know about neural networks?"
```

## 🏁 Ready to Go!

Your AMS-DB system is fully operational and ready for use. Start with:

```bash
python -m src.ams_db.cli.main chat start wizard_agent_001
```

And begin your magical journey into AI-powered conversations! 🧙‍♂️✨
