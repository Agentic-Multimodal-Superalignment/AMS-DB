#!/usr/bin/env python3
"""Test direct Ollama connection and model functionality"""

import requests
import json

def test_ollama_direct():
    """Test direct connection to Ollama"""
    print("🔍 Testing Direct Ollama Connection...")
    
    # Test basic connection
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Ollama connected, found {len(models['models'])} models")
            for model in models['models'][:3]:  # Show first 3
                print(f"   - {model['name']}")
        else:
            print(f"❌ Ollama connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama connection error: {e}")
        return False
    
    # Test model generation
    try:
        test_prompt = "Hello, please respond with exactly 'Test successful' if you can understand me."
        payload = {
            "model": "phi4:latest",
            "prompt": test_prompt,
            "stream": False
        }
        
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        if response.status_code == 200:
            result = response.json()
            response_text = result.get('response', '').strip()
            print(f"✅ Model test response: {response_text[:100]}...")
            return True
        else:
            print(f"❌ Model generation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Model generation error: {e}")
        return False

def test_openai_compat():
    """Test OpenAI-compatible endpoint"""
    print("\n🔍 Testing OpenAI-Compatible API...")
    
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer dummy"  # Ollama doesn't need real auth
        }
        
        payload = {
            "model": "phi4:latest",
            "messages": [
                {"role": "user", "content": "Say 'OpenAI compatibility test successful' if you understand."}
            ],
            "max_tokens": 50
        }
        
        response = requests.post("http://localhost:11434/v1/chat/completions", 
                               json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"✅ OpenAI API test: {message}")
            return True
        else:
            print(f"❌ OpenAI API failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Ollama Functionality\n")
    
    direct_ok = test_ollama_direct()
    openai_ok = test_openai_compat()
    
    print(f"\n📊 Results:")
    print(f"Direct API: {'✅ PASS' if direct_ok else '❌ FAIL'}")
    print(f"OpenAI API: {'✅ PASS' if openai_ok else '❌ FAIL'}")
    
    if direct_ok and openai_ok:
        print("🎉 Ollama is fully functional!")
    else:
        print("⚠️ Some Ollama features need attention")
