# AMS-DB: Code Architecture Deep Dive

This guide explains how AMS-DB works under the hood, perfect for developers who want to understand or extend the system.

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interfaces                         │
├─────────────────┬─────────────────┬─────────────────────────┤
│   CLI Interface │   REST API      │   Python Library       │
│   (Click-based) │   (FastAPI)     │   (Direct Import)       │
└─────────────────┴─────────────────┴─────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Core Business Logic                      │
├─────────────────┬─────────────────┬─────────────────────────┤
│ AgentConfig     │ PolarsDBHandler │ ConversationGenerator   │
│ (Personalities) │ (Data Storage)  │ (Multi-agent Chats)     │
└─────────────────┴─────────────────┴─────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Storage Layer                            │
├─────────────────┬─────────────────┬─────────────────────────┤
│ Polars DataFrames│ Graphiti RAG   │ File System            │
│ (Structured Data)│ (Knowledge)     │ (Configs & Exports)     │
└─────────────────┴─────────────────┴─────────────────────────┘
```

## 📁 Detailed Code Structure

### Core Components (`src/ams_db/core/`)

#### 1. `base_agent_config.py` - Agent Personality System

**Purpose**: Manages agent configurations and personalities

```python
class AgentConfig:
    """
    Central class for managing agent personalities and configurations.
    
    Key Responsibilities:
    - Store agent prompts (system, booster, vision, prime directive)
    - Manage modality flags (TTS, STT, vision, etc.)
    - Handle model configurations (LLM, embedding, vision models)
    - Serialize/deserialize configurations to/from JSON
    """
    
    def __init__(self, agent_id: str = ""):
        # Creates unified config structure matching original format
        self.config = {
            "agent_id": agent_id,
            "model_config": {...},      # Model settings
            "prompt_config": {...},     # Agent personalities
            "command_flags": {...},     # Feature toggles
            "databases": {...},         # Database paths
            "database_config": {...}    # Advanced DB settings
        }
```

**Key Methods Explained:**

```python
def set_prompt(self, prompt_type: str, prompt_text: str):
    """
    Set agent personality prompts.
    
    prompt_type options:
    - "llmSystem": Main personality prompt
    - "llmBooster": Enhanced reasoning prompt  
    - "visionSystem": Visual analysis prompt
    - "visionBooster": Enhanced vision prompt
    - "primeDirective": Core mission statement
    """

def set_modality_flag(self, flag_name: str, value: bool):
    """
    Enable/disable agent capabilities.
    
    Important flags:
    - LLM_SYSTEM_PROMPT_FLAG: Use system prompt
    - EMBEDDING_FLAG: Enable semantic search
    - AGENT_FLAG: Agent is active
    - TTS_FLAG: Text-to-speech
    - STT_FLAG: Speech-to-text
    """

def update_config(self, updates: Dict[str, Any]):
    """
    Deep merge configuration updates.
    Handles nested dictionary updates gracefully.
    """
```

**Configuration Format Deep Dive:**

```python
{
    "agent_id": "wizard_agent_001",
    
    # Model configurations for different AI capabilities
    "model_config": {
        "largeLanguageModel": {
            "names": ["llama3.1:70b", "qwen2.5:32b"],
            "instances": ["primary", "backup"],
            "model_config_template": {
                "temperature": 0.7,    # Creativity level
                "max_tokens": 4096,    # Response length
                "top_p": 0.9          # Token selection strategy
            }
        },
        "embeddingModel": {
            "names": ["nomic-embed-text"],
            "instances": ["primary"],
            "model_config_template": {
                "dimension": 768,      # Vector size
                "normalize": True      # Normalize vectors
            }
        }
    },
    
    # Agent personality and behavior prompts
    "prompt_config": {
        "userInput": "",           # Latest user message
        "agent": {
            "llmSystem": "🧙‍♂️ I am a mystical wizard...",     # Main personality
            "llmBooster": "When solving problems...",          # Enhanced reasoning
            "visionSystem": "When analyzing images...",        # Visual analysis
            "visionBooster": "For detailed visual analysis..." # Enhanced vision
        },
        "primeDirective": "Guide users through mystical programming arts..." # Core mission
    },
    
    # Feature flags for different capabilities
    "command_flags": {
        "TTS_FLAG": False,              # Text-to-speech
        "STT_FLAG": False,              # Speech-to-text
        "LLAVA_FLAG": False,            # Vision-language model
        "EMBEDDING_FLAG": True,         # Semantic search
        "AGENT_FLAG": True,             # Agent is active
        "LLM_SYSTEM_PROMPT_FLAG": True  # Use system prompt
    },
    
    # Database file paths for different data types
    "databases": {
        "agent_matrix": "wizard_agents.parquet",
        "conversation_history": "wizard_conversations.parquet",
        "knowledge_base": "wizard_knowledge.parquet",
        "research_collection": "wizard_research.parquet",
        "template_files": "wizard_templates.parquet"
    },
    
    # Advanced database configurations
    "database_config": {
        "conversation_modes": {
            "current_session_only": False,     # Include conversation history
            "use_past_conversations": True,     # Learn from past
            "max_history_turns": 100           # Memory limit
        },
        "knowledge_base_categories": [          # Knowledge organization
            "magical_algorithms",
            "arcane_architectures", 
            "mystical_patterns"
        ],
        "research_collection_fields": {         # Research domains
            "creative_coding": {"enabled": True, "priority": "high"},
            "algorithm_design": {"enabled": True, "priority": "medium"}
        }
    }
}
```

#### 2. `polars_db.py` - High-Performance Database

**Purpose**: Manages all data storage using Polars DataFrames

```python
class PolarsDBHandler:
    """
    High-performance database using Polars DataFrames.
    
    Key Features:
    - Lightning-fast data operations (10-100x faster than Pandas)
    - Memory-efficient handling of large datasets
    - Multiple export formats (CSV, Parquet, JSONL)
    - Automatic schema validation
    - Thread-safe operations
    """
```

**Database Schema:**

```python
# 1. Agent Matrix - Stores agent configurations
agent_matrix_schema = {
    "agent_id": pl.Utf8,           # Unique identifier
    "agent_name": pl.Utf8,         # Human-readable name  
    "created_at": pl.Datetime,     # Creation timestamp
    "updated_at": pl.Datetime,     # Last modification
    "config_json": pl.Utf8,        # Full agent configuration
    "description": pl.Utf8,        # Agent description
    "tags": pl.List(pl.Utf8),      # Searchable tags
    "is_active": pl.Boolean        # Active/inactive status
}

# 2. Conversation History - Multi-agent dialogue storage
conversation_schema = {
    "conversation_id": pl.Utf8,    # Conversation identifier
    "agent_id": pl.Utf8,           # Speaking agent
    "message_id": pl.Utf8,         # Unique message ID
    "timestamp": pl.Datetime,      # When message was sent
    "role": pl.Utf8,               # "user", "assistant", "system"
    "content": pl.Utf8,            # Message content
    "message_type": pl.Utf8,       # "text", "image", "audio"
    "metadata": pl.Utf8,           # JSON metadata
    "session_id": pl.Utf8          # Session grouping
}

# 3. Knowledge Base - Searchable information storage
knowledge_schema = {
    "kb_id": pl.Utf8,              # Knowledge base ID
    "agent_id": pl.Utf8,           # Owner agent
    "document_id": pl.Utf8,        # Document identifier
    "title": pl.Utf8,              # Document title
    "content": pl.Utf8,            # Full text content
    "content_type": pl.Utf8,       # "text", "code", "image"
    "source": pl.Utf8,             # Content source/category
    "tags": pl.List(pl.Utf8),      # Searchable tags
    "metadata": pl.Utf8,           # JSON metadata
    "created_at": pl.Datetime,     # Creation time
    "embedding": pl.List(pl.Float32) # Vector embedding for search
}
```

**Key Operations:**

```python
def add_agent_config(self, agent_config: Dict[str, Any], 
                    agent_name: str = None, description: str = "") -> str:
    """
    Add new agent to the system.
    
    Process:
    1. Generate unique agent_id if not provided
    2. Serialize configuration to JSON
    3. Add to agent_matrix DataFrame
    4. Return agent_id for reference
    """

def add_conversation_message(self, agent_id: str, role: str, content: str,
                           session_id: str = None, metadata: Dict = None) -> str:
    """
    Record a conversation message.
    
    Process:
    1. Generate unique message_id
    2. Create conversation_id from agent + session
    3. Store with timestamp and metadata
    4. Update conversation_history DataFrame
    """

def add_knowledge_document(self, agent_id: str, title: str, content: str,
                         content_type: str = "text", metadata: Dict = None) -> str:
    """
    Add knowledge to agent's knowledge base.
    
    Process:
    1. Generate document and kb IDs
    2. Create text embedding for semantic search
    3. Store in knowledge_base DataFrame
    4. Update search indexes
    """
```

**Performance Optimizations:**

```python
# Lazy evaluation - only process when needed
lazy_df = pl.scan_parquet("large_dataset.parquet")
result = lazy_df.filter(pl.col("agent_id") == "wizard_001").collect()

# Parallel processing - use all CPU cores
df.group_by("agent_id").agg([
    pl.col("message").count().alias("message_count"),
    pl.col("timestamp").max().alias("last_active")
])

# Memory-efficient streaming for large datasets
for batch in pl.read_csv_batched("huge_file.csv", batch_size=10000):
    process_batch(batch)
```

#### 3. `conversation_generator.py` - Multi-Agent Dialogue System

**Purpose**: Generate conversations between agents for training and demonstration

```python
class ConversationGenerator:
    """
    Generate multi-agent conversations with distinct personalities.
    
    Key Features:
    - Multi-agent dialogue simulation
    - Personality-driven responses
    - Knowledge-aware conversation
    - JSONL export for ML training
    - Configurable conversation parameters
    """
    
    def __init__(self, db_handler: PolarsDBHandler, graphiti_framework: GraphitiRAGFramework):
        self.db = db_handler
        self.graphiti = graphiti_framework
```

**Conversation Generation Process:**

```python
def generate_conversation(self, agents: List[str], topic: str, num_turns: int = 10) -> Dict:
    """
    Generate multi-agent conversation.
    
    Algorithm:
    1. Load agent configurations and personalities
    2. For each turn:
       a. Select next agent (round-robin or smart selection)
       b. Retrieve relevant knowledge from agent's KB
       c. Generate response using agent's personality + knowledge
       d. Store turn in database
    3. Return complete conversation structure
    """
    
    conversation = {
        "conversation_id": str(uuid.uuid4()),
        "topic": topic,
        "participants": agents,
        "turns": [],
        "metadata": {...}
    }
    
    for turn in range(num_turns):
        current_agent = agents[turn % len(agents)]
        
        # Get agent's personality and knowledge
        agent_config = self._get_agent_config(current_agent)
        knowledge_context = self.graphiti.search_knowledge(current_agent, topic)
        
        # Generate response based on personality
        response = self._generate_turn(
            agent_id=current_agent,
            agent_config=agent_config,
            topic=topic,
            previous_turns=conversation["turns"],
            knowledge_context=knowledge_context
        )
        
        conversation["turns"].append(response)
        self._store_conversation_turn(conversation["conversation_id"], response)
    
    return conversation
```

**Personality-Driven Response Generation:**

```python
def _generate_turn(self, agent_id: str, agent_config: Dict, topic: str, 
                  previous_turns: List, knowledge_context: List) -> Dict:
    """
    Generate agent response based on personality.
    
    Process:
    1. Extract agent personality from config
    2. Build context from previous turns
    3. Incorporate relevant knowledge
    4. Generate response in agent's style
    5. Add metadata (word count, sentiment, etc.)
    """
    
    # Extract personality traits
    system_prompt = agent_config["prompt_config"]["agent"]["llmSystem"]
    prime_directive = agent_config["prompt_config"]["primeDirective"]
    
    # Build conversation context
    context = "\n".join([
        f"{turn['agent_id']}: {turn['content']}" 
        for turn in previous_turns[-3:]  # Last 3 turns
    ])
    
    # Incorporate knowledge
    knowledge_text = "\n".join([
        f"- {entry['title']}: {entry['content'][:200]}..." 
        for entry in knowledge_context
    ])
    
    # Generate response (simulated - replace with actual LLM call)
    response_content = self._simulate_agent_response(
        agent_id=agent_id,
        personality=system_prompt,
        topic=topic,
        context=context,
        knowledge=knowledge_text
    )
    
    return {
        "turn_number": len(previous_turns),
        "agent_id": agent_id,
        "content": response_content,
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "word_count": len(response_content.split()),
            "knowledge_entries_used": len(knowledge_context),
            "personality_type": agent_config.get("agent_type", "unknown")
        }
    }
```

**JSONL Export for ML Training:**

```python
def export_conversation_jsonl(self, conversation_id: str, output_path: str) -> str:
    """
    Export conversation in JSONL format for machine learning training.
    
    JSONL Format:
    {"conversation_id": "conv_123", "turn_number": 0, "agent_id": "wizard_001", 
     "message": "🧙‍♂️ Greetings!", "timestamp": "2024-01-01T10:00:00", 
     "metadata": {"agent_type": "wizard", "word_count": 2}}
    {"conversation_id": "conv_123", "turn_number": 1, "agent_id": "expert_001",
     "message": "Hello. Let's discuss the technical aspects.", 
     "timestamp": "2024-01-01T10:00:05", "metadata": {"agent_type": "expert", "word_count": 7}}
    """
    
    conversation_df = self.db.get_conversation_history(conversation_id)
    
    jsonl_lines = []
    for row in conversation_df.iter_rows(named=True):
        entry = {
            "conversation_id": row["conversation_id"],
            "turn_number": row["turn_number"],
            "agent_id": row["agent_id"],
            "message": row["message"],
            "timestamp": row["timestamp"],
            "metadata": json.loads(row["metadata"]) if row["metadata"] else {}
        }
        jsonl_lines.append(json.dumps(entry, ensure_ascii=False))
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(jsonl_lines))
    
    return output_path
```

#### 4. `graphiti_pipe.py` - Knowledge Graph Management

**Purpose**: Integrates Graphiti for intelligent knowledge management

```python
class GraphitiRAGFramework:
    """
    Knowledge graph and RAG (Retrieval-Augmented Generation) system.
    
    Key Features:
    - Temporal knowledge graphs
    - Semantic search and retrieval
    - Context-aware knowledge linking
    - Agent-specific knowledge isolation
    - Conversation memory management
    """
```

**Knowledge Graph Structure:**

```
[Agent] ──has_knowledge──> [Knowledge_Entry]
   │                           │
   └──participates_in──> [Conversation] ──mentions──> [Topic]
                              │                        │
                              └──occurs_at──> [Time] ──relates_to──> [Context]
```

### Interface Layer

#### CLI Interface (`src/ams_db/cli/main.py`)

**Purpose**: Command-line interface for system management

```python
# Built with Click framework for intuitive commands
@click.group()
def app():
    """AMS-DB: Agentic Multimodal Super-alignment Database CLI"""

@app.group()
def agent():
    """Agent management commands"""

@agent.command()
def list():
    """List all agents"""
    db_handler = PolarsDBHandler()
    agents_df = db_handler.agent_matrix
    
    for row in agents_df.iter_rows(named=True):
        click.echo(f"• {row['agent_name']} ({row['agent_id']})")
        click.echo(f"  Created: {row['created_at']}")
        click.echo(f"  Description: {row['description']}")

@app.group() 
def conversation():
    """Conversation generation and management commands"""

@conversation.command()
@click.option('--agents', required=True, help='Comma-separated agent IDs')
@click.option('--topic', required=True, help='Conversation topic')
@click.option('--turns', default=10, help='Number of turns')
@click.option('--output', help='Output file (optional)')
def generate(agents: str, topic: str, turns: int, output: str):
    """Generate multi-agent conversation"""
    # Implementation handles conversation generation...
```

#### REST API (`src/ams_db/api/main.py`)

**Purpose**: Web API for external integrations

```python
# Built with FastAPI for high-performance web API
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="AMS-DB API", version="1.0.0")

class AgentCreateRequest(BaseModel):
    agent_id: str
    name: str
    description: str = ""
    config: dict = {}

@app.post("/agents", response_model=dict)
async def create_agent(request: AgentCreateRequest):
    """Create new agent"""
    db_handler = PolarsDBHandler()
    
    # Create agent configuration
    agent_config = AgentConfig(request.agent_id)
    agent_config.update_config(request.config)
    
    # Store in database
    agent_id = db_handler.add_agent_config(
        agent_config=agent_config.get_config(),
        agent_name=request.name,
        description=request.description
    )
    
    return {"agent_id": agent_id, "status": "created"}

@app.get("/agents", response_model=List[dict])
async def list_agents():
    """Get all agents"""
    db_handler = PolarsDBHandler()
    agents_df = db_handler.agent_matrix
    
    return [
        {
            "agent_id": row["agent_id"],
            "name": row["agent_name"],
            "description": row["description"],
            "created_at": row["created_at"].isoformat(),
            "is_active": row["is_active"]
        }
        for row in agents_df.iter_rows(named=True)
    ]

class ConversationRequest(BaseModel):
    agents: List[str]
    topic: str
    num_turns: int = 10

@app.post("/conversations/generate", response_model=dict)
async def generate_conversation(request: ConversationRequest):
    """Generate multi-agent conversation"""
    db_handler = PolarsDBHandler()
    graphiti_framework = GraphitiRAGFramework(db_handler)
    generator = ConversationGenerator(db_handler, graphiti_framework)
    
    conversation = generator.generate_conversation(
        agents=request.agents,
        topic=request.topic,
        num_turns=request.num_turns
    )
    
    return {
        "conversation_id": conversation["conversation_id"],
        "participants": conversation["participants"],
        "topic": conversation["topic"],
        "turns": len(conversation["turns"]),
        "status": "generated"
    }
```

## 🔄 Data Flow Examples

### Creating an Agent

```python
# 1. User creates agent via CLI/API/Python
agent_config = AgentConfig("wizard_001")
agent_config.set_prompt("llmSystem", "🧙‍♂️ I am a mystical wizard...")

# 2. Configuration stored in database
db_handler = PolarsDBHandler()
agent_id = db_handler.add_agent_config(
    agent_config=agent_config.get_config(),
    agent_name="Mystical Wizard",
    description="Creative coding assistant"
)

# 3. Agent is now available for conversations
# agent_matrix DataFrame updated with new row
# config_json column contains serialized configuration
```

### Generating Conversation

```python
# 1. User requests conversation
generator = ConversationGenerator(db_handler, graphiti_framework)
conversation = generator.generate_conversation(
    agents=["wizard_001", "expert_001"],
    topic="Database Design",
    num_turns=6
)

# 2. System processes each turn:
for turn in range(6):
    current_agent = agents[turn % 2]  # Alternate speakers
    
    # Get agent personality
    agent_config = db_handler.get_agent_config(current_agent)
    
    # Search knowledge base
    knowledge = graphiti_framework.search_knowledge(current_agent, "Database Design")
    
    # Generate response based on personality + knowledge
    response = generate_agent_response(agent_config, knowledge, previous_context)
    
    # Store in conversation_history DataFrame
    db_handler.add_conversation_message(
        agent_id=current_agent,
        content=response,
        session_id=conversation_id
    )

# 3. Export for training
generator.export_conversation_jsonl(
    conversation_id=conversation["conversation_id"],
    output_path="training_data.jsonl"
)
```

### Knowledge Search and Retrieval

```python
# 1. Agent needs knowledge during conversation
query = "How to optimize database queries?"
agent_id = "expert_001"

# 2. System searches knowledge base
knowledge_df = db_handler.knowledge_base.filter(
    pl.col("agent_id") == agent_id
)

# 3. Semantic search using embeddings
query_embedding = embed_text(query)
knowledge_with_scores = knowledge_df.with_columns([
    cosine_similarity(pl.col("embedding"), query_embedding).alias("similarity")
]).sort("similarity", descending=True)

# 4. Return top relevant entries
relevant_knowledge = knowledge_with_scores.head(5).to_dicts()

# 5. Use in conversation generation
context = "\n".join([
    f"- {entry['title']}: {entry['content'][:200]}..."
    for entry in relevant_knowledge
])
```

## 🚀 Performance Considerations

### Memory Management

```python
# Efficient data loading
df = pl.scan_parquet("large_dataset.parquet")  # Lazy loading
result = df.select(["agent_id", "timestamp"]).collect()  # Select only needed columns

# Batch processing for large datasets
def process_large_conversation_dataset(file_path: str):
    for batch in pl.read_csv_batched(file_path, batch_size=10000):
        # Process each batch independently
        processed = batch.group_by("conversation_id").agg([
            pl.col("message").count().alias("message_count")
        ])
        yield processed
```

### Database Optimization

```python
# Use appropriate data types
schema = {
    "agent_id": pl.Utf8,           # String data
    "timestamp": pl.Datetime,      # Temporal data
    "is_active": pl.Boolean,       # Boolean flags
    "score": pl.Float32,           # Numeric data (32-bit sufficient)
    "embedding": pl.List(pl.Float32)  # Vector data
}

# Efficient filtering and aggregation
result = df.lazy().filter(
    (pl.col("timestamp") > datetime(2024, 1, 1)) &
    (pl.col("is_active") == True)
).group_by("agent_id").agg([
    pl.col("message").count(),
    pl.col("timestamp").max()
]).collect()
```

### Concurrent Operations

```python
# Thread-safe database operations
import threading
from concurrent.futures import ThreadPoolExecutor

class ThreadSafePolarsDB(PolarsDBHandler):
    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
    
    def add_conversation_message(self, *args, **kwargs):
        with self._lock:
            return super().add_conversation_message(*args, **kwargs)

# Parallel conversation generation
def generate_multiple_conversations(topics: List[str], agents: List[str]):
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(generator.generate_conversation, agents, topic, 10)
            for topic in topics
        ]
        
        conversations = [future.result() for future in futures]
    return conversations
```

## 🧪 Testing Strategy

### Unit Tests

```python
# Test agent configuration
def test_agent_config_creation():
    config = AgentConfig("test_agent")
    assert config.config["agent_id"] == "test_agent"
    assert "model_config" in config.config
    assert "prompt_config" in config.config

def test_prompt_setting():
    config = AgentConfig("test_agent")
    config.set_prompt("llmSystem", "Test prompt")
    assert config.config["prompt_config"]["agent"]["llmSystem"] == "Test prompt"

# Test database operations  
def test_database_operations():
    db = PolarsDBHandler()
    
    # Test agent creation
    agent_config = AgentConfig("test_agent").get_config()
    agent_id = db.add_agent_config(agent_config, "Test Agent")
    assert agent_id == "test_agent"
    
    # Test conversation storage
    message_id = db.add_conversation_message(
        agent_id="test_agent",
        role="assistant", 
        content="Hello, world!"
    )
    assert message_id is not None

# Test conversation generation
def test_conversation_generation():
    db = PolarsDBHandler()
    graphiti = GraphitiRAGFramework(db)
    generator = ConversationGenerator(db, graphiti)
    
    conversation = generator.generate_conversation(
        agents=["test_agent_1", "test_agent_2"],
        topic="Test Topic",
        num_turns=4
    )
    
    assert len(conversation["turns"]) == 4
    assert conversation["topic"] == "Test Topic"
```

### Integration Tests

```python
def test_full_workflow():
    """Test complete agent creation -> conversation -> export workflow"""
    
    # 1. Create agents
    db = PolarsDBHandler()
    wizard_config = AgentConfig("wizard_test")
    wizard_config.set_prompt("llmSystem", "🧙‍♂️ Test wizard prompt")
    
    expert_config = AgentConfig("expert_test") 
    expert_config.set_prompt("llmSystem", "Expert test prompt")
    
    db.add_agent_config(wizard_config.get_config(), "Test Wizard")
    db.add_agent_config(expert_config.get_config(), "Test Expert")
    
    # 2. Generate conversation
    graphiti = GraphitiRAGFramework(db)
    generator = ConversationGenerator(db, graphiti)
    
    conversation = generator.generate_conversation(
        agents=["wizard_test", "expert_test"],
        topic="Test Integration",
        num_turns=6
    )
    
    # 3. Export conversation
    export_path = generator.export_conversation_jsonl(
        conversation_id=conversation["conversation_id"],
        output_path="test_export.jsonl"
    )
    
    # 4. Verify export
    assert os.path.exists(export_path)
    with open(export_path) as f:
        lines = f.readlines()
        assert len(lines) == 6  # 6 turns
        
        # Verify JSONL format
        for line in lines:
            data = json.loads(line)
            assert "conversation_id" in data
            assert "agent_id" in data
            assert "message" in data
```

## 🔧 Extension Points

### Adding New Agent Personalities

```python
def create_custom_agent():
    """Example: Creating a scientist agent personality"""
    config = AgentConfig(agent_id="scientist_001")
    
    scientist_prompt = """
    You are Dr. Sarah Chen, a brilliant research scientist specializing in 
    computational biology and data analysis. You approach problems with 
    rigorous scientific methodology and clear explanations.
    
    Your characteristics:
    - Evidence-based reasoning
    - Precise scientific terminology
    - Step-by-step hypothesis testing
    - Data-driven conclusions
    """
    
    config.set_prompt("llmSystem", scientist_prompt)
    config.set_prompt("primeDirective", 
                     "Advance scientific understanding through rigorous analysis")
    
    # Configure for research-heavy workflows
    config.set_modality_flag("EMBEDDING_FLAG", True)
    config.set_modality_flag("LLM_SYSTEM_PROMPT_FLAG", True)
    
    # Set research-focused database config
    config.update_config({
        "database_config": {
            "research_collection_fields": {
                "computational_biology": {"enabled": True, "priority": "high"},
                "data_analysis": {"enabled": True, "priority": "high"},
                "scientific_methodology": {"enabled": True, "priority": "medium"}
            }
        }
    })
    
    return config
```

### Custom Export Formats

```python
def export_conversation_markdown(conversation_id: str, output_path: str) -> str:
    """Export conversation in Markdown format for documentation"""
    
    db = PolarsDBHandler()
    conversation_df = db.get_conversation_history(conversation_id)
    
    markdown_lines = [
        f"# Conversation: {conversation_id}",
        f"Generated: {datetime.now().isoformat()}",
        ""
    ]
    
    for row in conversation_df.iter_rows(named=True):
        agent_id = row["agent_id"]
        message = row["message"]
        timestamp = row["timestamp"]
        
        markdown_lines.extend([
            f"## {agent_id}",
            f"*{timestamp}*",
            "",
            message,
            ""
        ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(markdown_lines))
    
    return output_path

def export_conversation_xml(conversation_id: str, output_path: str) -> str:
    """Export conversation in XML format for structured analysis"""
    
    db = PolarsDBHandler()
    conversation_df = db.get_conversation_history(conversation_id)
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<conversation id="{conversation_id}">',
        f'  <generated>{datetime.now().isoformat()}</generated>',
        '  <turns>'
    ]
    
    for row in conversation_df.iter_rows(named=True):
        xml_lines.extend([
            '    <turn>',
            f'      <agent_id>{row["agent_id"]}</agent_id>',
            f'      <timestamp>{row["timestamp"]}</timestamp>',
            f'      <message><![CDATA[{row["message"]}]]></message>',
            '    </turn>'
        ])
    
    xml_lines.extend(['  </turns>', '</conversation>'])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))
    
    return output_path
```

### Custom Knowledge Retrievers

```python
class SemanticKnowledgeRetriever:
    """Advanced semantic search for knowledge retrieval"""
    
    def __init__(self, db_handler: PolarsDBHandler):
        self.db = db_handler
        self.embedding_model = self._load_embedding_model()
    
    def search_knowledge(self, agent_id: str, query: str, 
                        limit: int = 5, similarity_threshold: float = 0.7) -> List[Dict]:
        """
        Advanced semantic search with similarity scoring.
        """
        # Get query embedding
        query_embedding = self.embedding_model.encode(query)
        
        # Search knowledge base
        knowledge_df = self.db.knowledge_base.filter(
            pl.col("agent_id") == agent_id
        )
        
        # Calculate similarities
        similarities = []
        for row in knowledge_df.iter_rows(named=True):
            content_embedding = np.array(row["embedding"])
            similarity = cosine_similarity(query_embedding, content_embedding)
            
            if similarity >= similarity_threshold:
                similarities.append({
                    "document_id": row["document_id"],
                    "title": row["title"],
                    "content": row["content"],
                    "similarity": similarity,
                    "metadata": json.loads(row["metadata"])
                })
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities[:limit]
    
    def _load_embedding_model(self):
        """Load sentence embedding model"""
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer('all-MiniLM-L6-v2')

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

This architecture guide provides Owen with a comprehensive understanding of how AMS-DB works internally, from high-level concepts down to implementation details. The code examples show both current functionality and extension points for future development.
