"""
AMS-DB Configuration Management

Utilities for managing configuration files and environment setup.
"""

import json
import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

from ..core import AgentConfig


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    db_path: str = "agent_database"
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"
    backup_interval_hours: int = 24
    max_backup_files: int = 10


@dataclass
class LLMConfig:
    """LLM configuration settings."""
    ollama_base_url: str = "http://localhost:11434/v1"
    llm_model: str = "phi4:latest"
    small_model: str = "gemma3:4b"
    embedding_model: str = "nomic-embed-text"
    embedding_dim: int = 768
    temperature: float = 0.7
    max_tokens: int = 2048


@dataclass
class SystemConfig:
    """System-wide configuration."""
    database: DatabaseConfig
    llm: LLMConfig
    log_level: str = "INFO"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    enable_cors: bool = True


class ConfigManager:
    """Configuration manager for AMS-DB."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager."""
        self.config_path = Path(config_path) if config_path else self._get_default_config_path()
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._config = self._load_config()
    
    def _get_default_config_path(self) -> Path:
        """Get default configuration file path."""
        # Try to use XDG config directory, fallback to home
        config_home = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
        return Path(config_home) / "ams-db" / "config.yaml"
    
    def _load_config(self) -> SystemConfig:
        """Load configuration from file or create default."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    data = yaml.safe_load(f)
                return self._dict_to_config(data)
            except Exception as e:
                print(f"Warning: Failed to load config from {self.config_path}: {e}")
                print("Using default configuration")
        
        # Create default config
        config = SystemConfig(
            database=DatabaseConfig(),
            llm=LLMConfig()
        )
        self.save_config(config)
        return config
    
    def _dict_to_config(self, data: Dict[str, Any]) -> SystemConfig:
        """Convert dictionary to SystemConfig."""
        return SystemConfig(
            database=DatabaseConfig(**data.get('database', {})),
            llm=LLMConfig(**data.get('llm', {})),
            log_level=data.get('log_level', 'INFO'),
            api_host=data.get('api_host', '127.0.0.1'),
            api_port=data.get('api_port', 8000),
            enable_cors=data.get('enable_cors', True)
        )
    
    def _config_to_dict(self, config: SystemConfig) -> Dict[str, Any]:
        """Convert SystemConfig to dictionary."""
        return {
            'database': {
                'db_path': config.database.db_path,
                'neo4j_uri': config.database.neo4j_uri,
                'neo4j_user': config.database.neo4j_user,
                'neo4j_password': config.database.neo4j_password,
                'backup_interval_hours': config.database.backup_interval_hours,
                'max_backup_files': config.database.max_backup_files
            },
            'llm': {
                'ollama_base_url': config.llm.ollama_base_url,
                'llm_model': config.llm.llm_model,
                'small_model': config.llm.small_model,
                'embedding_model': config.llm.embedding_model,
                'embedding_dim': config.llm.embedding_dim,
                'temperature': config.llm.temperature,
                'max_tokens': config.llm.max_tokens
            },
            'log_level': config.log_level,
            'api_host': config.api_host,
            'api_port': config.api_port,
            'enable_cors': config.enable_cors
        }
    
    def get_config(self) -> SystemConfig:
        """Get current configuration."""
        return self._config
    
    def update_config(self, **kwargs) -> None:
        """Update configuration values."""
        # Update nested values
        for key, value in kwargs.items():
            if hasattr(self._config, key):
                if hasattr(getattr(self._config, key), '__dict__'):
                    # It's a nested config object
                    for nested_key, nested_value in value.items():
                        setattr(getattr(self._config, key), nested_key, nested_value)
                else:
                    setattr(self._config, key, value)
        
        self.save_config(self._config)
    
    def save_config(self, config: SystemConfig) -> None:
        """Save configuration to file."""
        data = self._config_to_dict(config)
        
        with open(self.config_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, indent=2)
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults."""
        self._config = SystemConfig(
            database=DatabaseConfig(),
            llm=LLMConfig()
        )
        self.save_config(self._config)


class AgentTemplateManager:
    """Manager for predefined agent templates."""
    
    def __init__(self):
        """Initialize template manager."""
        self.templates = self._create_default_templates()
    
    def _create_default_templates(self) -> Dict[str, Dict[str, Any]]:
        """Create default agent templates."""
        templates = {}
        
        # Default Agent Template
        default_agent = AgentConfig("default_agent")
        default_agent.set_prompt("llmSystem", "You are a helpful AI assistant.")
        default_agent.set_modality_flag("ACTIVE_AGENT_FLAG", True)
        templates["default"] = {
            "name": "Default Agent",
            "description": "Basic helpful assistant",
            "config": default_agent.get_config(),
            "tags": ["basic", "assistant"]
        }
        
        # Speed Chat Agent Template
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
        templates["speed_chat"] = {
            "name": "Speed Chat Agent",
            "description": "Quick conversational assistant with speech support",
            "config": speed_chat.get_config(),
            "tags": ["chat", "speech", "conversational"]
        }
        
        # Minecraft Agent Template
        minecraft_agent = AgentConfig("minecraft_agent")
        minecraft_agent.set_prompt("llmSystem", (
            "You are a helpful Minecraft assistant. Given the provided screenshot data, "
            "please direct the user immediately. Prioritize the order in which to inform "
            "the player. Hostile mobs should be avoided or terminated. Danger is a top "
            "priority, but so is crafting and building. If they require help, quickly "
            "guide them to a solution in real time. Please respond in a quick conversational "
            "voice. Do not read off documentation; you need to directly explain quickly and "
            "effectively what's happening."
        ))
        minecraft_agent.set_modality_flag("STT_FLAG", True)
        minecraft_agent.set_modality_flag("LLAVA_FLAG", True)
        templates["minecraft"] = {
            "name": "Minecraft Assistant",
            "description": "Gaming assistant specialized for Minecraft",
            "config": minecraft_agent.get_config(),
            "tags": ["gaming", "minecraft", "vision"]
        }
        
        # Navigator Agent Template
        navigator = AgentConfig("general_navigator_agent")
        navigator.set_prompt("llmSystem", (
            "You are a helpful llm assistant, designated with fulfilling the user's request, "
            "the user is communicating with speech recognition and is sending their "
            "screenshot data to the vision model for decomposition. Receive this description and "
            "instruct the user and help them fulfill their request by collecting the vision data "
            "and responding."
        ))
        navigator.set_modality_flag("STT_FLAG", True)
        navigator.set_modality_flag("LLAVA_FLAG", True)
        templates["navigator"] = {
            "name": "General Navigator",
            "description": "Vision and navigation assistant",
            "config": navigator.get_config(),
            "tags": ["navigation", "vision", "assistant"]
        }
        
        return templates
    
    def get_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get a template by name."""
        return self.templates.get(template_name)
    
    def list_templates(self) -> Dict[str, Dict[str, Any]]:
        """List all available templates."""
        return {name: {
            "name": template["name"],
            "description": template["description"],
            "tags": template["tags"]
        } for name, template in self.templates.items()}
    
    def create_agent_from_template(self, template_name: str, agent_id: str = None) -> Optional[AgentConfig]:
        """Create an agent configuration from a template."""
        template = self.get_template(template_name)
        if not template:
            return None
        
        config = AgentConfig()
        config.from_dict(template["config"])
        
        if agent_id:
            config.set_agent_id(agent_id)
        
        return config
    
    def export_template(self, template_name: str, filepath: str) -> bool:
        """Export a template to a JSON file."""
        template = self.get_template(template_name)
        if not template:
            return False
        
        try:
            with open(filepath, 'w') as f:
                json.dump(template, f, indent=2)
            return True
        except Exception:
            return False
    
    def import_template(self, filepath: str, template_name: str) -> bool:
        """Import a template from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                template = json.load(f)
            
            # Validate template structure
            required_keys = ["name", "description", "config"]
            if not all(key in template for key in required_keys):
                return False
            
            self.templates[template_name] = template
            return True
        except Exception:
            return False


# Global instances
config_manager = ConfigManager()
template_manager = AgentTemplateManager()


def get_config() -> SystemConfig:
    """Get current system configuration."""
    return config_manager.get_config()


def get_template_manager() -> AgentTemplateManager:
    """Get template manager instance."""
    return template_manager
