#!/bin/bash

# MemSafe - Quick Start Script
# This script helps you run the Streamlit app

echo "🚀 Starting MemSafe..."

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "📝 Create a .env file with your OpenAI API key:"
    echo "   OPENAI_API_KEY=sk-your-key-here"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
python3 -m pip install -q streamlit openai python-dotenv 2>/dev/null || {
    echo "❌ Error installing dependencies. Try: pip install -r requirements.txt"
    exit 1
}

# Run Streamlit
echo "✅ Starting Streamlit app..."
echo "🌐 The app will open in your browser automatically"
echo "📋 You can also access it at: http://localhost:8501"
echo ""
streamlit run app/main.py

