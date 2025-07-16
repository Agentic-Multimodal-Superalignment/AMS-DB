#!/bin/bash
# AMS-DB Service Startup Script
# This script starts the necessary services for full AMS-DB functionality

echo "🚀 Starting AMS-DB Services..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "⚠️  Docker is not running. Please start Docker first."
    exit 1
fi

# Start Neo4j
echo "📊 Starting Neo4j database..."
docker run -d \
    --name ams-neo4j \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/password \
    -v ams-neo4j-data:/data \
    neo4j:latest

if [ $? -eq 0 ]; then
    echo "✅ Neo4j started successfully on http://localhost:7474"
else
    echo "❌ Failed to start Neo4j. Trying to start existing container..."
    docker start ams-neo4j
fi

# Check if Ollama is running
echo "🤖 Checking Ollama status..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is already running on http://localhost:11434"
else
    echo "⚠️  Ollama is not running. Please start it manually:"
    echo "   Run: ollama serve"
fi

echo ""
echo "🎉 Service startup complete!"
echo "📋 Service Status:"
echo "   - Neo4j:  http://localhost:7474 (username: neo4j, password: password)"
echo "   - Ollama: http://localhost:11434"
echo ""
echo "💬 You can now use full AI-powered chat with:"
echo "   ams-db chat send <alias> 'your message'"
