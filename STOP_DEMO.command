#!/bin/bash

# CareerPilot Demo Stopper
# Double-click this file to stop everything!

echo "🛑 Stopping CareerPilot..."
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Stop all services
docker compose down

echo ""
echo "✅ All services stopped!"
echo ""
read -p "Press Enter to close this window..."
