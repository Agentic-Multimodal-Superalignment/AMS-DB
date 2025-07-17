#!/usr/bin/env python3
"""
Simple test to debug import issues
"""

print("🧪 Starting import test...")

try:
    print("Importing basic modules...")
    import json
    import uuid
    from datetime import datetime
    print("✅ Basic modules imported")
    
    print("Importing polars...")
    import polars as pl
    print("✅ Polars imported")
    
    print("Importing AMS-DB components...")
    from ams_db.core.base_agent_config import AgentConfig
    print("✅ AgentConfig imported directly")
    
    from ams_db.core.polars_db import PolarsDBHandler
    print("✅ PolarsDBHandler imported directly")
    
    print("Testing basic functionality...")
    agent = AgentConfig("debug_test")
    print("✅ AgentConfig created")
    
    db = PolarsDBHandler("debug_test_db")
    print("✅ PolarsDBHandler created")
    
    print("🎉 All tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
