#!/bin/bash

# Setup script for Voice AI Agent with CrewAI

echo "=================================================="
echo "🚀 Voice AI Agent Setup Script"
echo "=================================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 is installed"
echo ""

# Check for system dependencies
echo "📋 Checking system dependencies..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Detected Linux"
    echo ""
    echo "Installing system dependencies..."
    sudo apt-get update
    sudo apt-get install -y python3-pyaudio portaudio19-dev ffmpeg python3-dev
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Detected macOS"
    echo ""
    echo "Installing system dependencies via Homebrew..."
    
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    brew install portaudio ffmpeg
    
else
    echo "⚠️  Unknown OS. Please install the following manually:"
    echo "   - PortAudio"
    echo "   - FFmpeg"
fi

echo ""
echo "✅ System dependencies installed"
echo ""

# Install Python packages
echo "📦 Installing Python packages..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python packages"
    exit 1
fi

echo "✅ Python packages installed"
echo ""

# Setup environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OpenAI API key:"
echo "   export OPENAI_API_KEY='your-api-key-here'"
echo ""
echo "2. Test the setup:"
echo "   python3 test_agent.py"
echo ""
echo "3. Run the simple text agent:"
echo "   python3 simple_voice_agent.py"
echo ""
echo "4. Run the full voice agent:"
echo "   python3 voice_ai_agent.py"
echo ""
echo "=================================================="
