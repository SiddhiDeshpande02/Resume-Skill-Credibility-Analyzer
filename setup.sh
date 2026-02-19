#!/bin/bash

echo "=========================================="
echo "Resume Skill Credibility Analyzer Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Download spaCy model
echo "🧠 Downloading spaCy language model..."
python -m spacy download en_core_web_sm

# Install Tesseract OCR info
echo ""
echo "=========================================="
echo "⚠️  IMPORTANT: Tesseract OCR Setup"
echo "=========================================="
echo ""
echo "For OCR functionality (image resume extraction), you need Tesseract OCR:"
echo ""
echo "Ubuntu/Debian:"
echo "  sudo apt-get install tesseract-ocr"
echo ""
echo "MacOS:"
echo "  brew install tesseract"
echo ""
echo "Windows:"
echo "  Download from: https://github.com/UB-Mannheim/tesseract/wiki"
echo ""

echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: streamlit run app.py"
echo ""
echo "The app will open in your browser at http://localhost:8501"
echo ""
