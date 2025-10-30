"""
Service de génération de contenu par Intelligence Artificielle
"""

import openai
import streamlit as st
from typing import List, Dict, Any, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
import os
import tempfile
from openai import OpenAI
from utils.token_utils import (
    count_tokens, count_tokens_messages, update_token_usage, 
    check_token_limits, init_token_counter, calculate_cost
)

# Configuration OpenAI
def initialiser_openai():
    """Initialise la configuration OpenAI"""
    api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if api_key:
        # Nouvelle structure OpenAI v1+
        client = OpenAI(api_key=api_key)
        return client
    return None

def load_and_split_documents(file_path: str) -> List[Document]:
    """
    Charge et divise un document PDF
    
    Args:
        file_path (str): Chemin vers le fichier PDF
    
    Returns:
        List[Document]: Liste des documents segmentés
    """
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        return text_splitter.split_documents(documents)
    except Exception as e:
        st.error(f"Erreur lors du chargement du document : {str(e)}")
        return []

def create_vectorstore(documents: List[Document]) -> Optional[FAISS]:
    """
    Crée un magasin vectoriel FAISS à partir des documents
    
    Args:
        documents (List[Document]): Liste des documents
    
    Returns:
        FAISS or None: Magasin vectoriel ou None en cas d'erreur
    """
    if not documents:
        return None
    
    try:
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(documents, embeddings)
        return vectorstore
    except Exception as e:
        st.error(f"Erreur lors de la création du magasin vectoriel : {str(e)}")
        return None

def search_similar_content(vectorstore: FAISS, query: str, k: int = 3) -> List[str]:
    """
    Recherche du contenu similaire dans le magasin vectoriel
    
    Args:
        vectorstore (FAISS): Magasin vectoriel
        query (str): Requête de recherche
        k (int): Nombre de résultats à retourner
    
    Returns:
        List[str]: Liste des contenus similaires
    """
    if not vectorstore:
        return []
    
    try:
        docs = vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
    except Exception as e:
        st.error(f"Erreur lors de la recherche : {str(e)}")
        return []

def generate_section(system_message, query, combined_content, business_model="", section_name=""):
    """
    Génère une section du business plan en utilisant l'IA
    
    Args:
        system_message (str): Message système pour guider l'IA
        query (str): Requête spécifique
        combined_content (str): Contenu combiné des données
        business_model (str): Business model existant
        section_name (str): Nom de la section générée
    
    Returns:
        str: Contenu généré par l'IA
    """
    try:
        # Initialisation du compteur de tokens
        init_token_counter()
        
        # Construction des messages
        messages = [
            {"role": "system", "content": system_message}
        ]
        
        # Construction du prompt utilisateur
        user_prompt = f"""
Contexte des données collectées:
{combined_content}

Business Model existant (si disponible):
{business_model}

Requête spécifique pour {section_name}:
{query}
"""
        
        messages.append({"role": "user", "content": user_prompt})
        
        # Comptage des tokens d'entrée avec tiktoken
        input_tokens = count_tokens_messages(messages, "gpt-4")
        
        # Vérification des limites
        can_proceed, limit_message = check_token_limits(input_tokens)
        if not can_proceed:
            st.error(f"Limite de tokens dépassée: {limit_message}")
            return f"Erreur: {limit_message}"
        
        # Configuration du client OpenAI
        api_key = st.secrets.get("API_KEY") or st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            st.error("Clé API OpenAI non configurée")
            return "Erreur: Clé API manquante"
        
        client = OpenAI(api_key=api_key)
        
        # Appel à l'API avec gestion d'erreurs
        with st.spinner(f"Génération de {section_name}..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=2000,
                temperature=0.7
            )
        
        # Extraction du contenu généré
        generated_content = response.choices[0].message.content
        
        # Récupération des tokens réels de l'API (si disponible)
        if hasattr(response, 'usage') and response.usage:
            actual_input_tokens = response.usage.prompt_tokens
            actual_output_tokens = response.usage.completion_tokens
        else:
            # Fallback: utilisation de tiktoken pour compter les tokens de sortie
            actual_input_tokens = input_tokens
            actual_output_tokens = count_tokens(generated_content, "gpt-4")
        
        # Mise à jour des statistiques de tokens
        update_token_usage(actual_input_tokens, actual_output_tokens, "gpt-4")
        
        # Affichage des informations de debug
        if st.session_state.get('debug_mode', False):
            st.info(f"""
**Debug - {section_name}:**
- Tokens entrée: {actual_input_tokens}
- Tokens sortie: {actual_output_tokens}
- Coût estimé: ${calculate_cost(actual_input_tokens, actual_output_tokens, 'gpt-4'):.4f}
            """)
        
        return generated_content
        
    except Exception as e:
        error_message = f"Erreur lors de la génération de {section_name}: {str(e)}"
        st.error(error_message)
        return f"Erreur: {str(e)}"

def generer_business_model_canvas(
    persona_data: Dict[str, Any],
    marche_data: Dict[str, Any],
    concurrence_data: Dict[str, Any],
    facteurs_limitants: Dict[str, Any],
    metaprompt: str,
    secteur: str = "",
    type_entreprise: str = "PME"
) -> str:
    """
    Génère un business model canvas complet
    
    Args:
        persona_data (dict): Données du persona
        marche_data (dict): Données d'analyse de marché
        concurrence_data (dict): Données de concurrence
        facteurs_limitants (dict): Facteurs limitants
        metaprompt (str): Prompt système spécifique au template
        secteur (str): Secteur d'activité
        type_entreprise (str): Type d'entreprise
    
    Returns:
        str: Business model canvas généré
    """
    # Construire le contexte à partir des données collectées
    contexte = f"""
    TYPE D'ENTREPRISE: {type_entreprise}
    SECTEUR D'ACTIVITÉ: {secteur}
    
    DONNÉES PERSONA:
    {persona_data}
    
    ANALYSE DE MARCHÉ:
    {marche_data}
    
    ANALYSE CONCURRENCE:
    {concurrence_data}
    
    FACTEURS LIMITANTS:
    {facteurs_limitants}
    """
    
    query = """
    Générez un business model canvas complet et détaillé basé sur les données fournies.
    Le business model doit être structuré selon les 9 sections classiques :
    1. Partenaires clés
    2. Activités clés
    3. Ressources clés
    4. Propositions de valeur
    5. Relations clients
    6. Canaux de distribution
    7. Segments de clientèle
    8. Structure de coûts
    9. Sources de revenus
    
    Pour chaque section, fournissez une analyse détaillée et des recommandations spécifiques.
    """
    
    return generate_section(
        system_message=metaprompt,
        user_query=query,
        additional_context=contexte,
        section_name="Business Model Canvas"
    )

def generer_suggestions_intelligentes(
    donnees_existantes: Dict[str, Any],
    section: str,
    template_nom: str = "COPA TRANSFORME"
) -> List[str]:
    """
    Génère des suggestions intelligentes pour une section donnée
    
    Args:
        donnees_existantes (dict): Données déjà saisies
        section (str): Section pour laquelle générer des suggestions
        template_nom (str): Nom du template à utiliser
    
    Returns:
        List[str]: Liste de suggestions
    """
    from templates import get_metaprompt
    
    metaprompt = get_metaprompt(template_nom)
    
    contexte = f"Données existantes: {donnees_existantes}"
    
    query = f"""
    Générez 5 suggestions courtes et pertinentes pour la section '{section}' 
    en tenant compte des données déjà saisies.
    Chaque suggestion doit être pratique et adaptée au contexte de la RDC.
    Formatez la réponse comme une liste numérotée.
    """
    
    try:
        response = generate_section(
            system_message=metaprompt,
            user_query=query,
            additional_context=contexte,
            section_name=f"Suggestions {section}",
            max_tokens=1000
        )
        
        # Extraire les suggestions de la réponse
        suggestions = []
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Nettoyer la ligne (enlever numérotation)
                suggestion = line.lstrip('0123456789.-').strip()
                if suggestion:
                    suggestions.append(suggestion)
        
        return suggestions[:5]  # Limiter à 5 suggestions
        
    except Exception as e:
        st.error(f"Erreur lors de la génération de suggestions : {str(e)}")
        return []

def analyser_coherence_donnees(donnees: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyse la cohérence des données saisies
    
    Args:
        donnees (dict): Données à analyser
    
    Returns:
        dict: Résultat de l'analyse avec recommandations
    """
    query = f"""
    Analysez la cohérence des données suivantes et identifiez les incohérences potentielles :
    {donnees}
    
    Fournissez :
    1. Les incohérences détectées
    2. Des recommandations d'amélioration
    3. Un score de cohérence sur 10
    """
    
    try:
        response = generate_section(
            system_message="Vous êtes un expert en analyse de données business.",
            user_query=query,
            section_name="Analyse de cohérence",
            max_tokens=1500
        )
        
        return {
            "analyse": response,
            "timestamp": st.session_state.get("timestamp", "")
        }
        
    except Exception as e:
        return {
            "analyse": f"Erreur lors de l'analyse : {str(e)}",
            "timestamp": ""
        }

def generer_contenu_personnalise(
    template_nom: str,
    type_contenu: str,
    donnees_contexte: Dict[str, Any]
) -> str:
    """
    Génère du contenu personnalisé selon le template sélectionné
    
    Args:
        template_nom (str): Nom du template
        type_contenu (str): Type de contenu à générer
        donnees_contexte (dict): Données de contexte
    
    Returns:
        str: Contenu généré
    """
    from templates import get_metaprompt, get_system_messages
    
    metaprompt = get_metaprompt(template_nom)
    system_messages = get_system_messages(template_nom)
    
    # Utiliser le message système spécifique si disponible
    system_message = system_messages.get(type_contenu, metaprompt)
    
    query = f"Générez du contenu pour '{type_contenu}' en utilisant les données suivantes : {donnees_contexte}"
    
    return generate_section(
        system_message=system_message,
        user_query=query,
        additional_context=str(donnees_contexte),
        section_name=type_contenu
    )