# 🚀 AMS-DB Quick Start Guide

*Get up and running with the Agent Management System in minutes! No more long UUIDs!* 🧙‍♂️✨

## 🎯 What is AMS-DB?

AMS-DB is a powerful system for managing AI agents with **smart short aliases** and multiple conversation modes:
- 🗣️ **Human Chat**: Direct conversation with AI agents (get aliases like `wiz1`, `code2`)
- 🤖 **Agent-to-Agent**: Generate conversations between AI agents  
- 🎭 **Roleplay**: Pretend to be an agent talking to another agent

## ⚡ Quick Setup (3 minutes)

1. **Create Python environment:**
```bash
uv venv -p 3.11 .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

2. **Install AMS-DB:**
```bash
uv pip install -e .
```

3. **Initialize database:**
```bash
ams-db db init
```

4. **Run demo to create sample agents:**
```bash
python simple_demo_safe.py
```

## 🎮 Start Chatting (The Easy Way!)

### Step 1: Start a chat session
```bash
# Chat with the wizard agent
ams-db chat start wizard_agent_001 --session-name="my_first_chat"
```
**Output:**
```
🎉 Started chat session!
   🏷️  Alias: wiz1 (easy to remember!)
   🤖 Agent: wizard_agent_001
   💭 Topic: General conversation
💡 Send messages with: ams-db chat send wiz1 "Your message here"
```

### Step 2: Send messages (using the short alias!)
```bash
# No more long UUIDs! Just use the short alias
ams-db chat send wiz1 "Hello! Can you help me understand AI?"
```

### Step 3: View your conversation
```bash
# See the full chat history
ams-db chat history wiz1

# List all your active chats
ams-db chat list
```

## 🤖 Other Cool Features

### Generate Agent Conversations
```bash
# Watch two AI agents discuss a topic
ams-db conversation generate --agents "wizard_agent_001,minecraft_assistant_001" \
  --topic "Building amazing AI systems" --turns 5
```

### Roleplay Mode
```bash
# Pretend to be "CodeMaster" talking to the wizard
ams-db chat roleplay "CodeMaster" wizard_agent_001 --session-name="epic_roleplay"
```

### Export Everything (Organized!)
```bash
# Export your chat session (automatically organized by date/mode)
ams-db chat export wiz1

# Export an agent's data (with timestamp)
ams-db agent export wizard_agent_001 data/exports/my_wizard_backup_
```

## 📁 Perfect File Organization

Your data is now automatically organized:
```
data/
├── conversations/
│   ├── human_chat/2025-07-16/     # Your chats by date
│   ├── agent_chat/2025-07-16/     # AI-to-AI conversations  
│   └── roleplay/2025-07-16/       # Roleplay sessions
├── sessions/
│   └── active_sessions.json       # Smart alias mapping
├── exports/                       # Agent backups
└── agents/                        # Agent templates
```

## 🎭 Chat Session Types

| Mode | Command | What It Does |
|------|---------|--------------|
| **Human Chat** | `ams-db chat start <agent>` | You talk directly to an AI agent |
| **Agent Chat** | `ams-db conversation generate` | Two AI agents talk to each other |
| **Roleplay** | `ams-db chat roleplay <you> <agent>` | You pretend to be an AI talking to another AI |

## � Quick Commands Reference

```bash
# Chat Management
ams-db chat start wizard_agent_001    # Start chatting (gets alias like 'wiz1')
ams-db chat send wiz1 "Hello!"        # Send message using short alias
ams-db chat list                      # List all active chats
ams-db chat history wiz1              # View chat history
ams-db chat export wiz1               # Export to organized folders

# Agent Management  
ams-db agent list                     # List all agents
ams-db agent export wizard_agent_001 backup/  # Export agent
ams-db db stats                       # Database statistics

# Conversation Generation
ams-db conversation generate --agents "agent1,agent2" --topic "Cool topic" --turns 5
```

## � You're Ready!

**No more typing long UUIDs!** 🙌 Just use simple aliases like:
- `wiz1` for wizard chats
- `mc2` for minecraft assistant chats  
- `code3` for expert coder chats
- `chat4` for general conversations

**Your conversations are automatically organized by date and type!** 📁✨

---

**Need more help?** Check out the [Ultimate Cheatsheet](ULTIMATE_CHEATSHEET.md) for all the wizardly commands! 🧙‍♂️
