# Changelog

## v1.0.3 - 2025-01-18

### Fixed

- **Critical: Responses API not available**
  - Fixed `AttributeError: 'OpenAI' object has no attribute 'responses'`
  - Root cause: OpenAI SDK 1.12.0 doesn't have responses API
  - Solution: Updated to require `openai>=1.50.0,<2.0.0`
  - Responses API was added in SDK 1.50.0
  - Version 2.x has breaking validation changes

### Changed

- **Dependencies**: Updated version constraints
  - `openai>=1.50.0,<2.0.0` (was `==1.12.0`)
  - Removed `httpx<0.25` constraint (handled by openai deps)
  - Added `packaging>=23.0` for version checking
- **Version checking**: Updated to validate >= 1.50.0, < 2.0.0
- **COMPATIBILITY.md**: Updated with correct version requirements
- **check_setup.py**: Improved version validation logic

### Tested

- ✅ OpenAI SDK 1.109.1 works perfectly
- ✅ Responses API available
- ✅ No validation errors
- ✅ All examples run successfully

## v1.0.2 - 2025-01-18

### Fixed

- **Critical: OpenAI SDK compatibility issue**
  - Fixed validation errors with OpenAI SDK 2.x (`logprobs`, `refusal` errors)
  - Pinned `openai==1.12.0` and `httpx<0.25` for compatibility
  - Added automatic version checking with warnings
  - Created `COMPATIBILITY.md` with detailed troubleshooting
  
### Added

- **`check_setup.py`**: Automated setup verification script
  - Checks Python version
  - Verifies OpenAI SDK and httpx versions
  - Tests package installation
  - Validates environment configuration
  - Confirms client creation works
- **`src/compat.py`**: Compatibility layer module
  - Version checking utilities
  - Error handling decorators
  - Compatibility warnings

### Changed

- **Dependencies**: Pinned exact compatible versions
  - `openai==1.12.0` (was `>=1.12.0`)
  - Added `httpx<0.25` constraint
- **README**: Added troubleshooting for validation errors
- **COMPATIBILITY.md**: Comprehensive compatibility guide

## v1.0.1 - 2025-01-18

### Fixed

- **ModuleNotFoundError**: Fixed import issues by adding proper package configuration
  - Added `pyproject.toml` for modern Python packaging (PEP 517/518)
  - Added `setup.py` for backward compatibility
  - Package now installs in editable mode with `uv pip install -e .`

### Added

- **Installation Guide** (`INSTALL.md`): Comprehensive installation documentation
  - Step-by-step setup instructions
  - Platform-specific notes (macOS, Linux, Windows)
  - Troubleshooting section
  - Docker setup (optional)
- **Quick Start Script** (`quick_start.sh`): Automated setup script
  - Installs UV if needed
  - Creates virtual environment
  - Installs package in editable mode
  - Sets up .env file
- **`.gitignore`**: Proper Git ignore patterns

### Changed

- **README.md**: Updated installation instructions
  - Added quick start section
  - Updated troubleshooting with import fix
  - Added reference to INSTALL.md
- **Dependencies**: Better organized in pyproject.toml
  - Core dependencies
  - Optional dev dependencies
  - Optional Jupyter support

## v1.0.0 - 2025-01-18

### Major Refactor: Tutorial Research Repository

This release represents a complete restructuring of the GPT-OSS tutorial repository into a professional, research-oriented codebase.

### ✨ New Structure

- **Modular Organization**: All examples organized into 6 logical modules
- **Shared Utilities**: Common configuration and client code in `src/`
- **Comprehensive Documentation**: README for each module with examples and best practices
- **Testing Framework**: Basic test suite with pytest

### 📦 Modules

1. **01_basic**: System instructions, simple conversations, multi-turn
2. **02_structured_output**: JSON Schema and Pydantic model parsing
3. **03_tools**: Function calling, web search, MCP integration
4. **04_multimodal**: Image processing (URL and base64)
5. **05_stateful**: Conversation state management
6. **06_advanced**: RAG with Pinecone, tool routing

### 🔧 Infrastructure

- **Configuration Management** (`src/config.py`): Centralized config with environment variables
- **Client Wrapper** (`src/client.py`): Simplified OpenAI client creation
- **Environment Template** (`.env.example`): Clear setup instructions
- **Requirements** (`requirements.txt`): All dependencies with versions
- **Tests** (`tests/`): Unit and integration tests

### 📚 Documentation

- **Main README**: Complete guide with quick start and API reference
- **Module READMEs**: Detailed docs for each feature area
- **Code Examples**: 20+ runnable examples with clear explanations
- **Best Practices**: Tips and patterns for production use

### 🔄 Migration from v0.x

Old flat file structure:
```
gpt_oss_*.py  # 10 separate files
```

New organized structure:
```
examples/
  01_basic/
  02_structured_output/
  03_tools/
  04_multimodal/
  05_stateful/
  06_advanced/
src/
  config.py
  client.py
tests/
  test_examples.py
```

### 🎯 Benefits

- **Easier Navigation**: Find examples by feature category
- **Code Reuse**: Shared utilities reduce duplication
- **Extensibility**: Add new features without restructuring
- **Maintainability**: Clear separation of concerns
- **Learning Path**: Progressive complexity from basic to advanced

### 🚀 Getting Started

```bash
# Setup
cp .env.example .env
# Add your API key to .env

pip install -r requirements.txt

# Run examples
python examples/01_basic/instructions.py
python examples/03_tools/function_calling.py
python examples/06_advanced/rag_pinecone.py
```

### 📝 Notes

- All old `gpt_oss_*.py` files have been removed
- Functionality preserved and enhanced in new structure
- No breaking changes to API usage patterns
- Examples are backward compatible with existing code

### 🔗 Resources

- Main README: Comprehensive overview and quick start
- Module READMEs: In-depth feature documentation
- Tests: Example usage and integration patterns

---

**Contributors**: AI-assisted refactoring
**Date**: January 18, 2025

