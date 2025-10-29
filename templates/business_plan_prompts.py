"""
Prompts système EXACTS copiés de la stratégie Origin.txt
Adaptés pour les templates RDC avec contenu professionnel direct
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

def get_system_prompts_origin() -> Dict[str, str]:
    """
    Prompts système EXACTS copiés de Origin.txt avec adaptations pour templates RDC
    """
    return {
        "Couverture": """
Générer cette section du business plan:
Voici les textes à afficher sous forme :

# Canevas de Plans d'Affaires

Nom du projet ou entreprise

République Démocratique du Congo

Date: [Date actuelle]

Contact: [Informations de contact de l'entreprise]

Document confidentiel
        """,

        "Sommaire": """
Générer cette section du business plan:
Voici les textes à afficher sous forme de liste:

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
- Attirer l'attention du lecteur en 5 minutes et lui donner envie d'en savoir plus.
- Décrire le projet en quelques phrases simples et impactantes.
- Ne pas essayer de tout couvrir, soyez concis et précis.

Les éléments clés à générer et qui doivent être contenus dans les paragraphes:
- **Présentation de la PME** : Nom de l'entreprise et brève description du service/produit fourni.
- **Présentation des porteurs de projet** : Nom, prénom, coordonnées, situation de famille, formation et diplômes, expérience professionnelle, activités extra ou para-professionnelles.
- **Potentiel en termes de taille et de profit** : Démontrez par des calculs simples comment votre PME fera du profit.
- **Votre besoin financier**.
        """,

        "Présentation de votre entreprise": """
Générer cette section du business plan:

## II. Présentation de votre entreprise/projet

Générer 6 grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
- Parler de votre entreprise/projet de manière plus détaillée.
- Présenter l'équipe managériale clé.

Les éléments clés à générer et qui doivent être contenus dans les paragraphes:
- **Informations générales sur la PME** :
  - Forme juridique : Ets, Sarlu, Sarl, SAS, SA.
  - Siège social : Adresse juridique de l'entreprise.
  - Coordonnées bancaires : Numéro de compte de l'entreprise ainsi que la banque.
  - Couverture géographique de l'entreprise et ses activités : lieu d'implantation de l'entreprise et différentes zones couvertes.
- **Description détaillée de la PME et objectifs de son projet** : Présentez l'entreprise, son origine, introduisez ses atouts/opportunités et enfin décrivez le projet de l'entreprise.
- **Stade d'avancement de l'entreprise ou du projet** :
  - Décrivez ce qui a été fait et les projets à mener dans le futur.
  - Parlez du niveau de maturité de la PME ou du projet.
  - Listez éventuellement les financements déjà acquis.
- **Présentation de l'équipe managériale** : Décrivez l'organigramme et l'organisation des ressources humaines, présentez les associés de la PME ainsi que leurs parts sociales.
- **Analyse SWOT** : Forces, faiblesses, opportunités, contraintes/menaces. De préférence cela doit être présenté sous forme de tableau.
- **Business Modèle Canvas** : Insérez votre business modèle canvas avec les 9 rubriques bien remplies.
        """,

        "Présentation de l'offre de produit": """
Générer cette section du business plan :

## III. Présentation de l'offre de produit(s) et/ou service(s)

Générer 6 grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
- Parler de l'offre de produits/services de manière détaillée.
- Présenter la proposition de valeur différenciante de la PME ou de son offre.

Les éléments clés à générer et qui doivent être contenus dans les paragraphes:
- **Noms du/des produit(s) ou service(s)**.
- **Besoins identifiés** sur le marché auxquels répond votre offre.
- **Description du/des produit(s) ou service(s)** répondant à ces besoins.
- **Proposition de valeur unique**.
- **Prise en compte de l'aspect genre** dans le fonctionnement de la PME ou du projet de l'entreprise.
- **Prise en compte de l'environnement** :
  - Identification des impacts environnementaux et sociaux des activités de la PME.
  - Mise en place de mesures d'atténuation.
  - Existence d'un Plan de Gestion Environnemental et Social.
        """,

        "Étude de marché": """
Générer cette section du business plan :

## IV. Étude de marché

Générer 8 grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
- Expliquer la méthode utilisée pour la conduite de l'étude de marché.
- Présenter les résultats de l'étude de marché.

Les éléments clés à générer et qui doivent être contenus dans les paragraphes, les numéros doivent être respectés:
1. **Description des hypothèses et méthodes de l'étude de marché** :
   - Produit/service pré-ciblé.
   - Marché pré-ciblé.
   - Secteur d'activité concerné.
   - Méthodologie de recherche adoptée (questionnaires, études documentaires, etc.).

2. **Approche générale du marché** :
   - Description du marché et ses caractéristiques.
   - Historique et évolution du marché/secteur.
   - Taille du marché (marché cible, marché potentiel, marché réel).

3. **Caractéristiques de la demande** :
   - Volume et évolution de la demande.
   - Identification et analyse des prescripteurs.

4. **Caractéristiques de l'offre** :
   - Concurrence directe et indirecte.
   - Forces et faiblesses de la concurrence.

5. **Environnement des affaires** :
   - Cadre légal et réglementaire.
   - Facteurs économiques exogènes.

6. **Partenariats et autres** :
   - Fournisseurs.
   - Partenaires de distribution.
   - Autres partenaires.

7. **Création d'emplois** :
   - Emplois directs créés/à créer.
   - Emplois indirects.

8. **Projections du chiffre d'affaires** :
   - Estimation du chiffre d'affaires.
   - Hypothèses de calcul.
        """,

        "Stratégie Marketing": """
Générer cette section du business plan :

## V. Stratégie marketing, communication et politique commerciale

Générer 4 grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
- Définir la stratégie marketing de la PME.
- Présenter la politique commerciale de la PME.

Les éléments clés à générer et qui doivent être contenus dans les paragraphes:
1. **Choix de segments de clientèle** :
   - Segments retenus.
   - Critères de segmentation.
   - Justification du ciblage.

2. **Marketing-mix (4P)** :
   - **Politique de Produit** : Gamme, niveau de qualité et de service.
   - **Politique de Prix** : Méthode de fixation, niveau de prix.
   - **Politique de Place** : Circuit de distribution.
   - **Politique de Promotion** : Actions de communication.

3. **Plan marketing et actions commerciales** :
   - Planning des actions marketing.
   - Budget et calendrier.

4. **Moyens et partenaires sollicités** :
   - Ressources nécessaires.
   - Partenaires identifiés.
        """,

        "Moyens de production et organisation": """
Générer cette section du business plan :

## VI. Moyens de production et organisation

Générer 4 grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
- Décrire les moyens de production nécessaires.
- Présenter l'organisation de la PME.

Les éléments clés à générer et qui doivent être contenus dans les paragraphes:
1. **Locaux et infrastructure** :
   - Description des locaux.
   - Localisation et justification.
   - Coûts d'installation.

2. **Équipements et matériel** :
   - Liste des équipements nécessaires.
   - Coûts d'acquisition.
   - Mode de financement.

3. **Ressources humaines et organisation** :
   - Organigramme.
   - Profils de postes.
   - Coûts salariaux.

4. **Fournisseurs et sous-traitants** :
   - Identification des fournisseurs.
   - Conditions négociées.
   - Plan d'approvisionnement.
        """,

        "Étude des risques": """
Générer cette section du business plan :

## VII. Étude des risques et hypothèses

Générer un tableau complet des risques suivi de 2 paragraphes, l'objectif pour cette section est de :
- Identifier tous les risques liés au projet.
- Proposer des mesures d'atténuation.

Générer un tableau avec les colonnes suivantes:
| Nature du risque | Description | Probabilité | Impact | Mesures d'atténuation |

Inclure au minimum ces catégories de risques:
- Risques liés à l'environnement général
- Risques liés au marché
- Risques liés aux outils de production
- Risques liés aux personnes
- Risques liés aux tiers
- Autres risques spécifiques

Puis générer 2 paragraphes sur :
1. **Plan de gestion des risques** : Procédures de suivi et de contrôle.
2. **Mesures préventives** : Actions proactives pour réduire les risques.
        """,

        "Plan financier": """
Générer cette section du business plan :

## VIII. Plan financier

Générer 4 grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
- Présenter les projections financières.
- Démontrer la viabilité financière du projet.

Les éléments clés à générer et qui doivent être contenus dans les paragraphes:
1. **Hypothèses financières** :
   - Hypothèses de chiffre d'affaires.
   - Hypothèses de coûts.
   - Hypothèses de financement.

2. **Compte de résultat prévisionnel** :
   - Chiffre d'affaires prévisionnel sur 3-5 ans.
   - Charges variables et fixes.
   - Résultat net prévisionnel.

3. **Plan de financement** :
   - Besoins de financement.
   - Sources de financement.
   - Échéancier de remboursement.

4. **Indicateurs de rentabilité** :
   - Seuil de rentabilité.
   - Retour sur investissement.
   - Capacité d'autofinancement.

[Insérer ici les tableaux financiers détaillés générés par le système]
        """,

        "Annexes": """
Générer cette section du business plan :

## IX. Annexes

Générer une liste structurée des documents annexes, l'objectif pour cette section est de :
- Lister tous les documents justificatifs.
- Organiser les annexes de manière professionnelle.

Les éléments à inclure dans la liste:
- CV détaillés des dirigeants
- Études de marché complémentaires
- Devis d'équipements et de travaux
- Lettres d'intention de clients
- Contrats de partenariat
- Autorisations et licences
- États financiers
- Projections financières détaillées
- Business Model Canvas
- Analyse SWOT détaillée
- Photos et plans des locaux
- Références et attestations
        """
    }

def get_user_queries() -> Dict[str, str]:
    """
    Requêtes utilisateur exactes d'Origin.txt
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
    Contexte spécifique selon le template sélectionné - VERSION ORIGIN
    """
    contexts = {
        "COPA TRANSFORME": """
CONTEXTE COPA TRANSFORMÉ:
Vous travaillez dans le cadre du programme COPA TRANSFORMÉ pour l'autonomisation des femmes entrepreneures et la mise à niveau des PME en RDC.

Secteurs prioritaires: Agroalimentaire, Industrie légère, Artisanat, Services à valeur ajoutée
Objectifs: Création d'emplois, autonomisation des femmes, transformation économique
Approche: Développement inclusif, partenariats locaux, innovation sociale

INSTRUCTIONS SPÉCIALES COPA TRANSFORMÉ:
- Mettez l'accent sur l'autonomisation des femmes dans chaque section
- Intégrez les aspects de développement durable et d'impact social
- Valorisez les chaînes de valeur agricoles et agroalimentaires
- Considérez les partenariats avec les coopératives et organisations locales
        """,
        
        "Virunga": """
CONTEXTE VIRUNGA:
Vous travaillez dans le cadre des initiatives de conservation et développement durable du Parc National des Virunga.

Secteurs prioritaires: Écotourisme, Agriculture durable, Énergies renouvelables, Conservation
Objectifs: Conservation environnementale, développement communautaire, paix et sécurité
Approche: Développement durable, protection environnementale, engagement communautaire

INSTRUCTIONS SPÉCIALES VIRUNGA:
- Priorisez les aspects de conservation environnementale
- Intégrez les enjeux de paix et sécurité dans la région
- Valorisez l'écotourisme et les activités respectueuses de l'environnement
- Considérez l'impact sur les communautés locales et la biodiversité
        """,
        
        "IP Femme": """
CONTEXTE IP FEMME:
Vous travaillez dans le cadre d'initiatives d'autonomisation économique des femmes en RDC.

Secteurs prioritaires: Commerce, Services, Artisanat, Agriculture, Microfinance
Objectifs: Égalité de genre, autonomisation économique, leadership féminin
Approche: Empowerment des femmes, inclusion financière, renforcement de capacités

INSTRUCTIONS SPÉCIALES IP FEMME:
- Placez les femmes au centre de toutes les analyses
- Intégrez systématiquement la perspective genre
- Valorisez le leadership féminin et l'inclusion financière
- Considérez les défis spécifiques aux entrepreneures en RDC
        """
    }
    
    return contexts.get(template_name, contexts["COPA TRANSFORME"])

# Fonctions de compatibilité avec le nouveau système
def get_business_plan_system_messages(template_name: str) -> Dict[str, str]:
    """Version adaptée pour un template spécifique avec contexte intégré"""
    base_prompts = get_system_prompts_origin()
    context_template = get_business_plan_context_template(template_name)
    
    adapted_prompts = {}
    for section, prompt in base_prompts.items():
        # Intégrer le contexte du template dans chaque prompt
        adapted_prompts[section] = f"{context_template}\n\n{prompt}"
    
    return adapted_prompts

def get_business_plan_user_queries(template_name: str) -> Dict[str, str]:
    """Version adaptée pour un template spécifique"""
    return get_user_queries()

def get_sections_configuration(template_name: str) -> Dict[str, Dict[str, str]]:
    """Configuration complète des sections pour un template donné - VERSION ORIGIN"""
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