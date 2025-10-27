"""
Application principale MixBPM - Version refactorisée
Business Model et Business Plan Generator
"""

import streamlit as st
import os
import sys
from datetime import datetime, date
import pandas as pd
import numpy as np
from io import BytesIO

# Configuration de la page Streamlit
st.set_page_config(
    page_title="MixBPM - Business Model & Plan Generator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports des modules refactorisés
try:
    from services.business import init_session_state
    from ui.components import configurer_sidebar_principal, afficher_template_info
    from ui.pages import page_collecte_donnees, page_generer_business_model
    from templates import get_templates_list
    
    # Import des pages financières de base (version simplifiée)
    from ui.pages.pages_financieres_base import (
        page_informations_generales, page_besoins_demarrage, page_financement,
        page_charges_fixes, page_chiffre_affaires, page_charges_variables,
        page_fonds_roulement, page_salaires, page_rentabilite, page_tresorerie,
        page_generation_business_plan
    )
    
    # Import des nouvelles pages refactorisées
    from ui.pages.recapitulatif import page_recapitulatif
    from ui.pages.investissements_financements import page_investissements_et_financements
    from ui.pages.detail_amortissements import page_detail_amortissements
    from ui.pages.generation_business_plan_complete import page_generation_business_plan_integree
    
except ImportError as e:
    st.error(f"Erreur d'importation : {str(e)}")
    st.info("Vérifiez que tous les modules sont correctement installés et que les chemins d'importation sont corrects.")
    st.stop()

def main():
    """Fonction principale de l'application"""
    
    # Initialisation du session state
    init_session_state()
    
    # Configuration de la sidebar principale
    configurer_sidebar_principal()
    
    # Affichage du titre principal avec le template sélectionné
    template_actuel = st.session_state.get('template_selectionne', 'COPA TRANSFORME')
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title('🎯 MixBPM - Business Model & Plan Generator')
        st.markdown(f"*Powered by {template_actuel}*")
    
    with col2:
        # Indicateur de statut
        templates_disponibles = get_templates_list()
        if len(templates_disponibles) > 1:
            st.success(f"✅ {len(templates_disponibles)} templates disponibles")
        
        # Nom d'entreprise dans l'en-tête
        nom_entreprise = st.session_state.get('nom_entreprise', '')
        if nom_entreprise:
            st.info(f"🏢 **{nom_entreprise}**")
    
    # Vérifications préliminaires
    if not st.session_state.get('nom_entreprise'):
        st.warning("⚠️ Veuillez configurer le nom de votre entreprise dans la sidebar pour commencer.")
    
    # Menu principal avec onglets
    create_main_navigation()

def create_main_navigation():
    """Crée la navigation principale de l'application"""
    
    # Définition des onglets avec les nouvelles pages refactorisées
    business_model_tabs = [
        "🎨 Créativité & Business Model",
        "🎯 Générer Business Model Final",
    ]
    
    financial_tabs = [
        "ℹ️ Informations Générales", 
        "💰 Besoins de Démarrage", 
        "🏦 Financement",
        "📋 Charges Fixes", 
        "📈 Chiffre d'Affaires", 
        "📊 Charges Variables",
        "💼 Fonds de Roulement", 
        "👥 Salaires", 
        "📊 Rentabilité", 
        "💰 Trésorerie",
        "📊 Récapitulatif Complet",
        "💼 Investissements & Financements",
        "📋 Détail Amortissements"
    ]
    
    final_tabs = [
        "📄 Génération Business Plan",
        "🎯 Business Plan Complet (Nouveau)"
    ]
    
    # Combinaison de tous les onglets
    all_tabs = business_model_tabs + financial_tabs + final_tabs
    
    # Création des onglets
    tabs = st.tabs(all_tabs)
    
    # Mapping des nouvelles pages refactorisées
    new_pages = {
        0: page_collecte_donnees,           # Créativité & Stratégie (contient Arbre à Problème + navigation)
        1: page_generer_business_model,     # Générer Business Model (amélioration IA)
    }
    
    # Mapping des pages existantes et nouvelles
    existing_pages = {
        2: page_informations_generales,     # Informations Générales
        3: page_besoins_demarrage,         # Besoins de Démarrage
        4: page_financement,               # Financement
        5: page_charges_fixes,             # Charges Fixes
        6: page_chiffre_affaires,          # Chiffre d'Affaires
        7: page_charges_variables,         # Charges Variables
        8: page_fonds_roulement,           # Fonds de Roulement
        9: page_salaires,                  # Salaires
        10: page_rentabilite,              # Rentabilité
        11: page_tresorerie,               # Trésorerie
        12: page_recapitulatif,            # Récapitulatif Complet - NOUVEAU
        13: page_investissements_et_financements,  # Investissements & Financements - NOUVEAU
        14: page_detail_amortissements,    # Détail Amortissements - NOUVEAU
        15: page_generation_business_plan,  # Génération Business Plan
        16: page_generation_business_plan_integree,  # Business Plan Complet - NOUVEAU
    }
    
    # Affichage des pages dans leurs onglets respectifs
    for i, tab in enumerate(tabs):
        with tab:
            try:
                # Pages refactorisées
                if i in new_pages:
                    new_pages[i]()
                # Pages existantes
                elif i in existing_pages:
                    # Indication pour les nouvelles pages refactorisées
                    if i in [12, 13, 14, 16]:  # Nouvelles pages
                        with st.expander("✨ Nouvelle fonctionnalité", expanded=False):
                            if i == 16:
                                st.success("🎯 **Business Plan Complet** - Nouvelle version qui intègre automatiquement tous les tableaux financiers dans le plan d'affaires généré!")
                            else:
                                st.success("Cette page a été nouvellement développée dans l'architecture refactorisée.")
                    # Ajout d'un indicateur pour les pages à migrer
                    elif i >= 2 and i <= 11:  # Pages financières existantes
                        with st.expander("ℹ️ Info de migration", expanded=False):
                            st.info("Cette page utilise encore l'ancienne architecture. La migration vers la nouvelle structure est prévue.")
                    
                    existing_pages[i]()
                else:
                    st.error(f"Page non trouvée pour l'onglet {i}")
                    
            except Exception as e:
                st.error(f"Erreur lors du chargement de la page : {str(e)}")
                st.info("Veuillez rafraîchir la page ou contacter le support technique.")

def afficher_sidebar_info():
    """Affiche des informations complémentaires dans la sidebar"""
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Progression")
    
    # Calcul de la progression basé sur les données complétées
    etapes_completees = []
    
    if st.session_state.get('persona_data'):
        etapes_completees.append("Persona")
    if st.session_state.get('analyse_marche'):
        etapes_completees.append("Analyse Marché")
    if st.session_state.get('business_model_precedent'):
        etapes_completees.append("Business Model")
    if st.session_state.get('export_data_investissements'):
        etapes_completees.append("Données Financières")
    
    progression = len(etapes_completees) / 4  # 4 étapes principales
    st.sidebar.progress(progression)
    st.sidebar.markdown(f"{len(etapes_completees)}/4 sections complétées")
    
    # Affichage des étapes complétées
    for etape in etapes_completees:
        st.sidebar.markdown(f"✅ {etape}")
    
    # Version et informations
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Informations")
    st.sidebar.markdown("**Version:** 2.0 (Refactorisée)")
    st.sidebar.markdown("**Dernière mise à jour:** " + datetime.now().strftime("%d/%m/%Y"))
    
    # Template actuel
    template_actuel = st.session_state.get('template_selectionne', 'COPA TRANSFORME')
    st.sidebar.markdown(f"**Template actuel:** {template_actuel}")

def handle_errors():
    """Gestion globale des erreurs"""
    try:
        main()
        afficher_sidebar_info()
    except Exception as e:
        st.error("🚨 Une erreur inattendue s'est produite")
        st.error(f"Détails de l'erreur : {str(e)}")
        
        with st.expander("🔧 Informations de débogage"):
            st.code(f"""
            Erreur: {str(e)}
            Type: {type(e).__name__}
            
            État du session:
            - Template: {st.session_state.get('template_selectionne', 'Non défini')}
            - Entreprise: {st.session_state.get('nom_entreprise', 'Non définie')}
            - Secteur: {st.session_state.get('secteur_activite', 'Non défini')}
            """)
        
        st.info("💡 Essayez de rafraîchir la page ou de redémarrer l'application.")
        
        # Option de réinitialisation d'urgence
        if st.button("🔄 Réinitialiser l'application"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Point d'entrée de l'application
if __name__ == "__main__":
    # Gestion des erreurs globales
    handle_errors()