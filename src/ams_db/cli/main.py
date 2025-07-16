"""
AMS-DB Command Line Interface

Main CLI entry point for managing agents, databases, and knowledge bases.
"""

import asyncio
import json
import random
import click
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..core import AgentConfig, PolarsDBHandler, GraphitiRAGFramework
from ..core.conversation_generator import ConversationGenerator
from ..core.conversation_modes import ConversationModes


@click.group()
@click.version_option()
def app():
    """🧙‍♂️ AMS-DB: Agentic Multimodal Super-alignment Database CLI"""
    pass


@app.group()
def agent():
    """👤 Agent management commands"""
    pass


@app.group()
def db():
    """💾 Database management commands"""
    pass


@app.group()
def knowledge():
    """📚 Knowledge base management commands"""
    pass


@app.group()
def chat():
    """💬 Interactive conversation commands"""
    pass


@app.group()
def conversation():
    """🤖 Multi-agent conversation generation"""
    pass


@app.group()
def export():
    """📤 Export data commands"""
    pass


# ===== CHAT COMMANDS (NEW!) =====
@chat.command()
@click.argument('agent_id')
@click.option('--session-name', help='Optional session name for organization')
def start(agent_id: str, session_name: str):
    """🗣️ Start a chat with an agent"""
    db_handler = PolarsDBHandler()
    conv_modes = ConversationModes(db_handler)
    
    try:
        session_id = conv_modes.start_human_chat(agent_id, session_name)
        click.echo(f"✅ Started chat with {agent_id}")
        click.echo(f"📋 Session ID: {session_id}")
        click.echo(f"💡 Use 'ams-db chat send {session_id} \"your message\"' to continue")
        
        # Show agent info
        agent_config = db_handler.get_agent_config(agent_id)
        if agent_config:
            personality = agent_config.get("prompt_config", {}).get("primeDirective", "")
            if personality:
                click.echo(f"🎭 Agent Personality: {personality[:100]}...")
                
    except Exception as e:
        click.echo(f"❌ Failed to start chat: {e}")


@chat.command()
@click.argument('session_id')
@click.argument('message')
def send(session_id: str, message: str):
    """📤 Send a message in a chat session"""
    db_handler = PolarsDBHandler()
    conv_modes = ConversationModes(db_handler)
    
    try:
        # Get session info to find the agent
        history = conv_modes.get_conversation_history(session_id, format="messages")
        if "error" in history:
            click.echo(f"❌ {history['error']}")
            return
            
        # Find the agent from participants
        participants = history.get("participants", [])
        agent_id = None
        for p in participants:
            if p != "human":
                agent_id = p
                break
                
        if not agent_id:
            click.echo("❌ Could not find agent in this session")
            return
        
        response = conv_modes.send_human_message(session_id, agent_id, message)
        
        click.echo(f"\n💬 You: {message}")
        click.echo(f"🤖 {agent_id}: {response['agent_response']}")
        click.echo(f"⏰ {response['timestamp']}")
        
    except Exception as e:
        click.echo(f"❌ Failed to send message: {e}")


@chat.command()
@click.argument('session_id')
@click.option('--format', default='chat', type=click.Choice(['chat', 'jsonl', 'messages']))
def history(session_id: str, format: str):
    """📜 View chat history"""
    db_handler = PolarsDBHandler()
    conv_modes = ConversationModes(db_handler)
    
    try:
        history = conv_modes.get_conversation_history(session_id, format)
        
        if "error" in history:
            click.echo(f"❌ {history['error']}")
            return
        
        click.echo(f"\n📋 Session: {history['session_name']}")
        click.echo(f"🎭 Mode: {history['mode']}")
        click.echo(f"👥 Participants: {', '.join(history['participants'])}")
        click.echo(f"📊 Messages: {history['message_count']}")
        click.echo("─" * 50)
        
        if format == "chat":
            for msg in history['messages']:
                sender = msg['sender']
                content = msg['content']
                timestamp = str(msg['timestamp'])[:19]  # Trim microseconds
                
                if msg['role'] == 'user':
                    click.echo(f"💬 {sender}: {content}")
                else:
                    click.echo(f"🤖 {sender}: {content}")
                click.echo(f"   ⏰ {timestamp}")
                click.echo()
        else:
            click.echo(json.dumps(history, indent=2, default=str))
            
    except Exception as e:
        click.echo(f"❌ Failed to get history: {e}")


@chat.command()
@click.option('--mode', type=click.Choice(['HUMAN_CHAT', 'AGENT_TO_AGENT', 'HUMAN_AS_AGENT']))
@click.option('--agent', help='Filter by agent ID')
def list(mode: str, agent: str):
    """📋 List chat sessions"""
    db_handler = PolarsDBHandler()
    conv_modes = ConversationModes(db_handler)
    
    try:
        sessions = conv_modes.list_sessions(mode, agent)
        
        if not sessions:
            click.echo("No chat sessions found")
            return
        
        click.echo(f"\n📋 Chat Sessions ({len(sessions)} found)")
        click.echo("=" * 60)
        
        for session in sessions:
            click.echo(f"🆔 {session['session_id'][:8]}... - {session['session_name']}")
            click.echo(f"   🎭 Mode: {session['mode']}")
            click.echo(f"   👥 Participants: {', '.join(session['participants'])}")
            click.echo(f"   📊 Messages: {session['message_count']}")
            click.echo(f"   📅 Created: {str(session['created_at'])[:19]}")
            if session.get('topic'):
                click.echo(f"   💭 Topic: {session['topic']}")
            click.echo()
            
    except Exception as e:
        click.echo(f"❌ Failed to list sessions: {e}")


@chat.command()
@click.argument('human_agent_name')
@click.argument('target_agent_id')
@click.option('--session-name', help='Optional session name')
def roleplay(human_agent_name: str, target_agent_id: str, session_name: str):
    """🎭 Start roleplay as an agent talking to another agent"""
    db_handler = PolarsDBHandler()
    conv_modes = ConversationModes(db_handler)
    
    try:
        session_id = conv_modes.start_human_as_agent(human_agent_name, target_agent_id, session_name)
        click.echo(f"✅ Started roleplay session")
        click.echo(f"🎭 You are: {human_agent_name}")
        click.echo(f"🤖 Talking to: {target_agent_id}")
        click.echo(f"📋 Session ID: {session_id}")
        click.echo(f"💡 Use 'ams-db chat roleplay-send {session_id} \"your message\"' to continue")
        
    except Exception as e:
        click.echo(f"❌ Failed to start roleplay: {e}")


@chat.command()
@click.argument('session_id')
@click.argument('message')
def roleplay_send(session_id: str, message: str):
    """🎭 Send a message in roleplay mode"""
    db_handler = PolarsDBHandler()
    conv_modes = ConversationModes(db_handler)
    
    try:
        # Get session info
        history = conv_modes.get_conversation_history(session_id, format="messages")
        if "error" in history:
            click.echo(f"❌ {history['error']}")
            return
        
        # Extract roleplay info from metadata
        participants = history.get("participants", [])
        if len(participants) < 2:
            click.echo("❌ Invalid roleplay session")
            return
            
        human_agent_name = participants[0]
        target_agent_id = participants[1]
        
        response = conv_modes.send_human_as_agent_message(
            session_id, human_agent_name, target_agent_id, message
        )
        
        click.echo(f"\n🎭 {human_agent_name}: {message}")
        click.echo(f"🤖 {target_agent_id}: {response['agent_response']}")
        
    except Exception as e:
        click.echo(f"❌ Failed to send roleplay message: {e}")


# ===== EXISTING AGENT COMMANDS =====


# Agent Commands
@agent.command()
@click.argument('agent_id')
@click.option('--name', help='Agent name')
@click.option('--description', help='Agent description')
@click.option('--config-file', type=click.Path(exists=True), help='Config file path')
def create(agent_id: str, name: Optional[str], description: Optional[str], config_file: Optional[str]):
    """Create a new agent"""
    
    if config_file:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        config = AgentConfig()
        config.from_dict(config_data)
    else:
        config = AgentConfig(agent_id)
    
    # Use direct database handler to avoid async issues in CLI
    db_handler = PolarsDBHandler()
    agent_id = db_handler.add_agent_config(
        config.get_config(), 
        name or agent_id, 
        description or ""
    )
    
    click.echo(f"✅ Created agent: {agent_id}")
    click.echo("💡 For Graphiti integration, use the API or direct Python code")


@agent.command()
def list():
    """List all agents"""
    db_handler = PolarsDBHandler()
    agents = db_handler.list_agents()
    
    if agents.height == 0:
        click.echo("No agents found")
        return
    
    click.echo("\n📋 Agents:")
    for agent in agents.to_dicts():
        click.echo(f"  • {agent['agent_id']} - {agent['agent_name']}")
        click.echo(f"    Created: {agent['created_at']}")
        if agent['description']:
            click.echo(f"    Description: {agent['description']}")
        click.echo()


@agent.command()
@click.argument('agent_id')
@click.argument('output_path')
def export(agent_id: str, output_path: str):
    """Export agent configuration and data"""
    db_handler = PolarsDBHandler()
    
    try:
        # If output_path doesn't have timestamp, add it (Windows-compatible)
        if output_path.endswith('_'):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"{output_path}{timestamp}"
        
        # Create output directory if it doesn't exist
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Export agent config
        agent_config_path = output_dir / f"{agent_id}_config.json"
        db_handler.export_agent_config(agent_id, str(agent_config_path))
        
        # Export agent conversations
        conversations_path = output_dir / f"{agent_id}_conversations.jsonl"
        db_handler.export_conversations_jsonl(agent_id, str(conversations_path))
        
        click.echo(f"✅ Exported agent {agent_id} to {output_path}")
        click.echo(f"  📄 Config: {agent_config_path.name}")
        click.echo(f"  💬 Conversations: {conversations_path.name}")
        
    except Exception as e:
        click.echo(f"❌ Failed to export agent {agent_id}: {e}")


@agent.command()
@click.argument('agent_id')
@click.option('--soft', is_flag=True, help='Soft delete (deactivate)')
def delete(agent_id: str, soft: bool):
    """Delete an agent"""
    db_handler = PolarsDBHandler()
    
    try:
        db_handler.delete_agent(agent_id, soft_delete=soft)
        action = "deactivated" if soft else "deleted"
        click.echo(f"✅ Agent {agent_id} {action}")
    except Exception as e:
        click.echo(f"❌ Failed to delete agent: {e}")


# Database Commands
@db.command()
def stats():
    """Show database statistics"""
    db_handler = PolarsDBHandler()
    stats = db_handler.get_database_stats()
    
    click.echo("\n📊 Database Statistics:")
    click.echo(f"  • Agents: {stats['agent_count']} ({stats['active_agent_count']} active)")
    click.echo(f"  • Conversations: {stats['conversation_count']}")
    click.echo(f"  • Knowledge Documents: {stats['knowledge_document_count']}")
    click.echo(f"  • Research Results: {stats['research_result_count']}")
    click.echo(f"  • Templates: {stats['template_count']}")
    click.echo(f"  • Database Size: {stats['database_size_mb']:.2f} MB")


@db.command()
@click.argument('backup_path')
def backup(backup_path: str):
    """Create a database backup"""
    db_handler = PolarsDBHandler()
    
    try:
        db_handler.export_database_backup(backup_path)
        click.echo(f"✅ Database backed up to {backup_path}")
    except Exception as e:
        click.echo(f"❌ Backup failed: {e}")


@db.command()
def init():
    """Initialize a new database"""
    try:
        db_handler = PolarsDBHandler()
        click.echo("✅ Database initialized")
        
        # Note: Predefined agents creation disabled in CLI due to async requirements
        # Use the API or direct Python code for full Graphiti integration
        click.echo("💡 Use the API or Python code for Graphiti-enabled agents")
        
    except Exception as e:
        click.echo(f"❌ Initialization failed: {e}")


# Knowledge Base Commands
@knowledge.command()
@click.argument('agent_id')
@click.argument('title')
@click.argument('content_file', type=click.Path(exists=True))
@click.option('--content-type', default='text', help='Content type')
@click.option('--source', help='Content source')
@click.option('--tags', help='Comma-separated tags')
def add(agent_id: str, title: str, content_file: str, content_type: str, source: str, tags: str):
    """Add knowledge document to agent's knowledge base"""
    with open(content_file, 'r') as f:
        content = f.read()
    
    tag_list = [tag.strip() for tag in tags.split(',')] if tags else []
    
    db_handler = PolarsDBHandler()
    kb_id = db_handler.add_knowledge_document(
        agent_id, title, content, content_type, source or "file", tag_list
    )
    
    click.echo(f"✅ Added knowledge document: {kb_id}")


@knowledge.command()
@click.argument('agent_id')
@click.argument('query')
def search(agent_id: str, query: str):
    """Search agent's knowledge base"""
    
    async def _search_knowledge():
        framework = GraphitiRAGFramework()
        framework.load_agent(agent_id)
        
        results = await framework.search_knowledge_with_context(query)
        return results
    
    results = asyncio.run(_search_knowledge())
    
    click.echo(f"\n🔍 Search results for '{query}':")
    
    if results['database_results']:
        click.echo("\n📚 Database Results:")
        for result in results['database_results']:
            click.echo(f"  • {result['title']}")
            click.echo(f"    Type: {result['content_type']}")
            click.echo(f"    Created: {result['created_at']}")
            click.echo()
    
    if results['graph_context']:
        click.echo("🧠 Graph Context:")
        click.echo(results['graph_context'])


@knowledge.command()
@click.argument('agent_id')
def list_docs(agent_id: str):
    """List knowledge documents for agent"""
    framework = GraphitiRAGFramework()
    framework.load_agent(agent_id)
    
    docs = framework.get_agent_knowledge_base()
    
    if not docs:
        click.echo("No knowledge documents found")
        return
    
    click.echo(f"\n📚 Knowledge Base for {agent_id}:")
    for doc in docs:
        click.echo(f"  • {doc['title']}")
        click.echo(f"    Type: {doc['content_type']}")
        click.echo(f"    Status: {doc['embedding_status']}")
        click.echo(f"    Created: {doc['created_at']}")
        click.echo()


# Export Commands
@app.group()
def export():
    """Export data commands"""
    pass

@export.command()
@click.argument('table', type=click.Choice(['agents', 'conversations', 'knowledge', 'research', 'templates']))
@click.option('--format', 'export_format', default='csv', 
              type=click.Choice(['csv', 'parquet', 'jsonl', 'json']),
              help='Export format')
@click.option('--output', help='Output file path (optional)')
def table(table: str, export_format: str, output: str):
    """Export database table to specified format"""
    db_handler = PolarsDBHandler()
    
    try:
        output_path = db_handler.export_data(table, export_format, output)
        click.echo(f"✅ Exported {table} to {export_format.upper()}: {output_path}")
    except Exception as e:
        click.echo(f"❌ Export failed: {e}")

@export.command()
@click.argument('agent_id')
@click.argument('output_path')
def conversations_jsonl(agent_id: str, output_path: str):
    """Export agent conversations in JSONL format"""
    db_handler = PolarsDBHandler()
    
    if db_handler.export_conversations_jsonl(agent_id, output_path):
        click.echo(f"✅ Exported conversations to {output_path}")
    else:
        click.echo(f"❌ Failed to export conversations for {agent_id}")

@export.command()
@click.argument('output_path')
def prompts_jsonl(output_path: str):
    """Export all agent prompt sets in JSONL format"""
    db_handler = PolarsDBHandler()
    
    if db_handler.export_prompt_sets_jsonl(output_path):
        click.echo(f"✅ Exported prompt sets to {output_path}")
    else:
        click.echo(f"❌ Failed to export prompt sets")


# Chat Commands (New!)
@app.group()
def chat():
    """💬 Interactive chat commands - Easy aliases, no long UUIDs!"""
    pass


@chat.command()
@click.argument('agent_id')
@click.option('--session-name', help='Friendly name for this chat session')
@click.option('--topic', default='General conversation', help='Chat topic')
def start(agent_id: str, session_name: str, topic: str):
    """🗣️ Start chatting with an agent (gets a short alias like 'wiz1')"""
    from .chat_manager import ChatManager
    
    db_handler = PolarsDBHandler()
    chat_manager = ChatManager(db_handler)
    
    try:
        session_id, alias = chat_manager.start_human_chat(agent_id, session_name, topic)
        
        click.echo(f"🎉 Started chat session!")
        click.echo(f"   🏷️  Alias: {alias} (easy to remember!)")
        click.echo(f"   🆔 Full ID: {session_id}")
        click.echo(f"   🤖 Agent: {agent_id}")
        click.echo(f"   💭 Topic: {topic}")
        click.echo(f"")
        click.echo(f"💡 Send messages with: ams-db chat send {alias} \"Your message here\"")
        
    except Exception as e:
        click.echo(f"❌ Failed to start chat: {e}")


@chat.command()
@click.argument('session_alias')
@click.argument('message')
def send(session_alias: str, message: str):
    """💬 Send a message to a chat session (use the short alias!)"""
    import asyncio
    from .chat_manager import ChatManager
    
    db_handler = PolarsDBHandler()
    chat_manager = ChatManager(db_handler)
    
    try:
        session = chat_manager.get_session_by_alias(session_alias)
        if not session:
            click.echo(f"❌ Session '{session_alias}' not found")
            click.echo("💡 Use 'ams-db chat list' to see active sessions")
            return
        
        # Add user message to database
        db_handler.add_conversation_message(
            agent_id="human",
            role="user", 
            content=message,
            session_id=session.id
        )
        
        # Get agent response using real Graphiti-powered conversation
        agent_id = [p for p in session.participants if p != "human"][0]
        
        click.echo(f"💬 You: {message}")
        click.echo(f"🤔 {agent_id} is thinking...")
        
        # Get real agent response using async method
        async def get_agent_response():
            return await chat_manager.send_message_to_agent(session.id, agent_id, message)
        
        # Run the async conversation
        agent_response = asyncio.run(get_agent_response())
        
        # Add agent response to database  
        db_handler.add_conversation_message(
            agent_id=agent_id,
            role="assistant",
            content=agent_response,
            session_id=session.id
        )
        
        # Update session activity
        chat_manager.update_session_activity(session_alias)
        
        # Display the conversation
        click.echo(f"🤖 {agent_id}: {agent_response}")
        click.echo(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        click.echo(f"❌ Failed to send message: {e}")
        click.echo("💡 Try: ams-db chat history {session_alias} to see if message was saved")


@chat.command()
@click.argument('session_alias')
@click.option('--limit', default=10, help='Number of recent messages to show')
def history(session_alias: str, limit: int):
    """📋 View chat history for a session"""
    from .chat_manager import ChatManager
    
    db_handler = PolarsDBHandler()
    chat_manager = ChatManager(db_handler)
    
    try:
        session = chat_manager.get_session_by_alias(session_alias)
        if not session:
            click.echo(f"❌ Session '{session_alias}' not found")
            return
        
        # Get conversation history
        conversations = db_handler.conversations.filter(
            db_handler.conversations["session_id"] == session.id
        ).sort("timestamp").tail(limit)
        
        if conversations.height == 0:
            click.echo(f"📭 No messages in session '{session_alias}' yet")
            return
        
        # Display session info
        click.echo(f"\n📋 Session: {session.name}")
        click.echo(f"🎭 Mode: {session.mode}")
        click.echo(f"👥 Participants: {', '.join(session.participants)}")
        click.echo(f"📊 Messages: {session.message_count}")
        click.echo("─" * 60)
        
        # Display conversation
        for row in conversations.to_dicts():
            role_icon = "💬" if row["role"] == "user" else "🤖"
            agent_display = row.get("agent_id", "unknown")
            timestamp = str(row["timestamp"]).split('.')[0].replace('T', ' ')
            
            click.echo(f"{role_icon} {agent_display}: {row['content']}")
            click.echo(f"   ⏰ {timestamp}")
            click.echo()
        
    except Exception as e:
        click.echo(f"❌ Failed to get history: {e}")


@chat.command()
@click.option('--mode', type=click.Choice(['HUMAN_CHAT', 'AGENT_CHAT', 'ROLEPLAY']), help='Filter by chat mode')
def list(mode: str):
    """📋 List all active chat sessions with their aliases"""
    from .chat_manager import ChatManager
    
    db_handler = PolarsDBHandler()
    chat_manager = ChatManager(db_handler)
    
    try:
        sessions = chat_manager.list_sessions(mode)
        
        if not sessions:
            click.echo("📭 No active chat sessions found")
            click.echo("💡 Start one with: ams-db chat start <agent_id>")
            return
        
        click.echo(f"\n📋 Chat Sessions ({len(sessions)} found)")
        click.echo("=" * 60)
        
        for session in sessions:
            click.echo(f"🆔 {session.alias}... - {session.name}")
            click.echo(f"   🎭 Mode: {session.mode}")
            click.echo(f"   👥 Participants: {', '.join(session.participants)}")
            click.echo(f"   📊 Messages: {session.message_count}")
            click.echo(f"   📅 Created: {session.created_at.strftime('%Y-%m-%d %H:%M')}")
            click.echo(f"   💭 Topic: {session.topic}")
            click.echo()
        
    except Exception as e:
        click.echo(f"❌ Failed to list sessions: {e}")


@chat.command()  
@click.argument('roleplay_agent_name')
@click.argument('target_agent_id')
@click.option('--session-name', help='Friendly name for this roleplay session')
@click.option('--topic', default='Roleplay conversation', help='Conversation topic')
def roleplay(roleplay_agent_name: str, target_agent_id: str, session_name: str, topic: str):
    """🎭 Start roleplay (you pretend to be an agent talking to another agent)"""
    from .chat_manager import ChatManager
    
    db_handler = PolarsDBHandler()
    chat_manager = ChatManager(db_handler)
    
    try:
        session_id, alias = chat_manager.start_roleplay_chat(
            roleplay_agent_name, target_agent_id, session_name, topic
        )
        
        click.echo(f"🎭 Started roleplay session!")
        click.echo(f"   🏷️  Alias: {alias}")
        click.echo(f"   🎪 You are: {roleplay_agent_name}")
        click.echo(f"   🤖 Talking to: {target_agent_id}")
        click.echo(f"   💭 Topic: {topic}")
        click.echo(f"")
        click.echo(f"💡 Send messages as {roleplay_agent_name}: ams-db chat roleplay-send {alias} \"Your message\"")
        
    except Exception as e:
        click.echo(f"❌ Failed to start roleplay: {e}")


@chat.command()
@click.argument('session_alias')
@click.argument('message')
def roleplay_send(session_alias: str, message: str):
    """🎭 Send a message in roleplay mode"""
    # Similar to send but handles roleplay logic
    send(session_alias, message)  # For now, reuse send logic


@chat.command()
@click.argument('session_alias')
@click.option('--format', default='jsonl', type=click.Choice(['jsonl', 'json', 'txt']), help='Export format')
def export(session_alias: str, format: str):
    """📤 Export a chat session to organized file structure"""
    from .chat_manager import ChatManager
    
    db_handler = PolarsDBHandler()
    chat_manager = ChatManager(db_handler)
    
    try:
        export_path = chat_manager.export_session(session_alias, format)
        click.echo(f"✅ Exported session '{session_alias}' to: {export_path}")
        
    except Exception as e:
        click.echo(f"❌ Failed to export session: {e}")


# Conversation Commands (Updated)
@app.group()
def conversation():
    """Conversation generation and management commands"""
    pass

@conversation.command()
@click.option('--agents', required=True, help='Comma-separated list of agent IDs')
@click.option('--topic', required=True, help='Conversation topic')
@click.option('--turns', default=10, help='Number of conversation turns')
@click.option('--output', help='Output file for conversation (optional)')
def generate(agents: str, topic: str, turns: int, output: str):
    """Generate a multi-agent conversation"""
    db_handler = PolarsDBHandler()
    
    try:
        from ..core.graphiti_pipe import GraphitiRAGFramework
        graphiti_framework = GraphitiRAGFramework()  # Use default parameters
        generator = ConversationGenerator(db_handler, graphiti_framework)
        
        agent_list = [agent.strip() for agent in agents.split(',')]
        
        click.echo(f"🤖 Generating conversation between: {', '.join(agent_list)}")
        click.echo(f"📝 Topic: {topic}")
        click.echo(f"🔄 Turns: {turns}")
        
        conversation = generator.generate_conversation(
            agents=agent_list,
            topic=topic,
            num_turns=turns
        )
        
        click.echo(f"✅ Generated conversation: {conversation['conversation_id']}")
        
        if output:
            generator.export_conversation_jsonl(
                conversation_id=conversation['conversation_id'],
                output_path=output
            )
            click.echo(f"📄 Exported to: {output}")
            
    except Exception as e:
        click.echo(f"❌ Failed to generate conversation: {e}")

@conversation.command()
@click.argument('conversation_id')
@click.argument('output_path')
@click.option('--format', 'export_format', default='jsonl', 
              type=click.Choice(['jsonl', 'json', 'csv']),
              help='Export format')
@click.option('--include-metadata', is_flag=True, help='Include metadata in export')
def export(conversation_id: str, output_path: str, export_format: str, include_metadata: bool):
    """Export a conversation to specified format"""
    db_handler = PolarsDBHandler()
    
    try:
        if export_format == 'jsonl':
            from ..core.graphiti_pipe import GraphitiRAGFramework
            graphiti_framework = GraphitiRAGFramework(db_handler)
            generator = ConversationGenerator(db_handler, graphiti_framework)
            
            exported_path = generator.export_conversation_jsonl(
                conversation_id=conversation_id,
                output_path=output_path,
                include_metadata=include_metadata
            )
            click.echo(f"✅ Exported conversation to JSONL: {exported_path}")
        else:
            # Use database export for other formats
            db_handler.export_conversation_data(conversation_id, output_path, format=export_format)
            click.echo(f"✅ Exported conversation to {export_format.upper()}: {output_path}")
            
    except Exception as e:
        click.echo(f"❌ Export failed: {e}")

@conversation.command()
@click.option('--topics-file', help='File containing topics (one per line)')
@click.option('--topics', help='Comma-separated list of topics')
@click.option('--agents', required=True, help='Comma-separated list of agent IDs')
@click.option('--turns', default=8, help='Number of turns per conversation')
@click.option('--output', default='training_dataset.jsonl', help='Output file for dataset')
def dataset(topics_file: str, topics: str, agents: str, turns: int, output: str):
    """Generate a training dataset of conversations"""
    db_handler = PolarsDBHandler()
    
    try:
        # Get topics list
        topic_list = []
        if topics_file:
            with open(topics_file, 'r', encoding='utf-8') as f:
                topic_list = [line.strip() for line in f if line.strip()]
        elif topics:
            topic_list = [topic.strip() for topic in topics.split(',')]
        else:
            click.echo("❌ Either --topics-file or --topics must be provided")
            return
        
        agent_list = [agent.strip() for agent in agents.split(',')]
        
        from ..core.graphiti_pipe import GraphitiRAGFramework
        graphiti_framework = GraphitiRAGFramework(db_handler)
        generator = ConversationGenerator(db_handler, graphiti_framework)
        
        click.echo(f"🏗️ Generating training dataset...")
        click.echo(f"📚 Topics: {len(topic_list)}")
        click.echo(f"🤖 Agents: {', '.join(agent_list)}")
        click.echo(f"🔄 Turns per conversation: {turns}")
        
        dataset_path = generator.generate_training_dataset(
            topic_list=topic_list,
            agents=agent_list,
            turns_per_conversation=turns,
            output_path=output
        )
        
        click.echo(f"✅ Training dataset generated: {dataset_path}")
        
    except Exception as e:
        click.echo(f"❌ Dataset generation failed: {e}")

@conversation.command()
def list():
    """List all conversations"""
    db_handler = PolarsDBHandler()
    
    try:
        conversations_df = db_handler.conversation_history
        
        if conversations_df.is_empty():
            click.echo("📭 No conversations found")
            return
        
        # Group by conversation_id and show summary
        summary = conversations_df.group_by("conversation_id").agg([
            db_handler.pl.col("turn_number").max().alias("max_turn"),
            db_handler.pl.col("agent_id").n_unique().alias("num_agents"),
            db_handler.pl.col("timestamp").min().alias("start_time")
        ]).sort("start_time", descending=True)
        
        click.echo("\n💬 Recent Conversations:")
        for row in summary.iter_rows(named=True):
            click.echo(f"  🆔 {row['conversation_id'][:8]}... | 🔄 {row['max_turn']+1} turns | 🤖 {row['num_agents']} agents | 📅 {row['start_time']}")
        
    except Exception as e:
        click.echo(f"❌ Failed to list conversations: {e}")


# Add the groups
app.add_command(chat)


# Main entry point
if __name__ == "__main__":
    app()


# 🧠 Knowledge Base Commands
@click.group()
def knowledge():
    """🧠 Manage agent knowledge bases and search knowledge."""
    pass


@knowledge.command("add")
@click.argument("title")
@click.argument("content")
@click.option("--agent", default=None, help="Agent to add knowledge for (uses current if not specified)")
@click.option("--source", default=None, help="Source of the knowledge")
@click.option("--tags", default=None, help="Comma-separated tags")
def add_knowledge(title: str, content: str, agent: Optional[str], source: Optional[str], tags: Optional[str]):
    """📚 Add knowledge to an agent's knowledge base."""
    try:
        db = PolarsDBHandler()
        
        # Get agent or use current
        if not agent:
            click.echo("⚠️ No agent specified. Use --agent to specify an agent.")
            return
            
        # Add to knowledge base
        kb_id = db.add_knowledge_document(
            agent_id=agent,
            title=title,
            content=content,
            source=source or "CLI",
            tags=tags.split(",") if tags else []
        )
        
        click.echo(f"✅ Knowledge added! ID: {kb_id}")
        click.echo(f"📚 Title: {title}")
        click.echo(f"🤖 Agent: {agent}")
        
    except Exception as e:
        click.echo(f"❌ Error adding knowledge: {e}")


@knowledge.command("search")
@click.argument("query")
@click.option("--agent", default=None, help="Agent to search knowledge for")
@click.option("--limit", default=5, help="Maximum number of results")
def search_knowledge(query: str, agent: Optional[str], limit: int):
    """🔍 Search agent knowledge base."""
    try:
        db = PolarsDBHandler()
        
        if not agent:
            click.echo("⚠️ No agent specified. Use --agent to specify an agent.")
            return
            
        results = db.search_knowledge_base(agent, query)
        
        if results.is_empty():
            click.echo(f"🔍 No knowledge found for query: '{query}'")
            return
            
        click.echo(f"🔍 Knowledge search results for '{query}':")
        click.echo("=" * 60)
        
        for i, row in enumerate(results.head(limit).iter_rows(named=True)):
            click.echo(f"\n📚 Result {i+1}:")
            click.echo(f"   📝 Title: {row['title']}")
            click.echo(f"   🤖 Agent: {row['agent_id']}")
            click.echo(f"   📖 Content: {row['content'][:200]}...")
            if row.get('tags'):
                click.echo(f"   🏷️  Tags: {row['tags']}")
                
    except Exception as e:
        click.echo(f"❌ Error searching knowledge: {e}")


@knowledge.command("list")
@click.option("--agent", default=None, help="Agent to list knowledge for")
@click.option("--limit", default=10, help="Maximum number of results")
def list_knowledge(agent: Optional[str], limit: int):
    """📋 List knowledge base entries."""
    try:
        db = PolarsDBHandler()
        
        if agent:
            # Filter by agent
            results = db.knowledge_base.filter(db.knowledge_base["agent_id"] == agent)
        else:
            results = db.knowledge_base
            
        if results.is_empty():
            agent_msg = f" for agent {agent}" if agent else ""
            click.echo(f"📚 No knowledge found{agent_msg}")
            return
            
        click.echo(f"📚 Knowledge Base Entries:")
        click.echo("=" * 60)
        
        for i, row in enumerate(results.head(limit).iter_rows(named=True)):
            click.echo(f"\n📝 {i+1}. {row['title']}")
            click.echo(f"    🤖 Agent: {row['agent_id']}")
            click.echo(f"    📅 Created: {row['created_at']}")
            click.echo(f"    📖 Content: {row['content'][:100]}...")
            
    except Exception as e:
        click.echo(f"❌ Error listing knowledge: {e}")


# 📄 Template Commands
@click.group()
def template():
    """📄 Manage agent templates and prompt templates."""
    pass


@template.command("add")
@click.argument("name")
@click.argument("template_type", type=click.Choice(["prompt", "config", "workflow"]))
@click.argument("content")
@click.option("--description", default=None, help="Template description")
@click.option("--category", default=None, help="Template category")
def add_template(name: str, template_type: str, content: str, description: Optional[str], category: Optional[str]):
    """➕ Add a new template."""
    try:
        db = PolarsDBHandler()
        
        template_id = db.add_template(
            name=name,
            template_type=template_type,
            content=content,
            description=description,
            category=category
        )
        
        click.echo(f"✅ Template added! ID: {template_id}")
        click.echo(f"📄 Name: {name}")
        click.echo(f"🔧 Type: {template_type}")
        
    except Exception as e:
        click.echo(f"❌ Error adding template: {e}")


@template.command("list")
@click.option("--type", "template_type", type=click.Choice(["prompt", "config", "workflow"]), help="Filter by type")
@click.option("--limit", default=10, help="Maximum number of results")
def list_templates(template_type: Optional[str], limit: int):
    """📋 List available templates."""
    try:
        db = PolarsDBHandler()
        
        results = db.templates
        if template_type:
            results = results.filter(results["template_type"] == template_type)
            
        if results.is_empty():
            type_msg = f" of type {template_type}" if template_type else ""
            click.echo(f"📄 No templates found{type_msg}")
            return
            
        click.echo(f"📄 Available Templates:")
        click.echo("=" * 60)
        
        for i, row in enumerate(results.head(limit).iter_rows(named=True)):
            click.echo(f"\n📝 {i+1}. {row['template_name']}")
            click.echo(f"    🔧 Type: {row['template_type']}")
            click.echo(f"    📅 Created: {row['created_at']}")
            if row.get('description'):
                click.echo(f"    📖 Description: {row['description']}")
            
    except Exception as e:
        click.echo(f"❌ Error listing templates: {e}")


@template.command("get")
@click.argument("template_id")
def get_template(template_id: str):
    """📄 Get template content by ID."""
    try:
        db = PolarsDBHandler()
        
        template = db.get_template(template_id)
        if not template:
            click.echo(f"❌ Template not found: {template_id}")
            return
            
        click.echo(f"📄 Template: {template['template_name']}")
        click.echo(f"🔧 Type: {template['template_type']}")
        click.echo("=" * 60)
        click.echo(template['content'])
        
    except Exception as e:
        click.echo(f"❌ Error getting template: {e}")


@knowledge.command("chat")
@click.argument("agent_id")
@click.option("--session-name", default=None, help="Name for the knowledge chat session")
def knowledge_chat(agent_id: str, session_name: Optional[str]):
    """💬 Start a chat session about an agent's knowledge base."""
    try:
        db = PolarsDBHandler()
        
        # Check if agent exists
        agent_row = db.agents.filter(db.agents["agent_id"] == agent_id)
        if agent_row.is_empty():
            click.echo(f"❌ Agent not found: {agent_id}")
            return
            
        agent_name = agent_row.select("name").item()
        
        # Create conversation session
        conv_modes = ConversationModes(db)
        session_id = conv_modes.start_knowledge_chat_session(
            agent_id=agent_id,
            session_name=session_name or f"knowledge_chat_{agent_name}"
        )
        
        click.echo(f"🧠 Started knowledge chat with {agent_name}")
        click.echo(f"📋 Session ID: {session_id}")
        click.echo(f"💬 Session Name: {session_name or f'knowledge_chat_{agent_name}'}")
        click.echo("\n💡 This agent can now answer questions about its knowledge base!")
        click.echo(f"   Use: ams-db chat send {session_id} \"What do you know about...?\"")
        
    except Exception as e:
        click.echo(f"❌ Error starting knowledge chat: {e}")


# ...existing code...
