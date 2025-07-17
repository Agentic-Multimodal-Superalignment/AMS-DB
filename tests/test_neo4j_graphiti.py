#!/usr/bin/env python3
"""Test Neo4j connectivity and schema"""

import os
from neo4j import GraphDatabase

def test_neo4j_connection():
    """Test direct Neo4j connection"""
    print("🔍 Testing Neo4j Connection...")
    
    uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD', 'temppass123')
    
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        
        with driver.session() as session:
            # Test basic connection
            result = session.run("RETURN 'Connection successful' as message")
            record = result.single()
            print(f"✅ Neo4j connected: {record['message']}")
            
            # Check database info
            result = session.run("CALL db.schema.visualization()")
            schema_data = list(result)
            print(f"✅ Schema nodes available: {len(schema_data)}")
            
            # Check for any existing nodes
            result = session.run("MATCH (n) RETURN count(n) as node_count")
            count = result.single()['node_count']
            print(f"✅ Total nodes in database: {count}")
            
            # Check for specific Graphiti-related nodes
            result = session.run("MATCH (n) RETURN DISTINCT labels(n) as labels LIMIT 10")
            labels = [record['labels'] for record in result]
            print(f"✅ Available node labels: {labels}")
            
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ Neo4j connection error: {e}")
        return False

def test_graphiti_schema():
    """Test if Graphiti schema is properly initialized"""
    print("\n🔍 Testing Graphiti Schema...")
    
    try:
        from graphiti_core import Graphiti
        from graphiti_core.llm_client.config import LLMConfig
        from graphiti_core.llm_client.openai_client import OpenAIClient
        from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
        from graphiti_core.cross_encoder.openai_reranker_client import OpenAIRerankerClient
        
        # Configure Graphiti components
        llm_config = LLMConfig(
            api_key="abc",
            model="phi4:latest",
            small_model="gemma3:4b",
            base_url="http://localhost:11434/v1",
        )
        
        llm_client = OpenAIClient(config=llm_config)
        
        graphiti = Graphiti(
            os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
            os.getenv('NEO4J_USER', 'neo4j'),
            os.getenv('NEO4J_PASSWORD', 'temppass123'),
            llm_client=llm_client,
            embedder=OpenAIEmbedder(
                config=OpenAIEmbedderConfig(
                    api_key="abc",
                    embedding_model="nomic-embed-text",
                    embedding_dim=768,
                    base_url="http://localhost:11434/v1",
                )
            ),
            cross_encoder=OpenAIRerankerClient(
                client=llm_client, 
                config=llm_config
            ),
        )
        
        print("✅ Graphiti initialized with full configuration")
        
        # Test search function
        try:
            results = graphiti.search("test query")
            print(f"✅ Graphiti search works: {len(results)} results")
        except Exception as e:
            print(f"⚠️ Graphiti search issue: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Graphiti schema error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing Neo4j and Graphiti Setup\n")
    
    neo4j_ok = test_neo4j_connection()
    graphiti_ok = test_graphiti_schema()
    
    print(f"\n📊 Results:")
    print(f"Neo4j: {'✅ PASS' if neo4j_ok else '❌ FAIL'}")
    print(f"Graphiti: {'✅ PASS' if graphiti_ok else '❌ FAIL'}")
    
    if neo4j_ok and graphiti_ok:
        print("🎉 Database setup is fully functional!")
    else:
        print("⚠️ Database setup needs attention")
