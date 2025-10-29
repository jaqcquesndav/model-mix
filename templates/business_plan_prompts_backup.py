"""
Prompts système détaillés pour la génération de business plans professionnels
Basés sur l'approche sophistiquée d'Origin.txt avec adaptation pour les templates RDC

COMPATIBILITÉ : Ce module coexiste avec l'ancien système template_manager.py
- business_plan_prompts.py : Système de génération de business plans complets
- template_manager.py : Système de templates pour métaprompts et contextes généraux
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
    Prompts système détaillés pour chaque section du business plan
    Inspirés d'Origin.txt et adaptés pour le contexte RDC
    """
    return {
        "Couverture": """
            Vous êtes un rédacteur de business plans professionnels. Générez UNIQUEMENT le contenu de la page de couverture.

            INSTRUCTION CRITIQUE : Ne donnez AUCUNE explication, commentaire ou conseil. Générez SEULEMENT le contenu final formaté.

            Format de sortie requis (utilisez exactement cette structure) :

            # PLAN D'AFFAIRES

            ## [Utiliser le nom de l'entreprise fourni]

            **Secteur d'activité :** [Déduire du contexte]
            **Localisation :** République Démocratique du Congo
            **Date :** [Date actuelle]

            ---

            ### PORTEURS DU PROJET
            - **Dirigeant Principal :** [À compléter selon contexte]
            - **Équipe :** [À compléter selon contexte]
            - **Contact :** [informations@entreprise.cd]

            ---

            ### RÉSUMÉ EXÉCUTIF
            [Une phrase décrivant l'activité principale]
            [Une phrase sur l'objectif commercial]

            ---

            **Document confidentiel - Usage strictement professionnel**
        """,

        "Sommaire": """
            Vous êtes un rédacteur de business plans professionnels. Générez UNIQUEMENT le sommaire structuré.

            INSTRUCTION CRITIQUE : Ne donnez AUCUNE explication. Générez SEULEMENT la table des matières numérotée.

            Format de sortie requis :

            # SOMMAIRE

            **I. RÉSUMÉ EXÉCUTIF**
            - Présentation du projet
            - Objectifs et vision
            - Demande de financement

            **II. PRÉSENTATION DE L'ENTREPRISE**
            - Informations générales
            - Équipe dirigeante
            - Analyse SWOT

            **III. OFFRE DE PRODUITS ET SERVICES**
            - Description de l'offre
            - Proposition de valeur
            - Innovation et différenciation

            **IV. ÉTUDE DE MARCHÉ**
            - Analyse du marché cible
            - Concurrence
            - Positionnement

            **V. STRATÉGIE MARKETING**
            - Plan marketing
            - Politique commerciale
            - Communication

            **VI. ORGANISATION ET PRODUCTION**
            - Moyens de production
            - Ressources humaines
            - Processus opérationnels

            **VII. ANALYSE DES RISQUES**
            - Identification des risques
            - Mesures d'atténuation
            - Plan de contingence

            **VIII. PLAN FINANCIER**
            - Projections financières
            - Besoins de financement
            - Rentabilité prévisionnelle

            **IX. ANNEXES**
            - Documents complémentaires
            
            ### RÉSUMÉ FINANCIER
            - **Investissement total :** [Montant] USD
            - **Chiffre d'affaires prévisionnel (Année 1) :** [Montant] USD
            - **Emplois créés :** [Nombre] postes
            
            ---
            
            *Document confidentiel - Ne pas reproduire sans autorisation*
        """,
            - Adaptez au contexte économique de la RDC
        """,
        
        "Sommaire": """
            Générez un sommaire structuré et professionnel pour un business plan adapté au contexte RDC :
            
            ## SOMMAIRE
            
            **I. Résumé Exécutif** .................................................... 3
            
            **II. Présentation de l'entreprise/projet** ............................. 5
            - 2.1 Informations générales sur l'entreprise
            - 2.2 Description détaillée et objectifs du projet  
            - 2.3 Stade d'avancement
            - 2.4 Équipe managériale
            - 2.5 Analyse SWOT
            - 2.6 Business Model Canvas
            
            **III. Présentation de l'offre de produits et/ou services** ............. 12
            - 3.1 Description de l'offre
            - 3.2 Besoins identifiés sur le marché
            - 3.3 Proposition de valeur unique
            - 3.4 Prise en compte de l'aspect genre
            - 3.5 Impact environnemental et social
            
            **IV. Étude de marché** ................................................. 18
            - 4.1 Méthodologie de l'étude
            - 4.2 Approche générale du marché
            - 4.3 Analyse de la demande
            - 4.4 Analyse de l'offre et concurrence
            - 4.5 Environnement des affaires
            - 4.6 Partenariats stratégiques
            - 4.7 Création d'emplois
            - 4.8 Projections du chiffre d'affaires
            
            **V. Stratégie marketing, communication et politique commerciale** ....... 28
            - 5.1 Segmentation et ciblage
            - 5.2 Marketing-mix (4P)
            - 5.3 Plan marketing et actions commerciales
            - 5.4 Moyens et partenaires
            
            **VI. Moyens de production et organisation** ............................ 35
            - 6.1 Locaux et infrastructure
            - 6.2 Équipements et matériel
            - 6.3 Ressources humaines
            - 6.4 Fournisseurs et sous-traitants
            
            **VII. Étude des risques et hypothèses** ................................ 42
            - 7.1 Identification des risques
            - 7.2 Stratégies d'atténuation
            - 7.3 Plan de contingence
            
            **VIII. Plan financier** ................................................ 48
            - 8.1 Investissements et financements
            - 8.2 Compte de résultats prévisionnel
            - 8.3 Plan de trésorerie
            - 8.4 Analyse de rentabilité
            - 8.5 Projections sur 3 ans
            
            **IX. Annexes** ......................................................... 58
            - CV des porteurs de projet
            - Lettres d'intention
            - Études techniques
            - Documents juridiques
            
            Instructions :
            - Numérotez les pages de manière cohérente
            - Adaptez les sous-sections selon le type d'entreprise
            - Maintenez la structure professionnelle
        """,
        
        "Résumé Exécutif": """
            Vous êtes un expert en business plans. Rédigez DIRECTEMENT le résumé exécutif sans commentaires.

            INSTRUCTION CRITIQUE : Générez SEULEMENT le contenu final formaté. Aucune explication sur "comment rédiger" ou "voici un exemple".

            Format de sortie requis :

            # I. RÉSUMÉ EXÉCUTIF

            ## Vue d'ensemble du projet

            [Rédigez un paragraphe de 4-5 phrases décrivant précisément l'entreprise, son activité principale, sa mission et sa valeur ajoutée unique. Utilisez les informations fournies dans le contexte.]

            ## Opportunité de marché et positionnement

            [Rédigez un paragraphe de 4-5 phrases expliquant le marché visé, la demande identifiée, l'avantage concurrentiel et le positionnement stratégique.]

            ## Projections financières et besoins

            [Rédigez un paragraphe de 3-4 phrases présentant les projections de chiffre d'affaires, la rentabilité attendue et les besoins de financement avec utilisation prévue.]

            ## Équipe et facteurs de succès

            [Rédigez un paragraphe de 3-4 phrases présentant les compétences clés de l'équipe dirigeante et les principaux atouts pour réussir.]

            **Montant recherché :** [Préciser selon contexte]  
            **Objectif :** [Préciser selon contexte]  
            **Retour attendu :** [Préciser selon contexte]
            
            ### Éléments clés à intégrer obligatoirement :
            - **Nom et localisation de l'entreprise**
            - **Produit/service principal en une phrase claire**
            - **Marché cible et taille estimée**
            - **Avantage concurrentiel unique**
            - **Chiffres financiers clés (investissement, CA prévisionnel)**
            - **Nombre d'emplois à créer**
            - **Besoin de financement précis**
            
            ### Ton et style :
            - Professionnel mais accessible
            - Orienté résultats et impact
            - Adapté au contexte économique congolais
            - Convaincant pour investisseurs et bailleurs
            
            Instructions spéciales :
            - Rédigez en français de qualité professionnelle
            - Utilisez des données chiffrées précises quand disponibles
            - Mettez en avant l'impact socio-économique
            - Adaptez au secteur d'activité spécifique
        """,
        
        "Présentation de votre entreprise": """
            Rédigez DIRECTEMENT la présentation de l'entreprise. Aucune explication ou commentaire.

            INSTRUCTION CRITIQUE : Générez SEULEMENT le contenu final structuré.

            Format de sortie requis :

            # II. PRÉSENTATION DE L'ENTREPRISE

            ## 1. Informations générales

            **Raison sociale :** [Nom complet de l'entreprise]  
            **Forme juridique :** [SARL, SA, ETS, etc.]  
            **Siège social :** [Adresse complète, RDC]  
            **Secteur d'activité :** [Secteur précis]  
            **Date de création :** [Date]  

            ## 2. Mission et vision

            **Mission :** [Une phrase claire décrivant la raison d'être de l'entreprise]

            **Vision :** [Une phrase décrivant l'ambition à long terme]

            **Valeurs :** [3-5 valeurs fondamentales]

            ## 3. Historique et développement

            [Paragraphe de 3-4 phrases retraçant l'origine du projet, les étapes importantes et le stade actuel de développement]

            ## 4. Équipe dirigeante

            **Dirigeant Principal :**
            - Nom et fonction
            - Formation et expérience
            - Responsabilités principales

            **Équipe clé :** [Autres membres importants]

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

            **Court terme (1 an) :** [Objectifs précis]  
            **Moyen terme (3 ans) :** [Objectifs précis]  
            **Long terme (5 ans) :** [Objectifs précis]
            
            **Siège social :**
            - Adresse juridique complète
            - Justification du choix de localisation
            - Avantages géographiques et logistiques
            
            **Coordonnées bancaires :**
            - Banque partenaire en RDC
            - Numéro de compte (format 23 chiffres)
            - Services bancaires utilisés
            
            **Couverture géographique :**
            - Zone d'implantation principale
            - Zones de chalandise et de distribution
            - Plans d'expansion géographique
            
            ### 2. DESCRIPTION DÉTAILLÉE ET OBJECTIFS DU PROJET
            
            **Origine et historique :**
            - Genèse du projet d'entreprise
            - Motivations des porteurs de projet
            - Évolution depuis la création
            
            **Mission et vision :**
            - Mission claire de l'entreprise
            - Vision à moyen et long terme
            - Valeurs fondamentales
            
            **Objectifs stratégiques :**
            - Objectifs quantitatifs (CA, parts de marché)
            - Objectifs qualitatifs (notoriété, impact social)
            - Timeline de réalisation
            
            ### 3. STADE D'AVANCEMENT
            
            **Réalisations actuelles :**
            - Étapes franchies depuis le lancement
            - Premiers résultats obtenus
            - Partenariats déjà établis
            
            **Projets futurs :**
            - Développements prévus à court terme
            - Innovations en cours de développement
            - Expansion planifiée
            
            **Niveau de maturité :**
            - Phase actuelle du projet (concept, lancement, croissance)
            - Indicateurs de progression
            - Financements déjà acquis
            
            ### 4. ÉQUIPE MANAGÉRIALE
            
            **Organigramme :**
            - Structure organisationnelle claire
            - Répartition des responsabilités
            - Lignes hiérarchiques
            
            **Profils des dirigeants :**
            - Formation et diplômes
            - Expérience professionnelle pertinente
            - Compétences spécifiques au projet
            
            **Gouvernance :**
            - Répartition des parts sociales
            - Processus de prise de décision
            - Conseil d'administration ou comité de direction
            
            ### 5. ANALYSE SWOT
            
            Présentez sous forme de tableau structuré :
            
            | **FORCES** | **FAIBLESSES** |
            |------------|----------------|
            | - Force 1 : [Description détaillée] | - Faiblesse 1 : [Description et plan d'amélioration] |
            | - Force 2 : [Description détaillée] | - Faiblesse 2 : [Description et plan d'amélioration] |
            | - Force 3 : [Description détaillée] | - Faiblesse 3 : [Description et plan d'amélioration] |
            
            | **OPPORTUNITÉS** | **MENACES** |
            |------------------|-------------|
            | - Opportunité 1 : [Description et stratégie de saisie] | - Menace 1 : [Description et stratégie d'atténuation] |
            | - Opportunité 2 : [Description et stratégie de saisie] | - Menace 2 : [Description et stratégie d'atténuation] |
            | - Opportunité 3 : [Description et stratégie de saisie] | - Menace 3 : [Description et stratégie d'atténuation] |
            
            ### 6. BUSINESS MODEL CANVAS
            
            Insérez un Business Model Canvas complet avec les 9 rubriques adaptées au contexte RDC :
            - Partenaires clés
            - Activités clés  
            - Ressources clés
            - Proposition de valeur
            - Relations clients
            - Canaux de distribution
            - Segments de clientèle
            - Structure de coûts
            - Sources de revenus
            
            ### Instructions spécifiques :
            - Rédigez des paragraphes détaillés (minimum 4-5 phrases chacun)
            - Utilisez des données concrètes et vérifiables
            - Adaptez au contexte économique et réglementaire de la RDC
            - Mettez en avant les spécificités locales
            - Justifiez chaque choix stratégique
        """,
        
        "Présentation de l'offre de produit": """
            Vous êtes un expert en développement de produits et services pour le marché congolais.
            
            Rédigez une présentation détaillée de l'offre en 6 sections principales :
            
            ## III. PRÉSENTATION DE L'OFFRE DE PRODUITS ET/OU SERVICES
            
            ### 1. DESCRIPTION DES PRODUITS/SERVICES
            - Noms précis des produits/services offerts
            - Caractéristiques techniques détaillées
            - Processus de production/réalisation
            - Standards de qualité et certifications
            
            ### 2. BESOINS IDENTIFIÉS SUR LE MARCHÉ
            - Problèmes spécifiques résolus
            - Gaps du marché comblés
            - Demandes non satisfaites identifiées
            - Évolution des besoins clients
            
            ### 3. PROPOSITION DE VALEUR UNIQUE
            - Avantages différenciateurs clés
            - Innovation apportée au marché
            - Bénéfices clients quantifiés
            - Positionnement concurrentiel
            
            ### 4. PRISE EN COMPTE DE L'ASPECT GENRE
            - Impact sur l'autonomisation des femmes
            - Emplois féminins créés
            - Services adaptés aux femmes
            - Leadership féminin dans l'entreprise
            
            ### 5. IMPACT ENVIRONNEMENTAL ET SOCIAL
            - Évaluation des impacts environnementaux
            - Mesures d'atténuation mises en place
            - Plan de Gestion Environnemental et Social
            - Contribution aux ODD
            
            ### 6. INNOVATION ET AVANTAGES TECHNOLOGIQUES
            - Technologies utilisées
            - Innovation dans les processus
            - Propriété intellectuelle
            - Avantages compétitifs durables
            
            Instructions : Adaptez au secteur d'activité et au contexte RDC
        """,
        
        "Étude de marché": """
            Vous êtes un expert en études de marché pour l'Afrique centrale et la RDC.
            
            Rédigez une étude de marché complète en 8 sections numérotées :
            
            ## IV. ÉTUDE DE MARCHÉ
            
            ### 1. DESCRIPTION DES HYPOTHÈSES ET MÉTHODES
            - Produit/service pré-ciblé
            - Marché pré-ciblé et secteur d'activité
            - Méthodologie de recherche (questionnaires, études documentaires, etc.)
            - Sources d'information utilisées
            - Limites de l'étude
            
            ### 2. APPROCHE GÉNÉRALE DU MARCHÉ
            - Description du marché et ses caractéristiques
            - Historique et évolution du secteur
            - Taille du marché (cible, potentiel, réel)
            - Perspectives de croissance
            - Menaces et opportunités identifiées
            
            ### 3. CARACTÉRISTIQUES DE LA DEMANDE
            - Volume et évolution de la demande
            - Tendances de consommation
            - Segmentation de la clientèle
            - Comportements d'achat
            - Prescripteurs et influenceurs
            
            ### 4. CARACTÉRISTIQUES DE L'OFFRE
            - Concurrence directe et indirecte
            - Analyse des concurrents principaux
            - Forces et faiblesses de la concurrence
            - Stratégies de différenciation
            - Parts de marché estimées
            
            ### 5. ENVIRONNEMENT DES AFFAIRES
            - Cadre légal et réglementaire RDC
            - Facteurs économiques externes
            - Évolution technologique
            - Infrastructures disponibles
            - Défis spécifiques au contexte local
            
            ### 6. PARTENARIATS STRATÉGIQUES
            - Fournisseurs clés identifiés
            - Partenaires de distribution
            - Alliances commerciales potentielles
            - Partenaires techniques et financiers
            
            ### 7. CRÉATION D'EMPLOIS
            - Emplois directs créés/à créer
            - Emplois indirects générés
            - Profils de postes recherchés
            - Impact sur l'emploi local
            
            ### 8. PROJECTIONS DU CHIFFRE D'AFFAIRES
            - Part de marché visée
            - Projections à 1, 2, 3 ans
            - Hypothèses de croissance
            - Scénarios optimiste/pessimiste/réaliste
            
            Instructions : Utilisez des données réalistes du marché congolais
        """,
        
        "Stratégie Marketing": """
            Vous êtes un expert en marketing pour les marchés africains, spécialisé en RDC.
            
            Élaborez une stratégie marketing complète en 4 sections :
            
            ## V. STRATÉGIE MARKETING, COMMUNICATION ET POLITIQUE COMMERCIALE
            
            ### 1. CHOIX DE SEGMENTS DE CLIENTÈLE
            - Segments prioritaires identifiés
            - Critères de segmentation utilisés
            - Justification du ciblage
            - Positionnement stratégique
            - Persona clients détaillés
            
            ### 2. MARKETING-MIX (4P)
            **Politique de Produit :**
            - Gamme de produits/services
            - Niveau de qualité et standards
            - Services associés
            - Image de marque et positionnement
            
            **Politique de Prix :**
            - Stratégie de pricing
            - Prix par segment
            - Conditions de paiement
            - Politique de remise
            
            **Politique de Place (Distribution) :**
            - Canaux de distribution
            - Couverture géographique
            - Logistique et approvisionnement
            - Partenaires de distribution
            
            **Politique de Promotion (Communication) :**
            - Message et slogan
            - Supports de communication
            - Budget publicitaire
            - Actions promotionnelles
            
            ### 3. PLAN MARKETING ET ACTIONS COMMERCIALES
            
            Tableau détaillé des actions par période :
            
            | Actions Marketing | Jan | Fév | Mar | Avr | Mai | Jun | Jul | Aoû | Sep | Oct | Nov | Déc |
            |-------------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
            | Campagne publicitaire | X | | X | | | X | | | X | | | X |
            | Événements commerciaux | | X | | X | | | X | | | X | | |
            | Promotions spéciales | | | X | | X | | | X | | | X | |
            
            ### 4. MOYENS ET PARTENAIRES SOLLICITÉS
            - Ressources humaines marketing
            - Budget marketing annuel
            - Partenaires médias
            - Agences et prestataires
            - Technologies marketing utilisées
            
            Instructions : Adaptez aux habitudes de consommation congolaises
        """,
        
        "Moyens de production et organisation": """
            Vous êtes un expert en organisation industrielle et gestion des opérations en RDC.
            
            Décrivez l'organisation opérationnelle en 4 sections :
            
            ## VI. MOYENS DE PRODUCTION ET ORGANISATION
            
            ### 1. LOCAUX ET INFRASTRUCTURE
            - Description des locaux nécessaires
            - Localisation et justification du choix
            - Superficie et aménagement
            - Conditions de bail ou d'acquisition
            - Coûts d'installation et d'aménagement
            - Contraintes d'urbanisme et autorisations
            
            ### 2. ÉQUIPEMENTS ET MATÉRIEL
            - Liste détaillée des équipements
            - Spécifications techniques
            - Mode d'acquisition (achat, leasing, location)
            - Coûts d'investissement
            - Plan de renouvellement
            - Maintenance et garanties
            
            ### 3. RESSOURCES HUMAINES ET ORGANISATION
            - Organigramme détaillé
            - Profils de postes recherchés
            - Plannings et horaires de travail
            - Coûts salariaux et charges sociales
            - Plan de formation du personnel
            - Répartition claire des tâches et responsabilités
            
            ### 4. FOURNISSEURS ET SOUS-TRAITANTS
            - Liste des fournisseurs principaux
            - Critères de sélection
            - Conditions négociées (prix, délais, qualité)
            - Plan de approvisionnement
            - Risques fournisseurs et alternatives
            - Contrats et accords commerciaux
            
            Instructions : Adaptez aux contraintes logistiques de la RDC
        """,
        
        "Étude des risques": """
            Vous êtes un expert en gestion des risques pour les entreprises en RDC.
            
            Réalisez une analyse complète des risques :
            
            ## VII. ÉTUDE DES RISQUES ET HYPOTHÈSES
            
            ### TABLEAU COMPLET DES RISQUES
            
            | Nature du Risque | Description Détaillée | Probabilité | Impact | Stratégie de Traitement |
            |------------------|----------------------|-------------|---------|-------------------------|
            | **Risques liés à l'environnement général** |
            | Instabilité politique | Changements de gouvernement, conflits | Moyenne | Élevé | Diversification géographique, assurances |
            | Fluctuations monétaires | Volatilité du franc congolais | Élevée | Élevé | Facturation en USD, couverture de change |
            | Inflation | Hausse générale des prix | Élevée | Moyen | Indexation des prix, stocks stratégiques |
            |
            | **Risques liés au marché** |
            | Concurrence nouvelle | Arrivée de nouveaux acteurs | Moyenne | Moyen | Innovation continue, fidélisation clients |
            | Évolution de la demande | Changement des goûts/besoins | Faible | Élevé | Veille marché, adaptation de l'offre |
            | Saisonnalité | Variations saisonnières importantes | Variable | Moyen | Diversification produits, trésorerie |
            |
            | **Risques liés aux outils** |
            | Pannes équipements | Arrêt de production | Moyenne | Élevé | Maintenance préventive, équipements de secours |
            | Obsolescence technologique | Dépassement technologique | Faible | Élevé | Veille technologique, investissements R&D |
            | Cybersécurité | Attaques informatiques | Moyenne | Moyen | Sécurisation SI, formation personnel |
            |
            | **Risques liés aux personnes** |
            | Départ personnel clé | Perte de compétences critiques | Moyenne | Élevé | Formation, documentation, succession |
            | Accidents de travail | Blessures, arrêts maladie | Faible | Moyen | Sécurité au travail, assurances |
            | Conflits sociaux | Grèves, revendications | Faible | Moyen | Dialogue social, conditions de travail |
            |
            | **Risques liés aux tiers** |
            | Défaillance fournisseurs | Ruptures d'approvisionnement | Moyenne | Élevé | Diversification, stocks de sécurité |
            | Impayés clients | Créances irrécouvrables | Moyenne | Moyen | Assurance-crédit, garanties |
            | Problèmes logistiques | Retards, avaries transport | Élevée | Moyen | Partenaires fiables, assurance transport |
            |
            | **Autres risques spécifiques** |
            | Catastrophes naturelles | Inondations, incendies | Faible | Élevé | Assurances multirisques, plans d'urgence |
            | Réglementations nouvelles | Changements réglementaires | Moyenne | Moyen | Veille réglementaire, conformité |
            | Corruption | Demandes de pots-de-vin | Moyenne | Élevé | Politique anti-corruption, transparence |
            
            ### PLAN DE GESTION DES RISQUES
            - Comité de gestion des risques
            - Procédures d'alerte et d'escalade
            - Assurances souscrites
            - Fonds de réserve pour contingences
            - Révision périodique des risques
            
            Instructions : Adaptez aux spécificités sectorielles et géographiques
        """,
        
        "Équipe dirigeante": """
            Vous êtes un expert en ressources humaines et gouvernance d'entreprise.
            
            Présentez l'équipe dirigeante de manière professionnelle :
            
            ## VIII. ÉQUIPE DIRIGEANTE ET CONSEIL D'ADMINISTRATION
            
            ### PRÉSENTATION DE L'ÉQUIPE DIRIGEANTE
            
            Pour chaque membre de l'équipe :
            
            **[Nom et Prénom]**
            - Poste occupé et responsabilités
            - Formation académique détaillée
            - Expérience professionnelle pertinente
            - Réalisations et succès antérieurs
            - Compétences spécifiques apportées
            - Réseau professionnel et contacts
            
            ### ORGANIGRAMME FONCTIONNEL
            - Structure hiérarchique claire
            - Répartition des pouvoirs et responsabilités
            - Processus de prise de décision
            - Comités spécialisés (audit, rémunération, etc.)
            
            ### CONSEIL D'ADMINISTRATION
            - Composition et profils des administrateurs
            - Expertise et expérience apportées
            - Indépendance et gouvernance
            - Fréquence des réunions et processus
            
            ### BESOINS EN RECRUTEMENT
            - Postes à pourvoir à court terme
            - Profils recherchés et critères
            - Stratégie de recrutement et formation
            - Plan de développement des compétences
            
            Instructions : Mettez en valeur l'expérience et la crédibilité de l'équipe
        """,
        
        "Plan de financement": """
            Vous êtes un expert financier spécialisé dans le financement d'entreprises en RDC.
            
            Élaborez un plan de financement détaillé :
            
            ## IX. PLAN DE FINANCEMENT ET RENTABILITÉ
            
            ### 1. BESOINS DE FINANCEMENT INITIAUX
            
            **Tableau des Investissements Initiaux :**
            
            | Poste d'investissement | Montant (USD) | % du total | Justification |
            |------------------------|---------------|------------|---------------|
            | Terrain et constructions | | | |
            | Équipements et matériel | | | |
            | Mobilier et aménagements | | | |
            | Véhicules | | | |
            | Frais d'établissement | | | |
            | Fonds de roulement initial | | | |
            | Imprévus (5-10%) | | | |
            | **TOTAL BESOINS** | | 100% | |
            
            ### 2. PLAN DE FINANCEMENT
            
            **Sources de Financement :**
            
            | Source de financement | Montant (USD) | % du total | Conditions |
            |-----------------------|---------------|------------|------------|
            | Apports personnels | | | Capital propre |
            | Prêt bancaire | | | Taux %, durée, garanties |
            | Subventions | | | Organismes, conditions |
            | Investisseurs | | | Participation au capital |
            | Autres financements | | | À préciser |
            | **TOTAL RESSOURCES** | | 100% | |
            
            ### 3. ANALYSE DE RENTABILITÉ
            
            **Indicateurs Financiers Clés :**
            - Chiffre d'affaires prévisionnel (3 ans)
            - Marge brute et marge nette
            - Point mort (break-even)
            - Retour sur investissement (ROI)
            - Valeur actuelle nette (VAN)
            - Taux de rentabilité interne (TRI)
            - Délai de récupération
            
            ### 4. PROJECTIONS FINANCIÈRES
            
            **Compte de Résultat Prévisionnel (3 ans) :**
            
            | Éléments | Année 1 | Année 2 | Année 3 |
            |----------|---------|---------|---------|
            | Chiffre d'affaires | | | |
            | - Coût des ventes | | | |
            | **= Marge brute** | | | |
            | - Charges d'exploitation | | | |
            | **= Résultat d'exploitation** | | | |
            | - Charges financières | | | |
            | **= Résultat net** | | | |
            
            **Plan de Trésorerie (12 mois) :**
            - Encaissements mensuels prévisionnels
            - Décaissements mensuels prévisionnels
            - Solde de trésorerie mensuel
            - Besoins de trésorerie identifiés
            
            Instructions : Utilisez des données réalistes du marché congolais
        """,
        
        "Impacts et durabilité": """
            Vous êtes un expert en développement durable et impact social.
            
            Analysez les impacts du projet :
            
            ## X. IMPACTS SOCIAUX, ENVIRONNEMENTAUX ET DURABILITÉ
            
            ### 1. IMPACT SOCIAL
            
            **Création d'Emplois :**
            - Emplois directs créés (nombre, types, salaires)
            - Emplois indirects générés dans la chaîne de valeur
            - Emplois pour les femmes et les jeunes
            - Développement des compétences locales
            
            **Impact Communautaire :**
            - Services aux communautés locales
            - Partenariats avec organisations locales
            - Programmes de responsabilité sociale
            - Contribution au développement local
            
            ### 2. IMPACT ENVIRONNEMENTAL
            
            **Évaluation Environnementale :**
            - Identification des impacts potentiels
            - Mesures d'atténuation mises en place
            - Technologies propres utilisées
            - Gestion des déchets et recyclage
            
            **Plan de Gestion Environnemental :**
            - Procédures de surveillance
            - Indicateurs de performance environnementale
            - Formation du personnel
            - Certification environnementale visée
            
            ### 3. DURABILITÉ DU PROJET
            
            **Viabilité Économique :**
            - Modèle économique durable
            - Adaptation aux évolutions du marché
            - Innovation et amélioration continue
            - Diversification des revenus
            
            **Durabilité Sociale :**
            - Engagement des parties prenantes
            - Transfert de compétences
            - Autonomisation des communautés
            - Gouvernance participative
            
            ### 4. CONTRIBUTION AUX ODD
            
            **Objectifs de Développement Durable visés :**
            - ODD 1 : Pas de pauvreté
            - ODD 5 : Égalité entre les sexes
            - ODD 8 : Travail décent et croissance économique
            - ODD 9 : Industrie, innovation et infrastructure
            - Autres ODD pertinents selon le secteur
            
            Instructions : Quantifiez les impacts autant que possible
        """,
        
        "Conclusion": """
            Vous êtes un expert en synthèse stratégique et communication d'entreprise.
            
            Rédigez une conclusion persuasive et professionnelle :
            
            ## XI. CONCLUSION ET PERSPECTIVES
            
            ### SYNTHÈSE DU PROJET
            - Récapitulatif de la proposition de valeur
            - Alignement avec les besoins du marché
            - Avantages concurrentiels durables
            - Retombées économiques et sociales attendues
            
            ### FACTEURS CLÉS DE SUCCÈS
            - Points forts du projet identifiés
            - Compétences et expérience de l'équipe
            - Partenariats stratégiques établis
            - Opportunités de marché saisies
            
            ### PERSPECTIVES DE DÉVELOPPEMENT
            - Vision à moyen et long terme
            - Plans d'expansion géographique
            - Diversification de l'offre
            - Innovation et amélioration continue
            
            ### APPEL À L'ACTION
            - Demande de financement claire
            - Prochaines étapes du projet
            - Calendrier de mise en œuvre
            - Invitation au partenariat
            
            Instructions : Terminez sur une note positive et convaincante
        """
    }
    
    return prompts.get(section, "Prompt système non trouvé pour cette section.")


def get_user_queries() -> Dict[str, str]:
    """
    Requêtes utilisateur personnalisées pour chaque section
    """
    return {
        "Couverture": """
            Créez une page de couverture professionnelle en utilisant les informations suivantes de mon entreprise :
            - Nom de l'entreprise
            - Secteur d'activité
            - Localisation
            - Données financières principales
            
            Adaptez au contexte de la République Démocratique du Congo et utilisez un format professionnel approprié pour un business plan.
        """,
        
        "Sommaire": """
            Générez un sommaire complet et professionnel pour mon business plan, adapté à une entreprise en RDC.
            Le sommaire doit être structuré, numéroté et refléter un document professionnel de qualité.
        """,
        
        "Résumé Exécutif": """
            Rédigez un résumé exécutif convaincant pour mon entreprise qui :
            - Présente clairement le projet et son potentiel
            - Met en avant l'équipe et les compétences
            - Démontre l'opportunité de marché
            - Précise les besoins financiers et le retour attendu
            - S'adapte au contexte économique de la RDC
            
            Le résumé doit être percutant et donner envie d'en savoir plus sur le projet.
        """,
        
        "Présentation de votre entreprise": """
            Rédigez une présentation complète et détaillée de mon entreprise en couvrant :
            - Les informations juridiques et administratives
            - L'historique et les objectifs du projet
            - Le niveau d'avancement actuel
            - L'équipe dirigeante et l'organisation
            - Une analyse SWOT approfondie
            - Le Business Model Canvas complet
            
            Adaptez le contenu au contexte réglementaire et économique de la RDC.
        """,
        
        "Présentation de l'offre de produit": """
            Rédigez une présentation détaillée de l'offre de produits/services en couvrant :
            - Description précise des produits/services
            - Besoins du marché identifiés
            - Proposition de valeur unique et différenciation
            - Prise en compte de l'aspect genre dans l'offre
            - Impact environnemental et social
            - Innovation et avantages technologiques
            
            Mettez en avant la valeur ajoutée pour les clients congolais.
        """,
        
        "Étude de marché": """
            Réalisez une étude de marché complète et professionnelle incluant :
            - Méthodologie de recherche utilisée
            - Analyse du marché global et local (RDC)
            - Caractéristiques de la demande et segmentation
            - Analyse de la concurrence directe et indirecte
            - Environnement des affaires en RDC
            - Partenariats stratégiques potentiels
            - Projections de chiffre d'affaires
            - Impact sur l'emploi local
            
            Basez-vous sur des données réalistes du marché congolais.
        """,
        
        "Stratégie Marketing": """
            Élaborez une stratégie marketing complète comprenant :
            - Segmentation et choix de clientèle cible
            - Marketing-mix adapté au contexte RDC (4P)
            - Plan marketing avec actions concrètes
            - Budget et calendrier des actions
            - Partenaires et moyens nécessaires
            - Adaptation aux habitudes de consommation locales
            
            Intégrez les spécificités culturelles et économiques congolaises.
        """,
        
        "Moyens de production et organisation": """
            Décrivez en détail l'organisation opérationnelle :
            - Locaux et infrastructure nécessaires
            - Équipements et technologies requis
            - Ressources humaines et organisation
            - Fournisseurs et chaîne d'approvisionnement
            - Processus de production/prestation
            - Contrôle qualité et certifications
            
            Adaptez aux contraintes et opportunités du contexte congolais.
        """,
        
        "Étude des risques": """
            Réalisez une analyse complète des risques comprenant :
            - Identification des risques par catégorie
            - Évaluation de l'impact et de la probabilité
            - Stratégies d'atténuation pour chaque risque
            - Plan de contingence et mesures préventives
            - Assurances et garanties nécessaires
            - Risques spécifiques au contexte RDC
            
            Proposez des solutions concrètes et réalistes.
        """
    }

def get_business_plan_context_template(template_name: str) -> str:
    """
    Contexte spécifique selon le template sélectionné
    """
    contexts = {
        "COPA TRANSFORME": """
            CONTEXTE COPA TRANSFORMÉ :
            Vous travaillez dans le cadre du programme COPA TRANSFORMÉ pour l'autonomisation des femmes entrepreneures et la mise à niveau des PME en RDC. 
            
            Secteurs prioritaires : Agroalimentaire, Industrie légère, Artisanat, Services à valeur ajoutée
            Objectifs : Création d'emplois, autonomisation des femmes, transformation économique
            Approche : Développement inclusif, partenariats locaux, innovation sociale
        """,
        
        "Virunga": """
            CONTEXTE VIRUNGA :
            Vous travaillez dans le cadre des initiatives de conservation et développement durable du Parc National des Virunga.
            
            Secteurs prioritaires : Écotourisme, Agriculture durable, Énergies renouvelables, Conservation
            Objectifs : Conservation environnementale, développement communautaire, paix et sécurité
            Approche : Développement durable, protection environnementale, engagement communautaire
        """,
        
        "IP Femme": """
            CONTEXTE IP FEMME :
            Vous travaillez dans le cadre d'initiatives d'autonomisation économique des femmes en RDC.
            
            Secteurs prioritaires : Commerce, Services, Artisanat, Agriculture, Microfinance
            Objectifs : Égalité de genre, autonomisation économique, leadership féminin
            Approche : Empowerment des femmes, inclusion financière, renforcement de capacités
        """
    }
    
    return contexts.get(template_name, contexts["COPA TRANSFORME"])


# ==================================================================================
# FONCTIONS DE COMPATIBILITÉ AVEC L'ANCIEN SYSTÈME TEMPLATE_MANAGER.PY
# ==================================================================================

def get_business_plan_system_messages(template_name: str) -> Dict[str, str]:
    """
    Version spécialisée de get_system_prompts() adaptée pour un template spécifique
    Compatible avec l'ancien système template_manager.py
    
    Args:
        template_name (str): Nom du template ("COPA TRANSFORME", "Virunga", "IP Femme")
    
    Returns:
        Dict[str, str]: Prompts système adaptés au template
    """
    base_prompts = get_system_prompts()
    context_template = get_business_plan_context_template(template_name)
    
    # Adapter chaque prompt avec le contexte spécifique du template
    adapted_prompts = {}
    for section, prompt in base_prompts.items():
        adapted_prompts[section] = f"{context_template}\n\n{prompt}"
    
    return adapted_prompts

def get_business_plan_user_queries(template_name: str) -> Dict[str, str]:
    """
    Version spécialisée de get_user_queries() adaptée pour un template spécifique
    
    Args:
        template_name (str): Nom du template
    
    Returns:
        Dict[str, str]: Requêtes utilisateur adaptées au template
    """
    base_queries = get_user_queries()
    
    # Adapter les requêtes selon le template
    template_adaptations = {
        "COPA TRANSFORME": {
            "Présentation de l'offre de produit": "Décrire l'offre en mettant l'accent sur l'agroalimentaire et l'autonomisation des femmes",
            "Étude de marché": "Analyser le marché agroalimentaire et les chaînes de valeur agricoles en RDC",
            "Stratégie Marketing": "Développer une stratégie marketing adaptée aux communautés rurales et urbaines"
        },
        "Virunga": {
            "Présentation de l'offre de produit": "Décrire l'offre en intégrant les aspects de conservation et développement durable",
            "Étude de marché": "Analyser les marchés de l'écotourisme et des produits durables",
            "Stratégie Marketing": "Stratégie marketing axée sur la conservation et l'écotourisme responsable"
        },
        "IP Femme": {
            "Présentation de l'offre de produit": "Décrire l'offre en mettant l'accent sur l'autonomisation économique des femmes",
            "Étude de marché": "Analyser les marchés avec perspective genre et inclusion financière",
            "Stratégie Marketing": "Stratégie marketing favorisant l'empowerment des femmes"
        }
    }
    
    adapted_queries = base_queries.copy()
    if template_name in template_adaptations:
        adapted_queries.update(template_adaptations[template_name])
    
    return adapted_queries

def get_sections_configuration(template_name: str) -> Dict[str, Dict[str, str]]:
    """
    Configuration complète des sections pour un template donné
    Combine system_prompts + user_queries + contexte template
    
    Args:
        template_name (str): Nom du template
        
    Returns:
        Dict[str, Dict[str, str]]: Configuration complète par section
    """
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

def is_compatible_with_template_manager() -> bool:
    """
    Vérifie la compatibilité avec le système template_manager.py
    """
    try:
        from templates.template_manager import get_template, get_templates_list
        return True
    except ImportError:
        return False

def merge_with_template_manager_context(template_name: str, section_name: str) -> str:
    """
    Fusionne le contexte de business_plan_prompts avec celui de template_manager
    
    Args:
        template_name (str): Nom du template
        section_name (str): Nom de la section
        
    Returns:
        str: Contexte fusionné
    """
    business_plan_context = get_business_plan_context_template(template_name)
    
    # Essayer d'importer le contexte du template_manager
    try:
        from templates.template_manager import get_metaprompt, get_organisation_info
        
        metaprompt = get_metaprompt(template_name)
        org_info = get_organisation_info(template_name)
        
        merged_context = f"""
{business_plan_context}

MÉTAPROMPT ORGANISATIONNEL :
{metaprompt}

INFORMATIONS ORGANISATION :
{org_info}
"""
        return merged_context
        
    except ImportError:
        # Si template_manager n'est pas disponible, utiliser seulement notre contexte
        return business_plan_context

# ==================================================================================
# FONCTIONS D'EXPORT POUR INTÉGRATION
# ==================================================================================

def export_template_configuration(template_name: str) -> Dict[str, Any]:
    """
    Exporte la configuration complète d'un template pour utilisation externe
    
    Args:
        template_name (str): Nom du template
        
    Returns:
        Dict[str, Any]: Configuration exportable
    """
    return {
        "template_name": template_name,
        "sections": get_business_plan_sections(),
        "system_prompts": get_business_plan_system_messages(template_name),
        "user_queries": get_business_plan_user_queries(template_name),
        "context_template": get_business_plan_context_template(template_name),
        "full_configuration": get_sections_configuration(template_name),
        "compatibility": {
            "template_manager": is_compatible_with_template_manager(),
            "version": "1.0.0",
            "source": "business_plan_prompts.py"
        }
    }