#!/bin/bash
# Quick Start Script for GPT-OSS Tutorial

set -e  # Exit on error

echo "🚀 GPT-OSS Tutorial - Quick Start"
echo "=================================="
echo ""

# Check if in correct directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the gpt-oss-tutorial directory"
    exit 1
fi

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing UV package manager..."
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "Please install UV manually on Windows:"
        echo "powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\""
        exit 1
    fi
    
    # Add UV to PATH for this session
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "✅ UV is installed"
echo ""

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "🔧 Creating virtual environment..."
    uv venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Install package
echo "📦 Installing gpt-oss-tutorial package..."
uv pip install -e .
echo "✅ Package installed"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "⚙️  Creating .env from template..."
        cp .env.example .env
        echo "✅ .env file created"
        echo ""
        echo "⚠️  IMPORTANT: Please edit .env and add your API keys:"
        echo "   - API_KEY=your_gpt_oss_api_key"
        echo "   - PINECONE_API_KEY=your_pinecone_key (optional)"
        echo ""
        read -p "Press Enter to open .env in editor (or Ctrl+C to skip)..."
        ${EDITOR:-nano} .env
    else
        echo "⚠️  Warning: .env.example not found"
    fi
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. Ensure API_KEY is set in .env"
echo "  3. Run an example: python examples/01_basic/instructions.py"
echo "  4. Run tests: pytest tests/"
echo ""
echo "📚 Documentation:"
echo "  - Main README: README.md"
echo "  - Installation guide: INSTALL.md"
echo "  - Module docs: examples/*/README.md"
echo ""

# Test import
echo "🧪 Testing import..."
if python -c "from src.client import create_client; print('✅ Import test passed')" 2>/dev/null; then
    echo ""
    echo "✨ Everything is ready! Happy coding! ✨"
else
    echo "⚠️  Import test failed. Please check installation."
fi

