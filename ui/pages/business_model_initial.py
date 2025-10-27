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
    """Création manuelle du business model selon les 9 blocs"""
    
    st.subheader("✍️ Business Model Canvas - 9 Blocs")
    
    # Récupération des données existantes
    business_model = st.session_state.get('business_model_initial', get_empty_business_model())
    
    # Organisation en colonnes pour une meilleure présentation
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("#### 🤝 Partenaires Clés")
        business_model['partenaires_cles'] = st.text_area(
            "Qui sont vos partenaires stratégiques ?",
            value=business_model.get('partenaires_cles', ''),
            height=120,
            help="Fournisseurs clés, partenaires stratégiques, alliances...",
            placeholder="Ex: Fournisseurs matières premières, distributeurs, partenaires technologiques..."
        )
        
        st.markdown("#### 🔧 Activités Clés")
        business_model['activites_cles'] = st.text_area(
            "Quelles sont vos activités principales ?",
            value=business_model.get('activites_cles', ''),
            height=120,
            help="Production, résolution de problèmes, plateforme/réseau...",
            placeholder="Ex: Production, marketing, R&D, logistique..."
        )
        
        st.markdown("#### 🛠️ Ressources Clés")
        business_model['ressources_cles'] = st.text_area(
            "Quelles ressources sont essentielles ?",
            value=business_model.get('ressources_cles', ''),
            height=120,
            help="Physiques, intellectuelles, humaines, financières...",
            placeholder="Ex: Équipements, brevets, équipe qualifiée, capital..."
        )
    
    with col2:
        st.markdown("#### 💡 Propositions de Valeur")
        business_model['propositions_valeur'] = st.text_area(
            "Quelle valeur créez-vous pour vos clients ?",
            value=business_model.get('propositions_valeur', ''),
            height=180,
            help="Produits/services qui créent de la valeur pour un segment client",
            placeholder="Ex: Résout le problème X, améliore la performance Y, réduit les coûts..."
        )
        
        st.markdown("#### 🤝 Relations Clients")
        business_model['relations_clients'] = st.text_area(
            "Comment maintenez-vous vos relations clients ?",
            value=business_model.get('relations_clients', ''),
            height=120,
            help="Assistance personnelle, self-service, communautés...",
            placeholder="Ex: Service client personnalisé, assistance en ligne, communauté..."
        )
        
        st.markdown("#### 📢 Canaux de Distribution")
        business_model['canaux_distribution'] = st.text_area(
            "Comment atteignez-vous vos clients ?",
            value=business_model.get('canaux_distribution', ''),
            height=120,
            help="Vente directe, partenaires, web, magasins...",
            placeholder="Ex: Boutique physique, site web, revendeurs, réseaux sociaux..."
        )
    
    with col3:
        st.markdown("#### 👥 Segments Clients")
        business_model['segments_clients'] = st.text_area(
            "Qui sont vos clients cibles ?",
            value=business_model.get('segments_clients', ''),
            height=120,
            help="Groupes de personnes/organisations que vous visez",
            placeholder="Ex: PME locales, particuliers 25-45 ans, entreprises industrielles..."
        )
        
        st.markdown("#### 💰 Structure de Coûts")
        business_model['structure_couts'] = st.text_area(
            "Quels sont vos principaux coûts ?",
            value=business_model.get('structure_couts', ''),
            height=120,
            help="Coûts fixes, variables, économies d'échelle...",
            placeholder="Ex: Matières premières, salaires, loyer, marketing..."
        )
        
        st.markdown("#### 💵 Sources de Revenus")
        business_model['sources_revenus'] = st.text_area(
            "Comment générez-vous des revenus ?",
            value=business_model.get('sources_revenus', ''),
            height=120,
            help="Vente, abonnement, commission, licence...",
            placeholder="Ex: Vente de produits, services mensuels, commissions..."
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