#!/usr/bin/env python3
"""Test Ollama using requests library"""
import requests
import json

def test_ollama_openai_api_sync():
    """Test Ollama using OpenAI-compatible API format (synchronous)"""
    
    url = "http://localhost:11434/v1/chat/completions"
    
    data = {
        "model": "phi4:latest",
        "messages": [
            {"role": "system", "content": "You are a helpful Python programming assistant."},
            {"role": "user", "content": "Write a simple Python function to add two numbers. Include docstring and example usage."}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }
    
    print("🧪 Testing Ollama OpenAI-compatible API...")
    print(f"URL: {url}")
    print(f"Model: {data['model']}")
    print()
    
    try:
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! Response received:")
            print(f"Response status: {response.status_code}")
            print()
            print("🔍 Response structure:")
            print(f"Type: {type(result)}")
            print(f"Keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            
            if 'choices' in result:
                print(f"Choices count: {len(result['choices'])}")
                if len(result['choices']) > 0:
                    choice = result['choices'][0]
                    print(f"First choice keys: {list(choice.keys())}")
                    if 'message' in choice:
                        message = choice['message']
                        content = message.get('content', '')
                        print()
                        print("📝 Generated content:")
                        print("="*50)
                        print(content)
                        print("="*50)
                        return content
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Error response: {response.text}")
                    
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

if __name__ == "__main__":
    test_ollama_openai_api_sync()
