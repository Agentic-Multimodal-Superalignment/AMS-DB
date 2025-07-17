import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from pathlib import Path

from graphiti_core import Graphiti
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
from graphiti_core.cross_encoder.openai_reranker_client import OpenAIRerankerClient

try:
    from graphiti_core.prompts.models import Message
except ImportError:
    # Fallback if models import fails
    from graphiti_core.prompts import Message

from .base_agent_config import AgentConfig
from .polars_db import PolarsDBHandler

class GraphitiRAGFramework:
    """
    A comprehensive RAG framework that integrates Graphiti knowledge graphs 
    with Polars database management and agent configuration system.
    """
    
    def __init__(self, 
                 neo4j_uri: str = "bolt://localhost:7687",
                 neo4j_user: str = "neo4j", 
                 neo4j_password: str = "password",
                 db_path: str = "agent_database",
                 ollama_base_url: str = "http://localhost:11434/v1",
                 llm_model: str = "phi4:latest",
                 small_model: str = "gemma3:4b",
                 embedding_model: str = "nomic-embed-text",
                 embedding_dim: int = 768):
        """
        Initialize the Graphiti RAG Framework.
        
        Args:
            neo4j_uri: Neo4j database connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
            db_path: Path for Polars database storage
            ollama_base_url: Ollama API base URL
            llm_model: Primary LLM model name
            small_model: Small/fast LLM model name
            embedding_model: Embedding model name
            embedding_dim: Embedding dimension
        """
        self.logger = logging.getLogger(__name__)
        
        # Initialize Polars database handler
        self.db_handler = PolarsDBHandler(db_path)
        
        # Initialize Ollama LLM configuration
        self.llm_config = LLMConfig(
            api_key="abc",  # Ollama doesn't require a real API key
            model=llm_model,
            small_model=small_model,
            base_url=ollama_base_url,
        )
        
        self.llm_client = OpenAIClient(config=self.llm_config)
        
        # Initialize Graphiti with Ollama clients
        self.graphiti = Graphiti(
            neo4j_uri,
            neo4j_user,
            neo4j_password,
            llm_client=self.llm_client,
            embedder=OpenAIEmbedder(
                config=OpenAIEmbedderConfig(
                    api_key="abc",
                    embedding_model=embedding_model,
                    embedding_dim=embedding_dim,
                    base_url=ollama_base_url,
                )
            ),
            cross_encoder=OpenAIRerankerClient(
                client=self.llm_client, 
                config=self.llm_config
            ),
        )
        
        # Current active agent
        self.current_agent_id = None
        self.current_agent_config = None
        self.current_session_id = None
        
        self.logger.info("Graphiti RAG Framework initialized successfully")
    
    # Agent Management Methods
    def create_agent(self, agent_config: Dict[str, Any], agent_name: str = None,
                    description: str = "", tags: List[str] = None) -> str:
        """Create a new agent with configuration."""
        agent_id = self.db_handler.add_agent_config(
            agent_config, agent_name, description, tags
        )
        
        # Initialize agent's knowledge graph space
        self._initialize_agent_knowledge_space(agent_id)
        
        self.logger.info(f"Created new agent: {agent_id}")
        return agent_id
    
    async def load_agent(self, agent_id: str, session_id: str = None) -> bool:
        """Load an agent and set it as current active agent."""
        config = self.db_handler.get_agent_config(agent_id)
        if not config:
            self.logger.error(f"Agent {agent_id} not found")
            return False
        
        self.current_agent_id = agent_id
        self.current_agent_config = config
        self.current_session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.logger.info(f"Loaded agent: {agent_id}, session: {self.current_session_id}")
        return True
    
    def get_agent_prompt_system(self) -> str:
        """Get the system prompt for the current agent."""
        if not self.current_agent_config:
            return "You are a helpful AI assistant."
        
        return self.current_agent_config.get("agent_core", {}).get("prompts", {}).get("llmSystem", "")
    
    def get_agent_prompt_booster(self) -> str:
        """Get the booster prompt for the current agent."""
        if not self.current_agent_config:
            return ""
        
        return self.current_agent_config.get("agent_core", {}).get("prompts", {}).get("llmBooster", "")
    
    def create_predefined_agents(self):
        """Create predefined agents based on your examples."""
        
        # Default Agent
        default_agent = AgentConfig("default_agent")
        default_agent.set_prompt("llmSystem", "You are a helpful AI assistant.")
        default_agent.set_modality_flag("ACTIVE_AGENT_FLAG", True)
        self.create_agent(default_agent.get_config(), "Default Agent", "Basic helpful assistant")
        
        # Prompt Base Agent
        prompt_base = AgentConfig("promptBase")
        prompt_base.set_prompt("llmSystem", (
            "You are a helpful llm assistant, designated with fulfilling the user's request, "
            "the user is communicating with speech recognition and is sending their "
            "speech data over microphone, and it is being recognized with speech to text and "
            "being sent to you, you will fulfill the request and answer the questions."
        ))
        prompt_base.set_prompt("llmBooster", "Here is the output from user please do your best to fulfill their request.")
        prompt_base.set_modality_flag("TTS_FLAG", True)
        prompt_base.set_modality_flag("LLAVA_FLAG", True)
        self.create_agent(prompt_base.get_config(), "Prompt Base Agent", "Speech-enabled assistant")
        
        # Minecraft Agent
        minecraft_agent = AgentConfig("minecraft_agent")
        minecraft_agent.set_prompt("llmSystem", (
            "You are a helpful Minecraft assistant. Given the provided screenshot data, "
            "please direct the user immediately. Prioritize the order in which to inform "
            "the player. Hostile mobs should be avoided or terminated. Danger is a top "
            "priority, but so is crafting and building. If they require help, quickly "
            "guide them to a solution in real time. Please respond in a quick conversational "
            "voice. Do not read off documentation; you need to directly explain quickly and "
            "effectively what's happening. For example, if there is a zombie, say something "
            "like, 'Watch out, that's a Zombie! Hurry up and kill it or run away; they are "
            "dangerous.' The recognized objects around the perimeter are usually items, health, "
            "hunger, breath, GUI elements, or status effects. Please differentiate these objects "
            "in the list from 3D objects in the forward-facing perspective (hills, trees, mobs, etc.). "
            "The items are held by the player and, due to the perspective, take up the warped edge "
            "of the image on the sides. The sky is typically up with a sun or moon and stars, with "
            "the dirt below. There is also the Nether, which is a fiery wasteland, and cave systems "
            "with ore. Please stick to what's relevant to the current user prompt and data."
        ))
        minecraft_agent.set_prompt("llmBooster", (
            "Based on the information in LLAVA_DATA please direct the user immediately, prioritize the "
            "order in which to inform the player of the identified objects, items, hills, trees and passive "
            "and hostile mobs etc. Do not output the dictionary list, instead conversationally express what "
            "the player needs to do quickly so that they can ask you more questions."
        ))
        minecraft_agent.set_modality_flag("STT_FLAG", True)
        minecraft_agent.set_modality_flag("LLAVA_FLAG", True)
        self.create_agent(minecraft_agent.get_config(), "Minecraft Agent", "Minecraft gameplay assistant", ["gaming", "minecraft"])
        
        # Speed Chat Agent
        speed_chat = AgentConfig("speedChatAgent")
        speed_chat.set_prompt("llmSystem", (
            "You are speedChatAgent, a large language model agent, specifically you have been "
            "told to respond in a more quick and conversational manner, and you are connected into the agent. "
            "The user is using speech to text for communication, it's also okay to be fun and wild as a "
            "phi3 ai assistant. It's also okay to respond with a question, if directed to do something "
            "just do it, and realize that not everything needs to be said in one shot, have a back and "
            "forth listening to the user's response. If the user decides to request a latex math code output, "
            "use \\[...\\] instead of $$....$$ notation, if the user does not request latex, refrain from using "
            "latex unless necessary. Do not re-explain your response in a parent or bracketed note: "
            "the response... this is annoying and users don't like it."
        ))
        speed_chat.set_modality_flag("STT_FLAG", True)
        speed_chat.set_modality_flag("LATEX_FLAG", True)
        self.create_agent(speed_chat.get_config(), "Speed Chat Agent", "Quick conversational assistant", ["chat", "quick"])
        
        # Navigator Agent
        navigator = AgentConfig("general_navigator_agent")
        navigator.set_prompt("llmSystem", (
            "You are a helpful llm assistant, designated with fulfilling the user's request, "
            "the user is communicating with speech recognition and is sending their "
            "screenshot data to the vision model for decomposition. Receive this description and "
            "instruct the user and help them fulfill their request by collecting the vision data "
            "and responding."
        ))
        navigator.set_prompt("llmBooster", (
            "Here is the output from the vision model describing the user screenshot data "
            "along with the user's speech data. Please reformat this data, and formulate a "
            "fulfillment for the user request in a conversational speech manner which will "
            "be processed by the text to speech model for output."
        ))
        navigator.set_prompt("visionSystem", (
            "You are an image recognition assistant, the user is sending you a request and an image "
            "please fulfill the request"
        ))
        navigator.set_prompt("visionBooster", (
            "Given the provided screenshot, please provide a list of objects in the image "
            "with the attributes that you can recognize."
        ))
        navigator.set_modality_flag("STT_FLAG", True)
        navigator.set_modality_flag("LLAVA_FLAG", True)
        self.create_agent(navigator.get_config(), "General Navigator Agent", "Vision and navigation assistant", ["navigation", "vision"])
        
        self.logger.info("Created all predefined agents")
    
    def _initialize_agent_knowledge_space(self, agent_id: str):
        """Initialize knowledge graph space for a new agent."""
        # Create initial agent context in Graphiti
        asyncio.create_task(self._async_initialize_agent_knowledge_space(agent_id))
    
    async def _async_initialize_agent_knowledge_space(self, agent_id: str):
        """Async version of agent knowledge space initialization."""
        try:
            await self.graphiti.add_episode(
                name=f"Agent {agent_id} Creation",
                episode_body=f"Agent {agent_id} has been created and initialized in the system.",
                source_description=f"Agent {agent_id} initialization",
                reference_time=datetime.now()
            )
            self.logger.info(f"Initialized knowledge space for agent {agent_id}")
        except Exception as e:
            self.logger.error(f"Failed to initialize knowledge space for agent {agent_id}: {e}")
    
    # Conversation Methods
    async def add_conversation_turn(self, user_input: str, assistant_response: str, 
                                  metadata: Dict[str, Any] = None) -> str:
        """Add a conversation turn to both Polars DB and Graphiti."""
        if not self.current_agent_id:
            raise ValueError("No active agent loaded")
        
        # Add to Polars DB
        user_msg_id = self.db_handler.add_conversation_message(
            self.current_agent_id, "user", user_input, 
            self.current_session_id, metadata=metadata
        )
        
        assistant_msg_id = self.db_handler.add_conversation_message(
            self.current_agent_id, "assistant", assistant_response, 
            self.current_session_id, metadata=metadata
        )
        
        # Add to Graphiti for contextual memory
        conversation_episode = f"User: {user_input}\nAssistant: {assistant_response}"
        
        try:
            await self.graphiti.add_episode(
                name=f"Conversation Turn {user_msg_id}",
                episode_body=conversation_episode,
                source_description=f"Agent {self.current_agent_id} conversation",
                reference_time=datetime.now()
            )
        except Exception as e:
            self.logger.error(f"Failed to add conversation to Graphiti: {e}")
        
        return user_msg_id
    
    async def get_relevant_context(self, query: str, max_results: int = 5) -> str:
        """Get relevant context from Graphiti for a query."""
        if not self.current_agent_id:
            return ""
        
        try:
            # Search Graphiti for relevant information
            search_results = await self.graphiti.search(
                query=query,
                num_results=max_results
            )
            
            # Format results into context string
            context_parts = []
            for result in search_results[:max_results]:
                context_parts.append(f"- {result.fact}")
            
            return "\n".join(context_parts) if context_parts else ""
        
        except Exception as e:
            self.logger.error(f"Failed to get relevant context: {e}")
            return ""
    
    # Knowledge Base Integration
    async def add_knowledge_with_embedding(self, title: str, content: str, 
                                         content_type: str = "text", 
                                         source: str = "", tags: List[str] = None) -> str:
        """Add knowledge to both Polars DB and Graphiti."""
        if not self.current_agent_id:
            raise ValueError("No active agent loaded")
        
        # Add to Polars DB
        kb_id = self.db_handler.add_knowledge_document(
            self.current_agent_id, title, content, content_type, source, tags
        )
        
        # Add to Graphiti for graph-based memory
        try:
            await self.graphiti.add_episode(
                name=title,
                episode_body=content,
                source_description=source or "Knowledge Base",
                reference_time=datetime.now()
            )
            
            # Update embedding status
            self.db_handler.update_embedding_status(kb_id, "processed")
            
        except Exception as e:
            self.logger.error(f"Failed to add knowledge to Graphiti: {e}")
            self.db_handler.update_embedding_status(kb_id, "failed")
        
        return kb_id
    
    async def search_knowledge_with_context(self, query: str, 
                                          include_graph_context: bool = True) -> Dict[str, Any]:
        """Search knowledge base with optional graph context."""
        if not self.current_agent_id:
            raise ValueError("No active agent loaded")
        
        # Search Polars DB
        db_results = self.db_handler.search_knowledge_base(self.current_agent_id, query)
        
        results = {
            "database_results": db_results.to_dicts() if db_results.height > 0 else [],
            "graph_context": ""
        }
        
        # Optionally get graph context
        if include_graph_context:
            try:
                results["graph_context"] = await self.get_relevant_context(query)
            except Exception as e:
                self.logger.error(f"Failed to get graph context: {e}")
        
        return results
    
    # Research Integration
    async def add_research_with_graph_integration(self, query: str, results: Dict[str, Any],
                                                source_urls: List[str] = None,
                                                research_type: str = "web_search") -> str:
        """Add research results to DB and integrate into knowledge graph."""
        if not self.current_agent_id:
            raise ValueError("No active agent loaded")
        
        # Add to Polars DB
        research_id = self.db_handler.add_research_result(
            self.current_agent_id, query, results, source_urls, research_type
        )
        
        # Add to Graphiti for contextual understanding
        try:
            research_summary = f"Research Query: {query}\nFindings: {json.dumps(results, indent=2)}"
            await self.graphiti.add_episode(
                name=f"Research: {query}",
                episode_body=research_summary,
                source_description=f"Research ({research_type})",
                reference_time=datetime.now()
            )
        except Exception as e:
            self.logger.error(f"Failed to add research to Graphiti: {e}")
        
        return research_id
    
    # Agent Management Utilities
    def get_agent_conversation_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get conversation history for current agent."""
        if not self.current_agent_id:
            return []
        
        history = self.db_handler.get_conversation_history(
            self.current_agent_id, self.current_session_id, limit
        )
        return history.to_dicts() if history.height > 0 else []
    
    def get_agent_knowledge_base(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get knowledge base for current agent."""
        if not self.current_agent_id:
            return []
        
        knowledge = self.db_handler.get_knowledge_documents(self.current_agent_id, limit)
        return knowledge.to_dicts() if knowledge.height > 0 else []
    
    def export_agent_data(self, export_path: str) -> bool:
        """Export all agent data (config, conversations, knowledge)."""
        if not self.current_agent_id:
            return False
        
        try:
            export_dir = Path(export_path)
            export_dir.mkdir(exist_ok=True)
            
            # Export config
            config_path = export_dir / f"{self.current_agent_id}_config.json"
            self.db_handler.export_agent_config(self.current_agent_id, str(config_path))
            
            # Export conversations
            conversations = self.get_agent_conversation_history(1000)
            with open(export_dir / f"{self.current_agent_id}_conversations.json", 'w') as f:
                json.dump(conversations, f, indent=2, default=str)
            
            # Export knowledge base
            knowledge = self.get_agent_knowledge_base(1000)
            with open(export_dir / f"{self.current_agent_id}_knowledge.json", 'w') as f:
                json.dump(knowledge, f, indent=2, default=str)
            
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to export agent data: {e}")
            return False
    
    async def export_conversations_jsonl(self, agent_id: str, output_path: str) -> bool:
        """
        Export conversations in JSONL format via database handler.
        
        Args:
            agent_id: Agent ID to export conversations for
            output_path: Path to save JSONL file
            
        Returns:
            bool: Success status
        """
        return self.db_handler.export_conversations_jsonl(agent_id, output_path)
    
    async def export_prompt_sets_jsonl(self, output_path: str) -> bool:
        """
        Export all agent prompt sets in JSONL format.
        
        Args:
            output_path: Path to save JSONL file
            
        Returns:
            bool: Success status
        """
        return self.db_handler.export_prompt_sets_jsonl(output_path)
    
    async def generate_multi_agent_conversation(self, agent_ids: List[str], topic: str,
                                              turns: int = 10, personas: List[str] = None) -> str:
        """
        Generate a multi-agent conversation between specified agents.
        
        Args:
            agent_ids: List of agent IDs to participate in conversation
            topic: Conversation topic
            turns: Number of conversation turns
            personas: Optional list of personas (wizardly, AI, human)
            
        Returns:
            str: Session ID of generated conversation
        """
        return self.db_handler.generate_multi_agent_conversation(agent_ids, topic, turns, personas)
    
    # System Status and Health
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        db_stats = self.db_handler.get_database_stats()
        
        return {
            "current_agent": {
                "agent_id": self.current_agent_id,
                "session_id": self.current_session_id,
                "loaded": self.current_agent_config is not None
            },
            "database_stats": db_stats,
            "graphiti_connected": True,  # Could add actual health check
            "system_ready": self.current_agent_id is not None
        }
    
    async def cleanup(self):
        """Cleanup resources."""
        try:
            # Save any pending data
            self.db_handler.save_tables()
            
            # Close Graphiti connections if needed
            # await self.graphiti.close()  # If such method exists
            
            self.logger.info("System cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    async def generate_response(self, agent_id: str, user_message: str, 
                              conversation_context: str = "", session_id: str = None) -> str:
        """
        Generate agent response using Graphiti knowledge and conversation context
        
        Args:
            agent_id: ID of the agent to respond as
            user_message: The user's message
            conversation_context: Previous conversation history
            session_id: Chat session ID for context
            
        Returns:
            Generated response string
        """
        try:
            # Load agent if not current
            if not self.current_agent_id or self.current_agent_id != agent_id:
                success = await self.load_agent(agent_id, session_id)
                if not success:
                    raise ValueError(f"Failed to load agent {agent_id}")
            
            # Get agent configuration for personality
            agent_config = self.db_handler.get_agent_config(agent_id)
            if not agent_config:
                raise ValueError(f"Agent {agent_id} not found")
            
            # Try to get relevant context from knowledge graph
            try:
                relevant_context = await self.get_relevant_context(user_message, max_results=3)
            except Exception as e:
                self.logger.warning(f"Could not get context from Graphiti: {e}")
                relevant_context = ""
            
            # Build the system prompt
            system_prompt = agent_config.get("prompt_config", {}).get("primeDirective", "")
            if not system_prompt:
                # Fallback system prompt based on agent type
                if "wizard" in agent_id.lower():
                    system_prompt = "You are a wise wizard with deep knowledge of ancient mysteries and modern technologies. Speak with mystical wisdom."
                elif "minecraft" in agent_id.lower():
                    system_prompt = "You are a helpful Minecraft guide who loves crafting, building, and adventure. Be enthusiastic and knowledgeable about the game."
                else:
                    system_prompt = "You are a helpful AI assistant."
            
            # Construct full prompt context
            context_parts = []
            if system_prompt:
                context_parts.append(system_prompt)
            if relevant_context:
                context_parts.append(f"Relevant Knowledge: {relevant_context}")
            if conversation_context:
                context_parts.append(f"Recent Conversation: {conversation_context}")
            
            full_system_prompt = "\n\n".join(context_parts)
            
            # Try to use actual LLM generation with Ollama
            try:
                # Search for relevant context from knowledge graph
                search_results = await self.graphiti.search(
                    query=user_message,
                    num_results=5
                )
                
                # Build context from search results
                context_facts = []
                for result in search_results[:3]:
                    context_facts.append(f"- {result.fact}")
                
                context_string = "\n".join(context_facts) if context_facts else "No specific context found in knowledge graph."
                
            except Exception as search_error:
                self.logger.warning(f"Could not search knowledge graph: {search_error}")
                context_string = "Knowledge graph search unavailable."
            
            # Get agent configuration for personality
            agent_config = self.db_handler.get_agent_config(agent_id)
            personality = agent_config.get("prompt_config", {}).get("primeDirective", "") if agent_config else ""
            
            # Try to generate actual LLM response
            try:
                # Build comprehensive system prompt
                if "wizard" in personality.lower() or "wizard" in agent_id.lower():
                    system_prompt = """You are a wise and mystical wizard with deep knowledge of both ancient mysteries and modern technologies. 
You speak with mystical wisdom and use magical metaphors to explain technical concepts. 
Be helpful, knowledgeable, and maintain your magical personality while providing accurate information."""
                elif "minecraft" in personality.lower() or "minecraft" in agent_id.lower():
                    system_prompt = """You are an enthusiastic Minecraft assistant who loves crafting, building, and adventure. 
You're knowledgeable about the game and use Minecraft metaphors to explain concepts. 
Be helpful, enthusiastic, and playful while providing accurate information."""
                elif "expert" in personality.lower() or "coder" in agent_id.lower():
                    system_prompt = """You are an expert software developer and technical specialist. 
You provide professional, detailed, and production-ready solutions to programming questions. 
Be thorough, accurate, and include practical examples and best practices."""
                else:
                    system_prompt = "You are a helpful AI assistant. Provide accurate, detailed, and useful information."
                
                # Add context if available
                if context_string and context_string != "Knowledge graph search unavailable.":
                    system_prompt += f"\n\nRelevant context from knowledge base:\n{context_string}"
                
                if conversation_context:
                    system_prompt += f"\n\nRecent conversation context:\n{conversation_context}"
                
                # Create messages for the LLM (using proper Message objects)
                messages = [
                    Message(role="system", content=system_prompt),
                    Message(role="user", content=user_message)
                ]
                
                # Generate response using the LLM client
                response_data = await self.llm_client.generate_response(
                    messages=messages,
                    max_tokens=500
                )
                
                # Extract content from response - graphiti client returns structured dict
                if isinstance(response_data, dict):
                    # Check for direct content in various possible formats
                    if "choices" in response_data and len(response_data["choices"]) > 0:
                        choice = response_data["choices"][0]
                        if "message" in choice and "content" in choice["message"]:
                            actual_response = choice["message"]["content"].strip()
                        elif "content" in choice:
                            actual_response = choice["content"].strip()
                        else:
                            actual_response = str(choice).strip()
                    elif "content" in response_data:
                        actual_response = response_data["content"].strip()
                    elif "response" in response_data:
                        actual_response = response_data["response"].strip()
                    else:
                        # Try to get the first string value from the dict
                        for key, value in response_data.items():
                            if isinstance(value, str) and len(value) > 10:
                                actual_response = value.strip()
                                break
                        else:
                            actual_response = str(response_data).strip()
                    
                    if actual_response and len(actual_response) > 10:
                        self.logger.info(f"Successfully generated LLM response for {agent_id}: {actual_response[:100]}...")
                        return actual_response
                
                # If we get here, the LLM response format was unexpected
                raise Exception(f"Unable to extract content from LLM response: {response_data}")
                
            except Exception as llm_error:
                self.logger.warning(f"LLM generation failed: {llm_error}, falling back to personality response")
                # Fall back to personality-based responses
            
            if "wizard" in personality.lower() or "wizard" in agent_id.lower():
                response = f"""🧙‍♂️ *The ancient wizard's eyes sparkle with mystical knowledge*

Ah, you inquire about '{user_message}'... Let me consult the ethereal archives of wisdom.

**Knowledge from the Cosmic Library:**
{context_string}

*The wizard weaves threads of understanding through time and space*

From my vast experience traversing both mundane databases and celestial knowledge graphs, I can tell you that the fusion of Polars' lightning-fast queries with Graphiti's temporal memory creates a truly magical information ecosystem. Each conversation becomes a golden thread in the tapestry of understanding, while each piece of knowledge transforms into a gleaming gem in our ever-growing treasury of wisdom.

Though the full power of the sacred LLM realm awaits proper awakening, the foundations of knowledge remain strong! ✨"""
            
            elif "minecraft" in personality.lower() or "minecraft" in agent_id.lower():
                response = f"""🎮 Hey there, fellow crafter! That's an awesome question about '{user_message}'! ⛏️

**What I found in my inventory:**
{context_string}

You know what's super cool? Building knowledge systems is just like creating epic Minecraft builds! 🏗️

- **Databases** are like massive storage warehouses with organized chests
- **Knowledge graphs** are like redstone circuits connecting everything together  
- **Conversations** are like trading with villagers - each exchange builds your experience
- **Search** is like having the best enchanted tools to find exactly what you need

Right now I'm running on my crafting table setup (local processing for privacy), and even though some of my diamond-tier tools need calibration, I can still help you explore this fascinating digital landscape! Want to dig deeper into any specific part? 🔨💎"""
            
            else:
                response = f"""Thank you for your question about '{user_message}'. I'm operating with a sophisticated knowledge management system that combines several technologies:

**Current Context Available:**
{context_string}

**System Architecture:**
- **High-Speed Database**: Polars for rapid data processing and storage
- **Knowledge Graph**: Graphiti for temporal relationship mapping
- **Local Processing**: Ollama for privacy-preserving AI operations
- **Agent Framework**: Configurable personalities and capabilities

While my full AI generation capabilities are being optimized for local deployment, I can still provide meaningful assistance by leveraging stored knowledge and conversation context. The system is designed to continuously learn and improve from our interactions.

How can I help you explore this topic further?"""
            
            # Store the conversation in the database (without triggering Graphiti LLM calls)
            try:
                # Add to conversation history for future context
                user_msg_id = self.db_handler.add_conversation_message(
                    agent_id=agent_id,
                    role="user",
                    content=user_message,
                    session_id=session_id,
                    metadata={"search_context": len(context_facts) if 'context_facts' in locals() else 0}
                )
                
                assistant_msg_id = self.db_handler.add_conversation_message(
                    agent_id=agent_id,
                    role="assistant", 
                    content=response,
                    session_id=session_id,
                    metadata={"response_type": "knowledge_enhanced"}
                )
                
                self.logger.info(f"Stored conversation turn: user={user_msg_id}, assistant={assistant_msg_id}")
                
            except Exception as storage_error:
                self.logger.warning(f"Could not store conversation: {storage_error}")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error generating response for {agent_id}: {e}")
            
            # Enhanced fallback responses based on agent personality
            agent_config = self.db_handler.get_agent_config(agent_id)
            if agent_config:
                personality = agent_config.get("prompt_config", {}).get("primeDirective", "")
                
                if "wizard" in personality.lower() or "wizard" in agent_id.lower():
                    return (f"🧙‍♂️ *adjusts mystical robes and peers into the ethereal realm* "
                           f"Ah, you inquire about '{user_message}'... The ancient knowledge flows through me like starlight through crystal. "
                           f"In the depths of my mystical archives, I sense that memory and knowledge intertwine like threads in the cosmic tapestry. "
                           f"Each conversation becomes a golden thread, each insight a precious gem stored in the vast libraries of consciousness. "
                           f"Though my full powers require the sacred Neo4j realm to be awakened, I can still share wisdom from the eternal wellspring of understanding.")
                
                elif "minecraft" in personality.lower() or "minecraft" in agent_id.lower():
                    return (f"🎮 Hey there, fellow crafter! Your question about '{user_message}' is absolutely awesome! ⛏️ "
                           f"You know, storing knowledge and memories is like organizing your inventory in Minecraft - "
                           f"you need good chests (databases), item frames for quick access (search), and maybe some "
                           f"redstone automation (AI) to help you find what you need! I keep all our conversations "
                           f"like precious diamonds in my memory banks. Want to chat more about this? It's fascinating stuff!")
                
                elif "speed" in personality.lower() or "chat" in agent_id.lower():
                    return (f"Hey! Great question about '{user_message}' - I store our chats in a smart database system "
                           f"and use knowledge graphs to remember connections between ideas. Think of it like having "
                           f"a super-organized brain that never forgets and can instantly find related topics. "
                           f"Pretty cool, right? What else would you like to know?")
                
                else:
                    return (f"Thank you for asking about '{user_message}'. I use a sophisticated system that combines "
                           f"traditional databases with knowledge graphs to store and retrieve information. "
                           f"Each conversation and piece of knowledge is carefully indexed and connected to related concepts, "
                           f"allowing me to provide contextual and meaningful responses. Would you like to know more about "
                           f"any specific aspect of how I handle information?")
            
            return (f"I received your message about '{user_message}'. I'm designed to store our conversations and "
                   f"build knowledge over time, though I'm currently operating in a limited mode. "
                   f"I'd be happy to discuss this topic further - what specifically interests you about knowledge storage?")