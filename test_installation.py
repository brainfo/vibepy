import sys
import subprocess
from importlib import import_module

def test_imports():
    """Test if all required packages can be imported."""
    packages = [
        'pyrate',
        'readchar',
        'openai',
        'requests',
        'colorama',
        'pyperclip'
    ]
    
    print("Testing package imports...")
    for package in packages:
        try:
            import_module(package)
            print(f"✓ {package} imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {package}: {e}")
            return False
    return True

def test_cli():
    """Test if the CLI command is available and works."""
    print("\nTesting CLI command...")
    try:
        # Try to run the command with a timeout
        result = subprocess.run(
            ['pyrate', '--help'],
            capture_output=True,
            text=True,
            timeout=10  # 10 second timeout
        )
        if result.returncode == 0:
            print("✓ CLI command works")
            return True
        else:
            print(f"✗ CLI command failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ CLI command timed out (took too long to respond)")
        return False
    except FileNotFoundError:
        print("✗ CLI command not found")
        return False
    except Exception as e:
        print(f"✗ CLI command failed with error: {e}")
        return False

def main():
    print("Testing pyrate package installation...\n")
    
    # Test Python version
    print(f"Python version: {sys.version}")
    
    # Run tests
    imports_ok = test_imports()
    cli_ok = test_cli()
    
    # Summary
    print("\nTest Summary:")
    print(f"Package imports: {'✓' if imports_ok else '✗'}")
    print(f"CLI command: {'✓' if cli_ok else '✗'}")
    
    if imports_ok and cli_ok:
        print("\nAll tests passed! Package is ready for release.")
        return 0
    else:
        print("\nSome tests failed. Please fix the issues before releasing.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 