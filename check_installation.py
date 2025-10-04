"""
Installation Checker for Voice AI Agent
Verifies that all required packages are installed correctly
"""

import sys


def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name}")
        return True
    except ImportError:
        print(f"❌ {package_name} - NOT INSTALLED")
        return False


def main():
    """Check all required packages"""
    print("\n" + "="*60)
    print("📦 CHECKING INSTALLATION")
    print("="*60 + "\n")
    
    packages = [
        ("CrewAI", "crewai"),
        ("LangChain", "langchain"),
        ("LangChain OpenAI", "langchain_openai"),
        ("LangChain Community", "langchain_community"),
        ("OpenAI", "openai"),
        ("Speech Recognition", "speech_recognition"),
        ("gTTS", "gtts"),
        ("Pygame", "pygame"),
        ("DuckDuckGo Search", "duckduckgo_search"),
        ("Python dotenv", "dotenv"),
        ("Pydantic", "pydantic"),
    ]
    
    all_installed = True
    
    print("Core Packages:")
    print("-" * 60)
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            all_installed = False
    
    # Check for PyAudio (optional for voice)
    print("\nVoice Packages (optional for text-only mode):")
    print("-" * 60)
    try:
        import pyaudio
        print("✅ PyAudio")
    except ImportError:
        print("⚠️  PyAudio - Not installed (required for microphone input)")
        print("   Install with: sudo apt-get install python3-pyaudio portaudio19-dev")
    
    # Check environment variable
    print("\nEnvironment:")
    print("-" * 60)
    import os
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OPENAI_API_KEY is set")
    else:
        print("❌ OPENAI_API_KEY is NOT set")
        print("   Set with: export OPENAI_API_KEY='your-key-here'")
        all_installed = False
    
    # Summary
    print("\n" + "="*60)
    if all_installed:
        print("✅ ALL REQUIRED PACKAGES INSTALLED!")
        print("="*60)
        print("\nYou can now run:")
        print("  python test_agent.py          - Test the setup")
        print("  python simple_voice_agent.py  - Simple text agent")
        print("  python voice_ai_agent.py      - Full voice agent")
    else:
        print("❌ SOME PACKAGES ARE MISSING")
        print("="*60)
        print("\nPlease install missing packages:")
        print("  pip install -r requirements.txt")
        print("\nFor PyAudio (voice input):")
        print("  Linux: sudo apt-get install python3-pyaudio portaudio19-dev")
        print("  Mac: brew install portaudio && pip install pyaudio")
    
    print("\n")
    return 0 if all_installed else 1


if __name__ == "__main__":
    sys.exit(main())
