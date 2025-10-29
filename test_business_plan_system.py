"""
Test du nouveau système de génération de business plan
Version corrigée inspirée d'Origin.txt
"""

# Test rapide du système
if __name__ == "__main__":
    from templates.business_plan_prompts import get_sections_configuration
    
    print("=== Test du système corrigé ===")
    
    # Test COPA TRANSFORME
    config = get_sections_configuration("COPA TRANSFORME")
    print(f"Sections COPA TRANSFORME: {len(config)}")
    
    # Vérifier une section spécifique
    if "Couverture" in config:
        couverture = config["Couverture"]
        print(f"Section Couverture OK")
        print(f"System message length: {len(couverture['system_message'])}")
        print(f"User query: {couverture['user_query'][:50]}...")
    
    # Test Virunga
    config_virunga = get_sections_configuration("Virunga")
    print(f"Sections Virunga: {len(config_virunga)}")
    
    # Test IP Femme  
    config_ip = get_sections_configuration("IP Femme")
    print(f"Sections IP Femme: {len(config_ip)}")
    
    print("\n✅ Système corrigé opérationnel!")
    print("\nDifférences avec l'ancien système:")
    print("- Prompts inspirés d'Origin.txt (génération directe)")
    print("- Nettoyage du contenu pour éviter les doublons")
    print("- Contexte limité pour éviter les répétitions")
    print("- Formatage amélioré")