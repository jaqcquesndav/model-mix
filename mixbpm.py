"""
Point d'entrée principal pour l'application MixBPM refactorisée
Ce fichier remplace l'ancien mixbpm.py
"""

# Import du module principal refactorisé
from main import main, handle_errors

# Configuration Streamlit
import streamlit as st

st.set_page_config(
    page_title="MixBPM - Business Model & Plan Generator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Lancement de l'application
if __name__ == "__main__":
    try:
        # Gestion globale des erreurs
        handle_errors()
    except Exception as e:
        st.error(f"Erreur critique de l'application : {str(e)}")
        st.info("L'application a été refactorisée. Le fichier principal est maintenant `main.py`")
        st.markdown("### 🔧 Pour les développeurs :")
        st.code("streamlit run main.py")