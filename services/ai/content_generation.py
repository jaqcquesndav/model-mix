"""
Service de génération de contenu par Intelligence Artificielle
"""

import openai
import streamlit as st
from typing import List, Dict, Any, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Import correct
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
import os
import tempfile
from openai import OpenAI
from utils.token_utils import (
    count_tokens, count_tokens_messages, update_token_usage, 
    check_token_limits, init_token_counter, calculate_cost
)

# Configuration OpenAI
def initialiser_openai():
    """Initialise la configuration OpenAI selon Origin.txt"""
    # Configuration exacte comme dans Origin.txt
    api_key = os.getenv("API_KEY")
    
    if api_key:
        # Configuration OpenAI legacy (comme dans Origin.txt)
        openai.api_key = api_key
        # Nouvelle structure OpenAI v1+ pour client
        client = OpenAI(api_key=api_key)
        return client
    return None

def tester_connexion_openai() -> Dict[str, Any]:
    """
    Teste la connexion à l'API OpenAI et retourne le statut
    Fonction inspirée des tests de Origin.txt
    """
    try:
        client = initialiser_openai()
        if not client:
            return {
                "status": "error",
                "message": "Clé API OpenAI non configurée",
                "details": "Variable d'environnement API_KEY manquante"
            }
        
        # Test simple avec un message court (comme dans Origin.txt)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant de test."},
                {"role": "user", "content": "Réponds juste 'OK' pour confirmer la connexion."},
            ],
            max_tokens=10,
            temperature=0.1
        )
        
        if response.choices[0].message.content:
            return {
                "status": "success",
                "message": "Connexion OpenAI active",
                "details": f"Modèle: gpt-3.5-turbo | Tokens: {response.usage.total_tokens if response.usage else 'N/A'}",
                "model_used": "gpt-3.5-turbo"
            }
        else:
            return {
                "status": "warning",
                "message": "Réponse API vide",
                "details": "La connexion fonctionne mais la réponse est vide"
            }
            
    except Exception as e:
        error_message = str(e)
        if "API key" in error_message:
            return {
                "status": "error",
                "message": "Erreur de clé API",
                "details": f"Vérifiez votre clé API_KEY: {error_message}"
            }
        elif "quota" in error_message.lower():
            return {
                "status": "error",
                "message": "Quota API dépassé",
                "details": f"Limite de quota atteinte: {error_message}"
            }
        elif "rate limit" in error_message.lower():
            return {
                "status": "warning",
                "message": "Limite de taux atteinte",
                "details": f"Trop de requêtes: {error_message}"
            }
        else:
            return {
                "status": "error",
                "message": "Erreur de connexion",
                "details": f"Erreur technique: {error_message}"
            }

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
            separators=["\n\n", "\n", " ", ""]
        )
        
        split_docs = text_splitter.split_documents(documents)
        return split_docs
        
    except Exception as e:
        st.error(f"Erreur lors du chargement du document : {e}")
        return []

def create_vector_store(documents: List[Document]) -> Optional[FAISS]:
    """
    Crée un store vectoriel à partir des documents
    
    Args:
        documents (List[Document]): Liste des documents
    
    Returns:
        Optional[FAISS]: Store vectoriel ou None si erreur
    """
    try:
        api_key = os.getenv("API_KEY")
        if not api_key:
            st.error("Clé API OpenAI non configurée")
            return None
            
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        vector_store = FAISS.from_documents(documents, embeddings)
        return vector_store
        
    except Exception as e:
        st.error(f"Erreur lors de la création du store vectoriel : {e}")
        return None

def search_similar_content(vector_store: FAISS, query: str, k: int = 3) -> List[str]:
    """
    Recherche du contenu similaire dans le store vectoriel
    
    Args:
        vector_store (FAISS): Store vectoriel
        query (str): Requête de recherche
        k (int): Nombre de résultats à retourner
    
    Returns:
        List[str]: Liste du contenu similaire
    """
    try:
        docs = vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
        
    except Exception as e:
        st.error(f"Erreur lors de la recherche : {e}")
        return []

def upload_and_process_pdf():
    """Interface pour télécharger et traiter un PDF"""
    uploaded_file = st.file_uploader("Télécharger un document PDF", type="pdf")
    
    if uploaded_file is not None:
        # Sauvegarder temporairement le fichier
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Traiter le document
        with st.spinner("Traitement du document..."):
            documents = load_and_split_documents(tmp_file_path)
            
            if documents:
                vector_store = create_vector_store(documents)
                
                if vector_store:
                    st.session_state['vector_store'] = vector_store
                    st.success(f"Document traité avec succès ! {len(documents)} segments créés.")
                    
                    # Interface de recherche
                    query = st.text_input("Rechercher dans le document:")
                    if query:
                        results = search_similar_content(vector_store, query)
                        if results:
                            st.write("**Résultats trouvés:**")
                            for i, result in enumerate(results, 1):
                                st.write(f"**Résultat {i}:**")
                                st.write(result[:500] + "..." if len(result) > 500 else result)
                                st.write("---")
        
        # Nettoyer le fichier temporaire
        os.unlink(tmp_file_path)

def generate_section(
    system_message: str, 
    user_query: str, 
    additional_context: str = "", 
    section_name: str = "Section",
    max_tokens: int = 5000,  # Utiliser 5000 comme dans Origin.txt
    temperature: float = 0.7,
    model: str = "gpt-4o"  # Utiliser gpt-4o comme dans Origin.txt
) -> str:
    """
    Génère du contenu pour une section spécifique du business model
    Version adaptée d'Origin.txt avec gestion d'erreurs améliorée
    """
    try:
        client = initialiser_openai()
        if not client:
            st.error("❌ Configuration OpenAI non disponible")
            return ""
        
        # Construire le contexte complet (comme dans Origin.txt)
        full_context = ""
        if additional_context:
            full_context = f"\n\nContexte additionnel:\n{additional_context}"
        
        # Construire le prompt final
        full_prompt = f"{user_query}{full_context}"
        
        # Messages pour l'API (format exact d'Origin.txt)
        messages = [
            {"role": "system", "content": "Tu es un assistant expert en génération de business et business plan."},  # Message exact d'Origin.txt
            {"role": "user", "content": full_prompt}
        ]
        
        # Vérification des tokens avant l'appel
        total_tokens = count_tokens_messages(messages, model=model)
        if not check_token_limits(total_tokens + max_tokens):
            st.warning("⚠️ Limite de tokens atteinte. Requête simplifiée.")
            return ""
        
        # Initialiser le compteur de tokens si nécessaire
        init_token_counter()
        
        # Appel à l'API OpenAI (format adapté d'Origin.txt)
        try:
            response = client.chat.completions.create(
                model=model,  # gpt-4o par défaut comme dans Origin.txt
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extraire le contenu (comme dans Origin.txt)
            content = response.choices[0].message.content.strip()
            
            # Mise à jour des statistiques de tokens
            usage = response.usage
            if usage:
                cost = calculate_cost(usage.total_tokens, model)
                update_token_usage(usage.prompt_tokens, usage.completion_tokens, cost)
            
            return content
            
        except Exception as api_error:
            error_str = str(api_error)
            
            # Gestion spécifique des erreurs comme dans Origin.txt
            if "model" in error_str.lower() and "gpt-4o" in error_str:
                st.warning(f"⚠️ GPT-4o non disponible, fallback vers GPT-3.5-turbo pour {section_name}")
                # Retry avec GPT-3.5-turbo
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=min(max_tokens, 4096),  # Limite pour GPT-3.5
                    temperature=temperature
                )
                content = response.choices[0].message.content.strip()
                
                # Mise à jour des tokens pour le modèle alternatif
                usage = response.usage
                if usage:
                    cost = calculate_cost(usage.total_tokens, "gpt-3.5-turbo")
                    update_token_usage(usage.prompt_tokens, usage.completion_tokens, cost)
                
                return content
            else:
                raise api_error
        
    except Exception as e:
        error_msg = f"Erreur génération {section_name}: {str(e)}"
        st.error(error_msg)
        
        # Log détaillé pour debugging (comme dans Origin.txt)
        if "API key" in str(e):
            st.error("🔑 Problème de clé API. Vérifiez votre configuration.")
        elif "quota" in str(e).lower():
            st.error("💳 Quota API dépassé. Vérifiez votre compte OpenAI.")
        elif "rate limit" in str(e).lower():
            st.warning("⏱️ Limite de taux atteinte. Veuillez patienter.")
        
        return ""

def generer_business_model_canvas(donnees: Dict[str, Any], template_nom: str = "COPA TRANSFORME") -> Dict[str, str]:
    """
    Génère un Business Model Canvas complet avec IA contextuelle
    """
    from templates import get_metaprompt, get_sections_prompts
    
    # Récupérer les prompts spécialisés
    metaprompt = get_metaprompt(template_nom)
    sections_prompts = get_sections_prompts(template_nom)
    
    # Extraire les informations clés
    nom_entreprise = donnees.get('nom_entreprise', '')
    secteur_activite = donnees.get('secteur_activite', '')
    type_entreprise = donnees.get('type_entreprise', 'PME')
    localisation = donnees.get('localisation', 'RDC')
    probleme_central = donnees.get('probleme_central', '')
    solution = donnees.get('solution', '')
    
    # Construire le contexte global
    contexte_global = f"""
    ENTREPRISE: {nom_entreprise}
    SECTEUR: {secteur_activite}
    TYPE: {type_entreprise}
    ZONE: {localisation}
    PROBLÈME: {probleme_central}
    SOLUTION: {solution}
    
    DONNÉES COMPLÈTES: {donnees}
    """
    
    # Sections du Business Model Canvas
    sections = [
        "segments_clients", "propositions_valeur", "canaux_distribution",
        "relations_clients", "sources_revenus", "ressources_cles",
        "activites_cles", "partenaires_cles", "structure_couts"
    ]
    
    resultats = {}
    
    for section in sections:
        try:
            # Récupérer le prompt spécialisé ou utiliser le metaprompt
            section_prompt = sections_prompts.get(section, metaprompt)
            
            # Créer la requête spécialisée pour la section
            user_query = f"""En tant qu'expert du secteur {secteur_activite}, générez le contenu pour '{section}' du Business Model Canvas.

CONTEXTE MÉTIER:
- Entreprise: {nom_entreprise} ({type_entreprise})
- Secteur: {secteur_activite} en {localisation}
- Problème: {probleme_central}
- Solution: {solution}

EXIGENCES SECTORIELLES:
- Expertise technique et réglementaire du secteur
- Connaissance de l'écosystème local ({localisation})
- Chiffres précis et réalistes
- Faisabilité économique validée

FORMAT: 3-4 éléments détaillés, chacun 100-150 mots avec chiffres concrets"""
            
            # Générer le contenu
            contenu = generate_section(
                system_message=section_prompt,
                user_query=user_query,
                additional_context=contexte_global,
                section_name=section,
                max_tokens=1000,
                temperature=0.7
            )
            
            resultats[section] = contenu
            
        except Exception as e:
            st.error(f"Erreur génération {section}: {str(e)}")
            resultats[section] = f"Erreur lors de la génération du contenu pour {section}"
    
    return resultats

def generer_suggestions_intelligentes(
    donnees_existantes: Dict[str, Any],
    section: str,
    template_nom: str = "COPA TRANSFORME"
) -> List[str]:
    """
    Génère des suggestions intelligentes pour une section donnée avec précision contextuelle
    """
    from templates import get_metaprompt
    
    metaprompt = get_metaprompt(template_nom)
    
    # Extraction des informations contextuelles clés
    nom_entreprise = donnees_existantes.get('nom_entreprise', '')
    secteur_activite = donnees_existantes.get('secteur_activite', '')
    type_entreprise = donnees_existantes.get('type_entreprise', 'PME')
    localisation = donnees_existantes.get('localisation', 'RDC')
    probleme_central = donnees_existantes.get('probleme_central', '')
    solution = donnees_existantes.get('solution', '')
    
    contexte = f"""CONTEXTE: {nom_entreprise} - {secteur_activite} en {localisation}
Problème: {probleme_central} | Solution: {solution}
Type: {type_entreprise} | Données: {donnees_existantes}"""
    
    query = f"""En tant qu'expert du secteur {secteur_activite}, générez 5 suggestions précises pour '{section}' du Business Model Canvas.

CONTEXTE: Secteur {secteur_activite} en {localisation} pour {type_entreprise}
Problème: {probleme_central} | Solution: {solution}

EXIGENCES:
- Chiffres précis et réalistes
- Partenaires locaux appropriés  
- Solutions concrètes aux contraintes
- Faisabilité économique validée

FORMAT: Liste numérotée avec détails pratiques"""
    
    try:
        response = generate_section(
            system_message=metaprompt,
            user_query=query,
            additional_context=contexte,
            section_name=f"Suggestions {section}",
            max_tokens=1000
        )
        
        # Extraire les suggestions
        suggestions = []
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                suggestion = line.lstrip('0123456789.-').strip()
                if suggestion:
                    suggestions.append(suggestion)
        
        return suggestions[:5]
        
    except Exception as e:
        st.error(f"Erreur génération suggestions: {str(e)}")
        return []

def analyser_coherence_donnees(donnees: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyse la cohérence des données saisies
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