"""
Configuration et widgets communs pour l'interface utilisateur
"""

import streamlit as st
from typing import Dict, List, Any, Optional
from templates import get_templates_list, get_secteurs
from utils.token_utils import (
    initialiser_compteur_tokens, 
    obtenir_statistiques_tokens, 
    configurer_limite_tokens,
    reinitialiser_compteur,
    formater_nombre_tokens,
    obtenir_pourcentage_utilisation
)

def configurer_sidebar_principal():
    """Configure la sidebar principale avec les paramètres globaux"""
    
    st.sidebar.header("Configuration Initiale")
    
    # Sélection du template
    templates_disponibles = get_templates_list()
    template_actuel = st.session_state.get('template_selectionne', 'COPA TRANSFORME')
    
    template_selectionne = st.sidebar.selectbox(
        "Sélectionnez votre template",
        templates_disponibles,
        index=templates_disponibles.index(template_actuel) if template_actuel in templates_disponibles else 0,
        key="template_selection_sidebar",
        help="Choisissez le template adapté à votre organisation ou contexte"
    )
    
    # Sauvegarder la sélection
    if template_selectionne != st.session_state.get('template_selectionne'):
        st.session_state['template_selectionne'] = template_selectionne
        st.rerun()
    
    # Type d'entreprise
    type_entreprise = st.sidebar.selectbox(
        "Type d'entreprise", 
        ["PME", "Startup"], 
        index=["PME", "Startup"].index(st.session_state.get('type_entreprise', 'PME')),
        key="type_entreprise_sidebar"
    )
    st.session_state['type_entreprise'] = type_entreprise
    
    # Secteur d'activité basé sur le template sélectionné
    secteurs = get_secteurs(template_selectionne)
    secteur_actuel = st.session_state.get('secteur_activite', secteurs[0] if secteurs else '')
    
    secteur_activite = st.sidebar.selectbox(
        "Secteur d'activité",
        secteurs,
        index=secteurs.index(secteur_actuel) if secteur_actuel in secteurs else 0,
        key="secteur_activite_sidebar",
        help="Secteurs prioritaires selon le template sélectionné"
    )
    st.session_state['secteur_activite'] = secteur_activite
    
    # Nom de l'entreprise
    nom_entreprise = st.sidebar.text_input(
        "Nom de l'entreprise",
        value=st.session_state.get('nom_entreprise', ''),
        key="nom_entreprise_sidebar"
    )
    st.session_state['nom_entreprise'] = nom_entreprise
    
    # Localisation
    localisation = st.sidebar.selectbox(
        "Localisation principale",
        [
            "Kinshasa", "Lubumbashi", "Goma", "Mbuji-Mayi",
            "Kisangani", "Bukavu", "Matadi", "Kolwezi",
            "Autre ville RDC"
        ],
        index=0,
        key="localisation_sidebar",
        help="Ville principale d'implantation"
    )
    st.session_state['localisation'] = localisation
    
    # Avertissements si données manquantes
    if not nom_entreprise:
        st.sidebar.warning("⚠️ Veuillez entrer le nom de votre entreprise")
    
    if not secteur_activite:
        st.sidebar.warning("⚠️ Veuillez sélectionner votre secteur d'activité")
    
    # Informations sur le template sélectionné
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Template actuel:** {template_selectionne}")
    
    # Descriptions des templates
    descriptions = {
        "COPA TRANSFORME": "🌾 Transformation agricole et entrepreneuriat rural",
        "Virunga": "🌿 Conservation environnementale et développement durable",
        "IP Femme": "👩‍💼 Autonomisation économique des femmes"
    }
    
    if template_selectionne in descriptions:
        st.sidebar.info(descriptions[template_selectionne])
    
    # Affichage du compteur de tokens
    afficher_compteur_tokens()

def afficher_compteur_tokens():
    """Affiche le compteur de tokens dynamique dans la sidebar"""
    
    # Initialiser si nécessaire
    initialiser_compteur_tokens()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔢 Gestion des Tokens")
    
    # Configuration de la limite
    with st.sidebar.expander("⚙️ Configuration", expanded=False):
        
        # Modèle OpenAI
        modele_actuel = st.session_state.get('token_usage', {}).get('model_used', 'gpt-4')
        modele_selectionne = st.selectbox(
            "Modèle OpenAI",
            ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
            index=["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"].index(modele_actuel),
            key="modele_openai_sidebar"
        )
        
        # Activer/désactiver la limite
        limite_activee = st.checkbox(
            "Activer la limite de tokens",
            value=st.session_state.get('token_usage', {}).get('limit_enabled', True),
            key="limite_tokens_activee"
        )
        
        # Configuration de la limite
        if limite_activee:
            limite_actuelle = st.session_state.get('token_usage', {}).get('user_limit', 4096)
            nouvelle_limite = st.number_input(
                "Limite de tokens",
                min_value=100,
                max_value=100000,
                value=limite_actuelle,
                step=500,
                key="limite_tokens_input",
                help="Limite totale de tokens pour cette session"
            )
            
            if nouvelle_limite != limite_actuelle:
                configurer_limite_tokens(nouvelle_limite, limite_activee)
        else:
            configurer_limite_tokens(0, False)
        
        # Bouton de réinitialisation
        if st.button("🔄 Réinitialiser compteur", key="reset_tokens"):
            reinitialiser_compteur()
            st.rerun()
    
    # Obtenir les statistiques
    stats = obtenir_statistiques_tokens()
    
    # Affichage principal des statistiques
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        st.metric(
            "Total Tokens",
            formater_nombre_tokens(stats['total_tokens']),
            help="Tokens envoyés + reçus"
        )
    
    with col2:
        st.metric(
            "Coût ($)",
            f"${stats['total_cost']:.4f}",
            help="Coût total estimé"
        )
    
    # Barre de progression si limite activée
    if stats['limit_enabled'] and stats['user_limit'] > 0:
        pourcentage = obtenir_pourcentage_utilisation()
        
        # Couleur selon le pourcentage
        if pourcentage < 50:
            couleur = "normal"
        elif pourcentage < 80:
            couleur = "⚠️"
        else:
            couleur = "🔴"
        
        st.sidebar.progress(
            pourcentage / 100,
            text=f"{couleur} {pourcentage:.1f}% utilisé"
        )
        
        # Tokens restants
        tokens_restants = stats['user_limit'] - stats['total_tokens']
        if tokens_restants <= 0:
            st.sidebar.error("❌ Limite atteinte !")
        elif tokens_restants < 500:
            st.sidebar.warning(f"⚠️ {formater_nombre_tokens(tokens_restants)} restants")
        else:
            st.sidebar.info(f"✅ {formater_nombre_tokens(tokens_restants)} restants")
    
    # Détails en petite taille
    st.sidebar.markdown(
        f"""
        <small>
        📤 Envoyés: {formater_nombre_tokens(stats['input_tokens'])} | 
        📥 Reçus: {formater_nombre_tokens(stats['output_tokens'])}<br>
        🔄 Requêtes: {stats['requests_count']} | 
        ⏱️ Session: {stats['session_duration']}<br>
        🤖 Modèle: {stats['model_used']}
        </small>
        """,
        unsafe_allow_html=True
    )

def afficher_indicateur_progression(etapes_completees: List[str], total_etapes: int = 11):
    """
    Affiche un indicateur de progression
    
    Args:
        etapes_completees (list): Liste des étapes complétées
        total_etapes (int): Nombre total d'étapes
    """
    progression = len(etapes_completees) / total_etapes
    
    st.sidebar.markdown("### 📊 Progression")
    st.sidebar.progress(progression)
    st.sidebar.markdown(f"{len(etapes_completees)}/{total_etapes} étapes complétées")
    
    if len(etapes_completees) > 0:
        st.sidebar.markdown("**Étapes terminées:**")
        for etape in etapes_completees:
            st.sidebar.markdown(f"✅ {etape}")

def widget_montant_devise(
    label: str, 
    key: str, 
    valeur_defaut: float = 0.0,
    devise: str = "USD",
    aide: str = "",
    min_value: float = 0.0,
    max_value: float = 999999999.0
) -> float:
    """
    Widget pour saisir un montant avec devise
    
    Args:
        label (str): Libellé du champ
        key (str): Clé unique pour Streamlit
        valeur_defaut (float): Valeur par défaut
        devise (str): Code de la devise
        aide (str): Texte d'aide
        min_value (float): Valeur minimale
        max_value (float): Valeur maximale
    
    Returns:
        float: Montant saisi
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        montant = st.number_input(
            label,
            min_value=min_value,
            max_value=max_value,
            value=valeur_defaut,
            step=0.01,
            key=key,
            help=aide
        )
    
    with col2:
        st.markdown(f"**{devise}**")
    
    return montant

def widget_pourcentage(
    label: str,
    key: str,
    valeur_defaut: float = 0.0,
    aide: str = "",
    min_value: float = 0.0,
    max_value: float = 100.0
) -> float:
    """
    Widget pour saisir un pourcentage
    
    Args:
        label (str): Libellé du champ
        key (str): Clé unique
        valeur_defaut (float): Valeur par défaut
        aide (str): Texte d'aide
        min_value (float): Valeur minimale
        max_value (float): Valeur maximale
    
    Returns:
        float: Pourcentage saisi
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        pourcentage = st.number_input(
            label,
            min_value=min_value,
            max_value=max_value,
            value=valeur_defaut,
            step=0.1,
            key=key,
            help=aide
        )
    
    with col2:
        st.markdown("**%**")
    
    return pourcentage

def afficher_section_aide(titre: str, contenu: str, type_alerte: str = "info"):
    """
    Affiche une section d'aide contextuelle
    
    Args:
        titre (str): Titre de l'aide
        contenu (str): Contenu de l'aide
        type_alerte (str): Type d'alerte ('info', 'success', 'warning', 'error')
    """
    with st.expander(f"ℹ️ {titre}"):
        if type_alerte == "info":
            st.info(contenu)
        elif type_alerte == "success":
            st.success(contenu)
        elif type_alerte == "warning":
            st.warning(contenu)
        elif type_alerte == "error":
            st.error(contenu)
        else:
            st.markdown(contenu)

def afficher_resume_donnees(donnees: Dict[str, Any], titre: str = "Résumé des données"):
    """
    Affiche un résumé des données saisies
    
    Args:
        donnees (dict): Données à résumer
        titre (str): Titre du résumé
    """
    if not donnees:
        return
    
    with st.expander(f"📋 {titre}"):
        for cle, valeur in donnees.items():
            if valeur:  # N'afficher que les valeurs non vides
                if isinstance(valeur, dict):
                    st.markdown(f"**{cle}:**")
                    for sous_cle, sous_valeur in valeur.items():
                        if sous_valeur:
                            st.markdown(f"  - {sous_cle}: {sous_valeur}")
                elif isinstance(valeur, list):
                    st.markdown(f"**{cle}:** {', '.join(map(str, valeur))}")
                else:
                    st.markdown(f"**{cle}:** {valeur}")

def bouton_sauvegarder_avec_confirmation(
    label: str = "Sauvegarder",
    key: str = "btn_save",
    donnees: Dict[str, Any] = None,
    cle_session: str = "",
    message_succes: str = "Données sauvegardées avec succès!"
) -> bool:
    """
    Bouton de sauvegarde avec message de confirmation
    
    Args:
        label (str): Texte du bouton
        key (str): Clé unique
        donnees (dict): Données à sauvegarder
        cle_session (str): Clé pour le session state
        message_succes (str): Message de succès
    
    Returns:
        bool: True si sauvegarde effectuée
    """
    if st.button(label, key=key, type="primary"):
        if donnees and cle_session:
            from services.business import sauvegarder_donnees_session
            sauvegarder_donnees_session(cle_session, donnees)
        
        st.success(message_succes)
        st.balloons()
        return True
    
    return False

def widget_validation_donnees(donnees: Dict[str, Any], validateur_func) -> Dict[str, Any]:
    """
    Widget pour valider les données avec affichage des erreurs
    
    Args:
        donnees (dict): Données à valider
        validateur_func: Fonction de validation
    
    Returns:
        dict: Résultat de la validation
    """
    if not donnees:
        return {"valide": True, "erreurs": [], "avertissements": []}
    
    resultat = validateur_func(donnees)
    
    # Affichage des erreurs
    if resultat.get("erreurs"):
        st.error("❌ Erreurs détectées:")
        for erreur in resultat["erreurs"]:
            st.error(f"• {erreur}")
    
    # Affichage des avertissements
    if resultat.get("avertissements"):
        st.warning("⚠️ Avertissements:")
        for avertissement in resultat["avertissements"]:
            st.warning(f"• {avertissement}")
    
    # Statut global
    if resultat.get("valide"):
        st.success("✅ Données valides")
    
    return resultat

def afficher_template_info():
    """Affiche les informations sur le template sélectionné"""
    template_actuel = st.session_state.get('template_selectionne', 'COPA TRANSFORME')
    
    from templates import get_organisation_info
    org_info = get_organisation_info(template_actuel)
    
    st.markdown(f"""
    ### 📋 Template Actuel: {org_info['nom']}
    
    **Description:** {org_info['description']}
    
    **Zone d'intervention:** {org_info['zone_intervention']}
    
    **Approche:** {org_info['approche']}
    """)
    
    # Secteurs prioritaires
    if org_info.get('secteurs_prioritaires'):
        st.markdown("**Secteurs prioritaires:**")
        secteurs = org_info['secteurs_prioritaires']
        # Afficher en colonnes pour un meilleur rendu
        cols = st.columns(2)
        for i, secteur in enumerate(secteurs):
            with cols[i % 2]:
                st.markdown(f"• {secteur}")

def navigation_etapes():
    """Crée une navigation entre les étapes"""
    etapes = [
        "Configuration", "Collecte Données", "Business Model", 
        "Informations Générales", "Besoins Démarrage", "Financement",
        "Charges Fixes", "Chiffre d'Affaires", "Charges Variables",
        "Fonds de Roulement", "Salaires", "Rentabilité", 
        "Trésorerie", "Génération Business Plan"
    ]
    
    etape_actuelle = st.session_state.get('etape_actuelle', 0)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if etape_actuelle > 0:
            if st.button("⬅️ Précédent"):
                st.session_state['etape_actuelle'] = etape_actuelle - 1
                st.rerun()
    
    with col2:
        st.markdown(f"**Étape {etape_actuelle + 1}/{len(etapes)}:** {etapes[etape_actuelle]}")
        progression = (etape_actuelle + 1) / len(etapes)
        st.progress(progression)
    
    with col3:
        if etape_actuelle < len(etapes) - 1:
            if st.button("Suivant ➡️"):
                st.session_state['etape_actuelle'] = etape_actuelle + 1
                st.rerun()