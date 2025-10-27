"""
Page de génération du business model
"""

import streamlit as st
from services.business import obtenir_business_model, sauvegarder_donnees_session, get_donnees_consolidees
from services.ai import generer_suggestions_intelligentes
from ui.components import afficher_template_info
from templates import get_metaprompt

def page_generer_business_model():
    """Page de génération du business model canvas"""
    
    st.title("🎯 Générateur de Business Model Canvas")
    
    # Affichage du template actuel
    template_actuel = st.session_state.get('template_selectionne', 'COPA TRANSFORME')
    afficher_template_info()
    
    # Vérification des données préalables
    donnees_consolidees = get_donnees_consolidees()
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.markdown("### 📋 État des données")
        
        # Vérification persona
        if donnees_consolidees['donnees_business']['persona']:
            st.success("✅ Données persona collectées")
        else:
            st.warning("⚠️ Données persona manquantes")
        
        # Vérification marché
        if donnees_consolidees['donnees_business']['marche']:
            st.success("✅ Analyse marché effectuée")
        else:
            st.warning("⚠️ Analyse marché manquante")
        
        # Vérification concurrence
        if donnees_consolidees['donnees_business']['concurrence']:
            st.success("✅ Analyse concurrence complétée")
        else:
            st.warning("⚠️ Analyse concurrence manquante")
    
    with col1:
        st.markdown("### 🚀 Génération du Business Model")
        
        # Options de génération
        mode_generation = st.radio(
            "Mode de génération",
            [
                "Génération automatique complète",
                "Génération par sections",
                "Amélioration du modèle existant"
            ],
            help="Choisissez comment vous souhaitez générer votre business model"
        )
        
        if mode_generation == "Génération automatique complète":
            generer_business_model_complet(donnees_consolidees, template_actuel)
        
        elif mode_generation == "Génération par sections":
            generer_par_sections(donnees_consolidees, template_actuel)
        
        elif mode_generation == "Amélioration du modèle existant":
            ameliorer_modele_existant(donnees_consolidees, template_actuel)

def generer_business_model_complet(donnees_consolidees, template_actuel):
    """Génère un business model complet automatiquement"""
    
    st.markdown("#### Génération Automatique Complète")
    
    # Vérification des données minimales
    donnees_business = donnees_consolidees['donnees_business']
    
    if not donnees_business['persona']:
        st.error("❌ Les données persona sont obligatoires pour la génération automatique.")
        st.info("Veuillez d'abord compléter l'onglet 'Collecte des Données' → 'Persona PME'")
        return
    
    st.info("Cette option génère un business model canvas complet basé sur toutes vos données collectées.")
    
    # Paramètres de génération
    with st.expander("⚙️ Paramètres avancés"):
        niveau_detail = st.selectbox(
            "Niveau de détail",
            ["Standard", "Détaillé", "Synthétique"],
            index=0,
            help="Niveau de détail souhaité pour le business model"
        )
        
        focus_secteur = st.checkbox(
            "Accent sur les spécificités sectorielles",
            value=True,
            help="Mettre l'accent sur les caractéristiques de votre secteur d'activité"
        )
        
        inclure_risques = st.checkbox(
            "Inclure l'analyse des risques",
            value=True,
            help="Ajouter une section sur les risques et leur gestion"
        )
    
    # Bouton de génération
    if st.button("🎯 Générer le Business Model Complet", type="primary"):
        
        with st.spinner("Génération en cours... Cela peut prendre quelques minutes."):
            
            try:
                # Génération du business model
                business_model_genere = obtenir_business_model(
                    donnees_consolidees['donnees_business'],
                    template_actuel
                )
                
                # Sauvegarde
                sauvegarder_donnees_session('business_model_precedent', business_model_genere)
                
                # Affichage du résultat
                st.success("✅ Business Model généré avec succès!")
                
                # Affichage avec possibilité d'édition
                business_model_edite = st.text_area(
                    "Business Model Canvas (modifiable)",
                    value=business_model_genere,
                    height=600,
                    help="Vous pouvez modifier le contenu généré avant de le sauvegarder définitivement"
                )
                
                # Boutons d'action
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("💾 Sauvegarder les modifications"):
                        sauvegarder_donnees_session('business_model_precedent', business_model_edite)
                        st.success("Modifications sauvegardées!")
                
                with col2:
                    if st.button("🔄 Régénérer"):
                        st.rerun()
                
                with col3:
                    if st.button("📥 Télécharger"):
                        st.download_button(
                            "Télécharger le Business Model",
                            business_model_edite,
                            file_name=f"business_model_{donnees_consolidees['donnees_generales']['nom_entreprise']}.txt",
                            mime="text/plain"
                        )
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération : {str(e)}")
                st.info("Veuillez vérifier vos données et réessayer.")

def generer_par_sections(donnees_consolidees, template_actuel):
    """Génère le business model section par section"""
    
    st.markdown("#### Génération par Sections")
    st.info("Cette option vous permet de générer et personnaliser chaque section individuellement.")
    
    # Sections du business model canvas
    sections_canvas = [
        ("Partenaires clés", "Qui sont vos partenaires et fournisseurs clés ?"),
        ("Activités clés", "Quelles sont vos activités les plus importantes ?"),
        ("Ressources clés", "De quelles ressources avez-vous absolument besoin ?"),
        ("Propositions de valeur", "Quelle valeur apportez-vous à vos clients ?"),
        ("Relations clients", "Comment maintenez-vous les relations avec vos clients ?"),
        ("Canaux de distribution", "Par quels moyens atteignez-vous vos clients ?"),
        ("Segments de clientèle", "Qui sont vos clients les plus importants ?"),
        ("Structure de coûts", "Quels sont vos coûts les plus importants ?"),
        ("Sources de revenus", "Comment générez-vous des revenus ?")
    ]
    
    # Sélection de la section à générer
    section_selectionnee = st.selectbox(
        "Choisissez une section à générer",
        [f"{i+1}. {nom}" for i, (nom, _) in enumerate(sections_canvas)],
        help="Sélectionnez la section du business model canvas que vous souhaitez générer"
    )
    
    section_index = int(section_selectionnee.split('.')[0]) - 1
    section_nom, section_description = sections_canvas[section_index]
    
    st.markdown(f"**Section sélectionnée :** {section_nom}")
    st.markdown(f"*{section_description}*")
    
    # Génération de la section
    if st.button(f"Générer '{section_nom}'", type="primary"):
        
        with st.spinner(f"Génération de la section '{section_nom}'..."):
            
            try:
                # Utiliser le service de génération de suggestions
                suggestions = generer_suggestions_intelligentes(
                    donnees_consolidees['donnees_business'],
                    section_nom,
                    template_actuel
                )
                
                st.success(f"✅ Section '{section_nom}' générée!")
                
                # Affichage des suggestions
                if suggestions:
                    st.markdown("**Suggestions générées :**")
                    for i, suggestion in enumerate(suggestions, 1):
                        st.markdown(f"{i}. {suggestion}")
                    
                    # Zone d'édition
                    contenu_section = st.text_area(
                        f"Contenu final pour '{section_nom}'",
                        value="\n".join([f"• {s}" for s in suggestions]),
                        height=200,
                        help="Modifiez le contenu selon vos besoins"
                    )
                    
                    # Sauvegarde de la section
                    if st.button(f"Sauvegarder '{section_nom}'"):
                        cle_section = f"business_model_section_{section_index}"
                        sauvegarder_donnees_session(cle_section, contenu_section)
                        st.success(f"Section '{section_nom}' sauvegardée!")
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération : {str(e)}")

def ameliorer_modele_existant(donnees_consolidees, template_actuel):
    """Améliore un business model existant"""
    
    st.markdown("#### Amélioration du Modèle Existant")
    
    business_model_existant = st.session_state.get('business_model_precedent', '')
    
    if not business_model_existant:
        st.warning("⚠️ Aucun business model existant trouvé.")
        st.info("Générez d'abord un business model complet ou créez-en un manuellement.")
        
        # Option de création manuelle
        with st.expander("✏️ Créer un business model manuellement"):
            business_model_manuel = st.text_area(
                "Saisissez votre business model actuel",
                height=400,
                placeholder="Entrez ici votre business model canvas existant..."
            )
            
            if st.button("Sauvegarder le modèle manuel"):
                sauvegarder_donnees_session('business_model_precedent', business_model_manuel)
                st.success("Business model manuel sauvegardé!")
                st.rerun()
        
        return
    
    st.info("Améliorez votre business model existant avec des suggestions personnalisées.")
    
    # Affichage du modèle existant
    with st.expander("📄 Business Model Actuel"):
        st.text_area(
            "Modèle actuel (lecture seule)",
            value=business_model_existant,
            height=300,
            disabled=True
        )
    
    # Options d'amélioration
    type_amelioration = st.selectbox(
        "Type d'amélioration",
        [
            "Optimisation générale",
            "Renforcement de la proposition de valeur",
            "Amélioration de la rentabilité",
            "Expansion des segments clients",
            "Diversification des revenus"
        ],
        help="Choisissez l'aspect que vous souhaitez améliorer"
    )
    
    # Contexte d'amélioration
    contexte_amelioration = st.text_area(
        "Contexte spécifique ou défis rencontrés",
        height=100,
        placeholder="Ex: Difficulté à fidéliser les clients, coûts trop élevés, concurrence accrue..."
    )
    
    # Génération des améliorations
    if st.button("🔧 Générer des Améliorations", type="primary"):
        
        with st.spinner("Génération des améliorations..."):
            
            # Ici, on utiliserait le service AI pour générer des améliorations
            # basées sur le modèle existant et le contexte
            try:
                from services.ai import generer_contenu_personnalise
                
                donnees_contexte = {
                    'business_model_existant': business_model_existant,
                    'type_amelioration': type_amelioration,
                    'contexte': contexte_amelioration,
                    'donnees_entreprise': donnees_consolidees['donnees_business']
                }
                
                ameliorations = generer_contenu_personnalise(
                    template_actuel,
                    "amelioration_business_model",
                    donnees_contexte
                )
                
                st.success("✅ Améliorations générées!")
                
                # Affichage des améliorations
                ameliorations_editees = st.text_area(
                    "Améliorations suggérées (modifiables)",
                    value=ameliorations,
                    height=400
                )
                
                # Options de sauvegarde
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("💾 Sauvegarder les améliorations"):
                        # Ajouter les améliorations au business model existant
                        business_model_ameliore = business_model_existant + "\n\n## AMÉLIORATIONS SUGGÉRÉES\n\n" + ameliorations_editees
                        sauvegarder_donnees_session('business_model_precedent', business_model_ameliore)
                        st.success("Améliorations ajoutées au business model!")
                
                with col2:
                    if st.button("🔄 Remplacer le modèle existant"):
                        sauvegarder_donnees_session('business_model_precedent', ameliorations_editees)
                        st.success("Business model remplacé par la version améliorée!")
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération d'améliorations : {str(e)}")

def afficher_historique_versions():
    """Affiche l'historique des versions du business model"""
    
    with st.expander("📚 Historique des versions"):
        st.info("Fonctionnalité à venir : historique et versioning des business models")
        # Ici on pourrait implémenter un système de versioning