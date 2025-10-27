#!/usr/bin/env python3
"""
Script d'installation et configuration pour MixBPM
=================================================

Ce script automatise l'installation et la configuration initiale
de l'application MixBPM refactorisée.

Usage:
    python setup.py
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Vérifier la version de Python."""
    print("🐍 Vérification de la version Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} détecté.")
        print("❌ Python 3.8+ requis.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} OK")
    return True

def install_dependencies():
    """Installer les dépendances."""
    print("📦 Installation des dépendances...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dépendances installées avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False

def create_config_file():
    """Créer le fichier de configuration."""
    print("⚙️ Création du fichier de configuration...")
    
    config = {
        "app": {
            "name": "MixBPM",
            "version": "2.0.0-refactored",
            "default_template": "copa_transforme"
        },
        "openai": {
            "api_key": "YOUR_OPENAI_API_KEY_HERE",
            "model": "gpt-4",
            "max_tokens": 2000,
            "temperature": 0.7
        },
        "templates": {
            "available": ["copa_transforme", "virunga", "ip_femme"],
            "validation": True
        },
        "export": {
            "formats": ["docx", "pdf"],
            "currency": "USD",
            "locale": "fr_CD"
        }
    }
    
    config_path = "config.json"
    if not os.path.exists(config_path):
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ Configuration créée: {config_path}")
    else:
        print(f"ℹ️ Configuration existante trouvée: {config_path}")
    
    return config_path

def setup_environment_file():
    """Créer le fichier .env pour les variables d'environnement."""
    print("🔧 Configuration des variables d'environnement...")
    
    env_content = """# Configuration MixBPM
# =====================

# Clé API OpenAI (OBLIGATOIRE)
OPENAI_API_KEY=your_openai_api_key_here

# Configuration de l'application
APP_NAME=MixBPM
APP_VERSION=2.0.0-refactored
DEFAULT_TEMPLATE=copa_transforme

# Configuration Streamlit
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true

# Configuration de l'IA
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7

# Configuration des exports
EXPORT_CURRENCY=USD
EXPORT_LOCALE=fr_CD

# Mode debug (true/false)
DEBUG_MODE=false
"""
    
    env_path = ".env"
    if not os.path.exists(env_path):
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print(f"✅ Fichier environnement créé: {env_path}")
        print("⚠️ N'oubliez pas de configurer votre clé API OpenAI dans .env")
    else:
        print(f"ℹ️ Fichier .env existant trouvé: {env_path}")
    
    return env_path

def create_data_directories():
    """Créer les répertoires de données nécessaires."""
    print("📁 Création des répertoires de données...")
    
    directories = [
        "data",
        "exports",
        "logs",
        "temp"
    ]
    
    created = []
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            created.append(directory)
            print(f"✅ Répertoire créé: {directory}/")
    
    if not created:
        print("ℹ️ Tous les répertoires existent déjà")
    
    return created

def validate_installation():
    """Valider l'installation."""
    print("🔍 Validation de l'installation...")
    
    # Tester les imports
    try:
        exec("""
# Test des imports principaux
from templates.template_manager import get_available_templates
from services.ai.content_generation import AIContentGenerator
from utils.validation_utils import validate_financial_data
from ui.components import create_sidebar_config

# Test basique
templates = get_available_templates()
assert len(templates) >= 3, "Pas assez de templates"
assert "copa_transforme" in templates, "Template COPA manquant"
assert "virunga" in templates, "Template Virunga manquant" 
assert "ip_femme" in templates, "Template IP Femme manquant"
""")
        print("✅ Tous les modules se chargent correctement")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la validation: {e}")
        return False

def show_next_steps():
    """Afficher les prochaines étapes."""
    print("\n" + "🎯" * 20)
    print("INSTALLATION TERMINÉE!")
    print("🎯" * 20)
    
    print("\n📋 Prochaines étapes:")
    print("1. 🔑 Configurez votre clé API OpenAI dans le fichier .env")
    print("2. 🚀 Lancez l'application: streamlit run main.py")
    print("3. 🌐 Ouvrez votre navigateur sur http://localhost:8501")
    print("4. 🎨 Testez les 3 templates disponibles")
    print("5. 📖 Consultez README.md pour plus d'informations")
    
    print("\n🔧 Commandes utiles:")
    print("• Tester l'architecture: python test_architecture.py")
    print("• Migrer depuis l'ancienne version: python migration.py")
    print("• Version legacy (comparaison): streamlit run mixbpm.py")
    
    print("\n📚 Documentation:")
    print("• README.md - Guide utilisateur complet")
    print("• ARCHITECTURE.md - Détails techniques")
    print("• config.json - Configuration de l'application")

def main():
    """Fonction principale d'installation."""
    print("🚀 MixBPM - Script d'Installation")
    print("=" * 40)
    
    # Vérifications préalables
    if not check_python_version():
        return 1
    
    # Installation des dépendances
    if not install_dependencies():
        return 1
    
    # Configuration
    create_config_file()
    setup_environment_file()
    create_data_directories()
    
    # Validation
    if not validate_installation():
        print("❌ Validation échouée. Vérifiez l'installation.")
        return 1
    
    # Instructions finales
    show_next_steps()
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)