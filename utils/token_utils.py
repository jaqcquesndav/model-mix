"""
Utilitaires pour le comptage et la gestion des tokens OpenAI
"""

import streamlit as st
import tiktoken
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

# Modèles et leurs coûts (USD par 1000 tokens)
TOKEN_COSTS = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03}, 
    "gpt-3.5-turbo": {"input": 0.001, "output": 0.002}
}

def get_encoding_for_model(model_name: str = "gpt-4"):
    """Récupère l'encodage approprié pour un modèle OpenAI"""
    try:
        return tiktoken.encoding_for_model(model_name)
    except KeyError:
        return tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str, model_name: str = "gpt-4") -> int:
    """Compte le nombre de tokens dans un texte"""
    if not text:
        return 0
    
    try:
        encoding = get_encoding_for_model(model_name)
        return len(encoding.encode(text))
    except Exception:
        # Estimation approximative en cas d'erreur
        return len(text.split()) * 1.3

def count_tokens_messages(messages: list, model_name: str = "gpt-4") -> int:
    """Compte le nombre de tokens dans une liste de messages de chat"""
    if not messages:
        return 0
    
    try:
        encoding = get_encoding_for_model(model_name)
        total_tokens = 0
        
        for message in messages:
            total_tokens += 4  # 4 tokens par message (overhead)
            
            for key, value in message.items():
                if isinstance(value, str):
                    total_tokens += len(encoding.encode(value))
                    if key == "name":
                        total_tokens += 1
        
        total_tokens += 2  # 2 tokens pour la réponse
        return total_tokens
    except Exception:
        # Estimation approximative
        total_chars = sum(len(str(msg.get('content', ''))) for msg in messages)
        return int(total_chars / 4)

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

def calculate_cost(input_tokens: int, output_tokens: int, model_name: str = "gpt-4") -> float:
    """Calcule le coût approximatif d'une requête"""
    model_pricing = TOKEN_COSTS.get(model_name, TOKEN_COSTS["gpt-4"])
    
    input_cost = input_tokens * (model_pricing["input"] / 1000)
    output_cost = output_tokens * (model_pricing["output"] / 1000)
    
    return input_cost + output_cost

def update_token_usage(input_tokens: int, output_tokens: int, model_name: str = "gpt-4"):
    """Met à jour les statistiques d'usage des tokens"""
    init_token_counter()
    
    request_cost = calculate_cost(input_tokens, output_tokens, model_name)
    
    # Mise à jour des totaux
    st.session_state['token_usage']['total_input_tokens'] += input_tokens
    st.session_state['token_usage']['total_output_tokens'] += output_tokens
    st.session_state['token_usage']['total_cost_usd'] += request_cost
    st.session_state['token_usage']['requests_count'] += 1
    
    # Usage journalier
    today = datetime.now().strftime('%Y-%m-%d')
    if 'daily_usage' not in st.session_state['token_usage']:
        st.session_state['token_usage']['daily_usage'] = {}
        
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

def check_token_limits(estimated_tokens: int) -> Tuple[bool, str]:
    """Vérifie si la requête respecte les limites"""
    # Limites par défaut
    daily_limit = 100000
    session_limit = 50000
    request_limit = 8000
    
    if estimated_tokens > request_limit:
        return False, f"Requête trop importante ({estimated_tokens} tokens). Limite: {request_limit}"
    
    init_token_counter()
    usage = st.session_state['token_usage']
    
    # Vérification limite de session
    session_total = usage['total_input_tokens'] + usage['total_output_tokens']
    if session_total + estimated_tokens > session_limit:
        return False, f"Limite de session atteinte ({session_total}/{session_limit} tokens)"
    
    # Vérification limite journalière
    today = datetime.now().strftime('%Y-%m-%d')
    daily_usage = usage['daily_usage'].get(today, {'input_tokens': 0, 'output_tokens': 0})
    daily_total = daily_usage.get('input_tokens', 0) + daily_usage.get('output_tokens', 0)
    
    if daily_total + estimated_tokens > daily_limit:
        return False, f"Limite journalière atteinte ({daily_total}/{daily_limit} tokens)"
    
    return True, "OK"

# Fonctions compatibles avec l'ancien code
def compter_tokens(text: str, model: str = "gpt-4") -> int:
    """Alias pour count_tokens"""
    return count_tokens(text, model)

def mettre_a_jour_usage_tokens(input_tokens: int, output_tokens: int, model: str = "gpt-4"):
    """Alias pour update_token_usage"""
    return update_token_usage(input_tokens, output_tokens, model)

def verifier_limite_tokens(prompt_tokens: int) -> Tuple[bool, str]:
    """Alias pour check_token_limits"""
    return check_token_limits(prompt_tokens)

def initialiser_compteur_tokens():
    """Alias pour init_token_counter"""
    return init_token_counter()

def obtenir_estimation_cout(tokens: int, model: str = "gpt-4", type_tokens: str = "input") -> float:
    """Estime le coût pour un nombre de tokens donné"""
    if model not in TOKEN_COSTS:
        return 0.0
    
    return (tokens / 1000) * TOKEN_COSTS[model][type_tokens]

def obtenir_statistiques_tokens() -> Dict[str, Any]:
    """Retourne les statistiques actuelles d'usage des tokens"""
    init_token_counter()
    usage = st.session_state['token_usage']
    
    # Calcul de la durée de session
    try:
        from datetime import datetime
        session_start = datetime.fromisoformat(usage['session_start'])
        session_duration = datetime.now() - session_start
        duration_str = str(session_duration).split('.')[0]  # Sans microsecondes
    except Exception:
        duration_str = "00:00:00"
    
    return {
        'total_tokens': usage['total_input_tokens'] + usage['total_output_tokens'],
        'input_tokens': usage['total_input_tokens'],
        'output_tokens': usage['total_output_tokens'],
        'total_cost': usage['total_cost_usd'],
        'requests_count': usage['requests_count'],
        'session_start': usage['session_start'],
        'session_duration': duration_str,
        'model_used': 'gpt-4',  # Modèle par défaut
        'user_limit': 50000,  # Limite par défaut
        'limit_enabled': True
    }

def configurer_limite_tokens(nouvelle_limite: int, activer: bool = True):
    """Configure la limite de tokens utilisateur"""
    init_token_counter()
    st.session_state['token_limit'] = nouvelle_limite
    st.session_state['token_limit_enabled'] = activer

def reinitialiser_compteur():
    """Remet à zéro le compteur de tokens"""
    if 'token_usage' in st.session_state:
        del st.session_state['token_usage']
    init_token_counter()

def formater_nombre_tokens(tokens: int) -> str:
    """Formate le nombre de tokens pour l'affichage"""
    if tokens < 1000:
        return str(tokens)
    elif tokens < 1000000:
        return f"{tokens/1000:.1f}K"
    else:
        return f"{tokens/1000000:.1f}M"

def obtenir_pourcentage_utilisation() -> float:
    """Calcule le pourcentage d'utilisation de la limite"""
    stats = obtenir_statistiques_tokens()
    limit_enabled = st.session_state.get('token_limit_enabled', True)
    user_limit = st.session_state.get('token_limit', 50000)
    
    if not limit_enabled or user_limit == 0:
        return 0.0
    
    return min(100.0, (stats['total_tokens'] / user_limit) * 100)