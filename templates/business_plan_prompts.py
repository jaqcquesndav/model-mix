"""
Système de prompts EXACTEMENT basé sur Origin.txt
Adapté pour les templates RDC (COPA TRANSFORME, Virunga, IP Femme)
"""

from typing import Dict, Any

def get_system_messages_origin_style(template_name: str = "COPA TRANSFORME") -> Dict[str, str]:
    """
    Messages système EXACTS de Origin.txt adaptés pour templates RDC
    """
    
    # Contexte spécifique selon le template
    template_context = get_template_context(template_name)
    
    return {
        "Couverture": f"""
            Générer cette section du business plan pour le template {template_name}:
            Voici les textes à afficher sous forme :
            
            # Canevas de Plans d'Affaires
            ## Template {template_name}

            Nom du projet ou entreprise
            Secteur d'activité
            République Démocratique du Congo
            
            {template_context}
        """,
        
        "Sommaire": f"""
            Générer cette section du business plan pour le template {template_name}:
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
        
        "Résumé Exécutif": f"""
            Générer cette section du business plan pour le template {template_name}:
            
            ## I. Résumé Exécutif « Executive Summary » / Pitch
            
            Générer deux grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
            - Attirer l'attention du lecteur en 5 minutes et lui donner envie d'en savoir plus.
            - Décrire le projet en quelques phrases simples et impactantes.
            - Ne pas essayer de tout couvrir, soyez concis et précis.
            
            Les éléments clés à générer et qui doivent être contenus dans les paragraphes :
            - **Présentation de la PME** : Nom de l'entreprise et brève description du service/produit fourni.
            - **Présentation des porteurs de projet** : Profil des entrepreneurs, formation, expérience.
            - **Potentiel en termes de taille et de profit** : Démontrez par des calculs simples comment votre PME fera du profit.
            - **Votre besoin financier** : Montant recherché et utilisation.
            
            Contexte spécifique {template_name} : {template_context}
            
            Rédigez directement les paragraphes sans explications additionnelles.
        """,
        
        "Présentation de votre entreprise": f"""
            Générer cette section du business plan pour le template {template_name}:

            ## II. Présentation de votre entreprise/projet

            Générer 6 grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
            - Parler de votre entreprise/projet de manière plus détaillée.
            - Présenter l'équipe managériale clé.

            Les éléments clés à générer et qui doivent être contenus dans les paragraphes :
            
            **1. Informations générales sur la PME** :
            - Forme juridique : Ets, Sarlu, Sarl, SAS, SA
            - Siège social : Adresse juridique de l'entreprise en RDC
            - Coordonnées bancaires : Numéro de compte de l'entreprise
            - Couverture géographique : lieu d'implantation et zones couvertes
            
            **2. Description détaillée de la PME et objectifs** :
            - Présentez l'entreprise, son origine, ses atouts/opportunités
            - Décrivez le projet spécifique à {template_name}
            
            **3. Stade d'avancement de l'entreprise** :
            - Ce qui a été fait et projets futurs
            - Niveau de maturité de la PME
            - Financements déjà acquis
            
            **4. Présentation de l'équipe managériale** :
            - Organigramme et organisation RH
            - Associés et parts sociales
            
            **5. Analyse SWOT** (à présenter sous forme de tableau) :
            - Forces, faiblesses, opportunités, contraintes/menaces
            
            **6. Business Model Canvas** :
            - Les 9 rubriques bien remplies selon {template_name}
            
            Contexte {template_name} : {template_context}
            
            Rédigez directement les paragraphes sans explications.
        """,
        
        "Présentation de l'offre de produit": f"""
            Générer cette section du business plan pour le template {template_name} :

            ## III. Présentation de l'offre de produit(s) et/ou service(s)
            
            Générer 6 grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
            - Parler de l'offre de produits/services de manière détaillée.
            - Présenter la proposition de valeur différenciante selon {template_name}.

            Les éléments clés à générer et qui doivent être contenus dans les paragraphes :
            
            **1. Noms du/des produit(s) ou service(s)** adaptés au contexte {template_name}
            
            **2. Besoins identifiés** sur le marché auxquels répond votre offre
            
            **3. Description du/des produit(s) ou service(s)** répondant à ces besoins
            
            **4. Proposition de valeur unique** selon les spécificités {template_name}
            
            **5. Prise en compte de l'aspect genre** dans le fonctionnement de la PME
            
            **6. Prise en compte de l'environnement** :
            - Identification des impacts environnementaux et sociaux
            - Mesures d'atténuation mises en place
            - Plan de Gestion Environnemental et Social
            
            Contexte {template_name} : {template_context}
            
            Rédigez directement les paragraphes détaillés sans explications.
        """,
        
        "Étude de marché": f"""
            Générer cette section du business plan pour le template {template_name} :

            ## IV. Étude de marché

            Générer 8 grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
            - Expliquer la méthode utilisée pour la conduite de l'étude de marché.
            - Présenter les résultats de l'étude de marché.

            Les éléments clés à générer et qui doivent être contenus dans les paragraphes, les numéros doivent être respectés :
            
            **1. Description des hypothèses et méthodes de l'étude de marché** :
            - Citer le produit ou service pré-ciblé
            - Préciser le marché pré-ciblé : secteur d'activité 
            - Présenter les méthodes : questionnaire, étude documentaire, etc.

            **2. Approche générale du marché** (précisez les sources) :
            - Décrire le marché, caractéristiques, historique, perspectives
            - Présenter les résultats : marché cible, potentiel, réel
            - Menaces et opportunités du marché

            **3. Caractéristiques de la demande** :
            - Volume et évolution de la demande
            - Tendances de consommation en RDC
            - Types de clientèle (segmentation)
            - Prescripteurs et partenaires

            **4. Caractéristiques de l'offre** :
            - Concurrence directe et indirecte
            - Points forts/faibles de la concurrence
            - Différenciation par rapport aux concurrents

            **5. Caractéristiques de l'environnement** :
            - Environnement des affaires en RDC
            - Cadre légal, réglementaire
            - Évolution des technologies
            - Menaces et opportunités

            **6. Partenariats** :
            - Partenariats stratégiques selon {template_name}
            - Fournisseurs, distributeurs, partenaires commerciaux

            **7. Création d'emplois** :
            - Impact en emplois directs créés ou à créer
            - Spécificités {template_name} en matière d'emploi

            **8. Chiffre d'affaires** :
            - Part de marché visée
            - Volume de CA prévisible à 1, 2, 3 ans
            
            Contexte {template_name} : {template_context}
            
            Rédigez directement les paragraphes détaillés avec données chiffrées.
        """,
        
        "Stratégie Marketing": f"""
            Générer cette section du business plan pour le template {template_name} :

            ## V. Stratégie Marketing, Communication et Politique Commerciale

            Générer cette section complète, l'objectif est de :
            - Présenter la stratégie marketing et commerciale à court et moyen terme selon {template_name}.

            Les éléments clés à générer, les numéros doivent être respectés :
            
            **1. Choix de segments de clientèle** :
            - Segments de clientèle cibles pour {template_name}
            - Justification de ce choix
            - Positionnement stratégique

            **2. Marketing-mix (4P : Produit – Prix – Place – Promotion)** :
            - Politique marketing générale :
                - Choix du nom, logo, couleurs
                - Message et slogan adaptés à {template_name}
            
            - Tableau synthétique des segments :

            | Segment de clientèle | Produit proposé | Positionnement prix | Lieu de distribution | Communication |
            |---------------------|-----------------|--------------------|--------------------|---------------|
            | Segment 1           | [À remplir]     | [À remplir]        | [À remplir]        | [À remplir]   |
            | Segment 2           | [À remplir]     | [À remplir]        | [À remplir]        | [À remplir]   |
            | Segment 3           | [À remplir]     | [À remplir]        | [À remplir]        | [À remplir]   |

            **3. Plan Marketing et actions commerciales** :
            - Lister les actions commerciales et communication prévues avec coûts

            | Types d'actions | Jan | Fév | Mar | Avr | Mai | Jun | Jul | Aoû | Sep | Oct | Nov | Déc |
            |-----------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
            | Action 1        |     |     |     |     |     |     |     |     |     |     |     |     |
            | Action 2        |     |     |     |     |     |     |     |     |     |     |     |     |

            **4. Moyens et partenaires sollicités** :
            - Moyens à mettre en œuvre
            - Partenaires sollicités pour actions commerciales
            
            Contexte {template_name} : {template_context}
            
            Rédigez directement le contenu avec tableaux remplis.
        """,
        
        "Moyens de production et organisation": f"""
            Générer cette section du business plan pour le template {template_name}:

            ## VI. Moyens de production et organisation

            Générer 4 grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
            - Spécifier les moyens humains et matériels à disposition de la PME selon {template_name}.

            Les éléments clés à générer et qui doivent être contenus dans les paragraphes :
            
            **1. Locaux** :
            - Liste des locaux nécessaires
            - Bail de location, conditions négociées, coût
            - Utilité et aménagements spécifiques à {template_name}

            **2. Matériel** :
            - Liste détaillée du matériel
            - Mode d'acquisition ou location, coût
            - Utilité pour les activités {template_name}
            - Plan de renouvellement

            **3. Moyens humains** :
            - Personnel nécessaire, plannings, horaires
            - Coût salarial et charges sociales en RDC
            - Répartition claire des tâches selon {template_name}

            **4. Fournisseurs et sous-traitants** :
            - Liste des fournisseurs principaux
            - Devis obtenus, tarifs, conditions négociées
            - Spécificités d'approvisionnement pour {template_name}
            
            Contexte {template_name} : {template_context}
            
            Rédigez directement les paragraphes détaillés avec coûts estimés.
        """,
        
        "Étude des risques": f"""
            Générer cette section du business plan pour le template {template_name}:

            ## VII. Étude des risques/hypothèses

            Générer cette section complète, l'objectif pour cette section est de :
            - Présenter la synthèse des risques et mesures d'atténuation identifiés pour le développement de la PME selon {template_name}.

            Les éléments clés à générer :
            
            **Tableau des risques** détaillé :

            | Nature de risque | Description détaillée | Stratégie de traitement |
            |------------------|----------------------|-------------------------|
            | Risques liés à l'environnement général | Instabilité politique RDC, inflation, change | [Stratégies spécifiques] |
            | Risques liés au marché | Concurrence, évolution demande, saisonnalité | [Stratégies spécifiques] |
            | Risques liés aux outils | Pannes équipement, obsolescence technologique | [Stratégies spécifiques] |
            | Risques liés aux personnes | Départ personnel clé, formation insuffisante | [Stratégies spécifiques] |
            | Risques liés aux tiers | Défaillance fournisseurs, impayés clients | [Stratégies spécifiques] |
            | Risques spécifiques {template_name} | [Risques particuliers au template] | [Stratégies adaptées] |

            **Analyse détaillée des risques** avec :
            - Probabilité d'occurrence (Faible/Moyenne/Élevée)
            - Impact sur l'activité (Faible/Moyen/Élevé)
            - Mesures préventives et correctives
            - Plan de contingence pour chaque risque majeur
            
            Contexte {template_name} : {template_context}
            
            Rédigez directement l'analyse complète avec tableau rempli.
        """,
        
        "Annexes": f"""
            Générer cette section du business plan pour le template {template_name}:
            
            ## VIII. ANNEXES

            Renvoyer en annexe les documents trop volumineux ou difficiles à lire :
            - Étude de marché complète
            - Contrats et conventions
            - Conditions générales
            - CV détaillés de l'équipe dirigeante
            - Études techniques spécialisées
            - Autorisations et licences
            - Documents financiers détaillés
            - Références et recommandations
            
            **Documents spécifiques {template_name}** :
            {template_context}
            
            **Liste des annexes jointes** :
            1. [Document 1]
            2. [Document 2]
            3. [Document 3]
            
            Rédigez directement la liste des annexes pertinentes.
        """
    }

def get_queries_origin_style() -> Dict[str, str]:
    """
    Requêtes EXACTES de Origin.txt
    """
    return {
        "Couverture": "Afficher seulement le texte fourni",
        "Sommaire": "Afficher seulement le texte fourni",
        "Résumé Exécutif": "Décrire brièvement le projet, son potentiel de profit et les qualifications de l'équipe.",
        "Présentation de votre entreprise": "Fournir une analyse détaillée de l'entreprise, incluant son origine, ses objectifs et son organisation.",
        "Présentation de l'offre de produit": "Décrire les produits ou services, leur proposition de valeur unique, et les besoins du marché qu'ils adressent.",
        "Étude de marché": "Analyser le marché cible, les tendances de consommation, et la concurrence directe et indirecte.",
        "Stratégie Marketing": "Décrire la stratégie marketing, y compris les segments cibles, le positionnement, le mix marketing et les actions commerciales prévues.",
        "Moyens de production et organisation": "Décrire les moyens humains et matériels, ainsi que l'organisation opérationnelle de l'entreprise.",
        "Étude des risques": "Identifier les risques potentiels et proposer des stratégies pour les atténuer.",
        "Annexes": "Inclure tous les documents annexes pertinents pour étayer le plan d'affaires."
    }

def get_template_context(template_name: str) -> str:
    """
    Contexte spécifique pour chaque template
    """
    contexts = {
        "COPA TRANSFORME": """
            Secteurs prioritaires : Agroalimentaire, transformation agricole, chaînes de valeur
            Focus : Autonomisation des femmes, développement rural, sécurité alimentaire
            Zone géographique : Provinces agricoles de la RDC
            Partenaires : Coopératives agricoles, institutions de microfinance rurales
        """,
        
        "Virunga": """
            Secteurs prioritaires : Écotourisme, conservation, énergies renouvelables
            Focus : Développement durable, protection environnementale, paix
            Zone géographique : Région des Grands Lacs, Nord-Kivu
            Partenaires : ONG de conservation, communautés locales, autorités parcs
        """,
        
        "IP Femme": """
            Secteurs prioritaires : Services, commerce, artisanat, microfinance
            Focus : Autonomisation économique des femmes, leadership féminin
            Zone géographique : Zones urbaines et péri-urbaines de la RDC
            Partenaires : Associations féminines, institutions de microfinance, centres de formation
        """
    }
    
    return contexts.get(template_name, contexts["COPA TRANSFORME"])

def get_sections_configuration_origin_style(template_name: str) -> Dict[str, Dict[str, str]]:
    """
    Configuration complète Origin.txt pour un template donné
    """
    system_messages = get_system_messages_origin_style(template_name)
    queries = get_queries_origin_style()
    
    sections = {
        "Couverture": "Page de couverture du business plan",
        "Sommaire": "Table des matières structurée", 
        "Résumé Exécutif": "Executive summary professionnel",
        "Présentation de votre entreprise": "Présentation détaillée de l'entreprise",
        "Présentation de l'offre de produit": "Description de l'offre produits/services",
        "Étude de marché": "Analyse complète du marché cible",
        "Stratégie Marketing": "Plan marketing et commercial détaillé",
        "Moyens de production et organisation": "Ressources et organisation opérationnelle",
        "Étude des risques": "Analyse des risques et mesures d'atténuation",
        "Annexes": "Documents complémentaires"
    }
    
    configuration = {}
    for section_name, description in sections.items():
        configuration[section_name] = {
            "description": description,
            "system_message": system_messages.get(section_name, "Message système non disponible"),
            "query": queries.get(section_name, "Requête non disponible"),
            "template_context": get_template_context(template_name)
        }
    
    return configuration