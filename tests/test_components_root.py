#!/usr/bin/env python3
"""
Simple test script for AMS-DB components
"""

def test_basic_imports():
    """Test basic Python imports"""
    print("🧪 Testing basic imports...")
    
    try:
        import json
        import uuid
        from datetime import datetime
        from pathlib import Path
        print("✅ Basic Python modules imported successfully!")
        return True
    except Exception as e:
        print(f"❌ Basic imports failed: {e}")
        return False

def test_polars():
    """Test polars import and basic functionality"""
    print("🧪 Testing Polars...")
    
    try:
        import polars as pl
        print("✅ Polars imported successfully!")
        
        # Test basic DataFrame creation
        df = pl.DataFrame({
            "test_col": [1, 2, 3],
            "name": ["agent1", "agent2", "agent3"]
        })
        print(f"✅ Polars DataFrame created with {df.height} rows!")
        return True
    except Exception as e:
        print(f"❌ Polars test failed: {e}")
        return False

def test_agent_config():
    """Test AgentConfig without external dependencies"""
    print("🧪 Testing AgentConfig...")
    
    try:
        import sys
        import os
        
        # Add src to path
        src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
        sys.path.insert(0, src_path)
        
        from ams_db.core.base_agent_config import AgentConfig
        print("✅ AgentConfig imported successfully!")
        
        # Test basic functionality
        agent = AgentConfig("test_agent")
        agent.set_prompt("llmSystem", "You are a test agent")
        agent.set_modality_flag("STT_FLAG", True)
        
        print("✅ AgentConfig basic functionality working!")
        return True
    except Exception as e:
        print(f"❌ AgentConfig test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_polars_db():
    """Test PolarsDBHandler"""
    print("🧪 Testing PolarsDBHandler...")
    
    try:
        import sys
        import os
        
        # Add src to path
        src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
        sys.path.insert(0, src_path)
        
        from ams_db.core.polars_db import PolarsDBHandler
        print("✅ PolarsDBHandler imported successfully!")
        
        # Test basic functionality
        db = PolarsDBHandler(db_path="test_db")
        print("✅ PolarsDBHandler created successfully!")
        
        # Test adding an agent config
        test_config = {"agent_id": "test", "test_data": "hello"}
        agent_id = db.add_agent_config(test_config, "Test Agent", "Test description")
        print(f"✅ Agent added with ID: {agent_id}")
        
        return True
    except Exception as e:
        print(f"❌ PolarsDBHandler test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧙‍♂️ AMS-DB Component Testing")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_polars,
        test_agent_config,
        test_polars_db
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
            print()
    
    print("=" * 50)
    print("📊 Test Results:")
    passed = sum(results)
    total = len(results)
    print(f"✅ Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! AMS-DB components are working!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
