#!/usr/bin/env python3
"""CLI test for chat commands"""
import os
import subprocess
import sys

# Set environment variables
os.environ['NEO4J_URI'] = 'bolt://localhost:7687'
os.environ['NEO4J_USER'] = 'neo4j'
os.environ['NEO4J_PASSWORD'] = 'temppass123'

def run_cli_command(command):
    """Run a CLI command and return output"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "src.ams_db.cli.main"] + command.split(),
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

if __name__ == "__main__":
    print("🧪 Testing CLI Chat Commands")
    print("=" * 40)
    
    # Test chat start
    print("\n1. Starting a new chat session with wizard...")
    stdout, stderr, code = run_cli_command("chat start wizard_agent_001 --session-name CLI_Test_Session")
    print(f"Exit code: {code}")
    if stdout:
        print(f"Output: {stdout}")
    if stderr:
        print(f"Error: {stderr}")
    
    # Test chat list
    print("\n2. Listing active chat sessions...")
    stdout, stderr, code = run_cli_command("chat list")
    print(f"Exit code: {code}")
    if stdout:
        print(f"Output: {stdout}")
    if stderr:
        print(f"Error: {stderr}")
