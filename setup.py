#!/usr/bin/env python3
"""
Setup script for LeInterview application
"""

import os
import sys
import subprocess
import pkg_resources
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    print("✅ Python version check passed")

def check_dependencies():
    """Check and install required system dependencies"""
    print("Checking system dependencies...")
    
    # Check for required system packages
    system_deps = {
        'gcc': 'GCC compiler',
        'g++': 'G++ compiler', 
        'javac': 'Java compiler (OpenJDK)',
        'python3': 'Python 3'
    }
    
    missing = []
    for cmd, desc in system_deps.items():
        try:
            subprocess.run([cmd, '--version'], capture_output=True, check=True)
            print(f"✅ {desc} found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(f"❌ {desc} not found")
    
    if missing:
        print("\nMissing system dependencies:")
        for dep in missing:
            print(dep)
        print("\nPlease install missing dependencies and run setup again.")
        return False
    
    return True

def install_requirements():
    """Install Python requirements"""
    print("\nInstalling Python dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        return False

def setup_environment():
    """Set up environment configuration"""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        print("\nSetting up environment configuration...")
        with open(env_example) as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env and add your GEMINI_API_KEY")
        return True
    elif env_file.exists():
        print("✅ Environment file already exists")
        return True
    else:
        print("❌ No .env.example file found")
        return False

def verify_installation():
    """Verify the installation by running basic checks"""
    print("\nVerifying installation...")
    
    try:
        # Try importing required packages
        import flask
        import flask_cors
        import google.generativeai
        import speech_recognition
        print("✅ All required packages can be imported")
        
        # Check if templates exist
        if Path('templates/index.html').exists() and Path('templates/interview.html').exists():
            print("✅ Template files found")
        else:
            print("❌ Template files missing")
            return False
            
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 LeInterview Setup Script")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check system dependencies
    if not check_dependencies():
        print("\n❌ Setup failed due to missing system dependencies")
        sys.exit(1)
    
    # Install Python requirements
    if not install_requirements():
        print("\n❌ Setup failed during package installation")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Setup failed during environment configuration")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("\n❌ Setup failed during verification")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your GEMINI_API_KEY")
    print("2. Run: python app.py")
    print("3. Open http://localhost:5000 in your browser")
    print("\nFor deployment instructions, see deploy.md")

if __name__ == "__main__":
    main()