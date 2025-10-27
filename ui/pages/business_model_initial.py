"""
Page Business Model Initial - Version simplifiée et professionnelle
Remplace la collecte persona/marché/concurrence par les 9 blocs du Business Model Canvas
"""

import streamlit as st
import json
from datetime import datetime
from services.business import sauvegarder_donnees_session
from ui.components import afficher_template_info, bouton_sauvegarder_avec_confirmation

def page_business_model_initial():
    """Page pour créer ou importer un Business Model Canvas initial"""
    
    st.title("🎯 Business Model Initial")
    st.markdown("### Définissez votre modèle d'affaires selon les 9 blocs du Business Model Canvas")
    
    # Options d'import/création
    col1, col2 = st.columns([3, 1])
    
    with col1:
        option = st.radio(
            "Comment voulez-vous procéder ?",
            ["✍️ Remplir manuellement", "📄 Importer depuis un fichier"],
            horizontal=True
        )
    
    with col2:
        # Type d'entreprise pour l'amélioration IA
        type_entreprise = st.selectbox(
            "Type d'entreprise",
            ["PME", "Startup"],
            help="Détermine la logique d'amélioration IA qui suivra"
        )
        st.session_state['type_entreprise'] = type_entreprise
    
    if option == "📄 Importer depuis un fichier":
        page_import_business_model()
    else:
        page_creation_business_model_manuel()

def page_import_business_model():
    """Import d'un business model depuis un fichier"""
    
    st.subheader("📄 Import Business Model")
    
    uploaded_file = st.file_uploader(
        "Choisissez un fichier",
        type=['json', 'txt'],
        help="Formats supportés: JSON (Business Model Canvas), TXT (description libre)"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.type == "application/json":
                content = json.loads(uploaded_file.getvalue().decode("utf-8"))
                st.success("✅ Fichier JSON importé avec succès!")
                
                # Validation et mapping des données
                if validate_business_model_json(content):
                    st.session_state['business_model_initial'] = content
                    st.rerun()
                else:
                    st.error("❌ Structure JSON invalide. Utilisez le format Business Model Canvas standard.")
                    
            else:  # TXT
                content = uploaded_file.getvalue().decode("utf-8")
                st.success("✅ Fichier texte importé!")
                
                # Conversion texte libre en structure
                business_model_from_text = parse_text_to_business_model(content)
                st.session_state['business_model_initial'] = business_model_from_text
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Erreur lors de l'import: {str(e)}")
    
    # Template d'exemple pour téléchargement
    st.markdown("---")
    st.subheader("📋 Template d'exemple")
    
    template_json = get_business_model_template()
    
    st.download_button(
        label="📥 Télécharger template JSON",
        data=json.dumps(template_json, indent=2, ensure_ascii=False),
        file_name="business_model_template.json",
        mime="application/json"
    )
    
    with st.expander("👁️ Voir le template"):
        st.json(template_json)

def page_creation_business_model_manuel():
    """Création manuelle du business model selon les 9 blocs avec suggestions IA automatiques"""
    
    st.subheader("✍️ Business Model Canvas - 9 Blocs")
    st.markdown("Remplissez les 9 blocs de votre modèle d'affaires. L'IA vous suggère du contenu automatiquement basé sur vos informations.")
    
    # Initialisation et pré-remplissage automatique intelligent
    if 'business_model_initial' not in st.session_state:
        st.session_state['business_model_initial'] = get_empty_business_model()
        
    # Pré-remplissage automatique au premier chargement avec données disponibles
    auto_prefill_on_load()
    
    # Bouton de pré-remplissage IA amélioré
    col_ai, col_clear, col_info = st.columns([2, 1, 1])
    
    with col_ai:
        if st.button("🔄 Actualiser les suggestions IA", help="Met à jour les suggestions basées sur vos dernières données"):
            with st.spinner("🧠 L'IA actualise les suggestions..."):
                if prefill_with_ai(force_update=True):
                    st.success("✨ Suggestions mises à jour ! Modifiez-les selon vos besoins.")
                    st.rerun()
                else:
                    st.warning("ℹ️ Ajoutez plus d'informations (informations générales, arbre à problème, analyse de marché) pour de meilleures suggestions.")
        
        # Bouton de test pour forcer le pré-remplissage
        if st.button("🧪 Test Pré-remplissage", help="Force le pré-remplissage même avec des données minimales"):
            st.session_state['auto_prefill_done'] = False  # Reset le flag
            with st.spinner("🔧 Test du pré-remplissage..."):
                if prefill_with_ai():
                    st.success("✅ Test réussi ! Business model pré-rempli.")
                    st.rerun()
                else:
                    st.error("❌ Échec du test. Vérifiez les données d'entrée.")
        
        # Bouton de données de test
        if st.button("📋 Données de test", help="Ajoute des données minimales pour tester l'IA"):
            # Ajouter des données minimales pour tester
            st.session_state['nom_entreprise'] = "MonEntreprise Test"
            st.session_state['secteur_activite'] = "Commerce"
            st.session_state['arbre_probleme'] = {
                'probleme_central': 'Les clients ont du mal à trouver des produits de qualité',
                'solution': 'Boutique en ligne avec sélection curatée',
                'causes': 'Manque d\'information, prix élevés',
                'consequences': 'Perte de temps, frustration'
            }
            st.success("✅ Données de test ajoutées ! Essayez maintenant l'actualisation IA.")
            st.rerun()
    
    with col_clear:
        if st.button("🧹 Effacer tout", help="Remet à zéro tous les champs"):
            st.session_state['business_model_initial'] = get_empty_business_model()
            st.session_state['auto_prefill_done'] = False  # Permettre un nouveau auto-remplissage
            st.success("🗑️ Champs effacés !")
            st.rerun()
    
    with col_info:
        donnees_disponibles = get_available_data_summary()
        if donnees_disponibles:
            with st.expander("📊 Données IA", expanded=False):
                st.write(donnees_disponibles)
                st.caption("💡 Plus vous remplissez d'informations, meilleures sont les suggestions IA.")
    
    # Récupération des données existantes
    business_model = st.session_state.get('business_model_initial', get_empty_business_model())
    
    # Indicateur de suggestions IA actives
    has_ai_data = has_sufficient_data()
    ai_indicator = "🤖 " if has_ai_data else ""
    ai_help_suffix = " (Suggestions IA disponibles)" if has_ai_data else " (Complétez d'abord vos informations pour l'aide IA)"
    
    # Organisation en colonnes pour une meilleure présentation
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown(f"#### {ai_indicator}🤝 Partenaires Clés")
        business_model['partenaires_cles'] = st.text_area(
            "Qui sont vos partenaires stratégiques ?",
            value=business_model.get('partenaires_cles', ''),
            height=120,
            help=f"Fournisseurs clés, partenaires stratégiques, alliances...{ai_help_suffix}",
            placeholder="Ex: Fournisseurs matières premières, distributeurs, partenaires technologiques..." + (" [IA peut suggérer]" if has_ai_data else "")
        )
        
        st.markdown(f"#### {ai_indicator}🔧 Activités Clés")
        business_model['activites_cles'] = st.text_area(
            "Quelles sont vos activités principales ?",
            value=business_model.get('activites_cles', ''),
            height=120,
            help=f"Production, résolution de problèmes, plateforme/réseau...{ai_help_suffix}",
            placeholder="Ex: Production, marketing, R&D, logistique..." + (" [IA peut suggérer]" if has_ai_data else "")
        )
        
        st.markdown(f"#### {ai_indicator}🛠️ Ressources Clés")
        business_model['ressources_cles'] = st.text_area(
            "Quelles ressources sont essentielles ?",
            value=business_model.get('ressources_cles', ''),
            height=120,
            help=f"Physiques, intellectuelles, humaines, financières...{ai_help_suffix}",
            placeholder="Ex: Équipements, brevets, équipe qualifiée, capital..." + (" [IA peut suggérer]" if has_ai_data else "")
        )
    
    with col2:
        st.markdown(f"#### {ai_indicator}💡 Propositions de Valeur")
        business_model['propositions_valeur'] = st.text_area(
            "Quelle valeur créez-vous pour vos clients ?",
            value=business_model.get('propositions_valeur', ''),
            height=180,
            help=f"Produits/services qui créent de la valeur pour un segment client{ai_help_suffix}",
            placeholder="Ex: Résout le problème X, améliore la performance Y, réduit les coûts..." + (" [IA peut suggérer]" if has_ai_data else "")
        )
        
        st.markdown(f"#### {ai_indicator}🤝 Relations Clients")
        business_model['relations_clients'] = st.text_area(
            "Comment maintenez-vous vos relations clients ?",
            value=business_model.get('relations_clients', ''),
            height=120,
            help=f"Assistance personnelle, self-service, communautés...{ai_help_suffix}",
            placeholder="Ex: Service client personnalisé, assistance en ligne, communauté..." + (" [IA peut suggérer]" if has_ai_data else "")
        )
        
        st.markdown(f"#### {ai_indicator}📢 Canaux de Distribution")
        business_model['canaux_distribution'] = st.text_area(
            "Comment atteignez-vous vos clients ?",
            value=business_model.get('canaux_distribution', ''),
            height=120,
            help=f"Vente directe, partenaires, web, magasins...{ai_help_suffix}",
            placeholder="Ex: Boutique physique, site web, revendeurs, réseaux sociaux..." + (" [IA peut suggérer]" if has_ai_data else "")
        )
    
    with col3:
        st.markdown(f"#### {ai_indicator}👥 Segments Clients")
        business_model['segments_clients'] = st.text_area(
            "Qui sont vos clients cibles ?",
            value=business_model.get('segments_clients', ''),
            height=120,
            help=f"Groupes de personnes/organisations que vous visez{ai_help_suffix}",
            placeholder="Ex: PME locales, particuliers 25-45 ans, entreprises industrielles..." + (" [IA peut suggérer]" if has_ai_data else "")
        )
        
        st.markdown(f"#### {ai_indicator}💰 Structure de Coûts")
        business_model['structure_couts'] = st.text_area(
            "Quels sont vos principaux coûts ?",
            value=business_model.get('structure_couts', ''),
            height=120,
            help=f"Coûts fixes, variables, économies d'échelle...{ai_help_suffix}",
            placeholder="Ex: Matières premières, salaires, loyer, marketing..." + (" [IA peut suggérer]" if has_ai_data else "")
        )
        
        st.markdown(f"#### {ai_indicator}💵 Sources de Revenus")
        business_model['sources_revenus'] = st.text_area(
            "Comment générez-vous des revenus ?",
            value=business_model.get('sources_revenus', ''),
            height=120,
            help=f"Vente, abonnement, commission, licence...{ai_help_suffix}",
            placeholder="Ex: Vente de produits, services mensuels, commissions..." + (" [IA peut suggérer]" if has_ai_data else "")
        )
    
    # Métadonnées
    st.markdown("---")
    st.markdown("#### 📋 Informations Complémentaires")
    
    col_meta1, col_meta2 = st.columns(2)
    
    with col_meta1:
        business_model['nom_modele'] = st.text_input(
            "Nom du modèle d'affaires",
            value=business_model.get('nom_modele', ''),
            placeholder="Ex: Modèle E-commerce B2C"
        )
        
        business_model['secteur_activite'] = st.text_input(
            "Secteur d'activité",
            value=business_model.get('secteur_activite', st.session_state.get('secteur_activite', '')),
            placeholder="Ex: Commerce de détail, Services numériques..."
        )
    
    with col_meta2:
        business_model['version'] = st.text_input(
            "Version",
            value=business_model.get('version', '1.0'),
            placeholder="1.0"
        )
        
        business_model['date_creation'] = st.date_input(
            "Date de création",
            value=datetime.now().date()
        ).isoformat()
    
    # Boutons d'action
    st.markdown("---")
    col_save, col_preview, col_export = st.columns([1, 1, 1])
    
    with col_save:
        if st.button("💾 Sauvegarder Business Model", type="primary"):
            # Validation des champs obligatoires
            if validate_business_model(business_model):
                st.session_state['business_model_initial'] = business_model
                sauvegarder_donnees_session('business_model_initial', business_model)
                st.success("✅ Business Model sauvegardé!")
                st.balloons()
            else:
                st.error("❌ Veuillez remplir tous les blocs obligatoires")
    
    with col_preview:
        if st.button("👁️ Aperçu"):
            show_business_model_preview(business_model)
    
    with col_export:
        if st.button("📥 Exporter JSON"):
            export_business_model_json(business_model)

def page_arbre_probleme():
    """Page spécialisée pour l'arbre à problème (conservée de l'ancienne logique)"""
    
    st.title("🌳 Arbre à Problème")
    st.markdown("### Analysez la problématique que votre entreprise résout")
    
    # Récupération des données existantes
    arbre_data = st.session_state.get('arbre_probleme', {})
    
    st.markdown("#### 🎯 Problème Central")
    probleme_central = st.text_area(
        "Quel est le problème principal que vous résolvez ?",
        value=arbre_data.get('probleme_central', ''),
        height=100,
        help="Le problème core que votre entreprise adresse",
        placeholder="Ex: Les PME locales n'ont pas accès à des solutions de gestion abordables..."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔗 Causes (Pourquoi ce problème existe-t-il ?)")
        causes = st.text_area(
            "Causes du problème",
            value=arbre_data.get('causes', ''),
            height=150,
            help="Les raisons pour lesquelles ce problème existe",
            placeholder="• Manque de budget\n• Solutions trop complexes\n• Manque de formation..."
        )
    
    with col2:
        st.markdown("#### 💥 Conséquences (Quel impact si non résolu ?)")
        consequences = st.text_area(
            "Conséquences du problème",
            value=arbre_data.get('consequences', ''),
            height=150,
            help="Ce qui arrive si le problème n'est pas résolu",
            placeholder="• Perte de compétitivité\n• Inefficacité opérationnelle\n• Croissance limitée..."
        )
    
    st.markdown("#### 💡 Votre Solution")
    solution = st.text_area(
        "Comment votre entreprise résout-elle ce problème ?",
        value=arbre_data.get('solution', ''),
        height=100,
        help="Votre approche pour résoudre le problème identifié",
        placeholder="Ex: Nous proposons une solution SaaS simple et abordable..."
    )
    
    if st.button("💾 Sauvegarder Arbre à Problème", type="primary"):
        arbre_probleme = {
            'probleme_central': probleme_central,
            'causes': causes,
            'consequences': consequences,
            'solution': solution,
            'date_creation': datetime.now().isoformat()
        }
        
        st.session_state['arbre_probleme'] = arbre_probleme
        sauvegarder_donnees_session('arbre_probleme', arbre_probleme)
        st.success("✅ Arbre à problème sauvegardé!")

# Fonctions utilitaires

def get_empty_business_model():
    """Retourne un business model vide"""
    return {
        'partenaires_cles': '',
        'activites_cles': '',
        'ressources_cles': '',
        'propositions_valeur': '',
        'relations_clients': '',
        'canaux_distribution': '',
        'segments_clients': '',
        'structure_couts': '',
        'sources_revenus': '',
        'nom_modele': '',
        'secteur_activite': '',
        'version': '1.0',
        'date_creation': datetime.now().isoformat()
    }

def get_business_model_template():
    """Retourne un template d'exemple pour le business model"""
    return {
        "nom_modele": "E-commerce Local",
        "secteur_activite": "Commerce électronique",
        "version": "1.0",
        "date_creation": datetime.now().isoformat(),
        "partenaires_cles": "• Fournisseurs locaux\n• Partenaires logistiques\n• Banques/systèmes de paiement",
        "activites_cles": "• Gestion de plateforme e-commerce\n• Marketing digital\n• Service client",
        "ressources_cles": "• Plateforme technologique\n• Base de données clients\n• Équipe technique",
        "propositions_valeur": "• Accès facile aux produits locaux\n• Livraison rapide\n• Prix compétitifs",
        "relations_clients": "• Service client responsive\n• Programme de fidélité\n• Support en ligne",
        "canaux_distribution": "• Site web\n• Application mobile\n• Réseaux sociaux",
        "segments_clients": "• Particuliers urbains 25-45 ans\n• Familles avec enfants\n• Professionnels actifs",
        "structure_couts": "• Développement technologique\n• Marketing digital\n• Coûts logistiques",
        "sources_revenus": "• Commissions sur ventes\n• Frais de livraison\n• Services premium"
    }

def validate_business_model(business_model):
    """Valide qu'un business model a les champs essentiels remplis"""
    champs_obligatoires = [
        'propositions_valeur', 'segments_clients', 'sources_revenus'
    ]
    
    for champ in champs_obligatoires:
        if not business_model.get(champ, '').strip():
            return False
    
    return True

def validate_business_model_json(content):
    """Valide qu'un JSON importé a la structure d'un business model"""
    champs_requis = [
        'partenaires_cles', 'activites_cles', 'ressources_cles',
        'propositions_valeur', 'relations_clients', 'canaux_distribution',
        'segments_clients', 'structure_couts', 'sources_revenus'
    ]
    
    return all(champ in content for champ in champs_requis)

def parse_text_to_business_model(text_content):
    """Parse un texte libre en structure business model"""
    # Implémentation basique - peut être améliorée avec IA
    return {
        **get_empty_business_model(),
        'propositions_valeur': text_content[:500] + "..." if len(text_content) > 500 else text_content,
        'date_creation': datetime.now().isoformat()
    }

def show_business_model_preview(business_model):
    """Affiche un aperçu du business model"""
    st.markdown("### 👁️ Aperçu Business Model Canvas")
    
    # Organisation en 3 colonnes comme un vrai canvas
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("**🤝 Partenaires Clés**")
        st.write(business_model.get('partenaires_cles', 'Non défini'))
        
        st.markdown("**🔧 Activités Clés**")
        st.write(business_model.get('activites_cles', 'Non défini'))
        
        st.markdown("**🛠️ Ressources Clés**")
        st.write(business_model.get('ressources_cles', 'Non défini'))
    
    with col2:
        st.markdown("**💡 Propositions de Valeur**")
        st.write(business_model.get('propositions_valeur', 'Non défini'))
        
        st.markdown("**🤝 Relations Clients**")
        st.write(business_model.get('relations_clients', 'Non défini'))
        
        st.markdown("**📢 Canaux**")
        st.write(business_model.get('canaux_distribution', 'Non défini'))
    
    with col3:
        st.markdown("**👥 Segments Clients**")
        st.write(business_model.get('segments_clients', 'Non défini'))
        
        st.markdown("**💰 Structure de Coûts**")
        st.write(business_model.get('structure_couts', 'Non défini'))
        
        st.markdown("**💵 Sources de Revenus**")
        st.write(business_model.get('sources_revenus', 'Non défini'))

def export_business_model_json(business_model):
    """Exporte le business model en JSON"""
    json_data = json.dumps(business_model, indent=2, ensure_ascii=False)
    
    st.download_button(
        label="📥 Télécharger Business Model (JSON)",
        data=json_data,
        file_name=f"business_model_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json"
    )

def get_available_data_summary():
    """Retourne un résumé des données disponibles pour l'IA"""
    summary = []
    
    # Informations générales
    nom_entreprise = st.session_state.get('nom_entreprise', '')
    secteur_activite = st.session_state.get('secteur_activite', '')
    type_entreprise = st.session_state.get('type_entreprise', '')
    localisation = st.session_state.get('localisation', '')
    
    if nom_entreprise:
        summary.append(f"✅ **Entreprise:** {nom_entreprise}")
    if secteur_activite:
        summary.append(f"✅ **Secteur:** {secteur_activite}")
    if type_entreprise:
        summary.append(f"✅ **Type:** {type_entreprise}")
    if localisation:
        summary.append(f"✅ **Localisation:** {localisation}")
    
    # Arbre à problème
    arbre_probleme = st.session_state.get('arbre_probleme', {})
    if arbre_probleme.get('probleme_central'):
        summary.append(f"✅ **Problème identifié:** {arbre_probleme['probleme_central'][:100]}...")
    if arbre_probleme.get('solution'):
        summary.append(f"✅ **Solution proposée:** {arbre_probleme['solution'][:100]}...")
    
    # Analyse de marché
    analyse_marche = st.session_state.get('analyse_marche', {})
    if analyse_marche.get('taille_marche'):
        summary.append(f"✅ **Marché:** {analyse_marche['taille_marche']}")
    if analyse_marche.get('type_clients'):
        summary.append(f"✅ **Clients:** {analyse_marche['type_clients']}")
    
    # Analyse de concurrence
    concurrence = st.session_state.get('concurrence', {})
    if concurrence.get('concurrents_directs'):
        nb_concurrents = len([c for c in concurrence['concurrents_directs'] if c.strip()])
        if nb_concurrents > 0:
            summary.append(f"✅ **Concurrence:** {nb_concurrents} concurrents identifiés")
    
    return "\n".join(summary) if summary else "Aucune donnée disponible. Remplissez d'abord les informations générales, l'arbre à problème ou l'analyse de marché."

def prefill_with_ai(force_update=False):
    """Pré-remplit les champs du business model avec l'IA"""
    try:
        # Vérifier qu'on a des données suffisantes
        if not has_sufficient_data():
            return False
        
        # Rassembler toutes les données disponibles
        context_data = gather_context_data()
        
        # Générer les suggestions avec l'IA
        suggestions = generate_business_model_suggestions(context_data)
        
        if suggestions:
            # Mettre à jour le business model avec les suggestions
            current_model = st.session_state.get('business_model_initial', get_empty_business_model())
            
            # Logique de remplacement : remplacer si vide OU si force_update=True
            for key, value in suggestions.items():
                if force_update or len(current_model.get(key, '').strip()) < 10:  # Seulement si le champ est vide ou très court, ou si force
                    current_model[key] = value
            
            st.session_state['business_model_initial'] = current_model
            return True
        
        return False
        
    except Exception as e:
        st.error(f"Erreur lors de la génération IA : {str(e)}")
        return False

def auto_prefill_on_load():
    """Pré-remplissage automatique intelligent au chargement de la page"""
    # Vérifier si on a des données et si le business model est vide ou presque
    current_model = st.session_state.get('business_model_initial', get_empty_business_model())
    
    # Compter les champs remplis
    filled_fields = sum(1 for value in current_model.values() if isinstance(value, str) and len(value.strip()) > 10)
    
    # Debug info
    debug_enabled = st.session_state.get('debug_ai', False)
    if debug_enabled:
        st.write(f"🔍 Champs remplis: {filled_fields}/9")
        st.write(f"🔍 Données suffisantes: {has_sufficient_data()}")
        st.write(f"🔍 Auto-remplissage déjà fait: {st.session_state.get('auto_prefill_done', False)}")
    
    # Si moins de 3 champs remplis ET qu'on a des données suffisantes → auto-remplissage
    if filled_fields < 3 and has_sufficient_data():
        # Marquer qu'on a fait un auto-remplissage pour éviter les boucles
        if not st.session_state.get('auto_prefill_done', False):
            if debug_enabled:
                st.write("🚀 Déclenchement auto-remplissage...")
            if prefill_with_ai():
                st.session_state['auto_prefill_done'] = True
                # Info subtile pour l'utilisateur
                st.info("💡 **Suggestions IA ajoutées automatiquement** basées sur vos informations. Modifiez-les selon vos besoins !")
            elif debug_enabled:
                st.error("❌ Échec du pré-remplissage IA")
    elif debug_enabled:
        if filled_fields >= 3:
            st.info("ℹ️ Business model déjà rempli (3+ champs)")
        elif not has_sufficient_data():
            st.warning("⚠️ Données insuffisantes pour l'auto-remplissage")

def has_sufficient_data():
    """Vérifie si on a suffisamment de données pour utiliser l'IA"""
    # Au minimum, il faut le nom de l'entreprise et soit l'arbre à problème, soit l'analyse de marché
    nom_entreprise = st.session_state.get('nom_entreprise', '')
    arbre_probleme = st.session_state.get('arbre_probleme', {})
    analyse_marche = st.session_state.get('analyse_marche', {})
    
    # Informations générales depuis les données
    data = st.session_state.get('data', {})
    info_gen = data.get('informations_generales', {})
    nom_entreprise_alt = info_gen.get('nom_entreprise', '')
    
    has_entreprise = bool(nom_entreprise.strip()) or bool(nom_entreprise_alt.strip())
    has_probleme = bool(arbre_probleme.get('probleme_central', '').strip())
    has_marche = bool(analyse_marche.get('besoin_principal', '').strip())
    
    # Debug - affichage temporaire
    debug_checkbox = st.checkbox("🔍 Debug IA", help="Affiche les données disponibles pour l'IA", value=True)  # Activé par défaut pour diagnostic
    st.session_state['debug_ai'] = debug_checkbox
    
    if debug_checkbox:
        st.write("**Données détectées:**")
        st.write(f"- Nom entreprise (session): '{nom_entreprise}'")
        st.write(f"- Nom entreprise (data): '{nom_entreprise_alt}'")
        st.write(f"- Has entreprise: {has_entreprise}")
        st.write(f"- Arbre problème: {arbre_probleme}")
        st.write(f"- Has problème: {has_probleme}")
        st.write(f"- Analyse marché: {analyse_marche}")
        st.write(f"- Has marché: {has_marche}")
        st.write(f"- Données suffisantes: {has_entreprise and (has_probleme or has_marche)}")
    
    return has_entreprise and (has_probleme or has_marche)

def gather_context_data():
    """Rassemble toutes les données de contexte disponibles"""
    context = {}
    
    # Informations générales - plusieurs sources possibles
    context['nom_entreprise'] = st.session_state.get('nom_entreprise', '')
    context['secteur_activite'] = st.session_state.get('secteur_activite', '')
    context['type_entreprise'] = st.session_state.get('type_entreprise', 'PME')
    context['localisation'] = st.session_state.get('localisation', '')
    
    # Essayer aussi depuis les données financières
    data = st.session_state.get('data', {})
    info_gen = data.get('informations_generales', {})
    if not context['nom_entreprise'] and info_gen.get('nom_entreprise'):
        context['nom_entreprise'] = info_gen.get('nom_entreprise', '')
    if not context['secteur_activite'] and info_gen.get('secteur_activite'):
        context['secteur_activite'] = info_gen.get('secteur_activite', '')
    
    # Arbre à problème
    arbre_probleme = st.session_state.get('arbre_probleme', {})
    context['probleme_central'] = arbre_probleme.get('probleme_central', '')
    context['solution'] = arbre_probleme.get('solution', '')
    context['causes'] = arbre_probleme.get('causes', '')
    context['consequences'] = arbre_probleme.get('consequences', '')
    
    # Analyse de marché
    analyse_marche = st.session_state.get('analyse_marche', {})
    context['taille_marche'] = analyse_marche.get('taille_marche', '')
    context['type_clients'] = analyse_marche.get('type_clients', '')
    context['budget_moyen'] = analyse_marche.get('budget_moyen', '')
    context['besoin_principal'] = analyse_marche.get('besoin_principal', '')
    context['tendances'] = analyse_marche.get('tendances', [])
    
    # Analyse de concurrence
    concurrence = st.session_state.get('concurrence', {})
    context['concurrents_directs'] = concurrence.get('concurrents_directs', [])
    context['strategie'] = concurrence.get('strategie', '')
    context['forces'] = concurrence.get('forces', '')
    
    return context

def generate_business_model_suggestions(context_data):
    """Génère les suggestions de business model avec l'IA"""
    try:
        from services.ai.content_generation import generer_suggestions_intelligentes
        
        # Générer des suggestions pour chaque bloc du business model
        suggestions = {}
        
        blocs = [
            'partenaires_cles', 'activites_cles', 'ressources_cles',
            'propositions_valeur', 'relations_clients', 'canaux_distribution',
            'segments_clients', 'structure_couts', 'sources_revenus'
        ]
        
        # Debug info
        if st.session_state.get('debug_ai', False):
            st.write("🔄 Tentative génération IA...")
        
        for bloc in blocs:
            suggestions_bloc = generer_suggestions_intelligentes(
                donnees_existantes=context_data,
                section=bloc.replace('_', ' ').title(),
                template_nom="COPA TRANSFORME"
            )
            # Joindre les suggestions avec des puces
            suggestions[bloc] = '\n'.join([f"• {s}" for s in suggestions_bloc[:3]]) if suggestions_bloc else ""
        
        # Vérifier si on a au moins quelques suggestions
        valid_suggestions = sum(1 for v in suggestions.values() if v.strip())
        
        if valid_suggestions > 0:
            if st.session_state.get('debug_ai', False):
                st.success(f"✅ IA: {valid_suggestions} blocs générés")
            return suggestions
        else:
            if st.session_state.get('debug_ai', False):
                st.warning("⚠️ IA: Aucune suggestion générée, utilisation du fallback")
            return generate_fallback_suggestions(context_data)
        
    except (ImportError, ModuleNotFoundError) as e:
        if st.session_state.get('debug_ai', False):
            st.warning(f"⚠️ Module IA non trouvé: {str(e)}, utilisation du fallback")
        return generate_fallback_suggestions(context_data)
    except Exception as e:
        if st.session_state.get('debug_ai', False):
            st.error(f"❌ Erreur IA: {str(e)}, utilisation du fallback")
        return generate_fallback_suggestions(context_data)

def create_business_model_prompt(context_data):
    """Crée un prompt contextualisé pour l'IA"""
    
    prompt = f"""
    Analysez les informations suivantes et générez des suggestions pour chacun des 9 blocs du Business Model Canvas.
    
    **CONTEXTE ENTREPRISE:**
    - Nom: {context_data.get('nom_entreprise', 'Non spécifié')}
    - Secteur: {context_data.get('secteur_activite', 'Non spécifié')}
    - Type: {context_data.get('type_entreprise', 'PME')}
    - Localisation: {context_data.get('localisation', 'Non spécifiée')}
    
    **PROBLÉMATIQUE:**
    - Problème central: {context_data.get('probleme_central', 'Non spécifié')}
    - Solution proposée: {context_data.get('solution', 'Non spécifiée')}
    
    **MARCHÉ:**
    - Taille du marché: {context_data.get('taille_marche', 'Non spécifiée')}
    - Type de clients: {context_data.get('type_clients', 'Non spécifié')}
    - Budget moyen: {context_data.get('budget_moyen', 'Non spécifié')}
    - Besoin principal: {context_data.get('besoin_principal', 'Non spécifié')}
    
    **CONCURRENCE:**
    - Stratégie: {context_data.get('strategie', 'Non spécifiée')}
    - Forces: {context_data.get('forces', 'Non spécifiées')}
    
    Générez des suggestions courtes et précises (2-3 lignes max par bloc) pour:
    1. Partenaires clés
    2. Activités clés  
    3. Ressources clés
    4. Propositions de valeur
    5. Relations clients
    6. Canaux de distribution
    7. Segments clients
    8. Structure de coûts
    9. Sources de revenus
    
    Adaptez les suggestions au contexte africain/RDC et au type d'entreprise ({context_data.get('type_entreprise', 'PME')}).
    """
    
    return prompt

def generate_fallback_suggestions(context_data):
    """Génère des suggestions basiques sans IA (fallback)"""
    
    secteur = context_data.get('secteur_activite', '').lower()
    type_entreprise = context_data.get('type_entreprise', 'PME')
    
    # Suggestions basiques selon le secteur et le type
    if 'tech' in secteur or type_entreprise == 'Startup':
        return {
            'partenaires_cles': '• Développeurs techniques\n• Partenaires technologiques\n• Investisseurs',
            'activites_cles': '• Développement produit\n• Marketing digital\n• Support client',
            'ressources_cles': '• Plateforme technologique\n• Équipe de développement\n• Base de données',
            'propositions_valeur': '• Solution innovante et accessible\n• Gain de temps et d\'efficacité\n• Prix compétitif',
            'relations_clients': '• Support en ligne 24/7\n• Communauté d\'utilisateurs\n• Formation et onboarding',
            'canaux_distribution': '• Site web et application\n• Réseaux sociaux\n• Partenaires distributeurs',
            'segments_clients': '• PME locales\n• Professionnels tech-savvy\n• Entreprises en croissance',
            'structure_couts': '• Développement technique\n• Marketing digital\n• Infrastructure cloud',
            'sources_revenus': '• Abonnements mensuels\n• Commissions sur transactions\n• Services premium'
        }
    else:
        return {
            'partenaires_cles': '• Fournisseurs locaux\n• Distributeurs\n• Institutions financières',
            'activites_cles': '• Production/Fabrication\n• Vente et distribution\n• Service client',
            'ressources_cles': '• Équipements de production\n• Main d\'œuvre qualifiée\n• Réseau de distribution',
            'propositions_valeur': '• Produits de qualité locale\n• Service personnalisé\n• Prix accessible',
            'relations_clients': '• Relation directe\n• Service après-vente\n• Fidélisation clients',
            'canaux_distribution': '• Magasins physiques\n• Réseau de revendeurs\n• Vente directe',
            'segments_clients': '• Consommateurs locaux\n• Entreprises B2B\n• Particuliers',
            'structure_couts': '• Coût des matières premières\n• Salaires et charges\n• Coûts de distribution',
            'sources_revenus': '• Vente de produits\n• Services associés\n• Contrats de maintenance'
        }