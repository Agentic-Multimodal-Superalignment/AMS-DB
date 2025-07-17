#!/usr/bin/env python3
"""Direct test of OpenAI client with Ollama"""
import asyncio
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.llm_client.openai_client import OpenAIClient

async def test_direct_openai_client():
    """Test the OpenAI client directly with Ollama"""
    
    # Initialize Ollama LLM configuration
    llm_config = LLMConfig(
        api_key="abc",  # Ollama doesn't require a real API key
        model="phi4:latest",
        small_model="gemma3:4b",
        base_url="http://localhost:11434/v1",
    )
    
    llm_client = OpenAIClient(config=llm_config)
    
    # Test messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]
    
    print("🧪 Testing OpenAI client directly with Ollama...")
    print("Messages:", messages)
    print()
    
    try:
        # Try to generate response
        response_data = await llm_client.generate_response(
            messages=messages,
            max_tokens=50
        )
        
        print("✅ SUCCESS! Raw response:")
        print(f"Type: {type(response_data)}")
        print(f"Response: {response_data}")
        
        # Try different ways to extract content
        if isinstance(response_data, dict):
            print("\n🔍 Trying different extraction methods:")
            if "choices" in response_data:
                print(f"Choices: {response_data['choices']}")
                if len(response_data["choices"]) > 0:
                    choice = response_data["choices"][0]
                    print(f"First choice: {choice}")
                    if "message" in choice:
                        message = choice["message"]
                        print(f"Message: {message}")
                        if "content" in message:
                            content = message["content"]
                            print(f"✅ Extracted content: {content}")
            
            if hasattr(response_data, 'content'):
                print(f"Has .content attribute: {response_data.content}")
            
            if "content" in response_data:
                print(f"Has 'content' key: {response_data['content']}")
        
        elif hasattr(response_data, 'content'):
            print(f"✅ Object has .content: {response_data.content}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_direct_openai_client())
