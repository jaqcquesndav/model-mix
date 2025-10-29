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
import openai
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de l'API OpenAI avec test de connectivité
from services.ai.content_generation import initialiser_openai, tester_connexion_openai, render_model_selector_sidebar

# Initialiser OpenAI et tester la connectivité
client_openai = initialiser_openai()
test_result = tester_connexion_openai()

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
    from templates import get_templates_list
    
    # Import des pages financières de base (version simplifiée)
    from ui.pages.pages_financieres_base import (
        page_informations_generales, page_besoins_demarrage, page_financement,
        page_charges_fixes, page_chiffre_affaires, page_charges_variables,
        page_fonds_roulement, page_salaires, page_rentabilite, page_tresorerie
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
    
    # Configuration du sidebar de sélection de modèle OpenAI
    render_model_selector_sidebar()
    
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
    
    # Onglets principaux restructurés
    main_tabs = [
        "ℹ️ Informations Générales",
        "📊 Analyse de Marché", 
        "🎨 Business Model", 
        "💰 Financier",
        "🎯 Business Plan Complet"
    ]
    
    # Création des onglets principaux
    main_tabs_ui = st.tabs(main_tabs)
    
    # 1. Informations Générales
    with main_tabs_ui[0]:
        page_informations_generales()
    
    # 2. Analyse de Marché (nouvel onglet principal)
    with main_tabs_ui[1]:
        analyse_marche_subtabs = [
            "� Arbre à Problème",
            "�🏪 Analyse du Marché",
            "⚔️ Analyse de la Concurrence"
        ]
        
        market_tabs = st.tabs(analyse_marche_subtabs)
        
        with market_tabs[0]:
            try:
                from ui.pages.business_model_initial import page_arbre_probleme
                page_arbre_probleme()
            except Exception as e:
                st.error(f"Erreur lors du chargement de l'arbre à problème : {str(e)}")
                st.info("Veuillez vérifier que le module arbre à problème est disponible")
        
        with market_tabs[1]:
            try:
                from ui.pages import afficher_analyse_marche
                afficher_analyse_marche()
            except Exception as e:
                st.error(f"Fonction d'analyse de marché non encore implémentée : {str(e)}")
                st.info("Cette section sera disponible prochainement")
        
        with market_tabs[2]:
            try:
                from ui.pages import afficher_analyse_concurrence
                afficher_analyse_concurrence()
            except Exception as e:
                st.error(f"Fonction d'analyse de concurrence non encore implémentée : {str(e)}")
                st.info("Cette section sera disponible prochainement")
    
    # 3. Business Model (simplifié, sans sous-onglets)
    with main_tabs_ui[2]:
        try:
            # Import de la page Business Model Initial directement
            from ui.pages.business_model_initial import page_business_model_initial
            page_business_model_initial()
        except Exception as e:
            st.error(f"Erreur lors du chargement du Business Model : {str(e)}")
            st.info("Veuillez vérifier que le module business_model_initial est disponible")
    
    # 4. Financier (avec sous-onglets pour tous les éléments financiers)
    with main_tabs_ui[3]:
        financial_subtabs = [
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
        
        fin_tabs = st.tabs(financial_subtabs)
        
        # Mapping des pages financières
        financial_pages = {
            0: page_besoins_demarrage,
            1: page_financement,
            2: page_charges_fixes,
            3: page_chiffre_affaires,
            4: page_charges_variables,
            5: page_fonds_roulement,
            6: page_salaires,
            7: page_rentabilite,
            8: page_tresorerie,
            9: page_recapitulatif,
            10: page_investissements_et_financements,
            11: page_detail_amortissements
        }
        
        # Affichage des pages financières
        for i, tab in enumerate(fin_tabs):
            with tab:
                try:
                    # Indication pour les nouvelles pages refactorisées
                    if i in [9, 10, 11]:  # Nouvelles pages
                        with st.expander("✨ Nouvelle fonctionnalité", expanded=False):
                            st.success("Cette page a été nouvellement développée dans l'architecture refactorisée.")
                    # Ajout d'un indicateur pour les pages à migrer
                    else:  # Pages financières existantes
                        with st.expander("ℹ️ Info de migration", expanded=False):
                            st.info("Cette page utilise encore l'ancienne architecture. La migration vers la nouvelle structure est prévue.")
                    
                    if i in financial_pages:
                        financial_pages[i]()
                    else:
                        st.error(f"Page financière non trouvée pour l'onglet {i}")
                        
                except Exception as e:
                    st.error(f"Erreur lors du chargement de la page financière : {str(e)}")
                    st.info("Veuillez rafraîchir la page ou contacter le support technique.")

    # 5. Business Plan Complet
    with main_tabs_ui[4]:
        try:
            with st.expander("✨ Nouvelle fonctionnalité", expanded=False):
                st.success("🎯 **Business Plan Complet** - Nouvelle version qui intègre automatiquement tous les tableaux financiers dans le plan d'affaires généré!")
            page_generation_business_plan_integree()
        except Exception as e:
            st.error(f"Erreur lors du chargement de la page : {str(e)}")

def handle_errors():
    """Gestion globale des erreurs"""
    try:
        main()
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