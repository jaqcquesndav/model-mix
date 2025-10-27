"""
Page de créativité simplifiée - Arbre à Problème + Business Model
"""

import streamlit as st
from datetime import datetime
from services.business import sauvegarder_donnees_session
from ui.pages.business_model_initial import page_business_model_initial, page_arbre_probleme
from ui.pages.amelioration_business_model import page_amelioration_business_model

def page_collecte_donnees():
    """Page principale de créativité simplifiée"""
    
    st.title("🎨 Créativité & Stratégie")
    st.markdown("### Approche simplifiée et professionnelle")
    
    # Navigation par onglets
    tab1, tab2, tab3 = st.tabs([
        "🌳 Arbre à Problème",
        "🎯 Business Model Initial", 
        "🚀 Amélioration IA"
    ])
    
    with tab1:
        st.markdown("### Analysez la problématique que résout votre entreprise")
        page_arbre_probleme()
    
    with tab2:
        st.markdown("### Créez votre Business Model Canvas professionnel")
        page_business_model_initial()
    
    with tab3:
        st.markdown("### Améliorez votre modèle avec l'intelligence artificielle")
        page_amelioration_business_model()

# Anciennes fonctions supprimées - remplacées par Business Model Canvas