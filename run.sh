#!/bin/bash

echo "=========================================="
echo "Resume Skill Credibility Analyzer"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run './setup.sh' first to set up the project."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "❌ Dependencies not installed!"
    echo "Please run './setup.sh' first to install dependencies."
    exit 1
fi

echo "✅ Environment ready!"
echo ""
echo "🚀 Starting Streamlit application..."
echo "📱 The app will open at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Run the Streamlit app
streamlit run app.py
