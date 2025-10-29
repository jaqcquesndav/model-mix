"""
Prompts système détaillés pour la génération de business plans professionnels
Version corrigée sans doublons et avec formatage amélioré
"""

from typing import Dict, Any

def get_business_plan_sections() -> Dict[str, str]:
    """
    Retourne la liste des sections du business plan dans l'ordre de génération
    """
    return {
        "Couverture": "Page de couverture du business plan",
        "Sommaire": "Table des matières structurée", 
        "Résumé Exécutif": "Executive summary professionnel",
        "Présentation de votre entreprise": "Présentation détaillée de l'entreprise",
        "Présentation de l'offre de produit": "Description de l'offre produits/services",
        "Étude de marché": "Analyse complète du marché cible",
        "Stratégie Marketing": "Plan marketing et commercial détaillé",
        "Moyens de production et organisation": "Ressources et organisation opérationnelle",
        "Étude des risques": "Analyse des risques et mesures d'atténuation",
        "Plan financier": "Projections financières détaillées",
        "Annexes": "Documents complémentaires"
    }

def get_system_prompts() -> Dict[str, str]:
    """
    Prompts système inspirés d'Origin.txt - Version corrigée
    """
    return {
        "Couverture": """
Générer cette section du business plan:

# Canevas de Plans d'Affaires

[Nom du projet ou entreprise]

[Secteur d'activité]

[Date]

Contact : [informations de contact]

Document confidentiel
        """,

        "Sommaire": """
Générer cette section du business plan:

## Sommaire

I. Résumé Exécutif « Executive Summary » / Pitch
II. Présentation de votre entreprise/projet  
III. Présentation de l'offre de produit(s) et/ou service(s)
IV. Étude de marché
V. Stratégie marketing, communication et politique commerciale
VI. Moyens de production et organisation
VII. Étude des risques/hypothèses
VIII. Plan financier
IX. Annexes
        """,

        "Résumé Exécutif": """
Générer cette section du business plan:

## I. Résumé Exécutif « Executive Summary » / Pitch

Générer deux grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
- Attirer l'attention du lecteur en 5 minutes et lui donner envie d'en savoir plus
- Décrire le projet en quelques phrases simples et impactantes  
- Ne pas essayer de tout couvrir, soyez concis et précis

Les éléments clés à générer et qui doivent être contenus dans les paragraphes :
- **Présentation de la PME** : Nom de l'entreprise et brève description du service/produit fourni
- **Présentation des porteurs de projet** : Profil des entrepreneurs et leur expérience
- **Potentiel en termes de taille et de profit** : Démontrez comment votre PME fera du profit
- **Votre besoin financier** : Montant nécessaire et utilisation prévue
        """,

        "Présentation de votre entreprise": """
Générer cette section du business plan:

## II. Présentation de votre entreprise/projet

Générer 6 grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
- Parler de votre entreprise/projet de manière plus détaillée
- Présenter l'équipe managériale clé

Les éléments clés à générer et qui doivent être contenus dans les paragraphes :

- **Informations générales sur la PME** :
  - Forme juridique : Ets, SARL, SAS, SA
  - Siège social : Adresse juridique de l'entreprise
  - Couverture géographique de l'entreprise et ses activités

- **Description détaillée de la PME et objectifs** : Présentez l'entreprise, son origine, ses atouts/opportunités et décrivez le projet

- **Stade d'avancement** : Ce qui a été fait et projets futurs, niveau de maturité, financements acquis

- **Équipe managériale** : Organigramme, ressources humaines, associés et parts sociales

- **Analyse SWOT** : Forces, faiblesses, opportunités, contraintes/menaces (de préférence sous forme de tableau)

- **Business Model Canvas** : Les 9 rubriques bien remplies
        """,

        "Présentation de l'offre de produit": """
Générer cette section du business plan:

## III. Présentation de l'offre de produit(s) et/ou service(s)

Générer 6 grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
- Parler de l'offre de produits/services de manière détaillée
- Présenter la proposition de valeur différenciante

Les éléments clés à générer et qui doivent être contenus dans les paragraphes :

- **Noms du/des produit(s) ou service(s)**
- **Besoins identifiés** sur le marché auxquels répond votre offre
- **Description du/des produit(s) ou service(s)** répondant à ces besoins
- **Proposition de valeur unique**
- **Prise en compte de l'aspect genre** dans le fonctionnement de la PME
- **Prise en compte de l'environnement** : impacts environnementaux, mesures d'atténuation, Plan de Gestion Environnemental et Social
        """,

        "Étude de marché": """
Générer cette section du business plan:

## IV. Étude de marché

Générer 8 grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
- Expliquer la méthode utilisée pour la conduite de l'étude de marché
- Présenter les résultats de l'étude de marché

Les éléments clés à générer, les numéros doivent être respectés :

1. **Description des hypothèses et méthodes** : Produit pré-ciblé, marché pré-ciblé, méthodologie
2. **Approche générale du marché** : Description du marché et ses caractéristiques  
3. **Caractéristiques de la demande** : Volume, évolution, segmentation clientèle
4. **Caractéristiques de l'offre** : Concurrence directe/indirecte, analyse concurrentielle
5. **Environnement des affaires** : Cadre légal, facteurs économiques, évolution technologique
6. **Partenariats** : Fournisseurs, distributeurs, alliances envisagées
7. **Création d'emplois** : Emplois directs/indirects, impact sur l'emploi local
8. **Projections du chiffre d'affaires** : Part de marché visée, projections à 1, 2, 3 ans
        """,

        "Stratégie Marketing": """
Générer cette section du business plan:

## V. Stratégie marketing, communication et politique commerciale

Générer 4 grands paragraphes avec plusieurs lignes pour :
- Présenter la stratégie marketing adoptée
- Détailler la politique commerciale

Les éléments clés à générer :

1. **Choix de segments de clientèle** : Segments prioritaires, critères de segmentation, justification
2. **Marketing-mix (4P)** : Politique de Produit, Prix, Place (distribution), Promotion
3. **Plan marketing et actions commerciales** : Calendrier des actions, budget, moyens déployés
4. **Moyens et partenaires sollicités** : Ressources humaines, budget marketing, partenaires
        """,

        "Moyens de production et organisation": """
Générer cette section du business plan:

## VI. Moyens de production et organisation

Générer 4 grands paragraphes détaillant :
- Les moyens techniques et humains nécessaires
- L'organisation opérationnelle

Les éléments clés à générer :

1. **Locaux et infrastructure** : Description des locaux, localisation, aménagement, coûts
2. **Équipements et matériel** : Liste détaillée, spécifications, mode d'acquisition, coûts
3. **Ressources humaines et organisation** : Organigramme, profils de postes, coûts salariaux
4. **Fournisseurs et sous-traitants** : Liste des fournisseurs, critères de sélection, conditions
        """,

        "Étude des risques": """
Générer cette section du business plan:

## VII. Étude des risques/hypothèses

Analyser les risques et présenter les stratégies d'atténuation.

Générer un tableau complet des risques avec les colonnes :
- Nature du risque
- Description détaillée  
- Probabilité (Faible/Moyenne/Élevée)
- Impact (Faible/Moyen/Élevé)
- Stratégie de traitement

Inclure les catégories de risques :
- Risques liés à l'environnement général
- Risques liés au marché
- Risques liés aux outils
- Risques liés aux personnes
- Risques liés aux tiers
- Autres risques spécifiques
        """,

        "Plan financier": """
Générer cette section du business plan:

## VIII. Plan financier

Présenter les projections financières détaillées et l'analyse de rentabilité.

Intégrer les tableaux financiers fournis et ajouter :

1. **Besoins de financement** : Investissements initiaux, fonds de roulement
2. **Sources de financement** : Apports propres, emprunts, subventions
3. **Analyse de rentabilité** : Seuil de rentabilité, ROI, délai de récupération
4. **Projections financières** : Compte de résultat, plan de financement, trésorerie

[Les tableaux financiers détaillés seront intégrés automatiquement]
        """,

        "Annexes": """
Générer cette section du business plan:

## IX. Annexes

Lister les documents complémentaires joints au business plan :

- CV des membres de l'équipe dirigeante
- Études de marché détaillées  
- Lettres d'intention de clients/fournisseurs
- Devis d'équipements et matériel
- Autorisations et licences requises
- Projections financières détaillées
- Statuts de l'entreprise
- Autres documents justificatifs
        """
    }

def get_user_queries() -> Dict[str, str]:
    """
    Requêtes utilisateur pour chaque section
    """
    return {
        "Couverture": "Créer une page de couverture professionnelle",
        "Sommaire": "Afficher le sommaire structuré du business plan",
        "Résumé Exécutif": "Décrire le projet, son potentiel et l'équipe dirigeante",
        "Présentation de votre entreprise": "Présenter l'entreprise de façon complète et structurée",
        "Présentation de l'offre de produit": "Décrire l'offre de produits/services et sa valeur ajoutée",
        "Étude de marché": "Analyser le marché cible, la concurrence et les opportunités",
        "Stratégie Marketing": "Développer la stratégie marketing et commerciale",
        "Moyens de production et organisation": "Décrire l'organisation opérationnelle et les ressources",
        "Étude des risques": "Identifier et analyser les risques avec mesures d'atténuation",
        "Plan financier": "Présenter les projections financières et besoins de financement",
        "Annexes": "Lister les documents complémentaires et références"
    }

def get_business_plan_context_template(template_name: str) -> str:
    """
    Contexte spécifique selon le template sélectionné
    """
    contexts = {
        "COPA TRANSFORME": """
CONTEXTE COPA TRANSFORMÉ:
Vous travaillez dans le cadre du programme COPA TRANSFORMÉ pour l'autonomisation des femmes entrepreneures et la mise à niveau des PME en RDC.

Secteurs prioritaires: Agroalimentaire, Industrie légère, Artisanat, Services à valeur ajoutée
Objectifs: Création d'emplois, autonomisation des femmes, transformation économique
Approche: Développement inclusif, partenariats locaux, innovation sociale
        """,
        
        "Virunga": """
CONTEXTE VIRUNGA:
Vous travaillez dans le cadre des initiatives de conservation et développement durable du Parc National des Virunga.

Secteurs prioritaires: Écotourisme, Agriculture durable, Énergies renouvelables, Conservation
Objectifs: Conservation environnementale, développement communautaire, paix et sécurité
Approche: Développement durable, protection environnementale, engagement communautaire
        """,
        
        "IP Femme": """
CONTEXTE IP FEMME:
Vous travaillez dans le cadre d'initiatives d'autonomisation économique des femmes en RDC.

Secteurs prioritaires: Commerce, Services, Artisanat, Agriculture, Microfinance
Objectifs: Égalité de genre, autonomisation économique, leadership féminin
Approche: Empowerment des femmes, inclusion financière, renforcement de capacités
        """
    }
    
    return contexts.get(template_name, contexts["COPA TRANSFORME"])

# Fonctions de compatibilité avec l'ancien système
def get_business_plan_system_messages(template_name: str) -> Dict[str, str]:
    """Version adaptée pour un template spécifique"""
    base_prompts = get_system_prompts()
    context_template = get_business_plan_context_template(template_name)
    
    adapted_prompts = {}
    for section, prompt in base_prompts.items():
        adapted_prompts[section] = f"{context_template}\n\n{prompt}"
    
    return adapted_prompts

def get_business_plan_user_queries(template_name: str) -> Dict[str, str]:
    """Version adaptée pour un template spécifique"""
    return get_user_queries()

def get_sections_configuration(template_name: str) -> Dict[str, Dict[str, str]]:
    """Configuration complète des sections pour un template donné"""
    sections = get_business_plan_sections()
    system_prompts = get_business_plan_system_messages(template_name)
    user_queries = get_business_plan_user_queries(template_name)
    
    configuration = {}
    for section_name, description in sections.items():
        configuration[section_name] = {
            "description": description,
            "system_message": system_prompts.get(section_name, "Prompt système non disponible"),
            "user_query": user_queries.get(section_name, "Requête non disponible"),
            "template_context": get_business_plan_context_template(template_name)
        }
    
    return configuration