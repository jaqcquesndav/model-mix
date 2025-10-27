"""
Module d'initialisation du package templates
"""

from .template_manager import (
    get_template,
    get_metaprompt,
    get_secteurs,
    get_system_messages,
    get_organisation_info,
    get_templates_list,
    TEMPLATES_DISPONIBLES
)

__all__ = [
    'get_template',
    'get_metaprompt', 
    'get_secteurs',
    'get_system_messages',
    'get_organisation_info',
    'get_templates_list',
    'TEMPLATES_DISPONIBLES'
]