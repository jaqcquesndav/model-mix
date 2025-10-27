"""
Service de gestion des données business et business model
"""

import streamlit as st
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

def init_session_state():
    """Initialise les variables de session state"""
    default_values = {
        # Données générales
        'nom_entreprise': '',
        'secteur_activite': '',
        'type_entreprise': 'PME',
        'localisation': '',
        'template_selectionne': 'COPA TRANSFORME',
        
        # Données collectées
        'persona_data': {},
        'analyse_marche': {},
        'concurrence': {},
        'facteurs_limitants_data': {},
        'problem_tree_data': {},
        'business_model_precedent': '',
        
        # Données financières
        'investissements': [],
        'charges_fixes': {},
        'ca_previsions': {},
        'charges_variables': {},
        'salaires': {},
        'financements': {},
        
        # Données export pour tableaux
        'export_data_investissements': {},
        'export_data_salaires_charges_sociales': {},
        'export_data_detail_amortissements': {},
        'export_data_compte_resultats_previsionnel': {},
        'export_data_soldes_intermediaires_de_gestion': {},
        'export_data_capacite_autofinancement': {},
        'export_data_seuil_rentabilite_economique': {},
        'export_data_besoin_fonds_roulement': {},
        'export_data_plan_financement_trois_ans': {},
        'export_data_budget_previsionnel_tresorerie_part1': {},
        'export_data_budget_previsionnel_tresorerie_part2': {},
        
        # Métadonnées
        'derniere_modification': datetime.now().isoformat(),
        'version': '1.0',
        'etapes_completees': []
    }
    
    for key, default_value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def sauvegarder_donnees_session(cle: str, donnees: Any):
    """
    Sauvegarde des données dans le session state
    
    Args:
        cle (str): Clé de sauvegarde
        donnees: Données à sauvegarder
    """
    st.session_state[cle] = donnees
    st.session_state['derniere_modification'] = datetime.now().isoformat()

def recuperer_donnees_session(cle: str, default=None) -> Any:
    """
    Récupère des données du session state
    
    Args:
        cle (str): Clé des données
        default: Valeur par défaut si la clé n'existe pas
    
    Returns:
        Any: Données récupérées
    """
    return st.session_state.get(cle, default)

def collect_persona_pme(template_nom: str = "COPA TRANSFORME") -> Dict[str, Any]:
    """
    Collecte les données de persona pour PME
    
    Args:
        template_nom (str): Nom du template à utiliser
    
    Returns:
        dict: Données du persona PME
    """
    from templates import get_secteurs
    
    secteurs = get_secteurs(template_nom)
    
    st.subheader("Informations de base sur votre PME")
    
    # Utiliser les données existantes si disponibles
    persona_existant = recuperer_donnees_session('persona_data', {})
    
    persona_data = {}
    
    # Informations générales
    persona_data['nom_entreprise'] = st.text_input(
        "Nom de votre PME",
        value=persona_existant.get('nom_entreprise', ''),
        help="Le nom officiel ou commercial de votre entreprise"
    )
    
    persona_data['secteur_activite'] = st.selectbox(
        "Secteur d'activité principal",
        secteurs,
        index=secteurs.index(persona_existant.get('secteur_activite', secteurs[0])) if persona_existant.get('secteur_activite') in secteurs else 0,
        help="Choisissez le secteur qui correspond le mieux à votre activité"
    )
    
    persona_data['forme_juridique'] = st.selectbox(
        "Forme juridique",
        ["À définir", "Entreprise individuelle", "SARLU", "SARL", "SAS", "SA", "Coopérative", "Association"],
        index=["À définir", "Entreprise individuelle", "SARLU", "SARL", "SAS", "SA", "Coopérative", "Association"].index(persona_existant.get('forme_juridique', 'À définir')),
        help="Statut juridique de votre entreprise"
    )
    
    persona_data['stade_developpement'] = st.selectbox(
        "Stade de développement",
        ["Idée/Projet", "Démarrage", "Croissance", "Maturité", "Expansion"],
        index=["Idée/Projet", "Démarrage", "Croissance", "Maturité", "Expansion"].index(persona_existant.get('stade_developpement', 'Idée/Projet')),
        help="À quel stade se trouve actuellement votre entreprise"
    )
    
    # Localisation et marché
    st.subheader("Localisation et marché cible")
    
    persona_data['localisation_principale'] = st.selectbox(
        "Localisation principale",
        ["Kinshasa", "Lubumbashi", "Goma", "Mbuji-Mayi", "Kisangani", "Bukavu", "Matadi", "Kolwezi", "Autre"],
        index=["Kinshasa", "Lubumbashi", "Goma", "Mbuji-Mayi", "Kisangani", "Bukavu", "Matadi", "Kolwezi", "Autre"].index(persona_existant.get('localisation_principale', 'Kinshasa')),
        help="Ville principale d'implantation de votre PME"
    )
    
    persona_data['zone_couverture'] = st.multiselect(
        "Zones de couverture",
        ["Local (quartier/commune)", "Municipal", "Provincial", "National", "Régional (SADC)", "International"],
        default=persona_existant.get('zone_couverture', ["Local (quartier/commune)"]),
        help="Zones géographiques que votre PME dessert ou prévoit desservir"
    )
    
    # Produits/Services
    st.subheader("Offre de produits/services")
    
    persona_data['description_activite'] = st.text_area(
        "Décrivez votre activité principale",
        value=persona_existant.get('description_activite', ''),
        height=100,
        help="Description détaillée de ce que fait votre PME"
    )
    
    persona_data['produits_services'] = st.text_area(
        "Principaux produits/services",
        value=persona_existant.get('produits_services', ''),
        height=80,
        help="Liste des produits ou services que vous proposez"
    )
    
    persona_data['valeur_ajoutee'] = st.text_area(
        "Votre valeur ajoutée unique",
        value=persona_existant.get('valeur_ajoutee', ''),
        height=80,
        help="Ce qui vous différencie de la concurrence"
    )
    
    # Équipe et ressources
    st.subheader("Équipe et ressources")
    
    persona_data['nb_employes'] = st.number_input(
        "Nombre d'employés actuels",
        min_value=0,
        max_value=1000,
        value=persona_existant.get('nb_employes', 1),
        help="Nombre total de personnes travaillant dans votre PME"
    )
    
    persona_data['competences_cles'] = st.text_area(
        "Compétences clés de l'équipe",
        value=persona_existant.get('competences_cles', ''),
        height=80,
        help="Principales compétences et expertises de votre équipe"
    )
    
    # Objectifs et vision
    st.subheader("Vision et objectifs")
    
    persona_data['objectifs_court_terme'] = st.text_area(
        "Objectifs à court terme (1-2 ans)",
        value=persona_existant.get('objectifs_court_terme', ''),
        height=80,
        help="Vos principaux objectifs pour les prochaines années"
    )
    
    persona_data['vision_long_terme'] = st.text_area(
        "Vision à long terme (3-5 ans)",
        value=persona_existant.get('vision_long_terme', ''),
        height=80,
        help="Où vous voyez-vous votre PME dans 5 ans"
    )
    
    # Sauvegarde
    if st.button("Sauvegarder les informations"):
        sauvegarder_donnees_session('persona_data', persona_data)
        st.success("Informations sauvegardées avec succès!")
        st.rerun()
    
    return persona_data

def collect_analyse_marche_pme(template_nom: str = "COPA TRANSFORME") -> Dict[str, Any]:
    """
    Collecte les données d'analyse de marché pour PME
    
    Args:
        template_nom (str): Nom du template à utiliser
    
    Returns:
        dict: Données d'analyse de marché
    """
    st.subheader("Analyse de votre marché")
    
    # Récupérer les données existantes
    marche_existant = recuperer_donnees_session('analyse_marche', {})
    
    marche_data = {}
    
    # Marché cible
    st.subheader("Votre marché cible")
    
    marche_data['taille_marche'] = st.selectbox(
        "Taille estimée de votre marché",
        ["Très petit (moins de 1000 clients)", "Petit (1000-5000 clients)", 
         "Moyen (5000-20000 clients)", "Grand (20000-100000 clients)", 
         "Très grand (plus de 100000 clients)"],
        index=0,
        help="Estimation du nombre de clients potentiels"
    )
    
    marche_data['croissance_marche'] = st.selectbox(
        "Tendance de croissance du marché",
        ["En déclin", "Stable", "Croissance lente", "Croissance rapide", "Émergent"],
        index=2,
        help="Comment évolue votre marché"
    )
    
    # Clients cibles
    st.subheader("Vos clients cibles")
    
    marche_data['segments_clients'] = st.multiselect(
        "Principaux segments de clientèle",
        ["Particuliers/Ménages", "Petites entreprises", "Moyennes entreprises", 
         "Grandes entreprises", "Institutions publiques", "ONGs", "Écoles/Universités", 
         "Hôpitaux/Centres de santé", "Hôtels/Restaurants", "Marchés/Commerçants"],
        default=marche_existant.get('segments_clients', ["Particuliers/Ménages"]),
        help="Types de clients que vous ciblez"
    )
    
    marche_data['besoins_clients'] = st.text_area(
        "Principaux besoins de vos clients",
        value=marche_existant.get('besoins_clients', ''),
        height=100,
        help="Quels problèmes résolvez-vous pour vos clients ?"
    )
    
    marche_data['pouvoir_achat'] = st.selectbox(
        "Pouvoir d'achat de vos clients",
        ["Très faible", "Faible", "Moyen", "Élevé", "Très élevé"],
        index=2,
        help="Capacité financière de vos clients cibles"
    )
    
    # Contexte local
    st.subheader("Contexte du marché en RDC")
    
    marche_data['defis_locaux'] = st.multiselect(
        "Principaux défis du marché local",
        ["Pouvoir d'achat limité", "Accès difficile au financement", 
         "Infrastructure défaillante", "Concurrence informelle", 
         "Fluctuation monétaire", "Réglementation complexe", 
         "Approvisionnement difficile", "Transport coûteux"],
        default=marche_existant.get('defis_locaux', []),
        help="Obstacles spécifiques au contexte congolais"
    )
    
    marche_data['opportunites_locales'] = st.multiselect(
        "Opportunités du marché local",
        ["Demande croissante", "Peu de concurrence", "Support gouvernemental", 
         "Ressources locales disponibles", "Main-d'œuvre qualifiée", 
         "Partenaires potentiels", "Marchés d'exportation", "Innovation possible"],
        default=marche_existant.get('opportunites_locales', []),
        help="Avantages et opportunités du marché congolais"
    )
    
    # Saisonnalité
    marche_data['saisonnalite'] = st.selectbox(
        "Votre activité est-elle saisonnière ?",
        ["Non", "Légèrement", "Modérément", "Fortement"],
        index=0,
        help="Impact des saisons sur votre activité"
    )
    
    if marche_data['saisonnalite'] != "Non":
        marche_data['periodes_fortes'] = st.multiselect(
            "Périodes de forte activité",
            ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
             "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
            help="Mois où votre activité est la plus intense"
        )
    
    # Sauvegarde
    if st.button("Sauvegarder l'analyse de marché"):
        sauvegarder_donnees_session('analyse_marche', marche_data)
        st.success("Analyse de marché sauvegardée!")
        st.rerun()
    
    return marche_data

def obtenir_business_model(donnees_collectees: Dict[str, Any], template_nom: str = "COPA TRANSFORME") -> str:
    """
    Génère le business model basé sur les données collectées
    
    Args:
        donnees_collectees (dict): Toutes les données collectées
        template_nom (str): Template à utiliser
    
    Returns:
        str: Business model généré
    """
    from services.ai import generer_business_model_canvas
    from templates import get_metaprompt
    
    metaprompt = get_metaprompt(template_nom)
    
    return generer_business_model_canvas(
        persona_data=donnees_collectees.get('persona_data', {}),
        marche_data=donnees_collectees.get('analyse_marche', {}),
        concurrence_data=donnees_collectees.get('concurrence', {}),
        facteurs_limitants=donnees_collectees.get('facteurs_limitants_data', {}),
        metaprompt=metaprompt,
        secteur=donnees_collectees.get('persona_data', {}).get('secteur_activite', ''),
        type_entreprise=donnees_collectees.get('type_entreprise', 'PME')
    )

def exporter_donnees_business() -> Dict[str, Any]:
    """
    Exporte toutes les données business collectées
    
    Returns:
        dict: Données exportées
    """
    donnees_export = {}
    
    # Données principales
    cles_principales = [
        'nom_entreprise', 'secteur_activite', 'type_entreprise', 'localisation',
        'template_selectionne', 'persona_data', 'analyse_marche', 'concurrence',
        'facteurs_limitants_data', 'problem_tree_data', 'business_model_precedent'
    ]
    
    for cle in cles_principales:
        donnees_export[cle] = recuperer_donnees_session(cle, {})
    
    # Métadonnées
    donnees_export['export_timestamp'] = datetime.now().isoformat()
    donnees_export['version'] = recuperer_donnees_session('version', '1.0')
    
    return donnees_export

def importer_donnees_business(donnees: Dict[str, Any]) -> bool:
    """
    Importe des données business
    
    Args:
        donnees (dict): Données à importer
    
    Returns:
        bool: Succès de l'importation
    """
    try:
        for cle, valeur in donnees.items():
            if cle != 'export_timestamp':  # Ne pas importer le timestamp d'export
                sauvegarder_donnees_session(cle, valeur)
        
        return True
    except Exception as e:
        st.error(f"Erreur lors de l'importation : {str(e)}")
        return False

def reinitialiser_donnees_business():
    """Remet à zéro toutes les données business"""
    cles_a_reinitialiser = [
        'persona_data', 'analyse_marche', 'concurrence',
        'facteurs_limitants_data', 'problem_tree_data', 'business_model_precedent'
    ]
    
    for cle in cles_a_reinitialiser:
        st.session_state[cle] = {}
    
    st.session_state['derniere_modification'] = datetime.now().isoformat()

def get_donnees_consolidees() -> Dict[str, Any]:
    """
    Récupère toutes les données consolidées
    
    Returns:
        dict: Données consolidées
    """
    return {
        'donnees_generales': {
            'nom_entreprise': recuperer_donnees_session('nom_entreprise', ''),
            'secteur_activite': recuperer_donnees_session('secteur_activite', ''),
            'type_entreprise': recuperer_donnees_session('type_entreprise', 'PME'),
            'localisation': recuperer_donnees_session('localisation', ''),
            'template_selectionne': recuperer_donnees_session('template_selectionne', 'COPA TRANSFORME')
        },
        'donnees_business': {
            'persona': recuperer_donnees_session('persona_data', {}),
            'marche': recuperer_donnees_session('analyse_marche', {}),
            'concurrence': recuperer_donnees_session('concurrence', {}),
            'facteurs_limitants': recuperer_donnees_session('facteurs_limitants_data', {}),
            'business_model': recuperer_donnees_session('business_model_precedent', '')
        },
        'metadonnees': {
            'derniere_modification': recuperer_donnees_session('derniere_modification', ''),
            'version': recuperer_donnees_session('version', '1.0'),
            'etapes_completees': recuperer_donnees_session('etapes_completees', [])
        }
    }