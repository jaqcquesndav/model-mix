"""
Page de génération du business model - Version épurée
"""

import streamlit as st
from services.business import obtenir_business_model, sauvegarder_donnees_session, get_donnees_consolidees
from services.ai import generer_suggestions_intelligentes
from ui.components import afficher_template_info
from templates import get_metaprompt

def page_generer_business_model():
    """Page de génération du business model canvas - Version simplifiée et épurée"""
    
    st.title("🎯 Business Model Final")
    
    # Vérification des données préalables
    donnees_consolidees = get_donnees_consolidees()
    donnees_business = donnees_consolidees['donnees_business']
    
    # Vérification simplifiée - seulement si persona manquant
    if not donnees_business['persona']:
        st.error("❌ **Persona requis pour générer votre business model**")
        st.info("💡 Complétez d'abord votre persona dans l'onglet **Business Model** → **Créativité & Business Model**")
        
        if st.button("🔗 Aller compléter le persona", type="primary"):
            st.info("Utilisez l'onglet 'Créativité & Business Model' ci-dessus")
        return
    
    # Interface principale épurée
    business_model_existant = st.session_state.get('business_model_precedent', '')
    
    if business_model_existant:
        # Business model existant - Édition
        st.markdown("### 📝 Votre Business Model")
        
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
    
    # Aide contextuelle compacte
    with st.expander("💡 Aide"):
        st.markdown("""
        **Comment utiliser cette page :**
        
        1. **Première génération :** Cliquez sur "Générer mon Business Model"  
        2. **Modifier :** Éditez directement le texte et sauvegardez
        3. **Améliorer :** Utilisez le bouton "Améliorer" pour une nouvelle version
        
        **Conseil :** Plus vos données initiales sont complètes, meilleur sera le business model
        """)