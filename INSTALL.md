# Installation Guide

## Quick Start

### 1. Install UV (Recommended)

UV is a fast Python package installer:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Set Up Virtual Environment

```bash
cd gpt-oss-tutorial

# Create virtual environment
uv venv .venv

# Activate it
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 3. Install the Package

```bash
# Install in editable mode (recommended for development)
uv pip install -e .

# Or with development tools
uv pip install -e ".[dev]"

# Or with Jupyter support
uv pip install -e ".[jupyter]"

# Or with everything
uv pip install -e ".[dev,jupyter]"
```

### 4. Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit .env and add your keys
nano .env  # or use your favorite editor
```

Required in `.env`:
```env
API_KEY=your_gpt_oss_api_key_here
BASE_URL=https://mkp-api.fptcloud.com
MODEL_NAME=gpt-oss-20b
PINECONE_API_KEY=your_pinecone_key_here  # Optional, for RAG examples
```

### 5. Verify Installation

```bash
# Run a simple example
python examples/01_basic/instructions.py

# Run tests
pytest tests/
```

## Alternative: Traditional pip

If you prefer traditional pip:

```bash
# Create venv
python -m venv .venv
source .venv/bin/activate

# Install
pip install -e .

# Or with extras
pip install -e ".[dev,jupyter]"
```

## Troubleshooting

### ModuleNotFoundError: No module named 'src'

**Problem**: The package isn't installed in editable mode.

**Solution**:
```bash
# Make sure you're in the project root
cd /path/to/gpt-oss-tutorial

# Install in editable mode
uv pip install -e .
```

### Import errors after installation

**Problem**: Virtual environment not activated.

**Solution**:
```bash
# Check if venv is active (should see (.venv) in prompt)
source .venv/bin/activate

# Verify package is installed
pip list | grep gpt-oss-tutorial
```

### Dependencies conflict

**Problem**: Conflicting package versions.

**Solution**:
```bash
# Clean install
rm -rf .venv
uv venv .venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Pinecone examples fail

**Problem**: PINECONE_API_KEY not set.

**Solution**:
```bash
# Add to .env file
echo "PINECONE_API_KEY=your_key_here" >> .env

# Or set in shell
export PINECONE_API_KEY=your_key_here
```

## Development Setup

For contributors and developers:

```bash
# Install with all dev tools
uv pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install

# Run linting
ruff check src/ examples/ tests/

# Run formatting
black src/ examples/ tests/

# Run type checking (if mypy is added)
mypy src/
```

## Docker Setup (Optional)

If you prefer Docker:

```dockerfile
# Dockerfile (create this)
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv pip install -e ".[dev]"

CMD ["python", "examples/01_basic/instructions.py"]
```

```bash
# Build and run
docker build -t gpt-oss-tutorial .
docker run --env-file .env gpt-oss-tutorial
```

## Platform-Specific Notes

### macOS
- UV install works via curl
- If you get security warnings, go to System Preferences → Security & Privacy

### Linux
- May need to add UV to PATH: `export PATH="$HOME/.cargo/bin:$PATH"`
- Add to `.bashrc` or `.zshrc` for persistence

### Windows
- Use PowerShell (not CMD)
- Activate venv: `.venv\Scripts\activate`
- If execution policy blocks UV install, run: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

## Verification Checklist

After installation, verify:

- [ ] Virtual environment is activated
- [ ] Package is installed: `pip list | grep gpt-oss-tutorial`
- [ ] Can import: `python -c "from src.client import create_client; print('OK')"`
- [ ] Environment variables set: `python -c "from src.config import get_config; print(get_config())"`
- [ ] Basic example runs: `python examples/01_basic/instructions.py`
- [ ] Tests pass: `pytest tests/test_examples.py::TestConfig -v`

## Need Help?

If you're still having issues:

1. Check that you're in the project root directory
2. Ensure virtual environment is activated
3. Try a clean reinstall: `rm -rf .venv && uv venv .venv && source .venv/bin/activate && uv pip install -e .`
4. Check Python version: `python --version` (needs 3.10+)
5. Open an issue with error details

## Next Steps

Once installed successfully:

1. Read the main [README.md](README.md)
2. Check out [examples/01_basic/README.md](examples/01_basic/README.md)
3. Try running examples progressively
4. Explore module READMEs for detailed docs

