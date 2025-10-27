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
    
    # Onglets principaux simplifiés
    main_tabs = [
        "ℹ️ Informations Générales",
        "🎨 Business Model", 
        "💰 Financier",
        "📄 Génération Business Plan"
    ]
    
    # Création des onglets principaux
    main_tabs_ui = st.tabs(main_tabs)
    
    # 1. Informations Générales (premier onglet)
    with main_tabs_ui[0]:
        page_informations_generales()
    
    # 2. Business Model (avec sous-onglets incluant analyse de marché)
    with main_tabs_ui[1]:
        business_model_subtabs = [
            "📊 Analyse de Marché",
            "🎨 Créativité & Business Model",
            "🎯 Business Model Final"
        ]
        
        bm_tabs = st.tabs(business_model_subtabs)
        
        # Analyse de Marché (combine marché + concurrence)
        with bm_tabs[0]:
            analyse_marche_subtabs = [
                "🏪 Analyse du Marché",
                "⚔️ Analyse de la Concurrence"
            ]
            
            market_tabs = st.tabs(analyse_marche_subtabs)
            
            with market_tabs[0]:
                try:
                    from ui.pages import afficher_analyse_marche
                    afficher_analyse_marche()
                except Exception as e:
                    st.error(f"Fonction d'analyse de marché non encore implémentée : {str(e)}")
                    st.info("Cette section sera disponible prochainement")
            
            with market_tabs[1]:
                try:
                    from ui.pages import afficher_analyse_concurrence
                    afficher_analyse_concurrence()
                except Exception as e:
                    st.error(f"Fonction d'analyse de concurrence non encore implémentée : {str(e)}")
                    st.info("Cette section sera disponible prochainement")
        
        # Créativité & Business Model
        with bm_tabs[1]:
            try:
                page_collecte_donnees()
            except Exception as e:
                st.error(f"Erreur lors du chargement de la page : {str(e)}")
        
        # Business Model Final
        with bm_tabs[2]:
            try:
                page_generer_business_model()
            except Exception as e:
                st.error(f"Erreur lors du chargement de la page : {str(e)}")
    
    # 3. Financier (avec sous-onglets pour tous les éléments financiers)
    with main_tabs_ui[2]:
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

    # 4. Génération Business Plan
    with main_tabs_ui[3]:
        business_plan_subtabs = [
            "📄 Génération Business Plan",
            "🎯 Business Plan Complet (Nouveau)"
        ]
        
        bp_tabs = st.tabs(business_plan_subtabs)
        
        with bp_tabs[0]:
            try:
                page_generation_business_plan()
            except Exception as e:
                st.error(f"Erreur lors du chargement de la page : {str(e)}")
        
        with bp_tabs[1]:
            try:
                with st.expander("✨ Nouvelle fonctionnalité", expanded=False):
                    st.success("🎯 **Business Plan Complet** - Nouvelle version qui intègre automatiquement tous les tableaux financiers dans le plan d'affaires généré!")
                page_generation_business_plan_integree()
            except Exception as e:
                st.error(f"Erreur lors du chargement de la page : {str(e)}")

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