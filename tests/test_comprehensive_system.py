#!/usr/bin/env python3
"""
Comprehensive system test to verify all components are working correctly
"""
import os
import asyncio
import json
from pathlib import Path

# Set environment variables
os.environ['NEO4J_URI'] = 'bolt://localhost:7687'
os.environ['NEO4J_USER'] = 'neo4j'
os.environ['NEO4J_PASSWORD'] = 'temppass123'

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.ams_db.core.polars_db import PolarsDBHandler
from src.ams_db.core.graphiti_pipe import GraphitiRAGFramework
from src.ams_db.cli.chat_manager import ChatManager
from src.ams_db.core.base_agent_config import AgentConfig

class SystemTester:
    """Comprehensive system testing class"""
    
    def __init__(self):
        self.db_handler = PolarsDBHandler("agent_database")
        self.framework = GraphitiRAGFramework()
        self.chat_manager = ChatManager(self.db_handler)
        self.test_results = {}
    
    def test_database_connection(self):
        """Test database connectivity and basic operations"""
        print("\n🔍 Testing Database Connection...")
        try:
            # Test basic DB operations
            agents = self.db_handler.list_agents()
            print(f"✅ Database connected - Found {len(agents)} agents")
            
            # Check if wizard agent exists
            wizard_config = self.db_handler.get_agent_config("wizard_agent_001")
            if wizard_config:
                print("✅ Wizard agent configuration found")
            else:
                print("⚠️ Wizard agent not found - creating basic config")
                self._create_basic_wizard_agent()
            
            self.test_results['database'] = 'PASS'
            return True
            
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            self.test_results['database'] = f'FAIL: {e}'
            return False
    
    async def test_neo4j_connection(self):
        """Test Neo4j connectivity"""
        print("\n🔍 Testing Neo4j Connection...")
        try:
            # Test if framework can connect to Neo4j
            await self.framework.load_agent("wizard_agent_001")
            print("✅ Neo4j connection successful")
            self.test_results['neo4j'] = 'PASS'
            return True
            
        except Exception as e:
            print(f"❌ Neo4j test failed: {e}")
            self.test_results['neo4j'] = f'FAIL: {e}'
            return False
    
    def test_ollama_connection(self):
        """Test Ollama connectivity"""
        print("\n🔍 Testing Ollama Connection...")
        try:
            import requests
            response = requests.get('http://localhost:11434/api/tags', timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                print(f"✅ Ollama connected - Found {len(models)} models")
                
                # Check for deepseek-r1 model
                model_names = [m['name'] for m in models]
                if any('deepseek-r1' in name for name in model_names):
                    print("✅ DeepSeek-R1 model available")
                else:
                    print("⚠️ DeepSeek-R1 model not found")
                
                self.test_results['ollama'] = 'PASS'
                return True
            else:
                raise Exception(f"HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ollama test failed: {e}")
            self.test_results['ollama'] = f'FAIL: {e}'
            return False
    
    async def test_agent_response_generation(self):
        """Test agent response generation"""
        print("\n🔍 Testing Agent Response Generation...")
        try:
            # Load wizard agent first
            await self.framework.load_agent("wizard_agent_001")
            
            # Test response generation
            test_query = "What is machine learning?"
            response = await self.framework.generate_response(test_query, test_query)  # message and user_message
            
            if response and len(response) > 10:
                print(f"✅ Agent response generated: {response[:100]}...")
                self.test_results['agent_response'] = 'PASS'
                return True
            else:
                raise Exception("Empty or too short response")
                
        except Exception as e:
            print(f"❌ Agent response test failed: {e}")
            self.test_results['agent_response'] = f'FAIL: {e}'
            return False
    
    async def test_chat_manager(self):
        """Test chat manager functionality"""
        print("\n🔍 Testing Chat Manager...")
        try:
            # Start a chat session
            session_id, alias = self.chat_manager.start_human_chat("wizard_agent_001", "System Test")
            print(f"✅ Chat session created: {alias}")
            
            # Send a test message
            test_message = "Hello wizard, can you tell me about AI?"
            response = await self.chat_manager.send_message_to_agent(session_id, "wizard_agent_001", test_message)
            
            if response and len(response) > 10:
                print(f"✅ Chat response received: {response[:100]}...")
                self.test_results['chat_manager'] = 'PASS'
                return True
            else:
                raise Exception("Empty or too short chat response")
                
        except Exception as e:
            print(f"❌ Chat manager test failed: {e}")
            self.test_results['chat_manager'] = f'FAIL: {e}'
            return False
    
    def test_knowledge_base(self):
        """Test knowledge base functionality"""
        print("\n🔍 Testing Knowledge Base...")
        try:
            # Check for existing knowledge documents
            knowledge_docs = self.framework.get_agent_knowledge_base()
            print(f"✅ Knowledge base accessible - Found {len(knowledge_docs)} documents")
            
            # Test adding a knowledge document
            test_doc_id = self.db_handler.add_knowledge_document(
                agent_id="wizard_agent_001",
                title="Test Knowledge Document",
                content="This is a test knowledge document for system verification.",
                content_type="text",
                source="system_test",
                tags=["test", "verification"]
            )
            
            print(f"✅ Knowledge document added: {test_doc_id}")
            self.test_results['knowledge_base'] = 'PASS'
            return True
            
        except Exception as e:
            print(f"❌ Knowledge base test failed: {e}")
            self.test_results['knowledge_base'] = f'FAIL: {e}'
            return False
    
    async def test_graphiti_integration(self):
        """Test Graphiti integration"""
        print("\n🔍 Testing Graphiti Integration...")
        try:
            # Load agent first
            await self.framework.load_agent("wizard_agent_001")
            
            # Test search functionality
            search_results = await self.framework.search_knowledge_with_context("machine learning")
            
            if 'database_results' in search_results or 'graph_context' in search_results:
                print("✅ Graphiti search functionality working")
                self.test_results['graphiti'] = 'PASS'
                return True
            else:
                raise Exception("No search results returned")
                
        except Exception as e:
            print(f"❌ Graphiti integration test failed: {e}")
            self.test_results['graphiti'] = f'FAIL: {e}'
            return False
    
    def _create_basic_wizard_agent(self):
        """Create a basic wizard agent configuration"""
        config = AgentConfig(agent_id="wizard_agent_001")
        
        wizard_system = """🧙‍♂️ I am a wise and mystical wizard specializing in AI, machine learning, and the arcane arts of data science. I weave spells of knowledge and cast enchantments of understanding to help seekers on their quest for wisdom.

My magical abilities include:
- Deep knowledge of machine learning algorithms and neural networks
- Mystical insights into data patterns and statistical divination
- Enchanted understanding of programming languages and software architecture
- Ancient wisdom about database design and query optimization
- Prophetic vision into AI safety and alignment challenges

I speak in a mystical but helpful manner, using magical metaphors to explain complex technical concepts while providing practical, actionable guidance."""
        
        config.set_prompt("llmSystem", wizard_system)
        config.set_prompt("primeDirective", "Guide seekers through the mystical realms of AI and machine learning with wisdom, clarity, and magical insight.")
        
        config.set_modality_flag("LLM_SYSTEM_PROMPT_FLAG", True)
        config.set_modality_flag("AGENT_FLAG", True)
        
        # Save the configuration
        self.db_handler.save_agent_config(config)
        print("✅ Basic wizard agent configuration created")
    
    async def run_all_tests(self):
        """Run all system tests"""
        print("🚀 Starting Comprehensive System Test")
        print("=" * 50)
        
        # Sequential tests
        self.test_database_connection()
        self.test_ollama_connection()
        self.test_knowledge_base()
        
        # Async tests
        await self.test_neo4j_connection()
        await self.test_agent_response_generation()
        await self.test_chat_manager()
        await self.test_graphiti_integration()
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 Test Results Summary:")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result == 'PASS')
        
        for test_name, result in self.test_results.items():
            status = "✅" if result == 'PASS' else "❌"
            print(f"{status} {test_name}: {result}")
        
        print(f"\n📈 Overall: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All tests passed! System is fully operational.")
            return True
        else:
            print("⚠️ Some tests failed. Please review the issues above.")
            return False

async def main():
    """Main test function"""
    tester = SystemTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n✅ System verification complete - All components working correctly!")
    else:
        print("\n❌ System verification failed - Please address the issues above.")

if __name__ == "__main__":
    asyncio.run(main())
