"""
AMS-DB Command Line Interface

Main CLI entry point for managing agents, databases, and knowledge bases.
"""

import asyncio
import json
import click
from pathlib import Path
from typing import Optional

from ..core import AgentConfig, PolarsDBHandler, GraphitiRAGFramework
from src.ams_db.core.conversation_generator import ConversationGenerator


@click.group()
@click.version_option()
def app():
    """AMS-DB: Agentic Multimodal Super-alignment Database CLI"""
    pass


@app.group()
def agent():
    """Agent management commands"""
    pass


@app.group()
def db():
    """Database management commands"""
    pass


@app.group()
def knowledge():
    """Knowledge base management commands"""
    pass


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
    framework = GraphitiRAGFramework()
    
    if framework.export_agent_data(output_path):
        click.echo(f"✅ Exported agent {agent_id} to {output_path}")
    else:
        click.echo(f"❌ Failed to export agent {agent_id}")


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


# Conversation Commands
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
        from src.ams_db.core.graphiti_pipe import GraphitiRAGFramework
        graphiti_framework = GraphitiRAGFramework(db_handler)
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
            from src.ams_db.core.graphiti_pipe import GraphitiRAGFramework
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
        
        from src.ams_db.core.graphiti_pipe import GraphitiRAGFramework
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

if __name__ == "__main__":
    app()
