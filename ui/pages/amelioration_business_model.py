"""
Page d'amélioration du Business Model avec IA
Utilise la logique PME ou Startup selon le choix utilisateur
"""

import streamlit as st
from services.ai.content_generation import generate_section
from services.business import sauvegarder_donnees_session
from templates.template_manager import get_metaprompt
from utils.token_utils import count_tokens, formater_nombre_tokens

def page_amelioration_business_model():
    """Page d'amélioration du business model avec IA"""
    
    st.title("🚀 Amélioration Business Model avec IA")
    
    # Vérification des prérequis
    if not st.session_state.get('business_model_initial'):
        st.warning("⚠️ Veuillez d'abord créer votre Business Model initial dans l'onglet précédent.")
        return
    
    # Récupération du type d'entreprise
    type_entreprise = st.session_state.get('type_entreprise', 'PME')
    
    st.markdown(f"### 🎯 Amélioration selon la logique **{type_entreprise}**")
    
    # Affichage du business model actuel
    with st.expander("📋 Votre Business Model Actuel", expanded=False):
        display_current_business_model()
    
    # Sélection du type d'amélioration
    col1, col2 = st.columns([2, 1])
    
    with col1:
        amelioration_type = st.selectbox(
            "Quel aspect voulez-vous améliorer ?",
            [
                "🎯 Analyse complète du modèle",
                "💡 Propositions de valeur",
                "👥 Segments clients",
                "💰 Modèle de revenus",
                "🚀 Stratégie de croissance",
                "⚠️ Analyse des risques",
                "🔄 Pivot strategy"
            ]
        )
    
    with col2:
        # Paramètres IA
        creativite = st.slider(
            "Niveau de créativité",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Plus élevé = suggestions plus créatives"
        )
    
    # Zone d'amélioration
    st.markdown("---")
    
    if amelioration_type == "🎯 Analyse complète du modèle":
        page_analyse_complete(type_entreprise, creativite)
    elif amelioration_type == "💡 Propositions de valeur":
        page_amelioration_propositions_valeur(type_entreprise, creativite)
    elif amelioration_type == "👥 Segments clients":
        page_amelioration_segments_clients(type_entreprise, creativite)
    elif amelioration_type == "💰 Modèle de revenus":
        page_amelioration_revenus(type_entreprise, creativite)
    elif amelioration_type == "🚀 Stratégie de croissance":
        page_strategie_croissance(type_entreprise, creativite)
    elif amelioration_type == "⚠️ Analyse des risques":
        page_analyse_risques(type_entreprise, creativite)
    elif amelioration_type == "🔄 Pivot strategy":
        page_pivot_strategy(type_entreprise, creativite)

def page_analyse_complete(type_entreprise, creativite):
    """Analyse complète du business model"""
    
    st.subheader("🎯 Analyse Complète du Business Model")
    
    business_model = st.session_state['business_model_initial']
    
    # Contexte spécifique
    contexte_supplementaire = st.text_area(
        "Contexte spécifique ou contraintes particulières",
        height=100,
        placeholder="Ex: Marché local, budget limité, réglementation spécifique..."
    )
    
    if st.button("🔄 Analyser avec IA", type="primary"):
        with st.spinner("🤖 Analyse en cours..."):
            
            # Construction du prompt selon le type d'entreprise
            if type_entreprise == "PME":
                prompt = build_pme_analysis_prompt(business_model, contexte_supplementaire)
            else:  # Startup
                prompt = build_startup_analysis_prompt(business_model, contexte_supplementaire)
            
            # Génération IA
            try:
                resultat = generate_section(
                    section="analyse_business_model",
                    donnees_contexte={"business_model": business_model, "contexte": contexte_supplementaire},
                    system_message=prompt,
                    temperature=creativite
                )
                
                st.success("✅ Analyse terminée!")
                
                # Affichage du résultat
                st.markdown("### 📊 Résultats de l'Analyse")
                st.markdown(resultat)
                
                # Sauvegarde
                if st.button("💾 Sauvegarder cette analyse"):
                    st.session_state['analyse_business_model'] = {
                        'type': 'analyse_complete',
                        'resultat': resultat,
                        'type_entreprise': type_entreprise,
                        'date': st.session_state.get('date', '')
                    }
                    sauvegarder_donnees_session('analyse_business_model', st.session_state['analyse_business_model'])
                    st.success("✅ Analyse sauvegardée!")
                
            except Exception as e:
                st.error(f"❌ Erreur lors de l'analyse: {str(e)}")

def page_amelioration_propositions_valeur(type_entreprise, creativite):
    """Amélioration des propositions de valeur"""
    
    st.subheader("💡 Optimisation des Propositions de Valeur")
    
    business_model = st.session_state['business_model_initial']
    propositions_actuelles = business_model.get('propositions_valeur', '')
    
    st.markdown("**Propositions actuelles:**")
    st.info(propositions_actuelles)
    
    col1, col2 = st.columns(2)
    
    with col1:
        focus_client = st.multiselect(
            "Focus client prioritaire",
            ["Particuliers", "PME", "Grandes entreprises", "Administrations", "ONG"],
            help="Sur quels segments concentrer l'amélioration"
        )
    
    with col2:
        dimension_valeur = st.multiselect(
            "Dimensions de valeur à renforcer",
            ["Prix/Coût", "Qualité", "Innovation", "Service", "Rapidité", "Commodité"],
            help="Aspects de votre proposition à améliorer"
        )
    
    if st.button("🚀 Générer nouvelles propositions", type="primary"):
        with st.spinner("🤖 Génération en cours..."):
            
            prompt = build_value_proposition_prompt(
                type_entreprise, propositions_actuelles, focus_client, dimension_valeur
            )
            
            try:
                resultat = generate_section(
                    section="propositions_valeur",
                    donnees_contexte={
                        "propositions_actuelles": propositions_actuelles,
                        "focus_client": focus_client,
                        "dimension_valeur": dimension_valeur
                    },
                    system_message=prompt,
                    temperature=creativite
                )
                
                st.success("✅ Nouvelles propositions générées!")
                st.markdown("### 💡 Propositions de Valeur Améliorées")
                st.markdown(resultat)
                
                # Option de mise à jour
                if st.button("🔄 Appliquer ces améliorations"):
                    business_model['propositions_valeur'] = resultat
                    st.session_state['business_model_initial'] = business_model
                    st.success("✅ Business Model mis à jour!")
                    st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")

def page_strategie_croissance(type_entreprise, creativite):
    """Stratégies de croissance selon PME/Startup"""
    
    st.subheader("🚀 Stratégies de Croissance")
    
    business_model = st.session_state['business_model_initial']
    
    # Paramètres de croissance
    col1, col2, col3 = st.columns(3)
    
    with col1:
        horizon_temps = st.selectbox(
            "Horizon temporel",
            ["6 mois", "1 an", "2-3 ans", "5+ ans"]
        )
    
    with col2:
        budget_disponible = st.selectbox(
            "Budget disponible",
            ["Très limité", "Modéré", "Confortable", "Important"]
        )
    
    with col3:
        appetite_risque = st.selectbox(
            "Appétit pour le risque",
            ["Conservateur", "Modéré", "Aggressif"]
        )
    
    # Objectifs de croissance
    objectifs = st.multiselect(
        "Objectifs de croissance prioritaires",
        [
            "Augmenter le chiffre d'affaires",
            "Conquérir de nouveaux marchés",
            "Développer de nouveaux produits",
            "Améliorer la rentabilité",
            "Étendre géographiquement",
            "Digitaliser l'activité",
            "Créer des partenariats"
        ]
    )
    
    if st.button("📈 Générer stratégies de croissance", type="primary"):
        with st.spinner("🤖 Génération des stratégies..."):
            
            prompt = build_growth_strategy_prompt(
                type_entreprise, business_model, horizon_temps, 
                budget_disponible, appetite_risque, objectifs
            )
            
            try:
                resultat = generate_section(
                    section="strategie_croissance",
                    donnees_contexte={
                        "business_model": business_model,
                        "horizon_temps": horizon_temps,
                        "budget": budget_disponible,
                        "risque": appetite_risque,
                        "objectifs": objectifs
                    },
                    system_message=prompt,
                    temperature=creativite
                )
                
                st.success("✅ Stratégies générées!")
                st.markdown("### 📈 Plan de Croissance")
                st.markdown(resultat)
                
                # Sauvegarde
                if st.button("💾 Sauvegarder le plan de croissance"):
                    st.session_state['plan_croissance'] = {
                        'contenu': resultat,
                        'type_entreprise': type_entreprise,
                        'objectifs': objectifs,
                        'horizon': horizon_temps
                    }
                    sauvegarder_donnees_session('plan_croissance', st.session_state['plan_croissance'])
                    st.success("✅ Plan sauvegardé!")
                
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")

# Fonctions de construction des prompts

def build_pme_analysis_prompt(business_model, contexte):
    """Construit le prompt d'analyse pour PME"""
    return f"""
Tu es un consultant expert en développement de PME en Afrique et spécifiquement au Congo RDC.

Analyse ce Business Model Canvas d'une PME et fournis des recommandations pratiques et réalisables:

BUSINESS MODEL À ANALYSER:
{format_business_model_for_prompt(business_model)}

CONTEXTE SPÉCIFIQUE:
{contexte}

Analyse selon la logique PME:
1. **FORCES** - Identifie 3-4 points forts du modèle
2. **FAIBLESSES** - Signale 3-4 points à améliorer
3. **OPPORTUNITÉS** - Suggest 2-3 opportunités réalistes
4. **MENACES** - Identifie 2-3 risques principaux
5. **RECOMMANDATIONS PRATIQUES** - 5 actions concrètes et réalisables

Focus PME: Rentabilité, durabilité, croissance maîtrisée, marchés locaux, ressources limitées.

Réponds en français avec des recommandations actionnables.
"""

def build_startup_analysis_prompt(business_model, contexte):
    """Construit le prompt d'analyse pour Startup"""
    return f"""
Tu es un mentor expert en startups technologiques et innovation.

Analyse ce Business Model Canvas de startup et fournis des recommandations pour l'accélération:

BUSINESS MODEL À ANALYSER:
{format_business_model_for_prompt(business_model)}

CONTEXTE SPÉCIFIQUE:
{contexte}

Analyse selon la logique Startup:
1. **POTENTIEL DE SCALABILITÉ** - Évalue la capacité de passage à l'échelle
2. **INNOVATION & DISRUPTION** - Identifie le potentiel disruptif
3. **PRODUCT-MARKET FIT** - Analyse l'adéquation produit-marché
4. **STRATÉGIE DE FINANCEMENT** - Recommandations sur les levées de fonds
5. **PIVOT POTENTIAL** - Suggest des pivots possibles si nécessaire
6. **MÉTRIQUES CLÉS** - Identifie les KPIs critiques à suivre

Focus Startup: Croissance rapide, innovation, scalabilité, disruption, investissement.

Réponds en français avec une approche startup/tech.
"""

def build_value_proposition_prompt(type_entreprise, propositions_actuelles, focus_client, dimensions):
    """Construit le prompt pour améliorer les propositions de valeur"""
    
    logique = "PME (rentabilité, pragmatisme, marchés locaux)" if type_entreprise == "PME" else "Startup (innovation, disruption, scalabilité)"
    
    return f"""
Tu es un expert en proposition de valeur. 

Améliore ces propositions de valeur selon la logique {logique}:

PROPOSITIONS ACTUELLES:
{propositions_actuelles}

FOCUS CLIENT: {', '.join(focus_client)}
DIMENSIONS À RENFORCER: {', '.join(dimensions)}

Génère 3-5 propositions de valeur améliorées qui:
1. Sont claires et compréhensibles
2. Résolvent des problèmes concrets
3. Créent un avantage concurrentiel
4. Sont adaptées au contexte {type_entreprise}

Format: Liste à puces avec explications courtes.
Réponds en français.
"""

def build_growth_strategy_prompt(type_entreprise, business_model, horizon, budget, risque, objectifs):
    """Construit le prompt pour les stratégies de croissance"""
    
    return f"""
Tu es un stratège d'entreprise spécialisé en {type_entreprise}.

Développe une stratégie de croissance pour cette entreprise:

BUSINESS MODEL:
{format_business_model_for_prompt(business_model)}

PARAMÈTRES:
- Horizon: {horizon}
- Budget: {budget}
- Appétit risque: {risque}
- Objectifs: {', '.join(objectifs)}

Propose un plan de croissance avec:
1. **STRATÉGIES PRINCIPALES** (2-3 stratégies clés)
2. **ACTIONS CONCRÈTES** (5-7 actions prioritaires)
3. **TIMELINE** (répartition dans le temps)
4. **RESSOURCES NÉCESSAIRES** (humaines, financières, techniques)
5. **INDICATEURS DE SUCCÈS** (KPIs à suivre)
6. **RISQUES ET MITIGATION** (principaux risques et solutions)

Adapte à la logique {type_entreprise} et au contexte africain/RDC.
Réponds en français avec des recommandations actionnables.
"""

def format_business_model_for_prompt(business_model):
    """Formate le business model pour inclusion dans un prompt"""
    formatted = ""
    for key, value in business_model.items():
        if key not in ['date_creation', 'version'] and value:
            formatted += f"- {key.replace('_', ' ').title()}: {value[:200]}...\n"
    return formatted

def display_current_business_model():
    """Affiche le business model actuel de façon compacte"""
    business_model = st.session_state['business_model_initial']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**💡 Propositions de Valeur:**")
        st.write(business_model.get('propositions_valeur', 'Non défini')[:200] + "...")
        
        st.markdown("**👥 Segments Clients:**")
        st.write(business_model.get('segments_clients', 'Non défini')[:200] + "...")
    
    with col2:
        st.markdown("**💰 Sources de Revenus:**")
        st.write(business_model.get('sources_revenus', 'Non défini')[:200] + "...")
        
        st.markdown("**📢 Canaux:**")
        st.write(business_model.get('canaux_distribution', 'Non défini')[:200] + "...")

# Fonctions pour les autres types d'amélioration (à implémenter selon besoins)

def page_amelioration_segments_clients(type_entreprise, creativite):
    """Amélioration des segments clients"""
    st.info("🚧 Module segments clients en développement")

def page_amelioration_revenus(type_entreprise, creativite):
    """Amélioration du modèle de revenus"""
    st.info("🚧 Module revenus en développement")

def page_analyse_risques(type_entreprise, creativite):
    """Analyse des risques"""
    st.info("🚧 Module analyse risques en développement")

def page_pivot_strategy(type_entreprise, creativite):
    """Stratégies de pivot"""
    st.info("🚧 Module pivot strategy en développement")