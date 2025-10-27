"""
Page de génération du business model
"""

import streamlit as st
from services.business import obtenir_business_model, sauvegarder_donnees_session, get_donnees_consolidees
from services.ai import generer_suggestions_intelligentes
from ui.components import afficher_template_info
from templates import get_metaprompt

def page_generer_business_model():
    """Page de génération du business model canvas - Version simplifiée"""
    
    st.title("🎯 Business Model Final")
    
    # Vérification des données préalables
    donnees_consolidees = get_donnees_consolidees()
    donnees_business = donnees_consolidees['donnees_business']
    
    # Interface simplifiée en deux colonnes
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown("### � Statut")
        
        # Vérification persona
        if donnees_business['persona']:
            st.success("✅ Persona")
        else:
            st.error("❌ Persona")
        
        # Vérification marché
        if donnees_business['marche']:
            st.success("✅ Marché")
        else:
            st.warning("⚠️ Marché")
        
        # Vérification concurrence
        if donnees_business['concurrence']:
            st.success("✅ Concurrence")
        else:
            st.warning("⚠️ Concurrence")
        
        st.markdown("---")
        
        # Statut global
        if donnees_business['persona']:
            st.success("🟢 Prêt à générer")
        else:
            st.error("🔴 Données manquantes")
            st.caption("Le persona est requis")
    
    with col1:
        # Business model existant
        business_model_existant = st.session_state.get('business_model_precedent', '')
        
        if business_model_existant:
            st.markdown("### � Votre Business Model")
            
            # Affichage et édition du business model
            business_model_edite = st.text_area(
                "Business Model Canvas",
                value=business_model_existant,
                height=400,
                help="Vous pouvez modifier directement votre business model ici"
            )
            
            # Boutons d'action
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("💾 Sauvegarder", type="primary"):
                    sauvegarder_donnees_session('business_model_precedent', business_model_edite)
                    st.success("✅ Sauvegardé!")
            
            with col_btn2:
                if st.button("🔄 Améliorer"):
                    if donnees_business['persona']:
                        with st.spinner("Amélioration en cours..."):
                            try:
                                business_model_ameliore = obtenir_business_model(
                                    donnees_business,
                                    st.session_state.get('template_selectionne', 'COPA TRANSFORME')
                                )
                                sauvegarder_donnees_session('business_model_precedent', business_model_ameliore)
                                st.success("✅ Business Model amélioré!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erreur : {str(e)}")
                    else:
                        st.error("❌ Complétez d'abord le persona")
            
            with col_btn3:
                nom_entreprise = donnees_consolidees['donnees_generales'].get('nom_entreprise', 'entreprise')
                st.download_button(
                    "📥 Télécharger",
                    business_model_edite,
                    file_name=f"business_model_{nom_entreprise}.txt",
                    mime="text/plain"
                )
        
        else:
            # Pas de business model - Génération initiale
            st.markdown("### 🚀 Générer votre Business Model")
            
            if not donnees_business['persona']:
                st.error("❌ **Persona requis**")
                st.info("💡 Allez dans **Business Model** → **Créativité & Business Model** pour compléter votre persona")
                
                # Lien direct vers la page précédente
                if st.button("🔗 Aller compléter le persona"):
                    st.info("Utilisez l'onglet 'Créativité & Business Model' ci-dessus")
            
            else:
                st.success("✅ **Prêt à générer votre business model**")
                
                # Options simples
                niveau_detail = st.selectbox(
                    "Niveau de détail",
                    ["Standard", "Détaillé", "Synthétique"],
                    index=0
                )
                
                # Bouton de génération principal
                if st.button("🎯 **Générer mon Business Model**", type="primary", use_container_width=True):
                    with st.spinner("⏳ Génération en cours..."):
                        try:
                            business_model_genere = obtenir_business_model(
                                donnees_business,
                                st.session_state.get('template_selectionne', 'COPA TRANSFORME')
                            )
                            
                            sauvegarder_donnees_session('business_model_precedent', business_model_genere)
                            st.success("🎉 **Business Model généré avec succès !**")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Erreur lors de la génération : {str(e)}")
                            st.info("💡 Vérifiez vos données et réessayez")
        
        # Aide contextuelle
        with st.expander("💡 Aide"):
            st.markdown("""
            **Comment utiliser cette page :**
            
            1. **Si c'est votre première fois :** Complétez d'abord votre persona dans l'onglet précédent
            2. **Pour générer :** Cliquez sur "Générer mon Business Model"  
            3. **Pour modifier :** Éditez directement le texte et sauvegardez
            4. **Pour améliorer :** Utilisez le bouton "Améliorer" pour une nouvelle version
            
            **Conseils :**
            - Plus vos données initiales sont complètes, meilleur sera le business model
            - Vous pouvez toujours modifier manuellement le contenu généré
            - N'hésitez pas à régénérer si le résultat ne vous convient pas
            """)