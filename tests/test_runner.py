#!/usr/bin/env python3
"""
Comprehensive test runner for AMS-DB system
"""
import os
import sys
import asyncio
import traceback
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Set environment variables
os.environ['NEO4J_URI'] = 'bolt://localhost:7687'
os.environ['NEO4J_USER'] = 'neo4j'
os.environ['NEO4J_PASSWORD'] = 'temppass123'
os.environ['OLLAMA_BASE_URL'] = 'http://localhost:11434'

class TestResult:
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.error = None
        self.details = ""

class TestRunner:
    """Comprehensive test runner for AMS-DB"""
    
    def __init__(self):
        self.results = []
    
    def run_test(self, test_name: str, test_func, *args, **kwargs):
        """Run a single test and capture results"""
        result = TestResult(test_name)
        
        try:
            print(f"\n🧪 Running {test_name}...")
            
            if asyncio.iscoroutinefunction(test_func):
                success = asyncio.run(test_func(*args, **kwargs))
            else:
                success = test_func(*args, **kwargs)
            
            result.passed = success if isinstance(success, bool) else True
            result.details = "✅ Passed"
            
        except Exception as e:
            result.passed = False
            result.error = str(e)
            result.details = f"❌ Failed: {str(e)[:100]}..."
            print(f"❌ {test_name} failed: {e}")
            
        self.results.append(result)
        return result.passed
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        for result in self.results:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(f"{status:8} | {result.name}")
            if not result.passed and result.error:
                print(f"         | Error: {result.error[:80]}...")
        
        print("="*60)
        print(f"TOTAL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! System is fully functional.")
        else:
            print("⚠️  Some tests failed. See details above.")
        
        return passed == total

# Individual test functions
def test_basic_imports():
    """Test basic imports"""
    try:
        import polars as pl
        from ams_db.core.base_agent_config import AgentConfig
        from ams_db.core.polars_db import PolarsDBHandler
        print("✅ All basic imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_polars_db():
    """Test Polars database functionality"""
    try:
        from ams_db.core.polars_db import PolarsDBHandler
        db = PolarsDBHandler("test_db")
        
        # Test basic functionality
        test_config = {"agent_id": "test_agent", "test": True}
        agent_id = db.add_agent_config(test_config, "Test Agent", "Test")
        
        retrieved = db.get_agent_config(agent_id)
        assert retrieved is not None
        assert retrieved["test"] == True
        
        print("✅ Polars DB operations successful")
        return True
    except Exception as e:
        print(f"❌ Polars DB test failed: {e}")
        return False

def test_service_connectivity():
    """Test external service connectivity"""
    import requests
    
    services = []
    
    # Test Neo4j
    try:
        response = requests.get("http://localhost:7474", timeout=5)
        services.append(("Neo4j", True))
        print("✅ Neo4j accessible")
    except:
        services.append(("Neo4j", False))
        print("❌ Neo4j not accessible")
    
    # Test Ollama
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            services.append(("Ollama", True))
            print(f"✅ Ollama accessible with {len(models)} models")
        else:
            services.append(("Ollama", False))
            print("❌ Ollama not responding")
    except:
        services.append(("Ollama", False))
        print("❌ Ollama not accessible")
    
    # Return True if all services are up
    return all(status for _, status in services)

async def test_graphiti_framework():
    """Test Graphiti framework integration"""
    try:
        from ams_db.core.graphiti_pipe import GraphitiRAGFramework
        
        framework = GraphitiRAGFramework(
            neo4j_uri='bolt://localhost:7687',
            neo4j_user='neo4j',
            neo4j_password='temppass123'
        )
        
        # Test agent loading
        loaded = await framework.load_agent("wizard_agent_001")
        
        print("✅ Graphiti framework initialized")
        return True
    except Exception as e:
        print(f"❌ Graphiti framework failed: {e}")
        return False

async def test_llm_generation():
    """Test actual LLM response generation"""
    try:
        from ams_db.core.graphiti_pipe import GraphitiRAGFramework
        
        framework = GraphitiRAGFramework(
            neo4j_uri='bolt://localhost:7687',
            neo4j_user='neo4j',
            neo4j_password='temppass123'
        )
        
        # Load agent and test response generation
        await framework.load_agent("wizard_agent_001")
        response = await framework.generate_response(
            agent_id="wizard_agent_001",
            user_message="Hello, test message for validation",
            session_id="test_session"
        )
        
        # Check if we got a real response (not just fallback)
        if len(response) > 50 and not "setup notice" in response.lower():
            print(f"✅ LLM response generated: {response[:100]}...")
            return True
        else:
            print(f"⚠️ Got fallback response: {response[:100]}...")
            return False
            
    except Exception as e:
        print(f"❌ LLM generation failed: {e}")
        return False

async def test_chat_manager():
    """Test chat manager functionality"""
    try:
        from ams_db.core.polars_db import PolarsDBHandler
        from ams_db.cli.chat_manager import ChatManager
        
        db = PolarsDBHandler("agent_database")
        chat_manager = ChatManager(db)
        
        # Start a chat session
        session_id, alias = chat_manager.start_human_chat("wizard_agent_001", "Test Session")
        
        # Send a test message
        response = await chat_manager.send_message_to_agent(
            session_id, "wizard_agent_001", "Test message"
        )
        
        print(f"✅ Chat manager working, response: {response[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ Chat manager failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AMS-DB Comprehensive Test Suite")
    print("="*60)
    
    runner = TestRunner()
    
    # Run tests in order of dependency
    runner.run_test("Basic Imports", test_basic_imports)
    runner.run_test("Service Connectivity", test_service_connectivity)
    runner.run_test("Polars Database", test_polars_db)
    runner.run_test("Graphiti Framework", test_graphiti_framework)
    runner.run_test("LLM Generation", test_llm_generation)
    runner.run_test("Chat Manager", test_chat_manager)
    
    # Print summary
    all_passed = runner.print_summary()
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
