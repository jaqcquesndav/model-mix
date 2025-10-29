"""
Script de test pour vérifier la configuration OpenAI
Inspiré des tests d'Origin.txt
"""

import os
import sys
from dotenv import load_dotenv

# Ajouter le chemin du projet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Charger les variables d'environnement
load_dotenv()

def test_openai_configuration():
    """Test de base de la configuration OpenAI"""
    print("🧪 Test de configuration OpenAI...")
    
    # Test 1: Vérifier la clé API
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("❌ Erreur: Variable API_KEY non définie")
        print("💡 Solution: Créez un fichier .env avec votre clé API")
        return False
    
    if not api_key.startswith("sk-"):
        print("❌ Erreur: Format de clé API invalide")
        print("💡 Solution: Vérifiez que votre clé commence par 'sk-'")
        return False
    
    print(f"✅ Clé API trouvée: {api_key[:8]}...{api_key[-4:]}")
    
    # Test 2: Import des modules
    try:
        from services.ai.content_generation import tester_connexion_openai
        print("✅ Modules importés avec succès")
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        return False
    
    # Test 3: Test de connexion réelle
    try:
        print("🔄 Test de connexion à l'API OpenAI...")
        status = tester_connexion_openai()
        
        if status["status"] == "success":
            print(f"✅ {status['message']}")
            print(f"📊 {status['details']}")
            return True
        else:
            print(f"❌ {status['message']}")
            print(f"📋 {status['details']}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_imports():
    """Test des imports principaux"""
    print("\n🧪 Test des imports...")
    
    modules_to_test = [
        "streamlit",
        "openai", 
        "pandas",
        "docx",
        "langchain",
        "services.ai.content_generation",
        "services.document.generation",
        "templates"
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")

if __name__ == "__main__":
    print("🚀 MixBPM - Test de configuration")
    print("="*50)
    
    # Test des imports
    test_imports()
    
    # Test de la configuration OpenAI
    print("\n" + "="*50)
    success = test_openai_configuration()
    
    print("\n" + "="*50)
    if success:
        print("🎉 Tous les tests sont passés! L'application est prête.")
        print("\n💡 Lancez l'application avec: streamlit run main.py")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")
        print("\n📋 Instructions:")
        print("1. Copiez .env.example vers .env")
        print("2. Ajoutez votre clé API OpenAI dans .env")
        print("3. Installez les dépendances: pip install -r requirements.txt")