"""
Advanced Example: Building a Minecraft Assistant Agent

This example demonstrates how to build a specialized agent using the
predefined Minecraft template and enhance it with custom knowledge.
"""

import asyncio
from pathlib import Path

from ams_db.core import AgentConfig, PolarsDBHandler, GraphitiRAGFramework
from ams_db.config import get_template_manager


def create_minecraft_knowledge_base():
    """Create a comprehensive Minecraft knowledge base"""
    
    knowledge_documents = [
        {
            "title": "Minecraft Hostile Mobs Guide",
            "content": """
            Hostile mobs in Minecraft are dangerous creatures that will attack players on sight.
            
            Common hostile mobs:
            - Zombies: Slow-moving undead that spawn in dark areas. Weak to sunlight.
            - Skeletons: Ranged attackers with bows. Avoid their arrows and close distance.
            - Creepers: Silent green mobs that explode when close to players. Very dangerous!
            - Spiders: Fast-moving mobs that become hostile in darkness.
            - Endermen: Tall black mobs that teleport. Don't look directly at them.
            
            Safety tips:
            - Always carry a sword and shield
            - Light up areas with torches to prevent mob spawning
            - Build walls and barriers for protection
            - Never go out at night without proper equipment
            """,
            "tags": ["mobs", "hostile", "combat", "safety"]
        },
        {
            "title": "Basic Crafting Recipes",
            "content": """
            Essential crafting recipes for survival:
            
            Tools:
            - Wooden Pickaxe: 3 wooden planks + 2 sticks
            - Stone Pickaxe: 3 cobblestone + 2 sticks
            - Iron Pickaxe: 3 iron ingots + 2 sticks
            
            Weapons:
            - Wooden Sword: 2 wooden planks + 1 stick
            - Stone Sword: 2 cobblestone + 1 stick
            - Iron Sword: 2 iron ingots + 1 stick
            
            Basic Items:
            - Torch: 1 coal/charcoal + 1 stick
            - Chest: 8 wooden planks
            - Crafting Table: 4 wooden planks
            - Furnace: 8 cobblestone
            """,
            "tags": ["crafting", "tools", "weapons", "recipes"]
        },
        {
            "title": "Building and Construction",
            "content": """
            Building tips for Minecraft:
            
            Basic Shelter:
            - Dig into a hillside for quick temporary shelter
            - Use dirt or wood for quick walls
            - Always include a door and lighting
            - Make it at least 3 blocks high inside
            
            Advanced Building:
            - Plan your structure before building
            - Use different materials for variety
            - Include multiple rooms: storage, bedroom, workshop
            - Add windows for natural light
            - Create a roof to prevent mob spawning on top
            
            Essential rooms:
            - Storage room with multiple chests
            - Smelting room with furnaces
            - Enchanting room (later game)
            - Workshop with crafting tables
            """,
            "tags": ["building", "construction", "shelter", "planning"]
        },
        {
            "title": "Resource Gathering and Mining",
            "content": """
            Mining and resource gathering strategies:
            
            Basic Resources:
            - Wood: Punch trees to get wood blocks
            - Stone: Mine stone blocks with a pickaxe
            - Coal: Found in stone, essential for torches and smelting
            - Iron: Gray blocks with brown spots, smelt to get iron ingots
            
            Mining Tips:
            - Always bring torches for lighting
            - Dig stairs down, not straight down (avoid falling)
            - Watch for lava and water
            - Listen for mob sounds
            - Mark your way back to the surface
            
            Advanced Mining:
            - Branch mining at Y-level 11 for diamonds
            - Strip mining for large ore veins
            - Cave exploration for natural ore deposits
            - Always carry backup tools
            """,
            "tags": ["mining", "resources", "ores", "strategy"]
        }
    ]
    
    return knowledge_documents


async def build_minecraft_assistant():
    """Build a complete Minecraft assistant with knowledge base"""
    print("🎮 Building Minecraft Assistant Agent")
    print("=" * 50)
    
    # Get template manager and create agent from template
    template_manager = get_template_manager()
    
    minecraft_agent = template_manager.create_agent_from_template(
        "minecraft",
        agent_id="advanced_minecraft_assistant"
    )
    
    if not minecraft_agent:
        print("❌ Failed to create agent from template")
        return None
    
    print(f"✅ Created Minecraft agent: {minecraft_agent.config['agent_id']}")
    
    # Initialize the framework (without Graphiti for this example)
    try:
        framework = GraphitiRAGFramework(db_path="minecraft_assistant_db")
        print("✅ Framework initialized with Graphiti")
        use_graphiti = True
    except Exception as e:
        print(f"⚠️ Graphiti not available ({e}), using database only")
        db = PolarsDBHandler("minecraft_assistant_db")
        use_graphiti = False
    
    # Add the agent to the database
    if use_graphiti:
        agent_id = framework.create_agent(
            minecraft_agent.get_config(),
            "Advanced Minecraft Assistant",
            "Specialized Minecraft gameplay assistant with comprehensive knowledge base",
            ["minecraft", "gaming", "assistant", "survival"]
        )
        framework.load_agent(agent_id)
        print(f"✅ Agent added to framework: {agent_id}")
    else:
        agent_id = db.add_agent_config(
            minecraft_agent.get_config(),
            "Advanced Minecraft Assistant",
            "Specialized Minecraft gameplay assistant with comprehensive knowledge base",
            ["minecraft", "gaming", "assistant", "survival"]
        )
        print(f"✅ Agent added to database: {agent_id}")
    
    # Add knowledge base
    knowledge_docs = create_minecraft_knowledge_base()
    print(f"\n📚 Adding {len(knowledge_docs)} knowledge documents...")
    
    for doc in knowledge_docs:
        if use_graphiti:
            kb_id = await framework.add_knowledge_with_embedding(
                doc["title"],
                doc["content"],
                "text",
                "minecraft_guide",
                doc["tags"]
            )
        else:
            kb_id = db.add_knowledge_document(
                agent_id,
                doc["title"],
                doc["content"],
                "text",
                "minecraft_guide",
                doc["tags"]
            )
        print(f"  ✅ Added: {doc['title']} (ID: {kb_id})")
    
    # Simulate some gameplay interactions
    print(f"\n🎮 Simulating gameplay interactions...")
    
    gameplay_scenarios = [
        {
            "user_input": "Help! There's a green thing following me and it's hissing!",
            "assistant_response": "That's a Creeper! Run away immediately! Creepers explode when they get close to you. Keep your distance and try to hit it with arrows if you have a bow, or carefully approach with a sword and quickly back away after hitting it. Never let it get too close!"
        },
        {
            "user_input": "I need to make a pickaxe but I don't know how",
            "assistant_response": "To make a pickaxe, you need 3 material blocks (wood planks, cobblestone, or iron ingots) and 2 sticks. Place the 3 material blocks in the top row of your crafting table, and put one stick in the middle of the second row and one stick in the middle of the bottom row. Start with a wooden pickaxe if you're just beginning!"
        },
        {
            "user_input": "It's getting dark and I hear scary sounds",
            "assistant_response": "You need to find shelter immediately! Dark areas spawn hostile mobs. If you don't have a house yet, quickly dig into a hillside or build a simple dirt shelter. Make sure to place torches inside for light. The scary sounds are zombies, skeletons, and other hostile mobs spawning. Stay inside until dawn!"
        }
    ]
    
    for i, scenario in enumerate(gameplay_scenarios, 1):
        if use_graphiti:
            await framework.add_conversation_turn(
                scenario["user_input"],
                scenario["assistant_response"]
            )
        else:
            db.add_conversation_message(
                agent_id, "user", scenario["user_input"], f"gameplay_session_{i}"
            )
            db.add_conversation_message(
                agent_id, "assistant", scenario["assistant_response"], f"gameplay_session_{i}"
            )
        
        print(f"  ✅ Scenario {i}: {scenario['user_input'][:50]}...")
    
    # Test knowledge retrieval
    print(f"\n🔍 Testing knowledge retrieval...")
    
    test_queries = ["creeper", "crafting pickaxe", "building shelter", "mining safety"]
    
    for query in test_queries:
        if use_graphiti:
            results = await framework.search_knowledge_with_context(query)
            db_results = len(results['database_results'])
            graph_context = bool(results['graph_context'])
            print(f"  Query: '{query}' -> {db_results} docs, graph context: {graph_context}")
        else:
            results = db.search_knowledge_base(agent_id, query)
            print(f"  Query: '{query}' -> {results.height} documents found")
    
    # Get final statistics
    if use_graphiti:
        stats = framework.get_system_status()
        db_stats = stats['database_stats']
    else:
        db_stats = db.get_database_stats()
    
    print(f"\n📊 Final Statistics:")
    print(f"  • Agents: {db_stats['agent_count']}")
    print(f"  • Conversations: {db_stats['conversation_count']}")
    print(f"  • Knowledge Documents: {db_stats['knowledge_document_count']}")
    print(f"  • Database Size: {db_stats['database_size_mb']:.2f} MB")
    
    # Export agent data
    export_path = "minecraft_assistant_export"
    if use_graphiti:
        success = framework.export_agent_data(export_path)
    else:
        success = db.export_agent_config(agent_id, f"{export_path}/config.json")
    
    if success:
        print(f"✅ Agent data exported to {export_path}/")
    
    return agent_id


async def main():
    """Main function"""
    print("🧙‍♂️ AMS-DB Advanced Example: Minecraft Assistant")
    print("=" * 60)
    print()
    
    try:
        agent_id = await build_minecraft_assistant()
        
        if agent_id:
            print(f"\n🎉 Successfully built Minecraft Assistant: {agent_id}")
            print("\n💡 The agent is now ready to help with:")
            print("  • Identifying and dealing with hostile mobs")
            print("  • Crafting tools and weapons") 
            print("  • Building shelters and structures")
            print("  • Mining and resource gathering strategies")
            print("  • Real-time gameplay assistance")
        else:
            print("\n❌ Failed to build Minecraft Assistant")
            
    except KeyboardInterrupt:
        print("\n⚠️ Build interrupted by user")
    except Exception as e:
        print(f"\n❌ Error building Minecraft Assistant: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
