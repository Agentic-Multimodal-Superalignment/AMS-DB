"""
🧙‍♂️ MAGICAL CHAT MANAGER - No More Long UUIDs! ✨
Smart session management with easy-to-remember aliases and organized storage.
Now with REAL Graphiti-powered conversations!
"""

import json
import uuid
import hashlib
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import polars as pl

from ..core.polars_db import PolarsDBHandler
from ..core.graphiti_pipe import GraphitiRAGFramework


@dataclass
class ChatSession:
    """Represents a chat session with easy aliases"""
    id: str                    # Full UUID
    alias: str                 # Short memorable name like "wiz1", "chat2"
    name: str                  # User-friendly name
    mode: str                  # HUMAN_CHAT, AGENT_CHAT, ROLEPLAY
    participants: List[str]    # List of participant IDs
    topic: str                 # Session topic
    created_at: datetime
    message_count: int = 0
    last_activity: Optional[datetime] = None


class ChatManager:
    """
    🎭 THE ULTIMATE CHAT MANAGER 🎭
    
    Features:
    - Short aliases (wiz1, chat2, etc.) instead of long UUIDs
    - Organized file storage by mode and date  
    - Easy session switching and management
    - Automatic conversation export and backup
    """
    
    def __init__(self, db_handler: PolarsDBHandler):
        self.db = db_handler
        self.sessions_file = Path("data/sessions/active_sessions.json")
        self.sessions_file.parent.mkdir(parents=True, exist_ok=True)
        self.active_sessions: Dict[str, ChatSession] = {}
        self.load_sessions()
    
    def create_short_alias(self, session_id: str, agent_id: str = None) -> str:
        """Create a short memorable alias from UUID"""
        # Use first 8 chars of session ID + agent prefix
        short_id = session_id[:8]
        
        if agent_id:
            if "wizard" in agent_id.lower():
                prefix = "wiz"
            elif "minecraft" in agent_id.lower():
                prefix = "mc"
            elif "expert" in agent_id.lower() or "coder" in agent_id.lower():
                prefix = "code"
            else:
                prefix = "chat"
        else:
            prefix = "chat"
        
        # Find available number for this prefix
        existing_nums = [
            int(alias[len(prefix):]) for alias in self.active_sessions.keys() 
            if alias.startswith(prefix) and alias[len(prefix):].isdigit()
        ]
        next_num = max(existing_nums, default=0) + 1
        
        return f"{prefix}{next_num}"
    
    def start_human_chat(self, agent_id: str, session_name: str = None, topic: str = "General conversation") -> Tuple[str, str]:
        """
        🗣️ Start a human chat with an agent
        Returns: (session_id, alias)
        """
        session_id = str(uuid.uuid4())
        alias = self.create_short_alias(session_id, agent_id)
        
        session = ChatSession(
            id=session_id,
            alias=alias,
            name=session_name or f"Chat with {agent_id}",
            mode="HUMAN_CHAT",
            participants=["human", agent_id],
            topic=topic,
            created_at=datetime.now()
        )
        
        self.active_sessions[alias] = session
        self.save_sessions()
        
        # Create organized session folder
        session_folder = Path(f"data/sessions/human_chat/{datetime.now().strftime('%Y-%m-%d')}")
        session_folder.mkdir(parents=True, exist_ok=True)
        
        return session_id, alias
    
    def start_roleplay_chat(self, roleplay_agent_name: str, target_agent_id: str, 
                           session_name: str = None, topic: str = "Roleplay conversation") -> Tuple[str, str]:
        """
        🎭 Start a roleplay chat (human pretending to be an agent)
        Returns: (session_id, alias)
        """
        session_id = str(uuid.uuid4())
        alias = self.create_short_alias(session_id, target_agent_id)
        
        session = ChatSession(
            id=session_id,
            alias=alias,
            name=session_name or f"{roleplay_agent_name} → {target_agent_id}",
            mode="ROLEPLAY",
            participants=[roleplay_agent_name, target_agent_id],
            topic=topic,
            created_at=datetime.now()
        )
        
        self.active_sessions[alias] = session
        self.save_sessions()
        
        # Create organized session folder
        session_folder = Path(f"data/sessions/roleplay/{datetime.now().strftime('%Y-%m-%d')}")
        session_folder.mkdir(parents=True, exist_ok=True)
        
        return session_id, alias
    
    def start_agent_conversation(self, agent_ids: List[str], topic: str, turns: int = 10) -> Tuple[str, str]:
        """
        🤖 Start an agent-to-agent conversation
        Returns: (session_id, alias)
        """
        session_id = str(uuid.uuid4())
        alias = self.create_short_alias(session_id)
        
        session = ChatSession(
            id=session_id,
            alias=alias,
            name=f"Agent Conversation: {' vs '.join(agent_ids)}",
            mode="AGENT_CHAT",
            participants=agent_ids,
            topic=topic,
            created_at=datetime.now()
        )
        
        self.active_sessions[alias] = session
        self.save_sessions()
        
        # Create organized session folder
        session_folder = Path(f"data/sessions/agent_chat/{datetime.now().strftime('%Y-%m-%d')}")
        session_folder.mkdir(parents=True, exist_ok=True)
        
        return session_id, alias
    
    def get_session_by_alias(self, alias: str) -> Optional[ChatSession]:
        """Get session by short alias"""
        return self.active_sessions.get(alias)
    
    def get_session_by_id(self, session_id: str) -> Optional[ChatSession]:
        """Get session by full UUID"""
        for session in self.active_sessions.values():
            if session.id == session_id:
                return session
        return None
    
    def list_sessions(self, mode: str = None) -> List[ChatSession]:
        """List all active sessions, optionally filtered by mode"""
        sessions = list(self.active_sessions.values())
        if mode:
            sessions = [s for s in sessions if s.mode == mode]
        return sorted(sessions, key=lambda x: x.created_at, reverse=True)
    
    def update_session_activity(self, alias: str):
        """Update last activity timestamp"""
        if alias in self.active_sessions:
            self.active_sessions[alias].last_activity = datetime.now()
            self.active_sessions[alias].message_count += 1
            self.save_sessions()
    
    def export_session(self, alias: str, format: str = "jsonl") -> str:
        """Export session conversations to organized file structure"""
        session = self.get_session_by_alias(alias)
        if not session:
            raise ValueError(f"Session '{alias}' not found")
        
        # Create organized export path
        date_str = session.created_at.strftime('%Y-%m-%d')
        mode_folder = session.mode.lower()
        export_folder = Path(f"data/conversations/{mode_folder}/{date_str}")
        export_folder.mkdir(parents=True, exist_ok=True)
        
        # Generate clean filename
        clean_name = "".join(c for c in session.name if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"{alias}_{clean_name.replace(' ', '_')}.{format}"
        export_path = export_folder / filename
        
        # Export conversation data from database
        conversations = self.db.conversations.filter(
            self.db.conversations["session_id"] == session.id
        ).sort("timestamp")
        
        if format == "jsonl":
            with open(export_path, 'w', encoding='utf-8') as f:
                for row in conversations.to_dicts():
                    entry = {
                        "alias": alias,
                        "session_name": session.name,
                        "mode": session.mode,
                        "timestamp": str(row["timestamp"]),
                        "role": row["role"],
                        "agent_id": row.get("agent_id", "human"),
                        "content": row["content"],
                        "metadata": json.loads(row.get("metadata", "{}"))
                    }
                    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        return str(export_path)
    
    def cleanup_old_sessions(self, days: int = 30):
        """Remove sessions older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        to_remove = [
            alias for alias, session in self.active_sessions.items()
            if session.created_at < cutoff_date
        ]
        
        for alias in to_remove:
            # Export before removing
            try:
                self.export_session(alias)
            except:
                pass  # Continue cleanup even if export fails
            
            del self.active_sessions[alias]
        
        self.save_sessions()
        return len(to_remove)
    
    def save_sessions(self):
        """Save active sessions to file"""
        sessions_data = {}
        for alias, session in self.active_sessions.items():
            sessions_data[alias] = {
                "id": session.id,
                "alias": session.alias,
                "name": session.name,
                "mode": session.mode,
                "participants": session.participants,
                "topic": session.topic,
                "created_at": session.created_at.isoformat(),
                "message_count": session.message_count,
                "last_activity": session.last_activity.isoformat() if session.last_activity else None
            }
        
        with open(self.sessions_file, 'w', encoding='utf-8') as f:
            json.dump(sessions_data, f, indent=2, ensure_ascii=False)
    
    def load_sessions(self):
        """Load active sessions from file"""
        if self.sessions_file.exists():
            try:
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    sessions_data = json.load(f)
                
                for alias, data in sessions_data.items():
                    session = ChatSession(
                        id=data["id"],
                        alias=data["alias"],
                        name=data["name"],
                        mode=data["mode"],
                        participants=data["participants"],
                        topic=data["topic"],
                        created_at=datetime.fromisoformat(data["created_at"]),
                        message_count=data.get("message_count", 0),
                        last_activity=datetime.fromisoformat(data["last_activity"]) if data.get("last_activity") else None
                    )
                    self.active_sessions[alias] = session
            
            except Exception as e:
                # If sessions file is corrupted, start fresh
                self.active_sessions = {}
    
    async def send_message_to_agent(self, session_id: str, agent_id: str, user_message: str) -> str:
        """
        🤖 Send a message to an agent using Graphiti for real conversation
        Returns the agent's response
        """
        try:
            # Initialize Graphiti framework for this agent
            import os
            graphiti = GraphitiRAGFramework(
                neo4j_uri=os.environ.get('NEO4J_URI', 'bolt://localhost:7687'),
                neo4j_user=os.environ.get('NEO4J_USER', 'neo4j'),
                neo4j_password=os.environ.get('NEO4J_PASSWORD', 'password')
            )
            
            # Load the agent's context and knowledge
            await graphiti.load_agent(agent_id)
            
            # Get conversation history for context
            conversation_history = self.db.conversations.filter(
                self.db.conversations["session_id"] == session_id
            ).sort("timestamp")
            
            # Build context from recent messages
            context_messages = []
            if conversation_history.height > 0:
                recent_messages = conversation_history.tail(10).to_dicts()  # Last 10 messages
                for msg in recent_messages:
                    role = "human" if msg["role"] == "user" else msg["agent_id"]
                    context_messages.append(f"{role}: {msg['content']}")
            
            # Get agent's response using Graphiti
            response = await graphiti.generate_response(
                agent_id=agent_id,
                user_message=user_message,
                conversation_context="\n".join(context_messages),
                session_id=session_id
            )
            
            return response
            
        except Exception as e:
            # Check what services might be missing and provide helpful feedback
            missing_services = []
            
            # Check Neo4j
            try:
                import requests
                requests.get("http://localhost:7474", timeout=2)
            except:
                missing_services.append("Neo4j (http://localhost:7474)")
            
            # Check Ollama 
            try:
                import requests
                requests.get("http://localhost:11434", timeout=2)
            except:
                missing_services.append("Ollama (http://localhost:11434)")
            
            # Fallback to personality-based simulation with service info
            agent_config = self.db.get_agent_config(agent_id)
            
            if missing_services:
                service_info = ", ".join(missing_services)
                setup_notice = f"\n\n🔧 **Setup Notice**: To enable full AI conversations, start: {service_info}"
            else:
                setup_notice = f"\n\n⚠️ **Note**: Graphiti error: {str(e)[:100]}..."
            
            if agent_config:
                personality = agent_config.get("prompt_config", {}).get("primeDirective", "")
                if "wizard" in personality.lower() or "wizard" in agent_id.lower():
                    base_response = f"🧙‍♂️ *adjusts mystical robes* Your question about '{user_message}' stirs ancient knowledge within my ethereal archives..."
                elif "minecraft" in personality.lower() or "minecraft" in agent_id.lower():
                    base_response = f"🎮 Hey there, crafter! Your question about '{user_message}' is like finding diamonds - totally awesome! ⛏️"
                elif "expert" in personality.lower() or "coder" in agent_id.lower():
                    base_response = f"From a technical perspective, '{user_message}' is an interesting topic that requires systematic analysis."
                else:
                    base_response = f"Thank you for asking about '{user_message}'. I'd be happy to discuss this topic with you."
            else:
                base_response = f"I understand you're asking about '{user_message}'. Let me share what I know..."
            
            return base_response + setup_notice
