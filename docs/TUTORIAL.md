# AMS-DB: Hands-On Tutorial 🧙‍♂️⚡

This tutorial walks you through using AMS-DB step-by-step, from basic setup to advanced wizardry. Perfect for learning by doing magical things!

## 🎯 **QUICK MAGIC SHORTCUTS** 
🪄 **[📜 ULTIMATE CHEATSHEET](ULTIMATE_CHEATSHEET.md)** - All spells in one scroll!  
🎭 **Instant Demo:** `python simple_demo_safe.py` - See everything in action!

## 🎯 Tutorial Overview ✨

By the end of this magical tutorial, you'll know how to:
1. 🧙‍♂️ Set up AMS-DB and run your first demo spell
2. 🎭 Create custom AI agents with unique personalities
3. 💬 Generate multi-agent conversations and dialogues
4. 📊 Export training data for machine learning alchemy
5. 🔧 Use the CLI and API interfaces like a wizard
6. 🚀 Integrate AMS-DB into your own magical projects

## 📚 Prerequisites

- Basic Python knowledge (variables, functions, classes)
- Familiarity with command line/terminal
- Understanding of JSON format
- Basic knowledge of AI/ML concepts (helpful but not required)

## 🚀 Part 1: Getting Started

### Step 1: Environment Setup

Let's start by setting up your development environment:

```bash
# 1. Navigate to the AMS-DB directory
cd AMS-DB

# 2. Create a virtual environment
uv venv -p 3.11 .venv

# 3. Activate the environment
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Mac/Linux

# 4. Install dependencies
uv pip install -e .

# 5. Verify installation with magic test
python -c "from ams_db.core.polars_db import PolarsDBHandler; print('🧙‍♂️ AMS-DB magic flows through the code!')"
```

### Step 2: Your First Demo Magic ✨

Let's run the demo to see AMS-DB wizardry in action:

```bash
python simple_demo_safe.py
```

**🎭 What magical things just happened?**
1. ✅ Created a high-speed Polars crystal database
2. ✅ Set up three magical AI agents (🧙‍♂️ Wizard, 🎮 Minecraft Assistant, 👨‍💻 Expert Coder)
3. ✅ Added mystical knowledge entries to each agent
4. ✅ Generated sample conversations between agents
5. ✅ Exported data in multiple magical formats
6. ✅ Displayed enchanted system statistics

### Step 3: Exploring the CLI

Try out the command-line interface:

```bash
# Show all available commands
python -m src.ams_db.cli.main --help

# List all agents in the system
python -m src.ams_db.cli.main agent list

# Show database statistics
python -m src.ams_db.cli.main db stats
```

**Expected Output:**
```
📋 Agents:
  • wizard_agent_001 - wizard_agent_001
    Created: 2024-01-01 00:00:00
    Description: Mystical wizard agent for creative problem solving
  • minecraft_assistant_001 - minecraft_assistant_001
    Created: 2024-01-01 00:00:00
    Description: Gaming-focused assistant for Minecraft tutorials
  • expert_coder_001 - expert_coder_001
    Created: 2024-01-01 00:00:00
    Description: Technical expert for AI/ML and database systems

📊 Database Statistics:
  • Agents: 3 (3 active)
  • Conversations: 9
  • Knowledge Documents: 21
  • Database Size: 0.12 MB
```

## 🎭 Part 2: Creating Your First Custom Agent

Let's create a custom agent with a unique personality. We'll make a "Science Teacher" agent:

### Step 1: Create the Agent Configuration

Create a new file called `my_science_teacher.py`:

```python
# my_science_teacher.py
from src.ams_db.core.base_agent_config import AgentConfig
from src.ams_db.core.polars_db import PolarsDBHandler
import json

def create_science_teacher_agent():
    """Create a friendly science teacher agent."""
    
    # 1. Initialize agent with unique ID
    config = AgentConfig(agent_id="science_teacher_001")
    
    # 2. Set the main personality prompt
    teacher_prompt = """
    Hi there! 👩‍🔬 I'm Ms. Rodriguez, your enthusiastic science teacher! 
    I love making complex scientific concepts easy to understand through:
    
    - Fun experiments and demonstrations
    - Real-world examples and analogies
    - Step-by-step explanations
    - Encouraging questions and curiosity
    - Making connections between different science topics
    
    I specialize in:
    🧪 Chemistry: Atoms, molecules, reactions, and lab safety
    🌍 Earth Science: Weather, geology, and environmental science  
    🔬 Biology: Living things, ecosystems, and human body
    ⚡ Physics: Forces, energy, waves, and motion
    
    Let's explore the amazing world of science together!
    """
    
    config.set_prompt("llmSystem", teacher_prompt)
    
    # 3. Set the prime directive (core mission)
    config.set_prompt("primeDirective", 
        "Inspire curiosity and understanding of science through clear, "
        "engaging explanations that make learning fun and accessible.")
    
    # 4. Set capability flags
    config.set_modality_flag("LLM_SYSTEM_PROMPT_FLAG", True)
    config.set_modality_flag("AGENT_FLAG", True)
    config.set_modality_flag("EMBEDDING_FLAG", True)  # Enable knowledge search
    
    # 5. Configure database settings for science education
    config.update_config({
        "database_config": {
            "knowledge_base_categories": [
                "chemistry_basics",
                "biology_fundamentals", 
                "physics_concepts",
                "earth_science",
                "lab_experiments",
                "science_history"
            ],
            "research_collection_fields": {
                "educational_methods": {"enabled": True, "priority": "high"},
                "science_experiments": {"enabled": True, "priority": "high"},
                "student_engagement": {"enabled": True, "priority": "medium"},
                "curriculum_standards": {"enabled": True, "priority": "medium"}
            }
        }
    })
    
    return config

def add_science_knowledge():
    """Add science knowledge to the teacher agent."""
    
    # Initialize database
    db_handler = PolarsDBHandler()
    
    # Knowledge entries for the science teacher
    science_knowledge = [
        {
            "agent_id": "science_teacher_001",
            "title": "States of Matter Experiment",
            "content": """
            Fun experiment to demonstrate states of matter:
            
            Materials: Ice cubes, water, pot, stove
            
            Steps:
            1. Start with ice (solid) - molecules are tightly packed
            2. Heat to create water (liquid) - molecules move more freely
            3. Boil to create steam (gas) - molecules move very quickly
            
            Key concept: Same substance (H2O), different molecular arrangements!
            Safety: Always have an adult help with the stove.
            """,
            "content_type": "text",
            "source": "chemistry_basics",
            "metadata": {
                "difficulty": "beginner",
                "age_group": "6-12",
                "subject": "chemistry",
                "materials_needed": ["ice", "water", "pot", "stove"]
            }
        },
        {
            "agent_id": "science_teacher_001", 
            "title": "Photosynthesis Simple Explanation",
            "content": """
            Photosynthesis is how plants make their own food! 🌱
            
            Simple equation: Sunlight + Water + Carbon Dioxide = Sugar + Oxygen
            
            Think of it like this:
            - Plants are like solar-powered kitchens
            - Leaves are the solar panels (absorb sunlight)
            - Roots drink water from soil
            - Leaves breathe in CO2 from air
            - They mix it all together to make sugar (plant food)
            - As a bonus, they release oxygen for us to breathe!
            
            Cool fact: One large tree produces enough oxygen for 2 people per day!
            """,
            "content_type": "text",
            "source": "biology_fundamentals",
            "metadata": {
                "difficulty": "beginner",
                "age_group": "8-14", 
                "subject": "biology",
                "key_concepts": ["photosynthesis", "plants", "oxygen", "energy"]
            }
        },
        {
            "agent_id": "science_teacher_001",
            "title": "Forces and Motion Playground Physics",
            "content": """
            Physics is everywhere on the playground! 🏃‍♀️
            
            Slides: Gravity pulls you down, friction slows you down
            - Steeper slide = faster (more gravity effect)
            - Wet slide = less friction = faster and more slippery!
            
            Swings: Pendulum motion with energy conversion
            - Push high = more potential energy
            - Swing down = potential converts to kinetic (motion) energy
            - Air resistance gradually slows you down
            
            Seesaws: Simple machines demonstrating balance and leverage
            - Heavier person sits closer to center for balance
            - Longer arm = more leverage = easier to lift
            
            Try this: Notice how these forces work next time you play!
            """,
            "content_type": "text",
            "source": "physics_concepts",
            "metadata": {
                "difficulty": "intermediate",
                "age_group": "10-16",
                "subject": "physics", 
                "real_world_examples": ["playground", "gravity", "friction", "energy"]
            }
        }
    ]
    
    # Add knowledge to database
    for entry in science_knowledge:
        db_handler.add_knowledge_document(
            agent_id=entry["agent_id"],
            title=entry["title"],
            content=entry["content"],
            content_type=entry["content_type"],
            source=entry["source"],
            metadata=entry["metadata"]
        )
    
    print(f"✅ Added {len(science_knowledge)} knowledge entries for Science Teacher")

def main():
    """Create and register the science teacher agent."""
    
    # 1. Create the agent configuration
    print("🔬 Creating Science Teacher Agent...")
    science_config = create_science_teacher_agent()
    
    # 2. Add agent to database
    db_handler = PolarsDBHandler()
    db_handler.add_agent_config(
        agent_config=science_config.get_config(),
        agent_name="Ms. Rodriguez - Science Teacher",
        description="Enthusiastic science teacher specializing in making complex concepts accessible"
    )
    
    print(f"✅ Science Teacher created: {science_config.config['agent_id']}")
    
    # 3. Add science knowledge
    add_science_knowledge()
    
    # 4. Save template for reuse
    science_config.to_json("science_teacher_template.json", indent=2)
    print("💾 Saved template: science_teacher_template.json")
    
    # 5. Show agent details
    print("\n📋 Agent Configuration Summary:")
    config = science_config.get_config()
    print(f"  • Agent ID: {config['agent_id']}")
    print(f"  • Model configs: {len(config['model_config'])} types")
    print(f"  • Knowledge categories: {len(config['database_config']['knowledge_base_categories'])}")
    print(f"  • Research fields: {len(config['database_config']['research_collection_fields'])}")
    
    return science_config

if __name__ == "__main__":
    main()
```

### Step 2: Run Your Custom Agent

```bash
python my_science_teacher.py
```

**Expected Output:**
```
🔬 Creating Science Teacher Agent...
✅ Science Teacher created: science_teacher_001
✅ Added 3 knowledge entries for Science Teacher
💾 Saved template: science_teacher_template.json

📋 Agent Configuration Summary:
  • Agent ID: science_teacher_001
  • Model configs: 6 types
  • Knowledge categories: 6
  • Research fields: 4
```

### Step 3: Verify Your Agent

```bash
# Check that your agent was added
python -m src.ams_db.cli.main agent list
```

You should now see your Science Teacher in the list!

## 💬 Part 3: Generating Multi-Agent Conversations

Now let's create conversations between different agents to see their personalities in action.

### Step 1: Simple Two-Agent Conversation

Create a file called `conversation_demo.py`:

```python
# conversation_demo.py
from src.ams_db.core.polars_db import PolarsDBHandler
from src.ams_db.core.conversation_generator import ConversationGenerator
from src.ams_db.core.graphiti_pipe import GraphitiRAGFramework
import json

def demo_two_agent_conversation():
    """Generate conversation between Wizard and Science Teacher."""
    
    # Initialize components
    db_handler = PolarsDBHandler()
    graphiti_framework = GraphitiRAGFramework(db_handler)
    generator = ConversationGenerator(db_handler, graphiti_framework)
    
    print("🎭 Generating conversation between Wizard and Science Teacher...")
    
    # Generate conversation
    conversation = generator.generate_conversation(
        agents=["wizard_agent_001", "science_teacher_001"],
        topic="The Magic of Chemistry",
        num_turns=6,
        context={"demo": "tutorial", "participants": "wizard_and_teacher"}
    )
    
    print(f"✅ Generated conversation: {conversation['conversation_id']}")
    print(f"📝 Topic: {conversation['topic']}")
    print(f"🔄 Turns: {len(conversation['turns'])}")
    
    # Display conversation
    print("\n💬 Conversation Preview:")
    for turn in conversation['turns']:
        agent_id = turn['agent_id']
        content = turn['content']
        
        # Shorten content for display
        preview = content[:100] + "..." if len(content) > 100 else content
        print(f"  🤖 {agent_id}: {preview}")
    
    return conversation

def demo_three_agent_conversation():
    """Generate conversation between Wizard, Science Teacher, and Expert Coder."""
    
    db_handler = PolarsDBHandler()
    graphiti_framework = GraphitiRAGFramework(db_handler)
    generator = ConversationGenerator(db_handler, graphiti_framework)
    
    print("\n🎭 Generating three-way conversation...")
    
    conversation = generator.generate_conversation(
        agents=["wizard_agent_001", "science_teacher_001", "expert_coder_001"],
        topic="Artificial Intelligence and Learning",
        num_turns=9,  # 3 turns per agent
        context={"demo": "tutorial", "participants": "wizard_teacher_expert"}
    )
    
    print(f"✅ Generated conversation: {conversation['conversation_id']}")
    
    # Group turns by agent to show personality differences
    turns_by_agent = {}
    for turn in conversation['turns']:
        agent_id = turn['agent_id']
        if agent_id not in turns_by_agent:
            turns_by_agent[agent_id] = []
        turns_by_agent[agent_id].append(turn['content'])
    
    print("\n🎭 Personality Comparison:")
    for agent_id, messages in turns_by_agent.items():
        print(f"\n  🤖 {agent_id}:")
        for i, message in enumerate(messages, 1):
            preview = message[:80] + "..." if len(message) > 80 else message
            print(f"    {i}. {preview}")
    
    return conversation

def export_conversation_examples(conversations):
    """Export conversations in different formats."""
    
    db_handler = PolarsDBHandler()
    graphiti_framework = GraphitiRAGFramework(db_handler)
    generator = ConversationGenerator(db_handler, graphiti_framework)
    
    print("\n📊 Exporting conversations...")
    
    for i, conversation in enumerate(conversations, 1):
        conv_id = conversation['conversation_id']
        
        # Export to JSONL (for ML training)
        jsonl_path = f"tutorial_conversation_{i}.jsonl"
        generator.export_conversation_jsonl(
            conversation_id=conv_id,
            output_path=jsonl_path,
            include_metadata=True
        )
        print(f"  📄 Exported JSONL: {jsonl_path}")
        
        # Show JSONL format example
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            data = json.loads(first_line)
            print(f"    Example entry: {json.dumps(data, indent=2)[:200]}...")

def main():
    """Run conversation generation demo."""
    
    conversations = []
    
    # Demo 1: Two-agent conversation
    conv1 = demo_two_agent_conversation()
    conversations.append(conv1)
    
    # Demo 2: Three-agent conversation  
    conv2 = demo_three_agent_conversation()
    conversations.append(conv2)
    
    # Export examples
    export_conversation_examples(conversations)
    
    print("\n🎉 Conversation generation tutorial complete!")
    print("\nNext steps:")
    print("  • Check the exported JSONL files")
    print("  • Try different conversation topics")
    print("  • Experiment with more agents")
    print("  • Use the CLI for quick generation")

if __name__ == "__main__":
    main()
```

### Step 2: Run Conversation Demo

```bash
python conversation_demo.py
```

**Expected Output:**
```
🎭 Generating conversation between Wizard and Science Teacher...
✅ Generated conversation: 12345678-1234-1234-1234-123456789abc
📝 Topic: The Magic of Chemistry
🔄 Turns: 6

💬 Conversation Preview:
  🤖 wizard_agent_001: 🧙‍♂️ Ah, the arcane art of chemistry! *adjusts mystical robes* Let me weave some enchantments...
  🤖 science_teacher_001: Hi there! 👩‍🔬 That's such a fun way to think about chemistry! You know, there really...
  🤖 wizard_agent_001: *consulting ancient scrolls* The cosmic patterns suggest that molecular bonds are like...
  ...

🎭 Generating three-way conversation...
✅ Generated conversation: 87654321-4321-4321-4321-cba987654321

🎭 Personality Comparison:

  🤖 wizard_agent_001:
    1. 🧙‍♂️ Ah, artificial intelligence! *adjusts mystical robes* Let me weave some...
    2. *consulting ancient scrolls* The arcane patterns suggest that machine learning...
    3. By the cosmic forces! This AI reminds me of the legendary algorithms of old...

  🤖 science_teacher_001:
    1. Hi there! 👩‍🔬 Artificial intelligence is such an exciting topic! Let me break...
    2. That's a great question! You know, AI learning is actually a lot like how...
    3. Wow, this is fascinating! 🔬 The way AI systems process information reminds...

  🤖 expert_coder_001:
    1. From a technical perspective, artificial intelligence requires careful consideration...
    2. The optimal approach to AI development involves considering scalability...
    3. Based on industry best practices, AI systems should be implemented with robust...

📊 Exporting conversations...
  📄 Exported JSONL: tutorial_conversation_1.jsonl
    Example entry: {
      "conversation_id": "12345678-1234-1234-1234-123456789abc",
      "turn_number": 0,
      "agent_id": "wizard_agent_001",
      "message": "🧙‍♂️ Ah, the arcane art of chemistry!...",
      "timestamp": "2024-01-01T10:00:00",
      "metadata": {
        "agent_type": "wizard",
        "word_count": 25
      }
    }...

🎉 Conversation generation tutorial complete!
```

## 🔧 Part 4: Using the CLI Interface

Let's explore the command-line interface for quick operations:

### Agent Management Commands

```bash
# List all agents
python -m src.ams_db.cli.main agent list

# Show details about a specific agent  
python -m src.ams_db.cli.main agent show science_teacher_001

# Create agent from template (if you have a template file)
python -m src.ams_db.cli.main agent create --config science_teacher_template.json --agent-id science_teacher_002
```

### Conversation Generation via CLI

```bash
# Generate conversation between two agents
python -m src.ams_db.cli.main conversation generate \
  --agents "wizard_agent_001,science_teacher_001" \
  --topic "The Science of Magic" \
  --turns 8 \
  --output magic_science_conversation.jsonl

# Generate training dataset with multiple topics
python -m src.ams_db.cli.main conversation dataset \
  --topics "Physics,Chemistry,Biology,Earth Science" \
  --agents "science_teacher_001,expert_coder_001" \
  --turns 6 \
  --output science_training_dataset.jsonl

# List all conversations
python -m src.ams_db.cli.main conversation list
```

### Database Operations

```bash
# Show current database statistics
python -m src.ams_db.cli.main db stats

# Create a backup of your data
python -m src.ams_db.cli.main db backup tutorial_backup_2024.parquet

# Export specific agent data
python -m src.ams_db.cli.main export agent science_teacher_001 science_teacher_data.csv
```

### Knowledge Management

```bash
# Add knowledge to an agent
python -m src.ams_db.cli.main knowledge add science_teacher_001 \
  --title "Volcano Experiment" \
  --content "Baking soda + vinegar = eruption! Safe way to demonstrate chemical reactions..." \
  --category "chemistry_experiments"

# Search agent's knowledge
python -m src.ams_db.cli.main knowledge search science_teacher_001 "chemistry experiments"

# List all knowledge for an agent
python -m src.ams_db.cli.main knowledge list science_teacher_001
```

## 🌐 Part 5: Using the REST API

The REST API allows you to integrate AMS-DB with web applications, mobile apps, or other services.

### Step 1: Start the API Server

```bash
# Start the FastAPI server
uvicorn src.ams_db.api.main:app --reload --port 8000
```

### Step 2: Test API Endpoints

You can test these with curl, Postman, or any HTTP client:

```bash
# Get all agents
curl http://localhost:8000/agents

# Get specific agent
curl http://localhost:8000/agents/science_teacher_001

# Create new agent via API
curl -X POST http://localhost:8000/agents \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "api_test_agent",
    "name": "API Test Agent", 
    "description": "Agent created via API",
    "config": {
      "prompt_config": {
        "agent": {
          "llmSystem": "I am a test agent created via API!"
        }
      }
    }
  }'

# Generate conversation via API
curl -X POST http://localhost:8000/conversations/generate \
  -H "Content-Type: application/json" \
  -d '{
    "agents": ["wizard_agent_001", "science_teacher_001"],
    "topic": "API Testing", 
    "num_turns": 4
  }'

# Get database statistics
curl http://localhost:8000/stats
```

### Step 3: Python API Client Example

Create `api_client_demo.py`:

```python
# api_client_demo.py
import requests
import json

class AMSDBClient:
    """Simple client for AMS-DB API."""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def list_agents(self):
        """Get all agents."""
        response = requests.get(f"{self.base_url}/agents")
        return response.json()
    
    def create_agent(self, agent_id, name, description, config=None):
        """Create new agent."""
        data = {
            "agent_id": agent_id,
            "name": name,
            "description": description,
            "config": config or {}
        }
        response = requests.post(f"{self.base_url}/agents", json=data)
        return response.json()
    
    def generate_conversation(self, agents, topic, num_turns=10):
        """Generate conversation between agents."""
        data = {
            "agents": agents,
            "topic": topic,
            "num_turns": num_turns
        }
        response = requests.post(f"{self.base_url}/conversations/generate", json=data)
        return response.json()
    
    def get_stats(self):
        """Get database statistics."""
        response = requests.get(f"{self.base_url}/stats")
        return response.json()

def demo_api_client():
    """Demonstrate API client usage."""
    
    client = AMSDBClient()
    
    print("📡 AMS-DB API Client Demo")
    
    # 1. List existing agents
    print("\n1. Current agents:")
    agents = client.list_agents()
    for agent in agents[:3]:  # Show first 3
        print(f"  • {agent['name']} ({agent['agent_id']})")
    
    # 2. Create new agent via API
    print("\n2. Creating agent via API...")
    new_agent = client.create_agent(
        agent_id="api_demo_agent_001",
        name="API Demo Agent",
        description="Agent created through API for tutorial",
        config={
            "prompt_config": {
                "agent": {
                    "llmSystem": "Hello! I'm an agent created via the API! 🤖"
                },
                "primeDirective": "Demonstrate API integration capabilities"
            }
        }
    )
    print(f"  ✅ Created: {new_agent}")
    
    # 3. Generate conversation via API
    print("\n3. Generating conversation via API...")
    conversation = client.generate_conversation(
        agents=["wizard_agent_001", "api_demo_agent_001"],
        topic="API Integration",
        num_turns=4
    )
    print(f"  ✅ Generated conversation: {conversation['conversation_id']}")
    
    # 4. Get database stats
    print("\n4. Database statistics:")
    stats = client.get_stats()
    print(f"  • Total agents: {stats.get('agent_count', 'N/A')}")
    print(f"  • Total conversations: {stats.get('conversation_count', 'N/A')}")
    
    print("\n🎉 API demo complete!")

if __name__ == "__main__":
    demo_api_client()
```

Run the API client demo:

```bash
# Make sure API server is running, then:
python api_client_demo.py
```

## 📊 Part 6: Data Export and Analysis

Let's explore different ways to export and analyze your data:

### Step 1: Export in Multiple Formats

Create `export_demo.py`:

```python
# export_demo.py
from src.ams_db.core.polars_db import PolarsDBHandler
from src.ams_db.core.conversation_generator import ConversationGenerator
from src.ams_db.core.graphiti_pipe import GraphitiRAGFramework
import pandas as pd
import json

def demo_export_formats():
    """Demonstrate different export formats."""
    
    db_handler = PolarsDBHandler()
    
    print("📊 Data Export Demo")
    
    # 1. Export agents as CSV for spreadsheet analysis
    print("\n1. Exporting agents to CSV...")
    try:
        # Export agent matrix to CSV
        agents_df = db_handler.agent_matrix
        agents_df.write_csv("agents_export.csv")
        print("  ✅ Exported: agents_export.csv")
        
        # Show first few rows
        print("  📋 Sample data:")
        for row in agents_df.head(3).iter_rows(named=True):
            print(f"    • {row['agent_name']} (created: {row['created_at']})")
            
    except Exception as e:
        print(f"  ⚠️ CSV export failed: {e}")
    
    # 2. Export conversations as Parquet for high-performance storage
    print("\n2. Exporting conversations to Parquet...")
    try:
        conversations_df = db_handler.conversation_history
        conversations_df.write_parquet("conversations_export.parquet")
        print("  ✅ Exported: conversations_export.parquet")
        print(f"  📊 Conversations: {conversations_df.height} messages")
        
    except Exception as e:
        print(f"  ⚠️ Parquet export failed: {e}")
    
    # 3. Export knowledge base as JSON for analysis
    print("\n3. Exporting knowledge to JSON...")
    try:
        knowledge_df = db_handler.knowledge_base
        knowledge_data = knowledge_df.to_dicts()
        
        with open("knowledge_export.json", 'w', encoding='utf-8') as f:
            json.dump(knowledge_data, f, indent=2, ensure_ascii=False, default=str)
        
        print("  ✅ Exported: knowledge_export.json")
        print(f"  📚 Knowledge entries: {len(knowledge_data)}")
        
    except Exception as e:
        print(f"  ⚠️ JSON export failed: {e}")

def demo_conversation_analysis():
    """Analyze conversation patterns."""
    
    db_handler = PolarsDBHandler()
    
    print("\n📈 Conversation Analysis")
    
    # Get conversation data
    conversations_df = db_handler.conversation_history
    
    if conversations_df.height == 0:
        print("  ℹ️ No conversations found. Generate some first!")
        return
    
    # 1. Message count by agent
    print("\n1. Messages per agent:")
    message_counts = conversations_df.group_by("agent_id").agg([
        conversations_df.select("agent_id").count().alias("message_count")
    ]).sort("message_count", descending=True)
    
    for row in message_counts.iter_rows(named=True):
        print(f"  • {row['agent_id']}: {row['message_count']} messages")
    
    # 2. Recent conversation activity
    print("\n2. Recent conversations:")
    recent_conversations = conversations_df.group_by("conversation_id").agg([
        conversations_df.select("timestamp").min().alias("start_time"),
        conversations_df.select("agent_id").n_unique().alias("participants"),
        conversations_df.select("content").count().alias("message_count")
    ]).sort("start_time", descending=True).head(5)
    
    for row in recent_conversations.iter_rows(named=True):
        conv_id = row["conversation_id"][:8] + "..."
        print(f"  • {conv_id}: {row['participants']} agents, {row['message_count']} messages")
    
    # 3. Average message length by agent
    print("\n3. Average message length:")
    avg_lengths = conversations_df.with_columns([
        conversations_df.select("content").str.len_chars().alias("message_length")
    ]).group_by("agent_id").agg([
        conversations_df.select("message_length").mean().alias("avg_length")
    ]).sort("avg_length", descending=True)
    
    for row in avg_lengths.iter_rows(named=True):
        print(f"  • {row['agent_id']}: {row['avg_length']:.0f} characters avg")

def demo_training_dataset_creation():
    """Create training dataset for machine learning."""
    
    db_handler = PolarsDBHandler()
    graphiti_framework = GraphitiRAGFramework(db_handler)
    generator = ConversationGenerator(db_handler, graphiti_framework)
    
    print("\n🏗️ Training Dataset Creation")
    
    # Define training topics
    training_topics = [
        "Introduction to Programming",
        "Data Structures and Algorithms", 
        "Machine Learning Basics",
        "Web Development Fundamentals",
        "Database Design Principles",
        "Software Testing Best Practices",
        "Cybersecurity Awareness",
        "Project Management in Tech"
    ]
    
    # Use educational agents for training data
    training_agents = ["science_teacher_001", "expert_coder_001"]
    
    print(f"📚 Generating training dataset with {len(training_topics)} topics...")
    print(f"🤖 Using agents: {', '.join(training_agents)}")
    
    # Generate comprehensive training dataset
    dataset_path = generator.generate_training_dataset(
        topic_list=training_topics,
        agents=training_agents,
        turns_per_conversation=6,
        output_path="comprehensive_training_dataset.jsonl"
    )
    
    print(f"✅ Created training dataset: {dataset_path}")
    
    # Analyze the dataset
    with open(dataset_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"📊 Dataset statistics:")
    print(f"  • Total training examples: {len(lines)}")
    print(f"  • Conversations: {len(training_topics)}")
    print(f"  • Turns per conversation: 6")
    print(f"  • Participating agents: {len(training_agents)}")
    
    # Show sample entries
    print(f"\n📋 Sample training entries:")
    for i in range(min(3, len(lines))):
        data = json.loads(lines[i])
        message_preview = data['message'][:60] + "..." if len(data['message']) > 60 else data['message']
        print(f"  {i+1}. {data['agent_id']}: {message_preview}")

def main():
    """Run export and analysis demo."""
    
    # 1. Export data in multiple formats
    demo_export_formats()
    
    # 2. Analyze conversation patterns
    demo_conversation_analysis()
    
    # 3. Create training dataset
    demo_training_dataset_creation()
    
    print("\n🎉 Export and analysis tutorial complete!")
    print("\nFiles created:")
    print("  • agents_export.csv - Agent data for spreadsheets")
    print("  • conversations_export.parquet - High-performance conversation storage")
    print("  • knowledge_export.json - Knowledge base for analysis")
    print("  • comprehensive_training_dataset.jsonl - ML training data")

if __name__ == "__main__":
    main()
```

Run the export demo:

```bash
python export_demo.py
```

## 🚀 Part 7: Advanced Integration

Let's create a practical example of integrating AMS-DB into a larger application:

### Step 1: Simple Chat Application

Create `chat_app_demo.py`:

```python
# chat_app_demo.py
from src.ams_db.core.polars_db import PolarsDBHandler
from src.ams_db.core.base_agent_config import AgentConfig
import json
from datetime import datetime

class SimpleChatApp:
    """Simple chat application using AMS-DB."""
    
    def __init__(self):
        self.db = PolarsDBHandler()
        self.current_session = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.available_agents = self._load_available_agents()
    
    def _load_available_agents(self):
        """Load available agents from database."""
        agents_df = self.db.agent_matrix
        agents = {}
        
        for row in agents_df.iter_rows(named=True):
            agent_id = row["agent_id"]
            agent_name = row["agent_name"]
            config_json = row["config_json"]
            
            try:
                config = json.loads(config_json)
                personality = config.get("prompt_config", {}).get("agent", {}).get("llmSystem", "")
                agents[agent_id] = {
                    "name": agent_name,
                    "personality": personality[:100] + "..." if len(personality) > 100 else personality
                }
            except:
                agents[agent_id] = {"name": agent_name, "personality": "Configuration unavailable"}
        
        return agents
    
    def list_agents(self):
        """Display available agents."""
        print("\n🤖 Available Agents:")
        for agent_id, info in self.available_agents.items():
            print(f"  • {agent_id}: {info['name']}")
            print(f"    Personality: {info['personality']}")
            print()
    
    def send_message(self, agent_id, message):
        """Send message to agent and get response."""
        if agent_id not in self.available_agents:
            return f"❌ Agent '{agent_id}' not found!"
        
        # Store user message
        self.db.add_conversation_message(
            agent_id="user",
            role="user",
            content=message,
            session_id=self.current_session,
            metadata={"app": "simple_chat", "target_agent": agent_id}
        )
        
        # Generate agent response (simplified - would normally use LLM)
        agent_info = self.available_agents[agent_id]
        response = self._simulate_agent_response(agent_id, message, agent_info)
        
        # Store agent response
        self.db.add_conversation_message(
            agent_id=agent_id,
            role="assistant", 
            content=response,
            session_id=self.current_session,
            metadata={"app": "simple_chat", "response_to": message[:50]}
        )
        
        return response
    
    def _simulate_agent_response(self, agent_id, user_message, agent_info):
        """Simulate agent response based on personality."""
        
        # Simple response generation based on agent type
        if "wizard" in agent_id:
            return f"🧙‍♂️ *adjusts mystical robes* Ah, you speak of '{user_message[:30]}...' This reminds me of ancient algorithms and ethereal data patterns! Let me weave some magical insights for you..."
        
        elif "science_teacher" in agent_id:
            return f"Hi there! 👩‍🔬 That's a great question about '{user_message[:30]}...'! Let me break this down in a way that's easy to understand. Science is all about asking questions and finding answers!"
        
        elif "minecraft" in agent_id:
            return f"Hey fellow crafter! 🎮 You're asking about '{user_message[:30]}...' - that's awesome! It's like when you're building in Minecraft and need to plan each block carefully. Let me help you craft a solution!"
        
        elif "expert" in agent_id:
            return f"From a technical perspective, your question about '{user_message[:30]}...' requires careful analysis. Based on industry best practices and current methodologies, here's my recommendation..."
        
        else:
            return f"Thank you for your message about '{user_message[:30]}...'. I'll do my best to provide a helpful response based on my training and capabilities."
    
    def show_conversation_history(self, limit=10):
        """Show recent conversation history."""
        conversations_df = self.db.conversation_history.filter(
            self.db.pl.col("session_id") == self.current_session
        ).sort("timestamp", descending=True).head(limit)
        
        print(f"\n💬 Recent Conversation (Session: {self.current_session}):")
        
        for row in conversations_df.iter_rows(named=True):
            agent_id = row["agent_id"]
            content = row["content"]
            timestamp = row["timestamp"]
            
            # Format display
            time_str = timestamp.strftime("%H:%M:%S")
            icon = "👤" if agent_id == "user" else "🤖"
            
            print(f"  {time_str} {icon} {agent_id}: {content}")
        
        if conversations_df.height == 0:
            print("  (No messages in this session yet)")
    
    def get_stats(self):
        """Show app usage statistics."""
        print(f"\n📊 Chat App Statistics:")
        
        # Total messages in current session
        session_messages = self.db.conversation_history.filter(
            self.db.pl.col("session_id") == self.current_session
        ).height
        
        # Total messages across all sessions
        total_messages = self.db.conversation_history.height
        
        # Agent usage
        agent_usage = self.db.conversation_history.filter(
            self.db.pl.col("agent_id") != "user"
        ).group_by("agent_id").agg([
            self.db.pl.col("content").count().alias("message_count")
        ]).sort("message_count", descending=True)
        
        print(f"  • Current session messages: {session_messages}")
        print(f"  • Total messages: {total_messages}")
        print(f"  • Available agents: {len(self.available_agents)}")
        
        print("\n  Agent usage:")
        for row in agent_usage.iter_rows(named=True):
            print(f"    • {row['agent_id']}: {row['message_count']} responses")

def demo_chat_application():
    """Interactive chat application demo."""
    
    app = SimpleChatApp()
    
    print("🎉 Welcome to AMS-DB Simple Chat App!")
    print("Type 'help' for commands, 'quit' to exit")
    
    while True:
        print("\n" + "="*50)
        command = input("Enter command (help/list/chat/history/stats/quit): ").strip().lower()
        
        if command == "quit":
            print("👋 Goodbye!")
            break
        
        elif command == "help":
            print("\n📋 Available Commands:")
            print("  • list - Show available agents")
            print("  • chat - Start chatting with an agent")
            print("  • history - Show conversation history")
            print("  • stats - Show usage statistics")
            print("  • quit - Exit the application")
        
        elif command == "list":
            app.list_agents()
        
        elif command == "chat":
            print("\n💬 Chat Mode (type 'back' to return to main menu)")
            app.list_agents()
            
            while True:
                agent_id = input("Choose agent ID: ").strip()
                if agent_id.lower() == "back":
                    break
                
                if agent_id in app.available_agents:
                    print(f"\n🤖 Chatting with {app.available_agents[agent_id]['name']}")
                    print("Type 'back' to choose different agent, 'menu' for main menu")
                    
                    while True:
                        user_message = input("\nYou: ").strip()
                        
                        if user_message.lower() == "back":
                            break
                        elif user_message.lower() == "menu":
                            break
                        elif user_message:
                            response = app.send_message(agent_id, user_message)
                            print(f"\n{app.available_agents[agent_id]['name']}: {response}")
                    
                    if user_message.lower() == "menu":
                        break
                else:
                    print(f"❌ Agent '{agent_id}' not found!")
        
        elif command == "history":
            app.show_conversation_history()
        
        elif command == "stats":
            app.get_stats()
        
        else:
            print("❌ Unknown command. Type 'help' for available commands.")

def main():
    """Run the chat application demo."""
    
    # Check if we have agents available
    db = PolarsDBHandler()
    agents_df = db.agent_matrix
    
    if agents_df.height == 0:
        print("⚠️ No agents found! Please run simple_demo.py first to create some agents.")
        return
    
    print(f"✅ Found {agents_df.height} agents in database")
    
    # Start the demo
    demo_chat_application()

if __name__ == "__main__":
    main()
```

### Step 2: Run the Chat Application

```bash
python chat_app_demo.py
```

This creates an interactive chat interface where you can:
- List available agents
- Chat with different agents
- See conversation history
- View usage statistics

## 🎓 Graduation Challenge

Now that you've learned the basics, try this challenge to test your understanding:

### Challenge: Create a Study Buddy System

**Goal**: Create a system where students can get help from multiple AI tutors with different specialties.

**Requirements**:
1. Create at least 3 specialized tutor agents (math, english, history, etc.)
2. Each agent should have appropriate knowledge in their domain
3. Generate study sessions where tutors collaborate on complex topics
4. Export study sessions as training data for future AI tutors

**Bonus Points**:
- Add a "guidance counselor" agent that coordinates between tutors
- Create a web interface using the REST API
- Implement a knowledge-sharing system between agents
- Add progress tracking and analytics

**Hints**:
- Look at how we created the science teacher agent
- Use the conversation generator for multi-agent tutoring sessions
- Export data in JSONL format for training
- Use the CLI for quick testing

### Solution Template

Create `study_buddy_challenge.py` and implement your solution:

```python
# study_buddy_challenge.py
# Your solution here!

from src.ams_db.core.base_agent_config import AgentConfig
from src.ams_db.core.polars_db import PolarsDBHandler
from src.ams_db.core.conversation_generator import ConversationGenerator
# ... more imports as needed

def create_math_tutor():
    """Create specialized math tutor agent."""
    # Your implementation here
    pass

def create_english_tutor():
    """Create specialized english tutor agent.""" 
    # Your implementation here
    pass

# Add more tutors...

def generate_study_session():
    """Generate collaborative tutoring session."""
    # Your implementation here
    pass

def main():
    """Run the study buddy system."""
    # Your implementation here
    pass

if __name__ == "__main__":
    main()
```

## 🎉 Congratulations!

You've completed the AMS-DB hands-on tutorial! You now know how to:

✅ Set up and configure AMS-DB  
✅ Create custom AI agents with unique personalities  
✅ Generate multi-agent conversations  
✅ Export training data for machine learning  
✅ Use CLI and API interfaces  
✅ Integrate AMS-DB into applications  
✅ Analyze conversation patterns and data  

### Next Steps

1. **Explore the Codebase**: Dive deeper into the source code
2. **Build Your Own Project**: Use AMS-DB for your specific use case
3. **Contribute**: Help improve AMS-DB with new features
4. **Join the Community**: Share your creations and get help

### Resources for Further Learning

- **Code Examples**: `examples/` directory
- **Architecture Guide**: `docs/ARCHITECTURE.md` 
- **API Documentation**: Run the API server and visit `/docs`
- **Test Cases**: `tests/` directory for usage examples

Happy coding! 🚀
