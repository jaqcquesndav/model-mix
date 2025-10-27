"""
Module d'initialisation de l'interface utilisateur
"""

from .components import (
    configurer_sidebar_principal,
    afficher_indicateur_progression,
    widget_montant_devise,
    widget_pourcentage,
    afficher_section_aide,
    afficher_resume_donnees,
    bouton_sauvegarder_avec_confirmation,
    widget_validation_donnees,
    afficher_template_info,
    navigation_etapes
)

from . import pages

__all__ = [
    'configurer_sidebar_principal',
    'afficher_indicateur_progression',
    'widget_montant_devise',
    'widget_pourcentage',
    'afficher_section_aide',
    'afficher_resume_donnees',
    'bouton_sauvegarder_avec_confirmation',
    'widget_validation_donnees',
    'afficher_template_info',
    'navigation_etapes',
    'pages'
]