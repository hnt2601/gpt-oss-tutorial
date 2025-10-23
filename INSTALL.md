# Installation Guide

This guide covers installation options for all GPT-OSS Tutorial examples.

## 📦 Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Virtual environment tool (recommended: `venv` or `conda`)

## 🚀 Quick Start

### Option 1: Standard Examples (Recommended for Most Users)

For examples 01-07 (basic, structured output, tools, multimodal, stateful, advanced, reasoning):

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install using requirements.txt (includes OpenAI SDK 1.x)
pip install -r requirements.txt

# OR using pyproject.toml
pip install -e ".[standard]"
```

### Option 2: Voice Agent Only (Example 08)

For voice agent example with OpenAI Agents SDK (requires OpenAI SDK 2.x):

```bash
# Create a separate virtual environment
python -m venv venv-voice
source venv-voice/bin/activate  # On Windows: venv-voice\Scripts\activate

# Install with voice dependencies
pip install -e ".[voice]"
```

**Note:** Due to OpenAI SDK version conflict, voice agent CANNOT be installed in the same environment as standard examples.

### Option 3: Development Setup

For contributors and developers:

```bash
# For standard examples development
python -m venv venv-dev
source venv-dev/bin/activate  # On Windows: venv-dev\Scripts\activate
pip install -e ".[standard,dev,jupyter]"

# OR for voice agent development (separate venv)
python -m venv venv-voice-dev
source venv-voice-dev/bin/activate
pip install -e ".[voice,dev,jupyter]"
```

## 🔧 Installation Options Explained

The project uses `pyproject.toml` for dependency management with several optional groups:

| Group | Command | Includes |
|-------|---------|----------|
| **standard** | `pip install -e ".[standard]"` | OpenAI SDK 1.x for examples 01-07 |
| **voice** | `pip install -e ".[voice]"` | OpenAI SDK 2.x + voice dependencies (example 08) |
| **dev** | `pip install -e ".[dev]"` | Testing and code quality tools |
| **jupyter** | `pip install -e ".[jupyter]"` | Jupyter notebook support |

**Combine multiple groups:**
```bash
# Standard with dev tools
pip install -e ".[standard,dev]"

# Voice with dev and jupyter
pip install -e ".[voice,dev,jupyter]"
```

## ⚠️ Important Notes

### OpenAI SDK Version Conflict

There is a version conflict between standard examples and the voice agent:

- **Examples 01-07**: Require `openai>=1.50.0,<2.0.0`
- **Example 08 (Voice)**: Requires `openai>=2.2.0` for `openai-agents` support

**Solutions:**

1. **Use separate virtual environments** (Recommended):
   ```bash
   # For standard examples
   python -m venv venv-standard
   source venv-standard/bin/activate
   pip install -r requirements.txt
   
   # For voice agent
   python -m venv venv-voice
   source venv-voice/bin/activate
   pip install -e ".[voice]"
   ```

2. **Switch between versions**:
   ```bash
   # For standard examples
   pip install "openai>=1.50.0,<2.0.0"
   
   # For voice agent
   pip install "openai>=2.2.0" openai-agents[voice]
   ```

## 🧪 Verify Installation

### For Standard Examples

```bash
python -c "import openai; print(f'OpenAI SDK version: {openai.__version__}')"
python check_setup.py
```

Expected output: `OpenAI SDK version: 1.x.x`

### For Voice Agent

```bash
python -c "import openai; print(f'OpenAI SDK version: {openai.__version__}')"
python -c "import agents; print('OpenAI Agents SDK installed')"
```

Expected output: 
```
OpenAI SDK version: 2.x.x
OpenAI Agents SDK installed
```

## 🌍 Environment Variables

Create a `.env` file in the project root:

```bash
# Required
API_KEY=your_fpt_cloud_api_key_here

# Optional (defaults shown)
OPENAI_BASE_URL=https://mkp-api.fptcloud.com
STT_MODEL_NAME=whisper-large-v3-turbo
LLM_MODEL_NAME=gpt-oss-20b
```

## 📚 Platform-Specific Notes

### macOS

```bash
# Install system dependencies for audio processing (voice agent)
brew install libsndfile

# Then install Python packages
pip install -e ".[voice]"
```

### Linux (Ubuntu/Debian)

```bash
# Install system dependencies for audio processing
sudo apt-get update
sudo apt-get install libsndfile1 ffmpeg

# Then install Python packages
pip install -e ".[voice]"
```

### Windows

```bash
# No additional system dependencies needed
# Just install Python packages
pip install -e ".[voice]"
```

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'openai'`

**Solution**: Make sure you activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Version conflict with `openai` package

**Solution**: Use separate virtual environments for standard and voice examples (see above).

### Issue: `soundfile` installation fails on macOS

**Solution**: Install libsndfile first:
```bash
brew install libsndfile
pip install soundfile
```

### Issue: `ImportError: cannot import name 'Agent' from 'agents'`

**Solution**: Make sure you're using OpenAI SDK 2.x:
```bash
pip install "openai>=2.2.0" openai-agents[voice]
```

## 📖 Next Steps

After installation:

1. **Review examples**: Start with `examples/01_basic/`
2. **Run check script**: `python check_setup.py`
3. **Read documentation**: Check each example's `README.md`
4. **Try tutorials**: Follow the tutorials in order (01 → 08)

## 💬 Support

If you encounter issues:

1. Check this installation guide
2. Review the [main README](README.md)
3. Check example-specific READMEs
4. Verify Python version: `python --version` (should be 3.10+)
5. Verify pip version: `pip --version`

## 🔗 References

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [pip Documentation](https://pip.pypa.io/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [OpenAI Agents SDK](https://github.com/openai/openai-agents)
