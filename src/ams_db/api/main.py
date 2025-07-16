"""
AMS-DB REST API

FastAPI-based REST API for managing agents, databases, and knowledge bases.
"""

import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import uvicorn

from ..core import AgentConfig, PolarsDBHandler, GraphitiRAGFramework


# Pydantic Models
class AgentConfigModel(BaseModel):
    agent_id: str
    agent_name: Optional[str] = None
    description: Optional[str] = ""
    tags: Optional[List[str]] = None
    config: Dict[str, Any]


class ConversationMessage(BaseModel):
    role: str
    content: str
    message_type: str = "text"
    metadata: Optional[Dict[str, Any]] = None


class KnowledgeDocument(BaseModel):
    title: str
    content: str
    content_type: str = "text"
    source: str = ""
    tags: Optional[List[str]] = None


class ResearchRequest(BaseModel):
    query: str
    research_type: str = "web_search"
    source_urls: Optional[List[str]] = None


# Initialize FastAPI app
app = FastAPI(
    title="AMS-DB API",
    description="REST API for Agentic Multimodal Super-alignment Database",
    version="0.1.0"
)

# Global framework instance
framework = None


@app.on_event("startup")
async def startup_event():
    """Initialize the framework on startup."""
    global framework
    framework = GraphitiRAGFramework()


# Agent Management Endpoints
@app.post("/agents/", response_model=dict)
def create_agent(agent_data: AgentConfigModel):
    """Create a new agent."""
    agent_id = framework.create_agent(
        agent_data.config,
        agent_data.agent_name,
        agent_data.description,
        agent_data.tags
    )
    return {"agent_id": agent_id, "status": "created"}


@app.get("/agents/")
def list_agents():
    """List all agents."""
    agents = framework.db_handler.list_agents()
    return {"agents": agents.to_dicts()}


@app.get("/agents/{agent_id}")
def get_agent(agent_id: str):
    """Get agent configuration."""
    config = framework.db_handler.get_agent_config(agent_id)
    if not config:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"agent_id": agent_id, "config": config}


@app.put("/agents/{agent_id}")
def update_agent(agent_id: str, agent_data: AgentConfigModel):
    """Update agent configuration."""
    framework.db_handler.update_agent_config(agent_id, agent_data.config)
    return {"agent_id": agent_id, "status": "updated"}


@app.delete("/agents/{agent_id}")
def delete_agent(agent_id: str, soft_delete: bool = True):
    """Delete an agent."""
    framework.db_handler.delete_agent(agent_id, soft_delete)
    return {"agent_id": agent_id, "status": "deleted"}


@app.post("/agents/{agent_id}/load")
def load_agent(agent_id: str, session_id: Optional[str] = None):
    """Load an agent as the current active agent."""
    success = framework.load_agent(agent_id, session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"agent_id": agent_id, "session_id": framework.current_session_id, "status": "loaded"}


# Conversation Endpoints
@app.post("/agents/{agent_id}/conversations/")
async def add_conversation_message(agent_id: str, message: ConversationMessage):
    """Add a message to the conversation."""
    # Load agent if not current
    if framework.current_agent_id != agent_id:
        framework.load_agent(agent_id)
    
    # For user messages, generate assistant response (placeholder)
    if message.role == "user":
        # This is where you'd integrate with your LLM
        assistant_response = f"Response to: {message.content}"
        
        msg_id = await framework.add_conversation_turn(
            message.content, 
            assistant_response, 
            message.metadata
        )
        
        return {
            "message_id": msg_id,
            "user_message": message.content,
            "assistant_response": assistant_response,
            "status": "processed"
        }
    else:
        # Just add the message
        msg_id = framework.db_handler.add_conversation_message(
            agent_id, message.role, message.content,
            framework.current_session_id, message.message_type, message.metadata
        )
        return {"message_id": msg_id, "status": "added"}


@app.get("/agents/{agent_id}/conversations/")
def get_conversation_history(agent_id: str, session_id: Optional[str] = None, limit: int = 50):
    """Get conversation history."""
    history = framework.db_handler.get_conversation_history(agent_id, session_id, limit)
    return {"conversations": history.to_dicts()}


@app.delete("/agents/{agent_id}/conversations/")
def clear_conversation_history(agent_id: str, session_id: Optional[str] = None):
    """Clear conversation history."""
    framework.db_handler.clear_conversation_history(agent_id, session_id)
    return {"status": "cleared"}


# Knowledge Base Endpoints
@app.post("/agents/{agent_id}/knowledge/")
async def add_knowledge_document(agent_id: str, document: KnowledgeDocument):
    """Add a knowledge document."""
    if framework.current_agent_id != agent_id:
        framework.load_agent(agent_id)
    
    kb_id = await framework.add_knowledge_with_embedding(
        document.title,
        document.content,
        document.content_type,
        document.source,
        document.tags
    )
    
    return {"kb_id": kb_id, "status": "added"}


@app.post("/agents/{agent_id}/knowledge/upload/")
async def upload_knowledge_file(agent_id: str, file: UploadFile = File(...)):
    """Upload a knowledge file."""
    if framework.current_agent_id != agent_id:
        framework.load_agent(agent_id)
    
    content = await file.read()
    content_str = content.decode('utf-8')
    
    kb_id = await framework.add_knowledge_with_embedding(
        file.filename,
        content_str,
        file.content_type or "text/plain",
        f"Upload: {file.filename}"
    )
    
    return {"kb_id": kb_id, "filename": file.filename, "status": "uploaded"}


@app.get("/agents/{agent_id}/knowledge/")
def list_knowledge_documents(agent_id: str, limit: int = 100):
    """List knowledge documents."""
    docs = framework.db_handler.get_knowledge_documents(agent_id, limit)
    return {"documents": docs.to_dicts()}


@app.get("/agents/{agent_id}/knowledge/search/")
async def search_knowledge_base(agent_id: str, query: str, include_context: bool = True):
    """Search the knowledge base."""
    if framework.current_agent_id != agent_id:
        framework.load_agent(agent_id)
    
    results = await framework.search_knowledge_with_context(query, include_context)
    return results


# Research Endpoints
@app.post("/agents/{agent_id}/research/")
async def add_research_result(agent_id: str, research: ResearchRequest):
    """Add research results."""
    if framework.current_agent_id != agent_id:
        framework.load_agent(agent_id)
    
    # Placeholder for actual research results
    results = {
        "query": research.query,
        "timestamp": datetime.now().isoformat(),
        "results": f"Research results for: {research.query}"
    }
    
    research_id = await framework.add_research_with_graph_integration(
        research.query,
        results,
        research.source_urls,
        research.research_type
    )
    
    return {"research_id": research_id, "status": "added"}


@app.get("/agents/{agent_id}/research/")
def search_research_collection(agent_id: str, query: str, research_type: Optional[str] = None):
    """Search research collection."""
    results = framework.db_handler.search_research_collection(agent_id, query, research_type)
    return {"research_results": results.to_dicts()}


# Export/Import Endpoints
@app.post("/export/conversations/{agent_id}")
async def export_conversations_jsonl(agent_id: str, output_path: str = "conversations.jsonl"):
    """Export agent conversations in JSONL format."""
    framework = GraphitiRAGFramework()
    
    success = await framework.export_conversations_jsonl(agent_id, output_path)
    if success:
        return {"message": f"Conversations exported to {output_path}", "success": True}
    else:
        raise HTTPException(status_code=400, detail="Failed to export conversations")

@app.post("/export/prompts")
async def export_prompts_jsonl(output_path: str = "prompts.jsonl"):
    """Export all agent prompt sets in JSONL format."""
    framework = GraphitiRAGFramework()
    
    success = await framework.export_prompt_sets_jsonl(output_path)
    if success:
        return {"message": f"Prompt sets exported to {output_path}", "success": True}
    else:
        raise HTTPException(status_code=400, detail="Failed to export prompt sets")


# Multi-Agent Conversation Generation
@app.post("/generate/conversation")
async def generate_multi_agent_conversation(
    agent_ids: List[str],
    topic: str,
    turns: int = 10,
    personas: Optional[List[str]] = None
):
    """Generate a multi-agent conversation."""
    framework = GraphitiRAGFramework()
    
    session_id = await framework.generate_multi_agent_conversation(
        agent_ids, topic, turns, personas
    )
    
    if session_id:
        return {
            "message": "Multi-agent conversation generated",
            "session_id": session_id,
            "agents": len(agent_ids),
            "turns": turns
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to generate conversation")


# System Endpoints
@app.get("/system/status/")
def get_system_status():
    """Get system status."""
    return framework.get_system_status()


@app.get("/system/stats/")
def get_database_stats():
    """Get database statistics."""
    return framework.db_handler.get_database_stats()


@app.post("/system/backup/")
def create_backup(backup_path: str):
    """Create a database backup."""
    try:
        framework.db_handler.export_database_backup(backup_path)
        return {"status": "success", "backup_path": backup_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "AMS-DB API",
        "version": "0.1.0",
        "description": "REST API for Agentic Multimodal Super-alignment Database",
        "docs": "/docs",
        "status": "running"
    }


def run_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = True):
    """Run the API server."""
    uvicorn.run("ams_db.api.main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    run_server()
