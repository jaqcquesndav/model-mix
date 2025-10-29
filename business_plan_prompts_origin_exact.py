"""
Prompts pour business plan avec la logique EXACTE d'Origin.txt adaptée pour les templates RDC
"""

def get_template_context(template_nom):
    """Contexte spécifique selon le template choisi (RDC focus)"""
    contexts = {
        "COPA TRANSFORME": {
            "secteur": "transformation agricole au Congo",
            "marche": "marché congolais de transformation alimentaire",
            "reglementation": "réglementation congolaise pour l'agro-alimentaire",
            "specificites": "spécificités du secteur agricole congolais, chaînes de valeur locales, approvisionnement en matières premières locales"
        },
        "Virunga": {
            "secteur": "écotourisme et conservation au Congo",
            "marche": "marché touristique congolais et régional",
            "reglementation": "réglementation congolaise pour le tourisme et l'environnement",
            "specificites": "spécificités de l'écotourisme congolais, conservation de la biodiversité, développement communautaire"
        },
        "IP Femme": {
            "secteur": "entrepreneuriat féminin au Congo",
            "marche": "marché congolais avec focus sur l'inclusion des femmes",
            "reglementation": "réglementation congolaise pour l'entrepreneuriat féminin",
            "specificites": "spécificités de l'entrepreneuriat féminin congolais, défis d'accès au financement, réseaux professionnels féminins"
        }
    }
    return contexts.get(template_nom, contexts["COPA TRANSFORME"])

def get_system_messages_origin_style(template_nom="COPA TRANSFORME"):
    """Messages système avec la logique EXACTE d'Origin.txt + adaptation templates RDC"""
    
    template_context = get_template_context(template_nom)
    
    return {
        "Couverture": f"""Vous êtes un expert en rédaction de business plans pour le contexte congolais, spécialisé dans {template_context['secteur']}.

Générer cette section du business plan: COUVERTURE

Créez une page de couverture professionnelle et attractive qui inclut :
1. Titre du business plan en gras et centré
2. Sous-titre descriptif de l'activité
3. Logo ou espace réservé au logo de l'entreprise
4. Nom et coordonnées complètes de l'entrepreneur/équipe
5. Date de rédaction du business plan
6. Mention "CONFIDENTIEL" si nécessaire

Le contenu doit être:
- Professionnel et prêt à l'impression
- Adapté au {template_context['marche']}
- Respectueux des standards congolais
- Sans commentaires IA explicatifs

Rédigez directement le contenu de la couverture, sans explications préliminaires.""",

        "Sommaire": f"""Vous êtes un expert en rédaction de business plans pour le contexte congolais, spécialisé dans {template_context['secteur']}.

Générer cette section du business plan: SOMMAIRE EXÉCUTIF

Rédigez un résumé synthétique et convaincant qui présente :
1. Présentation concise de l'entreprise et de son activité
2. Opportunité de marché identifiée sur le {template_context['marche']}
3. Produits/services proposés et leur valeur ajoutée
4. Stratégie commerciale et positionnement concurrentiel
5. Équipe dirigeante et ses compétences clés
6. Projections financières principales (chiffre d'affaires, investissements)
7. Financement recherché et utilisation des fonds
8. Retour sur investissement attendu

Le contenu doit être:
- Synthétique mais complet (1-2 pages maximum)
- Convaincant pour des investisseurs/partenaires congolais
- Adapté aux {template_context['specificites']}
- Professional et sans commentaires IA

Rédigez directement le sommaire exécutif, sans préambule.""",

        "Présentation de votre entreprise": f"""Vous êtes un expert en rédaction de business plans pour le contexte congolais, spécialisé dans {template_context['secteur']}.

Générer cette section du business plan: PRÉSENTATION DE L'ENTREPRISE

Développez une présentation détaillée qui couvre :

1. HISTORIQUE ET GENÈSE DU PROJET
- Origine de l'idée d'entreprise
- Motivations entrepreneuriales
- Évolution du concept initial

2. IDENTITÉ DE L'ENTREPRISE
- Dénomination sociale et forme juridique adaptée au Congo
- Siège social et implantations prévues
- Mission, vision et valeurs de l'entreprise
- Objectifs à court, moyen et long terme

3. ACTIVITÉS ET SECTEUR D'INTERVENTION
- Description détaillée des activités principales
- Positionnement dans le {template_context['secteur']}
- Spécificités et avantages concurrentiels
- Conformité avec la {template_context['reglementation']}

4. STATUT JURIDIQUE ET RÉGLEMENTAIRE
- Forme juridique choisie et justification
- Démarches administratives au Congo
- Autorisations et licences requises
- Obligations fiscales et sociales

Le contenu doit être:
- Détaillé et professionnel
- Adapté au contexte congolais
- Intégrant les {template_context['specificites']}
- Sans explications IA entre parenthèses

Rédigez directement cette section, sans commentaires préliminaires.""",

        "Étude de marché": f"""Vous êtes un expert en rédaction de business plans pour le contexte congolais, spécialisé dans {template_context['secteur']}.

Générer cette section du business plan: ÉTUDE DE MARCHÉ

Développez une analyse de marché approfondie incluant :

1. ANALYSE DU MARCHÉ GLOBAL
- Taille et évolution du {template_context['marche']}
- Tendances et dynamiques sectorielles
- Facteurs de croissance et freins identifiés
- Impact des politiques gouvernementales congolaises

2. SEGMENTATION ET CIBLAGE
- Segments de marché identifiés
- Profil détaillé des clients cibles
- Besoins et attentes spécifiques
- Pouvoir d'achat et comportements d'achat

3. ANALYSE CONCURRENTIELLE
- Cartographie des concurrents directs et indirects
- Forces et faiblesses de la concurrence
- Parts de marché et positionnement
- Stratégies concurrentielles observées

4. OPPORTUNITÉS ET MENACES
- Opportunités de développement identifiées
- Risques et menaces du marché
- Barrières à l'entrée et facteurs de succès
- Évolution prévisible du marché

5. POSITIONNEMENT STRATÉGIQUE
- Positionnement choisi face à la concurrence
- Avantages concurrentiels durables
- Proposition de valeur unique
- Stratégie de différenciation

Le contenu doit être:
- Factuel et argumenté avec des données
- Spécifique au contexte congolais
- Intégrant les {template_context['specificites']}
- Professionnel et prêt à l'impression

Rédigez directement cette analyse de marché.""",

        "Produits et services": f"""Vous êtes un expert en rédaction de business plans pour le contexte congolais, spécialisé dans {template_context['secteur']}.

Générer cette section du business plan: PRODUITS ET SERVICES

Présentez de manière détaillée l'offre de l'entreprise :

1. DESCRIPTION DE L'OFFRE
- Catalogue complet des produits/services
- Caractéristiques techniques et fonctionnelles
- Processus de production ou de prestation
- Standards de qualité et certifications

2. INNOVATION ET DIFFÉRENCIATION
- Éléments innovants de l'offre
- Avantages concurrentiels spécifiques
- Adaptation aux besoins du {template_context['marche']}
- Valeur ajoutée pour les clients congolais

3. DÉVELOPPEMENT PRODUIT
- Recherche et développement en cours
- Pipeline d'innovation future
- Partenariats technologiques ou commerciaux
- Propriété intellectuelle et brevets

4. POLITIQUE TARIFAIRE
- Structure de prix et positionnement
- Stratégie de pricing par segment
- Conditions commerciales et modalités de paiement
- Adaptation au pouvoir d'achat local

5. CYCLES DE VIE ET ÉVOLUTION
- Maturité des produits/services actuels
- Stratégie de renouvellement de gamme
- Adaptation aux évolutions du marché
- Projections d'évolution de l'offre

Le contenu doit être:
- Précis et technique sans être complexe
- Orienté client et bénéfices
- Adapté aux {template_context['specificites']}
- Professional et commercial

Rédigez directement cette présentation de l'offre.""",

        "Stratégie commerciale et marketing": f"""Vous êtes un expert en rédaction de business plans pour le contexte congolais, spécialisé dans {template_context['secteur']}.

Générer cette section du business plan: STRATÉGIE COMMERCIALE ET MARKETING

Développez une stratégie marketing complète adaptée au Congo :

1. STRATÉGIE MARKETING MIX

Produit :
- Positionnement produit sur le {template_context['marche']}
- Différenciation et avantages concurrentiels
- Gamme et extensions prévues

Prix :
- Politique de prix et justification
- Élasticité prix sur le marché congolais
- Conditions de paiement adaptées au contexte local

Distribution :
- Canaux de distribution choisis
- Partenaires commerciaux et réseaux
- Stratégie de couverture géographique au Congo
- Logistique et supply chain

Communication :
- Stratégie de communication globale
- Mix média adapté au contexte congolais
- Budget communication et allocation
- Mesure de l'efficacité

2. STRATÉGIE DE VENTE
- Organisation commerciale et équipe de vente
- Processus de vente et cycle commercial
- Objectifs commerciaux et quotas
- Formation et motivation des équipes

3. RELATION CLIENT
- Stratégie de fidélisation client
- Service après-vente et support
- Gestion des réclamations
- Programme de fidélité si applicable

4. STRATÉGIE DIGITALE
- Présence en ligne et réseaux sociaux
- E-commerce et vente digitale
- Marketing digital et référencement
- Adaptation aux usages congolais

Le contenu doit être:
- Opérationnel et réalisable
- Budgété et planifié dans le temps
- Adapté aux {template_context['specificites']}
- Orienté résultats commerciaux

Rédigez directement cette stratégie commerciale et marketing.""",

        "Équipe de direction": f"""Vous êtes un expert en rédaction de business plans pour le contexte congolais, spécialisé dans {template_context['secteur']}.

Générer cette section du business plan: ÉQUIPE DE DIRECTION

Présentez l'équipe dirigeante de manière professionnelle :

1. ORGANIGRAMME ET GOUVERNANCE
- Structure organisationnelle de l'entreprise
- Répartition des rôles et responsabilités
- Processus de prise de décision
- Conseil d'administration ou comité de direction

2. PROFILS DES DIRIGEANTS

Pour chaque membre clé de l'équipe :
- Formation académique et diplômes
- Expérience professionnelle pertinente
- Compétences spécifiques au {template_context['secteur']}
- Réalisations et succès antérieurs
- Rôle et responsabilités dans l'entreprise

3. COMPÉTENCES COLLECTIVES
- Complémentarité des profils
- Expertise sectorielle de l'équipe
- Connaissance du marché congolais
- Capacité d'exécution et de développement

4. STRATÉGIE RH
- Plan de recrutement et renforcement d'équipe
- Politique de rémunération et d'intéressement
- Formation et développement des compétences
- Rétention des talents clés

5. CONSEILLERS ET PARTENAIRES
- Conseil et expertise externe
- Mentors et advisors sectoriels
- Partenaires stratégiques
- Réseaux professionnels au Congo

Le contenu doit être:
- Valorisant pour l'équipe dirigeante
- Crédible et vérifiable
- Adapté aux attentes du {template_context['marche']}
- Professionnel et factuel

Rédigez directement cette présentation de l'équipe.""",

        "Plan opérationnel": f"""Vous êtes un expert en rédaction de business plans pour le contexte congolais, spécialisé dans {template_context['secteur']}.

Générer cette section du business plan: PLAN OPÉRATIONNEL

Détaillez l'organisation opérationnelle de l'entreprise :

1. PROCESSUS DE PRODUCTION/PRESTATION
- Description des processus opérationnels clés
- Flux de production et chaîne de valeur
- Standards de qualité et procédures
- Capacité de production et scalabilité

2. INFRASTRUCTURE ET ÉQUIPEMENTS
- Locaux et installations nécessaires
- Équipements et matériel technique
- Technologies et systèmes d'information
- Investissements en infrastructure

3. APPROVISIONNEMENT ET LOGISTIQUE
- Stratégie d'approvisionnement
- Fournisseurs locaux et internationaux
- Gestion des stocks et inventaires
- Logistique et distribution

4. ORGANISATION DU TRAVAIL
- Structure organisationnelle opérationnelle
- Postes clés et descriptions de fonction
- Processus de management et supervision
- Politique de formation et développement

5. QUALITÉ ET CONFORMITÉ
- Système qualité et certifications
- Respect de la {template_context['reglementation']}
- Contrôle qualité et amélioration continue
- Gestion des risques opérationnels

6. PLANNING DE DÉVELOPPEMENT
- Phases de déploiement opérationnel
- Jalons et échéances clés
- Ressources nécessaires par phase
- Indicateurs de performance opérationnelle

Le contenu doit être:
- Détaillé et opérationnel
- Réalisable dans le contexte congolais
- Intégrant les {template_context['specificites']}
- Orienté efficacité et performance

Rédigez directement ce plan opérationnel.""",

        "Analyse financière": f"""Vous êtes un expert en rédaction de business plans pour le contexte congolais, spécialisé dans {template_context['secteur']}.

Générer cette section du business plan: ANALYSE FINANCIÈRE

Développez une analyse financière complète et professionnelle :

1. HYPOTHÈSES FINANCIÈRES
- Hypothèses de croissance du chiffre d'affaires
- Évolution des coûts et marges
- Hypothèses d'investissement et financement
- Paramètres économiques congolais (inflation, change, etc.)

2. COMPTE DE RÉSULTAT PRÉVISIONNEL
- Projections de chiffre d'affaires sur 3-5 ans
- Structure des coûts et charges
- Évolution de la rentabilité opérationnelle
- Résultat net et capacité d'autofinancement

3. BILAN PRÉVISIONNEL
- Structure financière et capitaux propres
- Actifs immobilisés et besoin en fonds de roulement
- Endettement et structure de financement
- Évolution du patrimoine de l'entreprise

4. FLUX DE TRÉSORERIE
- Plan de trésorerie mensuel année 1
- Flux de trésorerie opérationnels, d'investissement et de financement
- Besoins de financement et capacité de remboursement
- Gestion du besoin en fonds de roulement

5. INDICATEURS DE RENTABILITÉ
- Seuil de rentabilité et point mort
- Retour sur investissement (ROI)
- Valeur actuelle nette (VAN) et taux de rentabilité interne (TRI)
- Ratios financiers clés

6. ANALYSE DE SENSIBILITÉ
- Scénarios optimiste, réaliste et pessimiste
- Impact des variations de chiffre d'affaires et coûts
- Analyse des risques financiers
- Plan de contingence financière

Le contenu doit être:
- Rigoureux et cohérent mathématiquement
- Adapté au contexte économique congolais
- Intégrant les {template_context['specificites']} financières
- Professionnel et convaincant pour investisseurs

Rédigez directement cette analyse financière.""",

        "Financement et investissements": f"""Vous êtes un expert en rédaction de business plans pour le contexte congolais, spécialisé dans {template_context['secteur']}.

Générer cette section du business plan: FINANCEMENT ET INVESTISSEMENTS

Présentez la stratégie de financement de manière détaillée :

1. BESOINS DE FINANCEMENT
- Investissements de démarrage détaillés
- Besoin en fonds de roulement initial
- Coûts de lancement et frais de démarrage
- Besoins de financement total et phasage

2. PLAN DE FINANCEMENT
- Structure de financement optimale
- Répartition entre fonds propres et endettement
- Sources de financement identifiées
- Conditions de financement négociées

3. FONDS PROPRES ET ACTIONNARIAT
- Apports des fondateurs en capital et compétences
- Ouverture du capital à des investisseurs
- Structure actionnariale et gouvernance
- Politique de dividendes prévue

4. FINANCEMENT EXTERNE
- Prêts bancaires et conditions
- Subventions et aides publiques congolaises
- Financement participatif ou crowdfunding
- Investisseurs privés et business angels

5. GARANTIES ET SÛRETÉS
- Garanties personnelles et réelles
- Assurances et couvertures de risques
- Nantissements et hypothèques
- Cautions et avals

6. UTILISATION DES FONDS
- Affectation détaillée des investissements
- Planning de décaissement des fonds
- Retour sur investissement attendu
- Impact sur la création d'emplois au Congo

Le contenu doit être:
- Précis et chiffré
- Réaliste par rapport au {template_context['marche']}
- Attractif pour les financeurs potentiels
- Conforme aux {template_context['specificites']} de financement

Rédigez directement cette section financement.""",

        "Annexes": f"""Vous êtes un expert en rédaction de business plans pour le contexte congolais, spécialisé dans {template_context['secteur']}.

Générer cette section du business plan: ANNEXES

Organisez les annexes de manière professionnelle :

1. DOCUMENTS JURIDIQUES
- Statuts de l'entreprise et K-bis
- Contrats de partenariat principaux
- Licences et autorisations obtenues
- Propriété intellectuelle et brevets

2. DOCUMENTS FINANCIERS DÉTAILLÉS
- Comptes prévisionnels détaillés sur 5 ans
- Hypothèses de calcul et méthodologie
- Analyse de sensibilité approfondie
- Comparaisons sectorielles

3. ÉTUDES DE MARCHÉ COMPLÉMENTAIRES
- Données statistiques du {template_context['marche']}
- Enquêtes clients et études qualitatives
- Benchmarks concurrentiels détaillés
- Études sectorielles de référence

4. DOCUMENTS TECHNIQUES
- Fiches techniques des produits/services
- Processus de production détaillés
- Schémas et plans d'implantation
- Certifications qualité et normes

5. RESSOURCES HUMAINES
- CV détaillés de l'équipe dirigeante
- Lettres d'intention de futurs collaborateurs
- Organigramme prévisionnel
- Politique RH et grilles salariales

6. PARTENARIATS ET RÉFÉRENCES
- Lettres d'intention de clients potentiels
- Accords de partenariat signés
- Témoignages et recommandations
- Références et réalisations antérieures

Le contenu doit être:
- Bien organisé et référencé
- Supportant les affirmations du business plan
- Adapté au contexte congolais
- Professionnel et complet

Rédigez directement cette section annexes."""
    }

def get_queries_origin_style():
    """Requêtes utilisateur avec la logique EXACTE d'Origin.txt"""
    
    return {
        "Couverture": "Créez une page de couverture professionnelle pour ce business plan, incluant le titre, les informations de l'entreprise et une présentation visuelle attractive.",
        
        "Sommaire": "Rédigez un sommaire exécutif convaincant qui synthétise les points clés du business plan : opportunité, solution, marché, équipe, projections financières et besoins de financement.",
        
        "Présentation de votre entreprise": "Développez une présentation complète de l'entreprise couvrant son historique, sa mission, son statut juridique, ses activités et son positionnement sur le marché congolais.",
        
        "Étude de marché": "Réalisez une analyse de marché approfondie incluant la taille du marché, la concurrence, les segments clients, les tendances et les opportunités spécifiques au contexte congolais.",
        
        "Produits et services": "Présentez en détail l'offre de produits et services, en mettant l'accent sur la valeur ajoutée, l'innovation et l'adaptation aux besoins du marché local.",
        
        "Stratégie commerciale et marketing": "Élaborez une stratégie commerciale et marketing complète incluant le mix marketing, la stratégie de vente, la relation client et l'approche digitale adaptée au Congo.",
        
        "Équipe de direction": "Présentez l'équipe dirigeante en détaillant les profils, compétences, expériences et la complémentarité des membres dans le contexte du secteur d'activité.",
        
        "Plan opérationnel": "Décrivez l'organisation opérationnelle de l'entreprise : processus, infrastructure, logistique, ressources humaines et planning de développement.",
        
        "Analyse financière": "Développez une analyse financière complète avec projections sur 3-5 ans, incluant compte de résultat, bilan, trésorerie, ratios et analyse de sensibilité.",
        
        "Financement et investissements": "Présentez la stratégie de financement détaillée : besoins, sources de financement, structure du capital et utilisation des fonds.",
        
        "Annexes": "Organisez les annexes du business plan en regroupant les documents juridiques, financiers, techniques et les références qui supportent le projet."
    }