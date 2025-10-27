"""
Utilitaires pour le comptage et la gestion des tokens OpenAI
"""

import streamlit as st
import tiktoken
from typing import Dict, Any, Optional
from datetime import datetime

def get_encoding_for_model(model_name: str = "gpt-4"):
    """
    Récupère l'encodage approprié pour un modèle OpenAI
    
    Args:
        model_name (str): Nom du modèle OpenAI
    
    Returns:
        tiktoken.Encoding: Encodage pour le modèle
    """
    try:
        return tiktoken.encoding_for_model(model_name)
    except KeyError:
        # Utilise cl100k_base par défaut pour les nouveaux modèles
        return tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str, model_name: str = "gpt-4") -> int:
    """
    Compte le nombre de tokens dans un texte pour un modèle donné
    
    Args:
        text (str): Texte à analyser
        model_name (str): Nom du modèle OpenAI
    
    Returns:
        int: Nombre de tokens
    """
    if not text:
        return 0
    
    try:
        encoding = get_encoding_for_model(model_name)
        return len(encoding.encode(text))
    except Exception as e:
        st.error(f"Erreur lors du comptage des tokens: {str(e)}")
        # Estimation approximative en cas d'erreur
        return len(text.split()) * 1.3

def count_tokens_messages(messages: list, model_name: str = "gpt-4") -> int:
    """
    Compte le nombre de tokens dans une liste de messages de chat
    
    Args:
        messages (list): Liste des messages (format OpenAI)
        model_name (str): Nom du modèle OpenAI
    
    Returns:
        int: Nombre total de tokens
    """
    if not messages:
        return 0
    
    try:
        encoding = get_encoding_for_model(model_name)
        total_tokens = 0
        
        for message in messages:
            # 4 tokens par message (overhead du format)
            total_tokens += 4
            
            for key, value in message.items():
                if isinstance(value, str):
                    total_tokens += len(encoding.encode(value))
                    if key == "name":  # Le champ name coûte 1 token supplémentaire
                        total_tokens += 1
        
        # 2 tokens supplémentaires pour la réponse
        total_tokens += 2
        
        return total_tokens
    except Exception as e:
        st.error(f"Erreur lors du comptage des tokens des messages: {str(e)}")
        # Estimation approximative
        total_chars = sum(len(str(msg.get('content', ''))) for msg in messages)
        return int(total_chars / 4)  # Approximation grossière

def init_token_counter():
    """Initialise le compteur de tokens dans le session state"""
    if 'token_usage' not in st.session_state:
        st.session_state['token_usage'] = {
            'total_input_tokens': 0,
            'total_output_tokens': 0,
            'total_cost_usd': 0.0,
            'requests_count': 0,
            'session_start': datetime.now().isoformat(),
            'daily_usage': {},
            'request_history': []
        }

def get_token_limits():
    """Récupère les limites de tokens configurées"""
    return {
        'daily_limit': st.session_state.get('token_daily_limit', 100000),
        'session_limit': st.session_state.get('token_session_limit', 50000),
        'single_request_limit': st.session_state.get('token_request_limit', 8000)
    }

def set_token_limits(daily_limit: int, session_limit: int, request_limit: int):
    """Configure les limites de tokens"""
    st.session_state['token_daily_limit'] = daily_limit
    st.session_state['token_session_limit'] = session_limit
    st.session_state['token_request_limit'] = request_limit

def calculate_cost(input_tokens: int, output_tokens: int, model_name: str = "gpt-4") -> float:
    """
    Calcule le coût approximatif d'une requête
    
    Args:
        input_tokens (int): Nombre de tokens d'entrée
        output_tokens (int): Nombre de tokens de sortie
        model_name (str): Nom du modèle
    
    Returns:
        float: Coût en USD
    """
    # Prix approximatifs en USD (octobre 2025)
    pricing = {
        "gpt-4": {"input": 0.03/1000, "output": 0.06/1000},
        "gpt-4-turbo": {"input": 0.01/1000, "output": 0.03/1000},
        "gpt-3.5-turbo": {"input": 0.001/1000, "output": 0.002/1000}
    }
    
    # Utilise gpt-4 par défaut si le modèle n'est pas trouvé
    model_pricing = pricing.get(model_name, pricing["gpt-4"])
    
    input_cost = input_tokens * model_pricing["input"]
    output_cost = output_tokens * model_pricing["output"]
    
    return input_cost + output_cost

def update_token_usage(input_tokens: int, output_tokens: int, model_name: str = "gpt-4"):
    """
    Met à jour les statistiques d'usage des tokens
    
    Args:
        input_tokens (int): Tokens d'entrée utilisés
        output_tokens (int): Tokens de sortie générés
        model_name (str): Modèle utilisé
    """
    init_token_counter()
    
    # Coût de la requête
    request_cost = calculate_cost(input_tokens, output_tokens, model_name)
    
    # Mise à jour des totaux
    st.session_state['token_usage']['total_input_tokens'] += input_tokens
    st.session_state['token_usage']['total_output_tokens'] += output_tokens
    st.session_state['token_usage']['total_cost_usd'] += request_cost
    st.session_state['token_usage']['requests_count'] += 1
    
    # Usage journalier
    today = datetime.now().strftime('%Y-%m-%d')
    if today not in st.session_state['token_usage']['daily_usage']:
        st.session_state['token_usage']['daily_usage'][today] = {
            'input_tokens': 0,
            'output_tokens': 0,
            'cost_usd': 0.0,
            'requests': 0
        }
    
    daily = st.session_state['token_usage']['daily_usage'][today]
    daily['input_tokens'] += input_tokens
    daily['output_tokens'] += output_tokens
    daily['cost_usd'] += request_cost
    daily['requests'] += 1
    
    # Historique des requêtes (garde les 100 dernières)
    history = st.session_state['token_usage']['request_history']
    history.append({
        'timestamp': datetime.now().isoformat(),
        'model': model_name,
        'input_tokens': input_tokens,
        'output_tokens': output_tokens,
        'cost_usd': request_cost
    })
    
    # Limite l'historique à 100 entrées
    if len(history) > 100:
        st.session_state['token_usage']['request_history'] = history[-100:]

def get_current_usage() -> Dict[str, Any]:
    """Récupère les statistiques d'usage actuelles"""
    init_token_counter()
    return st.session_state['token_usage']

def get_daily_usage() -> Dict[str, Any]:
    """Récupère l'usage du jour"""
    today = datetime.now().strftime('%Y-%m-%d')
    usage = get_current_usage()
    return usage['daily_usage'].get(today, {
        'input_tokens': 0,
        'output_tokens': 0,
        'cost_usd': 0.0,
        'requests': 0
    })

def check_token_limits(estimated_tokens: int) -> tuple[bool, str]:
    """
    Vérifie si la requête respecte les limites
    
    Args:
        estimated_tokens (int): Tokens estimés pour la requête
    
    Returns:
        tuple: (autorisé, message)
    """
    limits = get_token_limits()
    usage = get_current_usage()
    daily_usage = get_daily_usage()
    
    # Vérification limite par requête
    if estimated_tokens > limits['single_request_limit']:
        return False, f"Requête trop importante ({estimated_tokens} tokens). Limite: {limits['single_request_limit']}"
    
    # Vérification limite de session
    session_total = usage['total_input_tokens'] + usage['total_output_tokens']
    if session_total + estimated_tokens > limits['session_limit']:
        return False, f"Limite de session atteinte ({session_total}/{limits['session_limit']} tokens)"
    
    # Vérification limite journalière
    daily_total = daily_usage.get('input_tokens', 0) + daily_usage.get('output_tokens', 0)
    if daily_total + estimated_tokens > limits['daily_limit']:
        return False, f"Limite journalière atteinte ({daily_total}/{limits['daily_limit']} tokens)"
    
    return True, "OK"

def reset_session_usage():
    """Remet à zéro les compteurs de session"""
    if 'token_usage' in st.session_state:
        st.session_state['token_usage']['total_input_tokens'] = 0
        st.session_state['token_usage']['total_output_tokens'] = 0
        st.session_state['token_usage']['total_cost_usd'] = 0.0
        st.session_state['token_usage']['requests_count'] = 0
        st.session_state['token_usage']['session_start'] = datetime.now().isoformat()
        st.session_state['token_usage']['request_history'] = []

import streamlit as st
import tiktoken
from typing import Dict, Any, Optional
from datetime import datetime

# Modèles et leurs coûts (USD par 1000 tokens)
TOKEN_COSTS = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.001, "output": 0.002}
}

# Limites par défaut par modèle
DEFAULT_LIMITS = {
    "gpt-4": 8192,
    "gpt-4-turbo": 4096,
    "gpt-3.5-turbo": 4096
}

def initialiser_compteur_tokens():
    """Initialise le compteur de tokens dans le session state"""
    if 'token_usage' not in st.session_state:
        st.session_state['token_usage'] = {
            'total_input_tokens': 0,
            'total_output_tokens': 0,
            'total_cost': 0.0,
            'session_start': datetime.now().isoformat(),
            'requests_count': 0,
            'model_used': 'gpt-4',
            'user_limit': DEFAULT_LIMITS.get('gpt-4', 4096),
            'limit_enabled': True
        }

def compter_tokens(text: str, model: str = "gpt-4") -> int:
    """
    Compte le nombre de tokens dans un texte pour un modèle donné
    
    Args:
        text (str): Texte à analyser
        model (str): Modèle OpenAI utilisé
    
    Returns:
        int: Nombre de tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        # Fallback approximation: 4 caractères = 1 token
        return len(text) // 4

def mettre_a_jour_usage_tokens(input_tokens: int, output_tokens: int, model: str = "gpt-4"):
    """
    Met à jour les statistiques d'usage des tokens
    
    Args:
        input_tokens (int): Tokens envoyés
        output_tokens (int): Tokens reçus
        model (str): Modèle utilisé
    """
    if 'token_usage' not in st.session_state:
        initialiser_compteur_tokens()
    
    usage = st.session_state['token_usage']
    
    # Mise à jour des compteurs
    usage['total_input_tokens'] += input_tokens
    usage['total_output_tokens'] += output_tokens
    usage['requests_count'] += 1
    usage['model_used'] = model
    
    # Calcul du coût
    if model in TOKEN_COSTS:
        input_cost = (input_tokens / 1000) * TOKEN_COSTS[model]['input']
        output_cost = (output_tokens / 1000) * TOKEN_COSTS[model]['output']
        usage['total_cost'] += input_cost + output_cost
    
    st.session_state['token_usage'] = usage

def obtenir_statistiques_tokens() -> Dict[str, Any]:
    """
    Retourne les statistiques actuelles d'usage des tokens
    
    Returns:
        dict: Statistiques complètes
    """
    if 'token_usage' not in st.session_state:
        initialiser_compteur_tokens()
    
    usage = st.session_state['token_usage']
    
    # Calcul du temps de session
    session_start = datetime.fromisoformat(usage['session_start'])
    session_duration = datetime.now() - session_start
    
    return {
        'total_tokens': usage['total_input_tokens'] + usage['total_output_tokens'],
        'input_tokens': usage['total_input_tokens'],
        'output_tokens': usage['total_output_tokens'],
        'total_cost': usage['total_cost'],
        'requests_count': usage['requests_count'],
        'session_duration': str(session_duration).split('.')[0],  # Sans microsecondes
        'model_used': usage['model_used'],
        'user_limit': usage['user_limit'],
        'limit_enabled': usage['limit_enabled']
    }

def verifier_limite_tokens(prompt_tokens: int) -> tuple[bool, str]:
    """
    Vérifie si l'ajout de tokens dépasse la limite utilisateur
    
    Args:
        prompt_tokens (int): Tokens du prompt à envoyer
    
    Returns:
        tuple: (peut_continuer, message)
    """
    if 'token_usage' not in st.session_state:
        initialiser_compteur_tokens()
    
    usage = st.session_state['token_usage']
    
    if not usage['limit_enabled']:
        return True, ""
    
    total_actuel = usage['total_input_tokens'] + usage['total_output_tokens']
    nouveau_total = total_actuel + prompt_tokens
    
    if nouveau_total > usage['user_limit']:
        tokens_restants = usage['user_limit'] - total_actuel
        return False, f"Limite de tokens atteinte. Tokens restants: {tokens_restants}"
    
    return True, ""

def reinitialiser_compteur():
    """Remet à zéro le compteur de tokens"""
    if 'token_usage' in st.session_state:
        del st.session_state['token_usage']
    initialiser_compteur_tokens()

def configurer_limite_tokens(nouvelle_limite: int, activer: bool = True):
    """
    Configure la limite de tokens utilisateur
    
    Args:
        nouvelle_limite (int): Nouvelle limite en tokens
        activer (bool): Activer/désactiver la limite
    """
    if 'token_usage' not in st.session_state:
        initialiser_compteur_tokens()
    
    st.session_state['token_usage']['user_limit'] = nouvelle_limite
    st.session_state['token_usage']['limit_enabled'] = activer

def obtenir_estimation_cout(tokens: int, model: str = "gpt-4", type_tokens: str = "input") -> float:
    """
    Estime le coût pour un nombre de tokens donné
    
    Args:
        tokens (int): Nombre de tokens
        model (str): Modèle utilisé
        type_tokens (str): 'input' ou 'output'
    
    Returns:
        float: Coût estimé en USD
    """
    if model not in TOKEN_COSTS:
        return 0.0
    
    return (tokens / 1000) * TOKEN_COSTS[model][type_tokens]

def formater_nombre_tokens(tokens: int) -> str:
    """
    Formate le nombre de tokens pour l'affichage
    
    Args:
        tokens (int): Nombre de tokens
    
    Returns:
        str: Tokens formatés (ex: "1.2K", "15.3K")
    """
    if tokens < 1000:
        return str(tokens)
    elif tokens < 1000000:
        return f"{tokens/1000:.1f}K"
    else:
        return f"{tokens/1000000:.1f}M"

def obtenir_pourcentage_utilisation() -> float:
    """
    Calcule le pourcentage d'utilisation de la limite
    
    Returns:
        float: Pourcentage (0-100)
    """
    stats = obtenir_statistiques_tokens()
    if not stats['limit_enabled'] or stats['user_limit'] == 0:
        return 0.0
    
    return min(100.0, (stats['total_tokens'] / stats['user_limit']) * 100)