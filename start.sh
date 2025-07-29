#!/bin/bash

echo "🚀 Starting AFL Premiership Window..."

# Check if Python dependencies are installed
echo "📦 Checking Python dependencies..."
python3 -c "import requests, bs4, pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Python dependencies not found. Installing..."
    pip3 install requests beautifulsoup4 pandas
fi

# Check if Node dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Build the application
echo "🔨 Building application..."
npm run build

# Start the server
echo "🌐 Starting server on http://localhost:3000"
echo "Press Ctrl+C to stop the server"
npm run server 