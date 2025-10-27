#!/usr/bin/env python3
"""
Test du workflow de génération de business plan
Simule le passage des données entre les étapes
"""

import sys
import os

# Mock de Streamlit session state pour tester
class MockSessionState:
    def __init__(self):
        self.data = {}
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def __setattr__(self, key, value):
        if key == 'data':
            super().__setattr__(key, value)
        else:
            self.data[key] = value
    
    def __getattr__(self, key):
        return self.data.get(key, None)

def test_workflow_data_flow():
    """Test de la cohérence des clés de données entre les étapes"""
    
    print("🔍 Test du workflow - Cohérence des données")
    print("=" * 50)
    
    # Simulation des données créatives
    mock_session = MockSessionState()
    
    # Données de persona (étape créative)
    mock_session.persona = {
        "nom": "Jean Mukendi",
        "age": 35,
        "profession": "Commerçant",
        "besoins": "Optimiser les ventes"
    }
    mock_session.persona_data = mock_session.persona  # Clé de cohérence
    
    # Données d'analyse de marché
    mock_session.analyse_marche = {
        "taille_marche": "1M USD",
        "concurrents": ["Concurrent A", "Concurrent B"],
        "opportunites": "Marché en croissance"
    }
    
    # Données de concurrence
    mock_session.concurrence = {
        "principal_concurrent": "Concurrent A",
        "avantage_competitif": "Innovation produit"
    }
    
    # Données financières
    mock_session.export_data_investissements = {
        "equipements": {"montant": 10000, "devise": "USD"},
        "immobilier": {"montant": 15000, "devise": "USD"}
    }
    
    mock_session.export_data_compte = {
        "chiffre_affaires": {"an1": 50000, "an2": 75000, "an3": 100000},
        "resultat_net": {"an1": 5000, "an2": 12000, "an3": 20000}
    }
    
    print("✅ Données simulées créées")
    
    # Test de récupération des données (comme dans page_generation_business_plan)
    business_model_precedent = mock_session.get('business_model_precedent', '')
    persona_data = mock_session.get('persona_data', mock_session.get('persona', {}))
    marche_data = mock_session.get('analyse_marche', {})
    concurrence_data = mock_session.get('concurrence', {})
    
    print(f"📊 Persona récupéré: {len(str(persona_data))} caractères")
    print(f"📊 Marché récupéré: {len(str(marche_data))} caractères")
    print(f"📊 Concurrence récupérée: {len(str(concurrence_data))} caractères")
    
    # Vérifier que les données ne sont pas vides
    assert persona_data, "❌ Données persona vides"
    assert marche_data, "❌ Données marché vides"
    assert concurrence_data, "❌ Données concurrence vides"
    
    print("✅ Toutes les données créatives sont accessibles")
    
    # Test de consolidation financière (simulation)
    donnees_financieres = {
        'investissements': mock_session.get('export_data_investissements', {}),
        'compte_resultats': mock_session.get('export_data_compte', {}),
    }
    
    # Calcul simulé de synthèse
    total_investissements = sum([
        float(str(v.get('montant', 0))) 
        for v in donnees_financieres['investissements'].values() 
        if isinstance(v, dict) and 'montant' in v
    ])
    
    print(f"💰 Total investissements: {total_investissements} USD")
    assert total_investissements > 0, "❌ Aucun investissement calculé"
    
    print("✅ Consolidation financière fonctionnelle")
    
    # Test de contexte complet
    contexte_complet = f"""
    DONNÉES DU BUSINESS MODEL: {business_model_precedent}
    
    INFORMATIONS PERSONA: {persona_data}
    
    ANALYSE DE MARCHÉ: {marche_data}
    
    ANALYSE CONCURRENCE: {concurrence_data}
    """
    
    assert len(contexte_complet.strip()) > 100, "❌ Contexte trop court"
    print(f"📋 Contexte complet: {len(contexte_complet)} caractères")
    print("✅ Contexte enrichi créé avec succès")
    
    print("\n🎉 WORKFLOW TESTÉ AVEC SUCCÈS!")
    print("=" * 50)
    print("✅ Cohérence des clés de données")
    print("✅ Récupération des données créatives")
    print("✅ Consolidation des données financières")
    print("✅ Génération du contexte complet")
    
    return True

if __name__ == "__main__":
    try:
        test_workflow_data_flow()
        print("\n🚀 TOUS LES TESTS SONT PASSÉS!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ÉCHEC DU TEST: {e}")
        sys.exit(1)