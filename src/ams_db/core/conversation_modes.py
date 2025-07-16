"""
Conversation Modes for AMS-DB
Handles different types of conversations and interactions.
"""

import json
import uuid
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import polars as pl

from .polars_db import PolarsDBHandler
from .base_agent_config import AgentConfig

class ConversationModes:
    """
    Manages different conversation modes:
    1. HUMAN_CHAT: Human directly talking to an agent
    2. AGENT_TO_AGENT: Agents talking to each other (simulated)
    3. HUMAN_AS_AGENT: Human pretending to be an agent talking to another agent
    """
    
    def __init__(self, db_handler: PolarsDBHandler):
        self.db = db_handler
        self.logger = logging.getLogger(__name__)
        
    def start_human_chat(self, agent_id: str, session_name: str = None) -> str:
        """
        Start a conversation between human and agent.
        
        Args:
            agent_id: Agent to chat with
            session_name: Optional session name for organization
            
        Returns:
            session_id: Use this to continue the conversation
        """
        session_id = str(uuid.uuid4())
        session_name = session_name or f"chat_with_{agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Store session metadata
        self.db.add_conversation_message(
            agent_id=agent_id,
            role="system",
            content=f"Starting human chat session: {session_name}",
            session_id=session_id,
            metadata={
                "conversation_mode": "HUMAN_CHAT",
                "session_name": session_name,
                "participants": ["human", agent_id]
            }
        )
        
        self.logger.info(f"Started human chat session {session_id} with {agent_id}")
        return session_id
    
    def send_human_message(self, session_id: str, agent_id: str, message: str) -> Dict[str, Any]:
        """
        Send a message from human to agent and get response.
        
        Args:
            session_id: Session ID from start_human_chat
            agent_id: Agent to send message to
            message: Human's message
            
        Returns:
            Response with agent's reply
        """
        # Store human message
        human_msg_id = self.db.add_conversation_message(
            agent_id=agent_id,
            role="user",
            content=message,
            session_id=session_id,
            metadata={
                "conversation_mode": "HUMAN_CHAT",
                "sender": "human"
            }
        )
        
        # Get agent config for personality
        agent_config = self.db.get_agent_config(agent_id)
        if not agent_config:
            raise ValueError(f"Agent {agent_id} not found")
        
        # Generate agent response (simplified - would use actual LLM in production)
        agent_response = self._generate_agent_response(agent_config, message, session_id)
        
        # Store agent response
        agent_msg_id = self.db.add_conversation_message(
            agent_id=agent_id,
            role="assistant",
            content=agent_response,
            session_id=session_id,
            metadata={
                "conversation_mode": "HUMAN_CHAT",
                "sender": agent_id,
                "in_response_to": human_msg_id
            }
        )
        
        return {
            "session_id": session_id,
            "human_message": message,
            "agent_response": agent_response,
            "timestamp": datetime.now().isoformat(),
            "mode": "HUMAN_CHAT"
        }
    
    def start_agent_conversation(self, agent_ids: List[str], topic: str, turns: int = 10) -> str:
        """
        Start a conversation between multiple agents.
        
        Args:
            agent_ids: List of agents to participate
            topic: Conversation topic
            turns: Number of conversation turns
            
        Returns:
            session_id: Session identifier
        """
        session_id = str(uuid.uuid4())
        session_name = f"agent_conversation_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Store session metadata
        for agent_id in agent_ids:
            self.db.add_conversation_message(
                agent_id=agent_id,
                role="system",
                content=f"Starting agent conversation on topic: {topic}",
                session_id=session_id,
                metadata={
                    "conversation_mode": "AGENT_TO_AGENT",
                    "session_name": session_name,
                    "topic": topic,
                    "participants": agent_ids,
                    "total_turns": turns
                }
            )
        
        # Generate conversation turns
        for turn in range(turns):
            current_agent = agent_ids[turn % len(agent_ids)]
            
            # Get agent config
            agent_config = self.db.get_agent_config(current_agent)
            if not agent_config:
                continue
                
            # Generate response based on topic and previous context
            response = self._generate_agent_conversation_turn(
                agent_config, topic, session_id, turn, agent_ids
            )
            
            # Store the turn
            self.db.add_conversation_message(
                agent_id=current_agent,
                role="assistant",
                content=response,
                session_id=session_id,
                metadata={
                    "conversation_mode": "AGENT_TO_AGENT",
                    "turn_number": turn,
                    "topic": topic,
                    "participants": agent_ids
                }
            )
        
        self.logger.info(f"Generated {turns}-turn conversation between {agent_ids} on topic: {topic}")
        return session_id
    
    def start_human_as_agent(self, human_agent_name: str, target_agent_id: str, session_name: str = None) -> str:
        """
        Start a conversation where human pretends to be an agent talking to another agent.
        
        Args:
            human_agent_name: Name/persona the human will use
            target_agent_id: Agent the human will talk to
            session_name: Optional session name
            
        Returns:
            session_id: Session identifier
        """
        session_id = str(uuid.uuid4())
        session_name = session_name or f"human_as_{human_agent_name}_to_{target_agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Store session metadata
        self.db.add_conversation_message(
            agent_id=target_agent_id,
            role="system", 
            content=f"Starting conversation with {human_agent_name} (human pretending to be agent)",
            session_id=session_id,
            metadata={
                "conversation_mode": "HUMAN_AS_AGENT",
                "session_name": session_name,
                "human_persona": human_agent_name,
                "target_agent": target_agent_id,
                "participants": [human_agent_name, target_agent_id]
            }
        )
        
        self.logger.info(f"Started human-as-agent session: {human_agent_name} -> {target_agent_id}")
        return session_id
    
    def send_human_as_agent_message(self, session_id: str, human_agent_name: str, 
                                  target_agent_id: str, message: str) -> Dict[str, Any]:
        """
        Send a message as a human pretending to be an agent.
        """
        # Store human-as-agent message
        human_msg_id = self.db.add_conversation_message(
            agent_id=target_agent_id,  # Store under target agent for organization
            role="user",
            content=message,
            session_id=session_id,
            metadata={
                "conversation_mode": "HUMAN_AS_AGENT",
                "sender": human_agent_name,
                "actual_sender": "human"
            }
        )
        
        # Get target agent response
        agent_config = self.db.get_agent_config(target_agent_id)
        if not agent_config:
            raise ValueError(f"Agent {target_agent_id} not found")
        
        agent_response = self._generate_agent_response(agent_config, message, session_id)
        
        # Store agent response
        agent_msg_id = self.db.add_conversation_message(
            agent_id=target_agent_id,
            role="assistant",
            content=agent_response,
            session_id=session_id,
            metadata={
                "conversation_mode": "HUMAN_AS_AGENT",
                "sender": target_agent_id,
                "in_response_to": human_msg_id
            }
        )
        
        return {
            "session_id": session_id,
            "human_as_agent_message": message,
            "agent_response": agent_response,
            "human_persona": human_agent_name,
            "target_agent": target_agent_id,
            "mode": "HUMAN_AS_AGENT"
        }
    
    def get_conversation_history(self, session_id: str, format: str = "chat") -> Dict[str, Any]:
        """
        Get conversation history in different formats.
        
        Args:
            session_id: Session identifier
            format: 'chat', 'jsonl', 'messages'
            
        Returns:
            Formatted conversation history
        """
        # Get all messages for this session
        messages = self.db.conversations.filter(
            pl.col("session_id") == session_id
        ).sort("timestamp")
        
        if messages.height == 0:
            return {"error": f"No conversation found for session {session_id}"}
        
        # Get conversation metadata from first system message
        first_msg = messages.head(1).to_dicts()[0]
        metadata = json.loads(first_msg.get("metadata", "{}"))
        
        conversation_data = {
            "session_id": session_id,
            "mode": metadata.get("conversation_mode", "UNKNOWN"),
            "session_name": metadata.get("session_name", session_id),
            "participants": metadata.get("participants", []),
            "message_count": messages.height,
            "created_at": first_msg["timestamp"],
            "messages": []
        }
        
        if format == "chat":
            for msg in messages.to_dicts():
                if msg["role"] != "system":  # Skip system messages for chat view
                    msg_meta = json.loads(msg.get("metadata", "{}"))
                    conversation_data["messages"].append({
                        "sender": msg_meta.get("sender", msg["agent_id"]),
                        "content": msg["content"],
                        "timestamp": msg["timestamp"],
                        "role": msg["role"]
                    })
        elif format == "jsonl":
            conversation_data["messages"] = messages.to_dicts()
        elif format == "messages":
            conversation_data["messages"] = [
                {
                    "role": msg["role"],
                    "content": msg["content"],
                    "timestamp": str(msg["timestamp"]),
                    "metadata": json.loads(msg.get("metadata", "{}"))
                }
                for msg in messages.to_dicts()
            ]
        
        return conversation_data
    
    def list_sessions(self, mode: str = None, agent_id: str = None) -> List[Dict[str, Any]]:
        """
        List conversation sessions with optional filtering.
        
        Args:
            mode: Filter by conversation mode
            agent_id: Filter by agent participation
            
        Returns:
            List of session summaries
        """
        # Get all system messages (they mark session starts)
        system_messages = self.db.conversations.filter(
            pl.col("role") == "system"
        ).sort("timestamp", descending=True)
        
        sessions = []
        for msg in system_messages.to_dicts():
            metadata = json.loads(msg.get("metadata", "{}"))
            
            # Apply filters
            if mode and metadata.get("conversation_mode") != mode:
                continue
            if agent_id and agent_id not in metadata.get("participants", []):
                continue
            
            # Count messages in this session
            session_msg_count = self.db.conversations.filter(
                pl.col("session_id") == msg["session_id"]
            ).height
            
            sessions.append({
                "session_id": msg["session_id"],
                "session_name": metadata.get("session_name", msg["session_id"]),
                "mode": metadata.get("conversation_mode", "UNKNOWN"),
                "participants": metadata.get("participants", []),
                "created_at": msg["timestamp"],
                "message_count": session_msg_count,
                "topic": metadata.get("topic", "General conversation")
            })
        
        return sessions
    
    def _generate_agent_response(self, agent_config: Dict[str, Any], message: str, session_id: str) -> str:
        """Generate an agent response based on configuration and context."""
        # Get agent personality
        prompts = agent_config.get("prompt_config", {})
        agent_prompt = prompts.get("agent", {}).get("llmSystem", "")
        prime_directive = prompts.get("primeDirective", "")
        
        # Simple response generation (would use actual LLM in production)
        if "wizard" in agent_config.get("agent_id", "").lower():
            responses = [
                f"🧙‍♂️ Ah, regarding '{message}' - let me consult the ancient scrolls of wisdom...",
                f"*adjusts mystical robes* The ethereal patterns suggest that your query about '{message}' holds great potential!",
                f"By the cosmic forces! Your question about '{message}' reminds me of legendary algorithms from the data realms..."
            ]
        elif "minecraft" in agent_config.get("agent_id", "").lower():
            responses = [
                f"Hey there! 🎮 About '{message}' - that's like building the perfect redstone contraption!",
                f"You know what? '{message}' reminds me of when you're exploring caves and find diamonds!",
                f"*places block* That's a great question about '{message}' - let me help you build that knowledge!"
            ]
        elif "expert" in agent_config.get("agent_id", "").lower():
            responses = [
                f"From a technical perspective, '{message}' requires careful analysis of the requirements.",
                f"Based on industry best practices, the optimal approach to '{message}' involves scalable architecture.",
                f"Regarding '{message}', I recommend implementing robust patterns with comprehensive testing."
            ]
        else:
            responses = [
                f"Interesting question about '{message}'. Let me share my thoughts on this.",
                f"That's a great topic - '{message}'. Here's how I approach this challenge.",
                f"Regarding '{message}', I believe we should consider multiple perspectives."
            ]
        
        import random
        return random.choice(responses)
    
    def _generate_agent_conversation_turn(self, agent_config: Dict[str, Any], topic: str, 
                                        session_id: str, turn: int, participants: List[str]) -> str:
        """Generate a conversation turn for agent-to-agent mode."""
        # Similar to _generate_agent_response but tailored for multi-agent conversations
        agent_id = agent_config.get("agent_id", "")
        
        if "wizard" in agent_id.lower():
            return f"🧙‍♂️ *turn {turn}* Mystical insights on '{topic}': The arcane patterns reveal fascinating connections..."
        elif "minecraft" in agent_id.lower():
            return f"🎮 *turn {turn}* Building knowledge about '{topic}': This is like crafting the perfect strategy!"
        elif "expert" in agent_id.lower():
            return f"💻 *turn {turn}* Technical analysis of '{topic}': The optimal implementation requires careful consideration..."
        else:
            return f"*turn {turn}* Regarding '{topic}': Let me contribute my perspective to this discussion..."
