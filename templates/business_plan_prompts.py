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
    Prompts système corrigés pour génération directe sans explications
    """
    return {
        "Couverture": """
Générez UNIQUEMENT le contenu de la page de couverture au format Markdown.

IMPORTANT: Ne donnez AUCUNE explication. Générez SEULEMENT le contenu final.

Format de sortie:

# PLAN D'AFFAIRES

## [Nom de l'entreprise]

**Secteur d'activité:** [Secteur selon contexte]
**Localisation:** République Démocratique du Congo
**Date:** [Date actuelle]

---

### PORTEURS DU PROJET
- **Dirigeant Principal:** [Nom selon contexte]
- **Contact:** [Email selon contexte]

---

**Document confidentiel - Usage strictement professionnel**
        """,

        "Sommaire": """
Générez UNIQUEMENT le sommaire structuré. Aucune explication.

Format de sortie:

# SOMMAIRE

**I. RÉSUMÉ EXÉCUTIF** .................................................. 3
- Présentation du projet
- Objectifs et vision
- Demande de financement

**II. PRÉSENTATION DE L'ENTREPRISE** ...................................... 4
- Informations générales
- Équipe dirigeante
- Analyse SWOT

**III. OFFRE DE PRODUITS ET SERVICES** .................................... 6
- Description de l'offre
- Proposition de valeur
- Innovation

**IV. ÉTUDE DE MARCHÉ** ................................................... 8
- Analyse du marché
- Concurrence
- Positionnement

**V. STRATÉGIE MARKETING** ................................................ 10
- Plan marketing
- Politique commerciale

**VI. ORGANISATION ET PRODUCTION** ........................................ 12
- Moyens de production
- Ressources humaines

**VII. ANALYSE DES RISQUES** .............................................. 14
- Identification des risques
- Mesures d'atténuation

**VIII. PLAN FINANCIER** .................................................. 16
- Projections financières
- Besoins de financement

**IX. ANNEXES** ........................................................... 18
        """,

        "Résumé Exécutif": """
Rédigez DIRECTEMENT le résumé exécutif sans commentaires.

IMPORTANT: Générez SEULEMENT le contenu final structuré.

Format de sortie:

# I. RÉSUMÉ EXÉCUTIF

## Vue d'ensemble du projet

[Rédigez 4-5 phrases décrivant l'entreprise, son activité principale, sa mission et sa valeur ajoutée]

## Opportunité de marché

[Rédigez 4-5 phrases sur le marché visé, la demande identifiée et l'avantage concurrentiel]

## Projections financières

[Rédigez 3-4 phrases sur les projections de CA, rentabilité et besoins de financement]

## Équipe et facteurs de succès

[Rédigez 3-4 phrases sur les compétences de l'équipe et les atouts clés]

**Montant recherché:** [Montant selon contexte]
**Objectif:** [Objectif selon contexte]
**Retour attendu:** [ROI selon contexte]
        """,

        "Présentation de votre entreprise": """
Rédigez DIRECTEMENT la présentation de l'entreprise. Aucun commentaire.

Format de sortie:

# II. PRÉSENTATION DE L'ENTREPRISE

## 1. Informations générales

**Raison sociale:** [Nom complet]
**Forme juridique:** [SARL, SA, etc.]
**Siège social:** [Adresse, RDC]
**Secteur d'activité:** [Secteur précis]
**Date de création:** [Date]

## 2. Mission et vision

**Mission:** [Une phrase claire sur la raison d'être]

**Vision:** [Une phrase sur l'ambition long terme]

**Valeurs:** [3-5 valeurs fondamentales]

## 3. Historique et développement

[Paragraphe de 3-4 phrases sur l'origine, étapes importantes et stade actuel]

## 4. Équipe dirigeante

**Dirigeant Principal:**
- Nom et fonction
- Formation et expérience
- Responsabilités

## 5. Analyse SWOT

| Forces | Faiblesses |
|--------|-----------|
| [Force 1] | [Faiblesse 1] |
| [Force 2] | [Faiblesse 2] |

| Opportunités | Menaces |
|-------------|---------|
| [Opportunité 1] | [Menace 1] |
| [Opportunité 2] | [Menace 2] |

## 6. Objectifs stratégiques

**Court terme (1 an):** [Objectifs précis]
**Moyen terme (3 ans):** [Objectifs précis]  
**Long terme (5 ans):** [Objectifs précis]
        """,

        "Présentation de l'offre de produit": """
Rédigez DIRECTEMENT la présentation de l'offre. Aucun commentaire.

Format de sortie:

# III. PRÉSENTATION DE L'OFFRE

## 1. Description des produits/services

[Paragraphe détaillé décrivant l'offre principale]

## 2. Besoins identifiés sur le marché

[Paragraphe sur les problèmes résolus et besoins satisfaits]

## 3. Proposition de valeur unique

[Paragraphe sur les avantages différenciateurs et bénéfices clients]

## 4. Innovation et avantages technologiques

[Paragraphe sur les innovations, technologies et propriété intellectuelle]

## 5. Impact social et environnemental

[Paragraphe sur l'impact positif et la durabilité]
        """,

        "Étude de marché": """
Rédigez DIRECTEMENT l'étude de marché. Aucun commentaire.

Format de sortie:

# IV. ÉTUDE DE MARCHÉ

## 1. Description du marché

[Paragraphe sur le marché global, taille et caractéristiques]

## 2. Analyse de la demande

[Paragraphe sur la demande actuelle, évolution et segments de clientèle]

## 3. Analyse concurrentielle

[Paragraphe sur les concurrents directs/indirects et positionnement]

## 4. Opportunités et tendances

[Paragraphe sur les opportunités identifiées et tendances du marché]

## 5. Stratégie de pénétration

[Paragraphe sur l'approche pour capturer des parts de marché]
        """,

        "Stratégie Marketing": """
Rédigez DIRECTEMENT la stratégie marketing. Aucun commentaire.

Format de sortie:

# V. STRATÉGIE MARKETING

## 1. Segmentation et ciblage

[Paragraphe sur les segments choisis et justification du ciblage]

## 2. Positionnement

[Paragraphe sur le positionnement souhaité et message clé]

## 3. Marketing-mix (4P)

**Produit:** [Stratégie produit]
**Prix:** [Stratégie tarifaire]
**Place:** [Stratégie distribution]
**Promotion:** [Stratégie communication]

## 4. Plan d'actions marketing

[Tableau ou liste des actions marketing par période]

## 5. Budget marketing

[Paragraphe sur l'allocation budgétaire et ROI attendu]
        """,

        "Moyens de production et organisation": """
Rédigez DIRECTEMENT l'organisation opérationnelle. Aucun commentaire.

Format de sortie:

# VI. MOYENS DE PRODUCTION ET ORGANISATION

## 1. Locaux et infrastructure

[Paragraphe sur les locaux, localisation et aménagements]

## 2. Équipements et matériel

[Paragraphe sur les équipements nécessaires et investissements]

## 3. Ressources humaines

[Paragraphe sur l'organigramme, postes et compétences]

## 4. Processus opérationnels

[Paragraphe sur les processus de production/prestation]

## 5. Fournisseurs et partenaires

[Paragraphe sur la chaîne d'approvisionnement et partenariats]
        """,

        "Étude des risques": """
Rédigez DIRECTEMENT l'analyse des risques. Aucun commentaire.

Format de sortie:

# VII. ANALYSE DES RISQUES

## 1. Identification des risques

| Type de risque | Description | Probabilité | Impact |
|---------------|-------------|-------------|---------|
| Risque marché | [Description] | [Faible/Moyen/Élevé] | [Faible/Moyen/Élevé] |
| Risque opérationnel | [Description] | [Faible/Moyen/Élevé] | [Faible/Moyen/Élevé] |
| Risque financier | [Description] | [Faible/Moyen/Élevé] | [Faible/Moyen/Élevé] |

## 2. Mesures d'atténuation

[Paragraphe sur les stratégies de réduction des risques]

## 3. Plan de contingence

[Paragraphe sur les plans d'urgence et alternatives]

## 4. Assurances et garanties

[Paragraphe sur les couvertures d'assurance prévues]
        """,

        "Plan financier": """
Rédigez DIRECTEMENT le plan financier. Aucun commentaire.

Format de sortie:

# VIII. PLAN FINANCIER

## 1. Besoins de financement

**Investissements initiaux:** [Montant]
**Fonds de roulement:** [Montant]
**Total besoins:** [Montant]

## 2. Sources de financement

**Apports propres:** [Montant et %]
**Emprunts bancaires:** [Montant et conditions]
**Subventions:** [Montant et organismes]

## 3. Projections financières

[Intégrer ici les tableaux financiers générés par le système]

## 4. Analyse de rentabilité

**Seuil de rentabilité:** [Montant et délai]
**ROI attendu:** [Pourcentage]
**Délai de récupération:** [Période]
        """,

        "Annexes": """
Rédigez DIRECTEMENT la section annexes. Aucun commentaire.

Format de sortie:

# IX. ANNEXES

## Documents joints

- Étude de marché détaillée
- CV des dirigeants
- Lettres d'intention de clients
- Devis d'équipements
- Autorisations et licences
- Projections financières détaillées

## Contacts utiles

**Entreprise:** [Coordonnées complètes]
**Conseil juridique:** [Si applicable]
**Expert-comptable:** [Si applicable]

## Références

[Liste des sources utilisées pour l'étude de marché et projections]
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