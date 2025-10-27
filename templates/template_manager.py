"""
Gestionnaire des templates système
Permet de charger et utiliser les différents templates d'organisations
"""

from templates.copa_transforme import (
    METAPROMPT_COPA_TRANSFORME,
    SYSTEM_MESSAGES_COPA_TRANSFORME,
    SECTEURS_COPA_TRANSFORME,
    ORGANISATION_TYPE as COPA_TRANSFORME_ORG
)

from templates.virunga import (
    METAPROMPT_VIRUNGA,
    SYSTEM_MESSAGES_VIRUNGA,
    SECTEURS_VIRUNGA,
    ORGANISATION_TYPE as VIRUNGA_ORG
)

from templates.ip_femme import (
    METAPROMPT_IP_FEMME,
    SYSTEM_MESSAGES_IP_FEMME,
    SECTEURS_IP_FEMME,
    ORGANISATION_TYPE as IP_FEMME_ORG
)

# Secteurs spécialisés pour les startups (basé sur YC, Afrilab, Digital Africa)
SECTEURS_STARTUP = [
    "FinTech & Services Financiers",
    "HealthTech & MedTech",
    "EdTech & Formation",
    "AgriTech & FoodTech",
    "CleanTech & Énergie",
    "MobilityTech & Logistique",
    "E-Commerce & MarketPlace",
    "PropTech & Immobilier",
    "InsurTech & Assurance",
    "LegalTech & Juridique",
    "HRTech & Ressources Humaines",
    "MediaTech & Divertissement",
    "GameTech & Gaming",
    "SportTech & Fitness",
    "TravelTech & Tourisme",
    "RetailTech & Commerce",
    "B2B SaaS & Entreprise",
    "Deep Tech & IA",
    "Blockchain & Web3",
    "IoT & Hardware",
    "Cybersecurity & Sécurité",
    "Social Impact & Développement",
    "Consumer Apps & Mobile",
    "Data & Analytics",
    "API & Infrastructure"
]

# Dictionnaire des templates disponibles
TEMPLATES_DISPONIBLES = {
    "COPA TRANSFORME": {
        "metaprompt": METAPROMPT_COPA_TRANSFORME,
        "system_messages": SYSTEM_MESSAGES_COPA_TRANSFORME,
        "secteurs": SECTEURS_COPA_TRANSFORME,
        "organisation": COPA_TRANSFORME_ORG
    },
    "Virunga": {
        "metaprompt": METAPROMPT_VIRUNGA,
        "system_messages": SYSTEM_MESSAGES_VIRUNGA,
        "secteurs": SECTEURS_VIRUNGA,
        "organisation": VIRUNGA_ORG
    },
    "IP Femme": {
        "metaprompt": METAPROMPT_IP_FEMME,
        "system_messages": SYSTEM_MESSAGES_IP_FEMME,
        "secteurs": SECTEURS_IP_FEMME,
        "organisation": IP_FEMME_ORG
    }
}

def get_template(nom_template):
    """
    Récupère un template spécifique par son nom
    
    Args:
        nom_template (str): Nom du template ("COPA TRANSFORME", "Virunga", "IP Femme")
    
    Returns:
        dict: Configuration du template ou None si non trouvé
    """
    return TEMPLATES_DISPONIBLES.get(nom_template)

def get_metaprompt(nom_template):
    """
    Récupère le métaprompt d'un template spécifique
    
    Args:
        nom_template (str): Nom du template
    
    Returns:
        str: Métaprompt du template ou métaprompt par défaut
    """
    template = get_template(nom_template)
    if template:
        return template["metaprompt"]
    return METAPROMPT_COPA_TRANSFORME  # Par défaut

def get_secteurs(nom_template, type_entreprise="PME"):
    """
    Récupère la liste des secteurs prioritaires d'un template
    
    Args:
        nom_template (str): Nom du template
        type_entreprise (str): Type d'entreprise ("PME" ou "Startup")
    
    Returns:
        list: Liste des secteurs prioritaires
    """
    # Si c'est une startup, retourner les secteurs startup peu importe le template
    if type_entreprise == "Startup":
        return SECTEURS_STARTUP
    
    # Sinon, retourner les secteurs du template sélectionné
    template = get_template(nom_template)
    if template:
        return template["secteurs"]
    return SECTEURS_COPA_TRANSFORME  # Par défaut

def get_system_messages(nom_template):
    """
    Récupère les messages système d'un template
    
    Args:
        nom_template (str): Nom du template
    
    Returns:
        dict: Messages système du template
    """
    template = get_template(nom_template)
    if template:
        return template["system_messages"]
    return SYSTEM_MESSAGES_COPA_TRANSFORME  # Par défaut

def get_organisation_info(nom_template):
    """
    Récupère les informations d'organisation d'un template
    
    Args:
        nom_template (str): Nom du template
    
    Returns:
        dict: Informations de l'organisation
    """
    template = get_template(nom_template)
    if template:
        return template["organisation"]
    return COPA_TRANSFORME_ORG  # Par défaut

def get_templates_list():
    """
    Récupère la liste des noms de templates disponibles
    
    Returns:
        list: Liste des noms des templates
    """
    return list(TEMPLATES_DISPONIBLES.keys())