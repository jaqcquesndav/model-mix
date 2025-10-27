"""
Pages d'analyse de marché et de concurrence - Version simplifiée
"""

import streamlit as st
import pandas as pd
from services.business import (
    recuperer_donnees_session, 
    sauvegarder_donnees_session
)

def afficher_analyse_marche():
    """Page d'analyse du marché simplifiée"""
    
    st.title("🏪 Analyse du Marché")
    st.markdown("### Analysez votre marché cible en quelques points clés")
    
    # Récupération des données existantes
    marche_existant = recuperer_donnees_session('analyse_marche', {})
    
    # Interface simplifiée
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Marché cible")
        
        taille_marche = st.selectbox(
            "Taille de votre marché",
            ["Niche (< 50K clients)", "Local (50K-200K)", "Régional (200K-1M)", "National (1M+)"],
            index=marche_existant.get('taille_marche_index', 0)
        )
        
        type_clients = st.selectbox(
            "Type de clients principaux",
            ["Particuliers (B2C)", "Entreprises (B2B)", "Administrations (B2G)", "Mixte"],
            index=marche_existant.get('type_clients_index', 0)
        )
        
        maturite_marche = st.selectbox(
            "Maturité du marché",
            ["Émergent", "En croissance", "Mature", "En déclin"],
            index=marche_existant.get('maturite_marche_index', 1)
        )
    
    with col2:
        st.subheader("🎯 Opportunités")
        
        saisonnalite = st.selectbox(
            "Saisonnalité",
            ["Pas de saisonnalité", "Légère saisonnalité", "Forte saisonnalité"],
            index=marche_existant.get('saisonnalite_index', 0)
        )
        
        tendances = st.multiselect(
            "Tendances favorables",
            ["Digitalisation", "Écologie", "Santé/Bien-être", "Économie locale", "Remote/Télétravail", "Autres"],
            default=marche_existant.get('tendances', [])
        )
        
        budget_moyen = st.selectbox(
            "Budget moyen par client",
            ["< 100$", "100$ - 500$", "500$ - 2000$", "2000$ - 10000$", "> 10000$"],
            index=marche_existant.get('budget_moyen_index', 1)
        )
    
    # Analyse des besoins clients
    st.subheader("💭 Besoins clients")
    besoin_principal = st.text_area(
        "Quel est le besoin principal que vous résolvez ?",
        value=marche_existant.get('besoin_principal', ''),
        height=80,
        placeholder="Ex: Gagner du temps, Réduire les coûts, Améliorer la qualité..."
    )
    
    # Sauvegarde
    marche_data = {
        'taille_marche': taille_marche,
        'taille_marche_index': ["Niche (< 50K clients)", "Local (50K-200K)", "Régional (200K-1M)", "National (1M+)"].index(taille_marche),
        'type_clients': type_clients,
        'type_clients_index': ["Particuliers (B2C)", "Entreprises (B2B)", "Administrations (B2G)", "Mixte"].index(type_clients),
        'maturite_marche': maturite_marche,
        'maturite_marche_index': ["Émergent", "En croissance", "Mature", "En déclin"].index(maturite_marche),
        'saisonnalite': saisonnalite,
        'saisonnalite_index': ["Pas de saisonnalité", "Légère saisonnalité", "Forte saisonnalité"].index(saisonnalite),
        'tendances': tendances,
        'budget_moyen': budget_moyen,
        'budget_moyen_index': ["< 100$", "100$ - 500$", "500$ - 2000$", "2000$ - 10000$", "> 10000$"].index(budget_moyen),
        'besoin_principal': besoin_principal
    }
    
    if st.button("💾 Sauvegarder l'Analyse du Marché", type="primary"):
        sauvegarder_donnees_session('analyse_marche', marche_data)
        st.success("✅ Analyse du marché sauvegardée !")
        st.rerun()

def afficher_analyse_concurrence():
    """Page d'analyse de la concurrence avec tableau croisé"""
    
    st.title("⚔️ Analyse de la Concurrence")
    st.markdown("### Tableau croisé des concurrents et critères d'analyse")
    
    # Récupération des données existantes
    concurrence_existante = recuperer_donnees_session('concurrence', {})
    
    # Section 1: Liste des concurrents
    st.subheader("1️⃣ Identification des concurrents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🏢 Concurrents directs**")
        concurrents_directs_text = st.text_area(
            "Listez vos concurrents directs (un par ligne)",
            value="\n".join(concurrence_existante.get('concurrents_directs', [])),
            height=100,
            key="directs"
        )
        concurrents_directs = [c.strip() for c in concurrents_directs_text.split('\n') if c.strip()]
    
    with col2:
        st.markdown("**🔄 Concurrents indirects**")
        concurrents_indirects_text = st.text_area(
            "Listez vos concurrents indirects (un par ligne)",
            value="\n".join(concurrence_existante.get('concurrents_indirects', [])),
            height=100,
            key="indirects"
        )
        concurrents_indirects = [c.strip() for c in concurrents_indirects_text.split('\n') if c.strip()]
    
    # Section 2: Tableau croisé d'analyse
    st.subheader("2️⃣ Tableau croisé d'analyse concurrentielle")
    
    # Critères d'analyse
    criteres = ["Prix", "Qualité", "Service Client", "Innovation", "Notoriété", "Présence Digitale"]
    
    # Combinaison de tous les concurrents
    tous_concurrents = concurrents_directs + concurrents_indirects
    if not tous_concurrents:
        tous_concurrents = ["Concurrent 1", "Concurrent 2", "Concurrent 3"]  # Exemples par défaut
    
    # Ajouter "Votre entreprise" en premier
    tous_concurrents = ["Votre entreprise"] + tous_concurrents
    
    st.info("💡 **Instructions :** Notez chaque concurrent de 1 (Très faible) à 5 (Excellent) pour chaque critère")
    
    # Création du tableau croisé
    tableau_data = {}
    
    # Récupérer les données existantes du tableau
    tableau_existant = concurrence_existante.get('tableau_concurrence', {})
    
    for concurrent in tous_concurrents[:6]:  # Limiter à 6 concurrents max
        tableau_data[concurrent] = {}
        
        st.markdown(f"**{concurrent}**")
        cols = st.columns(len(criteres))
        
        for i, critere in enumerate(criteres):
            with cols[i]:
                key = f"{concurrent}_{critere}"
                valeur_existante = tableau_existant.get(concurrent, {}).get(critere, 3)
                
                valeur = st.selectbox(
                    critere,
                    options=[1, 2, 3, 4, 5],
                    index=valeur_existante - 1,
                    key=key,
                    format_func=lambda x: f"{x} ⭐" if x <= 2 else f"{x} ⭐⭐" if x <= 3 else f"{x} ⭐⭐⭐" if x <= 4 else f"{x} ⭐⭐⭐⭐⭐"
                )
                tableau_data[concurrent][critere] = valeur
    
    # Section 3: Visualisation du tableau
    st.subheader("3️⃣ Tableau de comparaison")
    
    # Création du DataFrame pour affichage
    df_data = []
    for concurrent in tableau_data.keys():
        row = {"Concurrent": concurrent}
        for critere in criteres:
            note = tableau_data[concurrent].get(critere, 3)
            row[critere] = f"{note}/5 {'⭐' * note}"
        df_data.append(row)
    
    df = pd.DataFrame(df_data)
    
    # Affichage du tableau avec style
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Section 4: Analyse et conclusions
    st.subheader("4️⃣ Votre positionnement")
    
    col1, col2 = st.columns(2)
    
    with col1:
        forces = st.text_area(
            "💪 Vos forces principales",
            value=concurrence_existante.get('forces', ''),
            height=100,
            placeholder="Sur quels critères vous excellez..."
        )
    
    with col2:
        faiblesses = st.text_area(
            "🎯 Points d'amélioration",
            value=concurrence_existante.get('faiblesses', ''),
            height=100,
            placeholder="Sur quels critères progresser..."
        )
    
    strategie = st.selectbox(
        "🎪 Votre stratégie concurrentielle",
        ["Leader en prix", "Différenciation qualité", "Service premium", "Innovation", "Niche spécialisée"],
        index=concurrence_existante.get('strategie_index', 0)
    )
    
    # Sauvegarde complète
    concurrence_data = {
        'concurrents_directs': concurrents_directs,
        'concurrents_indirects': concurrents_indirects,
        'tableau_concurrence': tableau_data,
        'forces': forces,
        'faiblesses': faiblesses,
        'strategie': strategie,
        'strategie_index': ["Leader en prix", "Différenciation qualité", "Service premium", "Innovation", "Niche spécialisée"].index(strategie)
    }
    
    if st.button("💾 Sauvegarder l'Analyse de Concurrence", type="primary"):
        sauvegarder_donnees_session('concurrence', concurrence_data)
        st.success("✅ Analyse de concurrence sauvegardée !")
        st.rerun()
    
    # Section 5: Résumé graphique
    if tableau_data:
        afficher_resume_graphique(tableau_data, criteres)

def afficher_resume_graphique(tableau_data, criteres):
    """Affiche un résumé graphique de l'analyse concurrentielle"""
    
    with st.expander("📊 Résumé graphique", expanded=False):
        try:
            import plotly.graph_objects as go
            
            # Créer un graphique radar pour "Votre entreprise"
            if "Votre entreprise" in tableau_data:
                valeurs_entreprise = [tableau_data["Votre entreprise"].get(critere, 3) for critere in criteres]
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=valeurs_entreprise,
                    theta=criteres,
                    fill='toself',
                    name='Votre entreprise',
                    line_color='blue'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 5]
                        )),
                    showlegend=True,
                    title="Profil concurrentiel de votre entreprise"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
        except ImportError:
            # Fallback si plotly n'est pas disponible
            st.info("📊 Résumé des notes moyennes :")
            if "Votre entreprise" in tableau_data:
                for critere in criteres:
                    note = tableau_data["Votre entreprise"].get(critere, 3)
                    st.write(f"• {critere}: {note}/5 {'⭐' * note}")

# Fonctions de compatibilité (gardées pour éviter les erreurs d'import)
def afficher_analyse_marche_pme():
    """Redirections vers la version simplifiée"""
    afficher_analyse_marche()

def afficher_analyse_marche_startup():
    """Redirections vers la version simplifiée"""
    afficher_analyse_marche()

def afficher_resume_marche(data):
    """Résumé simplifié de l'analyse de marché"""
    pass

def afficher_resume_concurrence(data):
    """Résumé simplifié de l'analyse de concurrence"""
    pass