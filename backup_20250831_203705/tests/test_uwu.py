#!/usr/bin/env python3
"""
Simple test script for UwU-CLI
Tests basic functionality without full shell
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from utils.tokenizer import context_entities, inject_context
        print("✅ Tokenizer module imported")
    except ImportError as e:
        print(f"❌ Tokenizer import failed: {e}")
        return False
    
    try:
        from utils.config import load_config, get_alias
        print("✅ Config module imported")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from utils.ascii_ui import print_with_effect, get_random_effect
        print("✅ ASCII UI module imported")
    except ImportError as e:
        print(f"❌ ASCII UI import failed: {e}")
        return False
    
    try:
        from phrases.pokemon import get_pokemon_roast
        print("✅ Pokémon phrases imported")
    except ImportError as e:
        print(f"❌ Pokémon phrases import failed: {e}")
        return False
    
    return True

def test_tokenizer():
    """Test tokenizer functionality"""
    print("\n🧪 Testing tokenizer...")
    
    try:
        from utils.tokenizer import context_entities, inject_context
        
        # Test context detection
        test_text = "def my_function(): git commit -m 'test' python script.py"
        entities = context_entities(test_text)
        
        print(f"✅ Context entities detected: {len(entities)} types")
        print(f"   Functions: {entities['functions']}")
        print(f"   Git commands: {entities['git_commands']}")
        print(f"   Python commands: {entities['python_commands']}")
        
        # Test context injection
        roast = "H-hey, {function} trainer! Keep {git} my vibes!"
        injected = inject_context(roast, test_text)
        print(f"✅ Context injection: {injected}")
        
        return True
    except Exception as e:
        print(f"❌ Tokenizer test failed: {e}")
        return False

def test_phrases():
    """Test phrase functionality"""
    print("\n🧪 Testing phrases...")
    
    try:
        from phrases.pokemon import get_pokemon_roast
        from phrases.digimon import get_digimon_roast
        
        pokemon_roast = get_pokemon_roast()
        digimon_roast = get_digimon_roast()
        
        print(f"✅ Pokémon roast: {pokemon_roast[:50]}...")
        print(f"✅ Digimon roast: {digimon_roast[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ Phrases test failed: {e}")
        return False

def test_config():
    """Test configuration functionality"""
    print("\n🧪 Testing configuration...")
    
    try:
        from utils.config import load_config, set_config_value, get_config_value
        
        config = load_config()
        print(f"✅ Config loaded: {len(config)} settings")
        
        # Test setting/getting values
        set_config_value("test_key", "test_value")
        value = get_config_value("test_key")
        print(f"✅ Config set/get: {value}")
        
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_ascii_ui():
    """Test ASCII UI functionality"""
    print("\n🧪 Testing ASCII UI...")
    
    try:
        from utils.ascii_ui import print_with_effect, get_random_effect
        
        # Test effect generation
        effect = get_random_effect("uwu")
        print(f"✅ Random effect generated: {effect[:30] if effect else 'None'}...")
        
        # Test themed prompt
        from utils.ascii_ui import get_themed_prompt
        prompt = get_themed_prompt("feral", "~/Documents")
        print(f"✅ Themed prompt: {prompt}")
        
        return True
    except Exception as e:
        print(f"❌ ASCII UI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("╔════════════════════════════════════════════╗")
    print("║              UwU-CLI Tests                 ║")
    print("╚════════════════════════════════════════════╝")
    
    tests = [
        test_imports,
        test_tokenizer,
        test_phrases,
        test_config,
        test_ascii_ui
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! UwU-CLI is ready to use!")
        print("\n🚀 To start UwU-CLI, run:")
        print("   python uwu_cli.py")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 