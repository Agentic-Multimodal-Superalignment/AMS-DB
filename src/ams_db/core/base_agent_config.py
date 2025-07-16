import json
import copy
from typing import Dict, Any, Optional

class AgentConfig:
    """
    A class to manage agent configurations with JSON serialization/deserialization.
    """
    
    def __init__(self, agent_id: str = ""):
        """
        Initialize with base configuration template.
        
        Args:
            agent_id: Unique identifier for the agent
        """
        self.config = {
            "agent_id": agent_id,
            "model_config": {
                "largeLanguageModel": {
                    "names": [], 
                    "instances": [], 
                    "model_config_template": {}
                },
                "embeddingModel": {
                    "names": [], 
                    "instances": [], 
                    "model_config_template": {}
                },
                "largeLanguageAndVisionAssistant": {
                    "names": [], 
                    "instances": [], 
                    "model_config_template": {}
                },
                "yoloVision": {
                    "names": [], 
                    "instances": [], 
                    "model_config_template": {}
                },
                "speechRecognitionSTT": {
                    "names": [], 
                    "instances": [], 
                    "model_config_template": {}
                },
                "voiceGenerationTTS": {
                    "names": [], 
                    "instances": [], 
                    "model_config_template": {}
                }
            },
            "prompt_config": {
                "userInput": "",
                "agent": {
                    "llmSystem": "",
                    "llmBooster": "",
                    "visionSystem": "",
                    "visionBooster": "",
                },
                "primeDirective": ""
            },
            "command_flags": {
                "TTS_FLAG": False,
                "STT_FLAG": False,
                "CHUNK_AUDIO_FLAG": False,
                "AUTO_SPEECH_FLAG": False,
                "LLAVA_FLAG": False,
                "SCREEN_SHOT_FLAG": False,
                "SPLICE_VIDEO_FLAG": False,
                "AUTO_COMMANDS_FLAG": False,
                "CLEAR_MEMORY_FLAG": False,
                "ACTIVE_AGENT_FLAG": False,
                "EMBEDDING_FLAG": False,
                "LLM_SYSTEM_PROMPT_FLAG": False,
                "LLM_BOOSTER_PROMPT_FLAG": False,
                "VISION_SYSTEM_PROMPT_FLAG": False,
                "VISION_BOOSTER_PROMPT_FLAG": False,
                "LATEX_FLAG": False,
                "CMD_RUN_FLAG": False,
                "AGENT_FLAG": True,
                "MEMORY_CLEAR_FLAG": False
            },
            "databases": {
                "agent_matrix": "",
                "conversation_history": "",
                "knowledge_base": "",
                "research_collection": "",
                "template_files": ""
            },
            # Enhanced database-specific configs
            "database_config": {
                "conversation_modes": {
                    "current_session_only": False,
                    "use_past_conversations": True,
                    "max_history_turns": 100
                },
                "knowledge_base_categories": ["general", "technical", "domain_specific"],
                "research_collection_fields": {
                    "mathematics": {"enabled": True, "priority": "high"},
                    "physics": {"enabled": True, "priority": "medium"}, 
                    "software_development": {"enabled": True, "priority": "high"},
                    "ai_ml": {"enabled": True, "priority": "high"},
                    "database_systems": {"enabled": True, "priority": "medium"},
                    "agentic_alignment": {"enabled": True, "priority": "high"}
                }
            }
        }
    
    def set_agent_id(self, agent_id: str):
        """Set the agent ID."""
        self.config["agent_id"] = agent_id
    
    def set_prompt(self, prompt_type: str, prompt_text: str):
        """
        Set a specific prompt type.
        
        Args:
            prompt_type: Type of prompt (llmSystem, llmBooster, visionSystem, visionBooster, primeDirective)
            prompt_text: The prompt text content
        """
        valid_prompt_types = ["llmSystem", "llmBooster", "visionSystem", "visionBooster", "primeDirective"]
        
        if prompt_type not in valid_prompt_types:
            raise ValueError(f"Invalid prompt type. Must be one of: {valid_prompt_types}")
        
        if prompt_type == "primeDirective":
            self.config["prompt_config"]["primeDirective"] = prompt_text
        else:
            self.config["prompt_config"]["agent"][prompt_type] = prompt_text
    
    def set_modality_flag(self, flag_name: str, value: bool):
        """
        Set a modality flag.
        
        Args:
            flag_name: Name of the flag
            value: Boolean value for the flag
        """
        valid_flags = list(self.config["command_flags"].keys())
        
        if flag_name not in valid_flags:
            raise ValueError(f"Invalid flag name. Must be one of: {valid_flags}")
        
        self.config["command_flags"][flag_name] = value
    
    def set_database(self, db_name: str, db_path: str):
        """
        Set a database path.
        
        Args:
            db_name: Name of the database
            db_path: Path to the database
        """
        valid_databases = list(self.config["databases"].keys())
        
        if db_name not in valid_databases:
            raise ValueError(f"Invalid database name. Must be one of: {valid_databases}")
        
        self.config["databases"][db_name] = db_path
    
    def update_config(self, updates: Dict[str, Any]):
        """
        Update configuration with nested dictionary updates.
        
        Args:
            updates: Dictionary of updates to apply
        """
        def deep_update(base_dict, update_dict):
            for key, value in update_dict.items():
                if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
                    deep_update(base_dict[key], value)
                else:
                    base_dict[key] = value
        
        deep_update(self.config, updates)
    
    def get_config(self) -> Dict[str, Any]:
        """Get the current configuration as a dictionary."""
        return copy.deepcopy(self.config)
    
    def to_json(self, filepath: str, indent: int = 2):
        """
        Save configuration to JSON file.
        
        Args:
            filepath: Path to save the JSON file
            indent: JSON indentation level
        """
        with open(filepath, 'w') as f:
            json.dump(self.config, f, indent=indent)
    
    def from_json(self, filepath: str):
        """
        Load configuration from JSON file.
        
        Args:
            filepath: Path to the JSON file
        """
        with open(filepath, 'r') as f:
            self.config = json.load(f)
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self.get_config()
    
    def from_dict(self, config_dict: Dict[str, Any]):
        """
        Load configuration from dictionary.
        
        Args:
            config_dict: Configuration dictionary
        """
        self.config = copy.deepcopy(config_dict)
    
    def __str__(self):
        """String representation of the configuration."""
        return json.dumps(self.config, indent=2)
    
    def __repr__(self):
        """Representation of the AgentConfig object."""
        return f"AgentConfig(agent_id='{self.config['agent_id']}')"

# Example usage:
if __name__ == "__main__":
    # Create a new agent config
    agent = AgentConfig("speedChatAgent")
    
    # Set some prompts
    agent.set_prompt("llmSystem", "You are a speed chat agent...")
    
    # Set modality flags
    agent.set_modality_flag("STT_FLAG", True)
    agent.set_modality_flag("LATEX_FLAG", True)
    
    # Set database paths
    agent.set_database("conversation_history", "speedChatAgent_conversation.db")
    
    # Update with complex nested data
    agent.update_config({
        "model_config": {"temperature": 0.7, "max_tokens": 1000},
        "agent_core": {
            "models": {
                "largeLanguageModel": {
                    "names": ["gpt-4", "claude-3"],
                    "instances": [1, 2]
                }
            }
        }
    })
    
    # Save to JSON
    agent.to_json("speed_chat_config.json")
    
    # Load from JSON
    new_agent = AgentConfig()
    new_agent.from_json("speed_chat_config.json")
    
    print(new_agent)