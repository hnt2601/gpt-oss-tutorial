# Compatibility Guide

## OpenAI SDK Version Compatibility

### ⚠️ Critical: OpenAI SDK Version Requirements

The GPT-OSS API has specific version requirements:

**✅ Required: OpenAI SDK >= 1.50.0, < 2.0.0**

- **Minimum 1.50.0**: The `responses` API was added in this version
- **Maximum < 2.0.0**: Version 2.x has breaking changes in validation

**❌ Common Errors:**

1. **Version < 1.50.0**: `AttributeError: 'OpenAI' object has no attribute 'responses'`
2. **Version >= 2.0.0**: Validation errors with `logprobs`, `refusal` fields

### ✅ Solution

Install compatible version range:

```bash
# Install correct version
uv pip install "openai>=1.50.0,<2.0.0"

# Or reinstall the full package (recommended)
uv pip install -e .
```

### 🔍 Checking Your Version

```bash
# Check installed version
python -c "import openai; print(openai.__version__)"

# Should output: 1.12.0
```

### 📋 Known Issues by Version

| SDK Version | Status | Notes |
|-------------|--------|-------|
| < 1.50.0 | ❌ No `responses` API | Missing required API |
| 1.10.0 - 1.49.x | ❌ Incompatible | No responses API support |
| **1.50.0 - 1.99.x** | ✅ **Recommended** | Full compatibility |
| 1.109.1 | ✅ Tested & Working | Current tested version |
| 2.0.0+ | ❌ Incompatible | Breaking validation changes |
| 2.5.0+ | ❌ Incompatible | Validation errors with logprobs |

### 🐛 Error Symptoms

#### Error 1: Missing responses API (version too old)
```
AttributeError: 'OpenAI' object has no attribute 'responses'
```
**Cause**: OpenAI SDK < 1.50.0  
**Fix**: `uv pip install "openai>=1.50.0,<2.0.0"`

#### Error 2: Validation errors (version too new)
```
ResponseOutputTextParam.logprobs
Input should be iterable [type=iterable_type, input_value=None, input_type=NoneType]
```
**Cause**: OpenAI SDK >= 2.0.0  
**Fix**: `uv pip install "openai>=1.50.0,<2.0.0"`

#### Error 3: refusal field
```
ResponseOutputRefusalParam.refusal
Field required [type=missing]
```
**Cause**: OpenAI SDK >= 2.0.0  
**Fix**: `uv pip install "openai>=1.50.0,<2.0.0"`

### 🔧 Fixing Version Issues

#### Quick Fix
```bash
cd /path/to/gpt-oss-tutorial
source .venv/bin/activate
uv pip install "openai>=1.50.0,<2.0.0"
```

#### Clean Reinstall
```bash
# Remove current environment
rm -rf .venv

# Fresh install
uv venv .venv
source .venv/bin/activate
uv pip install -e .

# Verify version
python -c "import openai; print(f'OpenAI SDK: {openai.__version__}')"
```

### 📦 Dependency Management

Our `pyproject.toml` and `requirements.txt` are configured to use the correct version:

```toml
# pyproject.toml
dependencies = [
    "openai==1.12.0",  # Pinned for GPT-OSS compatibility
    ...
]
```

```txt
# requirements.txt
openai==1.12.0  # Note: Using specific version for compatibility
```

### 🔄 Why This Happens

**Version < 1.50.0**: The `responses` API is a newer feature that didn't exist in older SDK versions.

**Version >= 2.0.0**: OpenAI SDK 2.x introduced breaking changes:
- Stricter response validation
- Expects `logprobs` to be an iterable (list), not `None`
- Added new required fields like `refusal`
- Changed type validation for response items

**Sweet Spot**: Versions 1.50.0 - 1.99.x have the responses API and are compatible with GPT-OSS response format.

### 🛡️ Built-in Checks

The tutorial includes automatic version checking:

```python
from src.client import create_client

# Automatically warns if incompatible version
client = create_client()  # Will show warning if version != 1.12.0

# Disable check if needed
client = create_client(check_version=False)
```

### 📝 Best Practices

1. **Pin the version** in your own projects:
   ```bash
   uv pip freeze | grep openai >> requirements.txt
   ```

2. **Use virtual environments** to isolate dependencies:
   ```bash
   uv venv .venv
   source .venv/bin/activate
   ```

3. **Check version** before running examples:
   ```bash
   python -c "import openai; assert openai.__version__ == '1.12.0', f'Wrong version: {openai.__version__}'"
   ```

4. **Update carefully** - test thoroughly if upgrading SDK

### 🔗 Related Issues

- OpenAI SDK 2.0 changelog: https://github.com/openai/openai-python/releases
- Response validation changes
- Pydantic 2.x compatibility

### 💡 Workarounds (Not Recommended)

If you **must** use a newer SDK version, you could:

1. **Patch response handling** (complex, fragile)
2. **Use raw HTTP requests** instead of SDK
3. **Contact GPT-OSS team** to update response format

However, **we strongly recommend using SDK 1.12.0** instead.

### 🆘 Getting Help

If you still have issues after following this guide:

1. Verify SDK version: `python -c "import openai; print(openai.__version__)"`
2. Check you're in venv: Look for `(.venv)` in terminal prompt
3. Try clean reinstall (see above)
4. Check error message matches known issues
5. Open an issue with:
   - SDK version
   - Full error traceback
   - Example code that fails

### ✅ Verification Script

Run this to verify your setup:

```bash
python << 'EOF'
import openai
from src.client import create_client

print("🔍 Checking compatibility...")
print(f"OpenAI SDK version: {openai.__version__}")

if openai.__version__ == "1.12.0":
    print("✅ Correct version!")
else:
    print(f"❌ Wrong version! Expected 1.12.0, got {openai.__version__}")
    print("   Run: uv pip install 'openai==1.12.0'")
    exit(1)

print("\n🧪 Testing client creation...")
try:
    client = create_client()
    print("✅ Client created successfully!")
except Exception as e:
    print(f"❌ Client creation failed: {e}")
    exit(1)

print("\n🎉 All checks passed!")
EOF
```

Save this as `check_compatibility.py` and run before using examples.

---

**Last updated**: 2025-01-18  
**Tested with**: OpenAI SDK 1.12.0, Python 3.10-3.12

