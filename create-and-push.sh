#!/bin/bash

echo "🚀 Creating GitHub repository and pushing code..."
echo ""

# Create the repository via GitHub website
echo "Step 1: Please create the repository on GitHub"
echo "Go to: https://github.com/new"
echo ""
echo "Repository name: careerpilot"
echo "Description: Open-source JobRight.ai alternative with AI-powered resume matching"
echo "Visibility: Public"
echo "Do NOT initialize with README"
echo ""
read -p "Press Enter after you've created the repository..."

# Push the code
echo ""
echo "Step 2: Pushing code to GitHub..."
cd /Users/ryleymao/careerpilot

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Your code is now on GitHub!"
    echo "🔗 Visit: https://github.com/ryleymao/careerpilot"
    echo ""
    echo "Next steps:"
    echo "1. Add topics: job-search, resume-matching, ai, fastapi, python, docker"
    echo "2. Star your own repo ⭐"
    echo "3. Share it!"
else
    echo ""
    echo "❌ Push failed. You may need to authenticate:"
    echo "Run: git push -u origin main"
    echo "If prompted, use your GitHub username and a Personal Access Token"
    echo "Get token from: https://github.com/settings/tokens"
fi
