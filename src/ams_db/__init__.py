"""
AMS-DB: Agentic Multimodal Super-alignment Database

A comprehensive database foundation for multimodal agent projects with
Graphiti knowledge graphs and Polars high-performance data management.
"""

from .core.base_agent_config import AgentConfig
from .core.polars_db import PolarsDBHandler
from .core.graphiti_pipe import GraphitiRAGFramework

__version__ = "0.1.0"
__author__ = "AMS Team"

__all__ = [
    "AgentConfig",
    "PolarsDBHandler", 
    "GraphitiRAGFramework",
]
