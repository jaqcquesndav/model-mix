"""
Module d'initialisation des pages UI
"""

from .collecte_donnees import page_collecte_donnees
from .generer_business_model import page_generer_business_model
from .analyse_marche import afficher_analyse_marche, afficher_analyse_concurrence

__all__ = [
    'page_collecte_donnees',
    'page_generer_business_model',
    'afficher_analyse_marche',
    'afficher_analyse_concurrence'
]