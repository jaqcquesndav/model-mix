"""
Module d'initialisation du package templates
Supporte l'ancien système (template_manager) ET le nouveau système (business_plan_prompts)
"""

# Ancien système (template_manager.py)
from .template_manager import (
    get_template,
    get_metaprompt,
    get_secteurs,
    get_system_messages,
    get_organisation_info,
    get_templates_list,
    TEMPLATES_DISPONIBLES
)

# Nouveau système (business_plan_prompts.py) - Import conditionnel pour éviter les conflits
try:
    from .business_plan_prompts import (
        get_business_plan_sections,
        get_system_prompts as get_business_plan_system_prompts_raw,
        get_user_queries,
        get_business_plan_context_template,
        get_business_plan_system_messages,
        get_business_plan_user_queries,
        get_sections_configuration,
        export_template_configuration
    )
    BUSINESS_PLAN_SYSTEM_AVAILABLE = True
except ImportError:
    BUSINESS_PLAN_SYSTEM_AVAILABLE = False

__all__ = [
    # Ancien système
    'get_template',
    'get_metaprompt', 
    'get_secteurs',
    'get_system_messages',
    'get_organisation_info',
    'get_templates_list',
    'TEMPLATES_DISPONIBLES',
    
    # Nouveau système (si disponible)
    'get_business_plan_sections',
    'get_user_queries',
    'get_business_plan_context_template',
    'get_business_plan_system_messages',
    'get_business_plan_user_queries', 
    'get_sections_configuration',
    'export_template_configuration',
    'BUSINESS_PLAN_SYSTEM_AVAILABLE'
]