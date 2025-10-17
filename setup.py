"""
Setup script for Renters Insurance Data Extractor
"""
import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version.split()[0]}")
    return True

def check_tesseract():
    """Check if Tesseract is installed"""
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✓ Tesseract installed: {version}")
            return True
    except FileNotFoundError:
        print("❌ Tesseract OCR not found")
        print("   Please install Tesseract:")
        print("   Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   Linux: sudo apt-get install tesseract-ocr")
        print("   macOS: brew install tesseract")
        return False

def create_directories():
    """Create necessary directories"""
    dirs = ['uploads', 'exports', 'core', 'extractors', 'models', 'api', 
            'static/css', 'static/js', 'templates']
    
    for directory in dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✓ Directories created")

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not Path('.env').exists():
        if Path('.env.example').exists():
            import shutil
            shutil.copy('.env.example', '.env')
            print("✓ .env file created from .env.example")
            print("  Please update the settings in .env file")
        else:
            print("⚠ .env.example not found")
    else:
        print("✓ .env file already exists")

def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling Python dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
                             '-r', 'requirements.txt'])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_init_files():
    """Create __init__.py files"""
    init_dirs = ['core', 'extractors', 'models', 'api']
    for directory in init_dirs:
        init_file = Path(directory) / '__init__.py'
        if not init_file.exists():
            init_file.write_text(f'"""{directory.capitalize()} package"""\n')
    print("✓ __init__.py files created")

def main():
    """Main setup function"""
    print("=" * 60)
    print("Renters Insurance Data Extractor - Setup")
    print("=" * 60)
    print()
    
    # Check requirements
    print("Checking requirements...")
    if not check_python_version():
        return False
    
    if not check_tesseract():
        print("\n⚠ Please install Tesseract and run setup again")
        return False
    
    print()
    
    # Setup
    print("Setting up project...")
    create_directories()
    create_init_files()
    create_env_file()
    
    print()
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    print()
    print("=" * 60)
    print("✓ Setup completed successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Update settings in .env file")
    print("2. Run: python app.py")
    print("3. Open: http://localhost:5000")
    print()
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)