#!/bin/bash

# CareerPilot Demo Starter
# Double-click this file to start everything!

echo "🚀 Starting CareerPilot..."
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running!"
    echo ""
    echo "Please start Docker Desktop first:"
    echo "1. Open Docker Desktop app"
    echo "2. Wait for it to fully start (whale icon stops moving)"
    echo "3. Then double-click this file again"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ Docker is running!"
echo ""
echo "🏗️  Building and starting all services..."
echo "This will take 2-3 minutes the first time..."
echo ""

# Start everything
docker compose up -d --build

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check status
docker compose ps

echo ""
echo "✅ CareerPilot is ready!"
echo ""
echo "🌐 Open your browser to: http://localhost:3000"
echo ""
echo "📖 Demo guide: Check DEMO_GUIDE.md for what to do next"
echo ""
echo "Press Enter to open the frontend in your browser..."
read

# Open browser
open http://localhost:3000

echo ""
echo "🎉 Enjoy CareerPilot!"
echo ""
read -p "Press Enter to close this window..."
