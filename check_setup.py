#!/usr/bin/env python
"""
Setup verification script for GPT-OSS Tutorial

Run this to verify your installation is correct before running examples.
"""

import sys


def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version >= (3, 10):
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} (need 3.10+)")
        return False


def check_openai_version():
    """Check OpenAI SDK version"""
    print("\n📦 Checking OpenAI SDK...")
    try:
        import openai
        version = openai.__version__
        
        try:
            from packaging import version as pkg_version
            v = pkg_version.parse(version)
            min_v = pkg_version.parse("1.50.0")
            max_v = pkg_version.parse("2.0.0")
            
            if min_v <= v < max_v:
                print(f"   ✅ OpenAI SDK {version} (compatible)")
                return True
            elif v < min_v:
                print(f"   ❌ OpenAI SDK {version} (too old, need >= 1.50.0)")
                print(f"      Responses API requires version >= 1.50.0")
                print(f"      Fix: uv pip install 'openai>=1.50.0,<2.0.0'")
                return False
            else:
                print(f"   ⚠️  OpenAI SDK {version} (may have issues)")
                print(f"      Recommended: 1.50.0 <= version < 2.0.0")
                print(f"      Fix: uv pip install 'openai>=1.50.0,<2.0.0'")
                return False
        except ImportError:
            # Fallback if packaging not available
            if "1." in version and not version.startswith("1.0") and not version.startswith("1.1") and not version.startswith("1.2") and not version.startswith("1.3") and not version.startswith("1.4"):
                print(f"   ✅ OpenAI SDK {version} (appears compatible)")
                return True
            else:
                print(f"   ⚠️  OpenAI SDK {version} (cannot verify)")
                return True
                
    except ImportError:
        print("   ❌ OpenAI SDK not installed")
        print("      Fix: uv pip install -e .")
        return False


def check_httpx_version():
    """Check httpx version compatibility"""
    print("\n🌐 Checking httpx version...")
    try:
        import httpx
        version = httpx.__version__
        print(f"   ✅ httpx {version} (installed)")
        # httpx compatibility is handled by openai's dependencies
        return True
    except ImportError:
        print("   ❌ httpx not installed")
        return False


def check_package_installed():
    """Check if gpt-oss-tutorial package is installed"""
    print("\n📦 Checking package installation...")
    try:
        from src.client import create_client
        from src.config import get_config
        print("   ✅ Package installed (can import from src)")
        return True
    except ImportError as e:
        print(f"   ❌ Package not installed: {e}")
        print("      Fix: cd /path/to/gpt-oss-tutorial && uv pip install -e .")
        return False


def check_env_file():
    """Check if .env file exists and has API_KEY"""
    print("\n⚙️  Checking environment configuration...")
    import os
    from pathlib import Path
    
    env_file = Path(".env")
    if not env_file.exists():
        print("   ❌ .env file not found")
        print("      Fix: cp .env.example .env")
        return False
    
    # Try to load config
    try:
        from src.config import get_config
        config = get_config()
        if config.api_key and config.api_key != "your_api_key_here":
            print(f"   ✅ API_KEY configured")
            return True
        else:
            print("   ⚠️  API_KEY not set or using placeholder")
            print("      Fix: Edit .env and add your actual API key")
            return False
    except Exception as e:
        print(f"   ❌ Error reading config: {e}")
        return False


def check_client_creation():
    """Check if client can be created"""
    print("\n🔌 Testing client creation...")
    try:
        from src.client import create_client
        client = create_client(check_version=False)
        print("   ✅ Client created successfully")
        return True
    except Exception as e:
        print(f"   ❌ Client creation failed: {e}")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("GPT-OSS Tutorial - Setup Verification")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_openai_version(),
        check_httpx_version(),
        check_package_installed(),
        check_env_file(),
        check_client_creation(),
    ]
    
    print("\n" + "=" * 60)
    
    if all(checks):
        print("🎉 All checks passed! You're ready to go!")
        print("\nNext steps:")
        print("  • Run examples: python examples/01_basic/instructions.py")
        print("  • Run tests: pytest tests/")
        print("  • Read docs: cat README.md")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nQuick fix:")
        print("  cd /path/to/gpt-oss-tutorial")
        print("  rm -rf .venv")
        print("  ./quick_start.sh")
        return 1


if __name__ == "__main__":
    sys.exit(main())

