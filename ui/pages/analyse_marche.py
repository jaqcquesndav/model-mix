"""
Pages d'analyse de marché et de concurrence
"""

import streamlit as st
from services.business import (
    collect_analyse_marche_pme, 
    recuperer_donnees_session, 
    sauvegarder_donnees_session
)

def afficher_analyse_marche():
    """Page d'analyse du marché"""
    
    st.title("🏪 Analyse du Marché")
    st.markdown("### Analysez votre marché cible et les opportunités")
    
    # Récupération du type d'entreprise
    persona_data = recuperer_donnees_session('persona_data', {})
    type_entreprise = persona_data.get('type_entreprise', 'PME')
    
    if type_entreprise == 'PME':
        afficher_analyse_marche_pme()
    else:
        afficher_analyse_marche_startup()

def afficher_analyse_marche_pme():
    """Analyse de marché pour PME"""
    
    st.info("💡 **Conseil :** Une bonne analyse de marché est essentielle pour comprendre vos clients et opportunités")
    
    with st.form("form_analyse_marche_pme"):
        analyse_marche = collect_analyse_marche_pme()
        submit_analyse_marche = st.form_submit_button("💾 Sauvegarder l'Analyse du Marché", type="primary")
    
    if submit_analyse_marche:
        sauvegarder_donnees_session('analyse_marche', analyse_marche)
        st.success("✅ Analyse du marché sauvegardée avec succès!")
        st.balloons()
    
    # Affichage du résumé si des données existent
    marche_existant = recuperer_donnees_session('analyse_marche', {})
    if marche_existant:
        afficher_resume_marche(marche_existant)

def afficher_analyse_marche_startup():
    """Analyse de marché pour Startup"""
    
    st.info("💡 **Conseil :** Pour une startup, l'analyse de marché doit être particulièrement rigoureuse")
    
    # Récupérer les données existantes
    marche_existant = recuperer_donnees_session('analyse_marche', {})
    
    marche_data = {}
    
    # Marché cible
    st.subheader("🎯 Votre marché cible")
    
    col1, col2 = st.columns(2)
    
    with col1:
        marche_data['taille_marche'] = st.selectbox(
            "Taille estimée de votre marché",
            ["Marché de niche (< 10K)", "Marché spécialisé (10K-100K)", 
             "Marché moyen (100K-1M)", "Marché large (1M-10M)", 
             "Marché de masse (> 10M)"],
            index=marche_existant.get('taille_marche_index', 0)
        )
    
    with col2:
        marche_data['croissance_marche'] = st.selectbox(
            "Tendance de croissance",
            ["Décroissant", "Stable", "Croissance lente", "Croissance rapide", "Croissance explosive"],
            index=marche_existant.get('croissance_marche_index', 2)
        )
    
    # Innovation et disruption
    st.subheader("🚀 Innovation et Disruption")
    
    marche_data['niveau_innovation'] = st.selectbox(
        "Niveau d'innovation de votre solution",
        ["Amélioration incrémentale", "Innovation significative", "Innovation disruptive", "Nouvelle catégorie"],
        index=marche_existant.get('niveau_innovation_index', 0)
    )
    
    marche_data['barriers_entry'] = st.multiselect(
        "Barrières à l'entrée identifiées",
        ["Réglementaires", "Technologiques", "Financières", "Réseau", "Marque", "Brevets", "Autres"],
        default=marche_existant.get('barriers_entry', [])
    )
    
    # Validation du marché
    st.subheader("✅ Validation du Marché")
    
    marche_data['validation_effectuee'] = st.checkbox(
        "Avez-vous validé votre idée auprès de clients potentiels ?",
        value=marche_existant.get('validation_effectuee', False)
    )
    
    if marche_data['validation_effectuee']:
        marche_data['methodes_validation'] = st.multiselect(
            "Méthodes de validation utilisées",
            ["Interviews clients", "Surveys", "MVP/Prototype", "Landing page", "Pré-commandes", "Focus groups"],
            default=marche_existant.get('methodes_validation', [])
        )
        
        marche_data['feedback_principal'] = st.text_area(
            "Principal feedback reçu",
            value=marche_existant.get('feedback_principal', ''),
            height=100
        )
    
    # Sauvegarde
    if st.button("💾 Sauvegarder l'Analyse du Marché", type="primary"):
        sauvegarder_donnees_session('analyse_marche', marche_data)
        st.success("✅ Analyse du marché sauvegardée avec succès!")
        st.balloons()
    
    # Affichage du résumé
    if marche_data or marche_existant:
        afficher_resume_marche(marche_data if marche_data else marche_existant)

def afficher_analyse_concurrence():
    """Page d'analyse de la concurrence"""
    
    st.title("⚔️ Analyse de la Concurrence")
    st.markdown("### Identifiez et analysez vos concurrents")
    
    st.info("💡 **Conseil :** Connaître sa concurrence permet de mieux se positionner et d'identifier des opportunités")
    
    # Récupération des données existantes
    concurrence_existante = recuperer_donnees_session('concurrence', {})
    
    concurrence_data = {}
    
    # Concurrents directs
    st.subheader("🏢 Concurrents Directs")
    st.caption("Entreprises offrant des produits/services similaires aux vôtres")
    
    concurrents_directs_text = st.text_area(
        "Listez vos principaux concurrents directs (un par ligne)",
        value="\n".join(concurrence_existante.get('concurrents_directs', [])),
        height=100,
        help="Ex: Entreprise A, Entreprise B, etc."
    )
    concurrence_data['concurrents_directs'] = [c.strip() for c in concurrents_directs_text.split('\n') if c.strip()]
    
    # Concurrents indirects
    st.subheader("🔄 Concurrents Indirects")
    st.caption("Solutions alternatives qui répondent au même besoin")
    
    concurrents_indirects_text = st.text_area(
        "Listez vos concurrents indirects (un par ligne)",
        value="\n".join(concurrence_existante.get('concurrents_indirects', [])),
        height=100,
        help="Ex: Solutions de substitution, autres méthodes"
    )
    concurrence_data['concurrents_indirects'] = [c.strip() for c in concurrents_indirects_text.split('\n') if c.strip()]
    
    # Analyse concurrentielle
    st.subheader("📊 Analyse Concurrentielle")
    
    col1, col2 = st.columns(2)
    
    with col1:
        concurrence_data['niveau_concurrence'] = st.selectbox(
            "Niveau de concurrence",
            ["Très faible", "Faible", "Modéré", "Élevé", "Très élevé"],
            index=concurrence_existante.get('niveau_concurrence_index', 2)
        )
        
        concurrence_data['facteurs_differentiation'] = st.multiselect(
            "Vos facteurs de différenciation",
            ["Prix", "Qualité", "Service client", "Innovation", "Rapidité", "Localisation", "Personnalisation", "Autre"],
            default=concurrence_existante.get('facteurs_differentiation', [])
        )
    
    with col2:
        concurrence_data['avantages_concurrentiels'] = st.text_area(
            "Vos principaux avantages concurrentiels",
            value=concurrence_existante.get('avantages_concurrentiels', ''),
            height=120,
            help="Qu'est-ce qui vous rend unique par rapport à la concurrence ?"
        )
    
    # Forces et faiblesses
    st.subheader("💪 Forces et Faiblesses vs Concurrence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        concurrence_data['forces_vs_concurrence'] = st.text_area(
            "🟢 Vos forces face à la concurrence",
            value=concurrence_existante.get('forces_vs_concurrence', ''),
            height=100
        )
    
    with col2:
        concurrence_data['faiblesses_vs_concurrence'] = st.text_area(
            "🔴 Vos faiblesses face à la concurrence",
            value=concurrence_existante.get('faiblesses_vs_concurrence', ''),
            height=100
        )
    
    # Stratégie concurrentielle
    st.subheader("🎯 Stratégie Concurrentielle")
    
    concurrence_data['strategie_positionnement'] = st.selectbox(
        "Votre stratégie de positionnement",
        ["Leader en prix", "Différenciation premium", "Niche spécialisée", "Suiveur/imitateur", "Challenger disruptif"],
        index=concurrence_existante.get('strategie_positionnement_index', 2)
    )
    
    concurrence_data['reponse_concurrence'] = st.text_area(
        "Comment comptez-vous répondre à la concurrence ?",
        value=concurrence_existante.get('reponse_concurrence', ''),
        height=100,
        help="Votre plan pour faire face à la pression concurrentielle"
    )
    
    # Sauvegarde
    if st.button("💾 Sauvegarder l'Analyse de Concurrence", type="primary"):
        sauvegarder_donnees_session('concurrence', concurrence_data)
        st.success("✅ Analyse de concurrence sauvegardée avec succès!")
        st.balloons()
    
    # Affichage du résumé
    if concurrence_data or concurrence_existante:
        afficher_resume_concurrence(concurrence_data if concurrence_data else concurrence_existante)

def afficher_resume_marche(data):
    """Affiche un résumé de l'analyse de marché"""
    
    with st.expander("📋 Résumé de votre analyse de marché", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            if 'taille_marche' in data:
                st.metric("Taille du marché", data['taille_marche'])
            if 'croissance_marche' in data:
                st.metric("Croissance", data['croissance_marche'])
        
        with col2:
            if 'segments_clients' in data:
                st.write("**Segments clients:**")
                for segment in data['segments_clients'][:3]:  # Limite à 3
                    st.write(f"• {segment}")

def afficher_resume_concurrence(data):
    """Affiche un résumé de l'analyse de concurrence"""
    
    with st.expander("📋 Résumé de votre analyse de concurrence", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            if 'niveau_concurrence' in data:
                st.metric("Niveau de concurrence", data['niveau_concurrence'])
            if 'concurrents_directs' in data and data['concurrents_directs']:
                st.write("**Concurrents directs:**")
                for concurrent in data['concurrents_directs'][:3]:  # Limite à 3
                    if concurrent.strip():
                        st.write(f"• {concurrent}")
        
        with col2:
            if 'facteurs_differentiation' in data:
                st.write("**Facteurs de différenciation:**")
                for facteur in data['facteurs_differentiation'][:3]:  # Limite à 3
                    st.write(f"• {facteur}")