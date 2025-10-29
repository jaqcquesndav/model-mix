"""
Service de génération de business plan avec intégration des tableaux financiers
Version cyclique adaptée d'Origin.txt avec système de templates
"""

import streamlit as st
from typing import Dict, Any, List
from services.ai.content_generation import generate_section
from services.financial.calculations import calculer_tableaux_financiers_5_ans
from services.document.generation import format_table_to_markdown
from templates import get_metaprompt, get_system_messages
import pandas as pd
import tempfile
import os

def page_generation_business_plan_integree():
    """Page de génération du business plan avec tableaux financiers intégrés - Version cyclique"""
    st.title("🎯 Générateur de Business Plan Complet")
    
    # Récupération du template sélectionné
    template_actuel = st.session_state.get('template_selectionne', 'COPA TRANSFORME')
    
    st.info(f"🎨 **Template actuel :** {template_actuel}")
    st.info("📋 Cette version génère un business plan complet section par section, avec intégration automatique des tableaux financiers.")
    
    # Options de génération
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Option 1: Génération avec document")
        uploaded_file = st.file_uploader("Téléchargez un document de référence (PDF)", type="pdf", key="upload_doc")
        
        if uploaded_file:
            st.success(f"✅ Document chargé: {uploaded_file.name}")
    
    with col2:
        st.markdown("### ✍️ Option 2: Génération par description")
        user_text_input = st.text_area(
            "Décrivez votre projet/entreprise:",
            height=150,
            placeholder="Décrivez votre entreprise, ses produits/services, son marché cible, ses objectifs...",
            key="user_description"
        )
    
    # Options de génération
    st.markdown("### ⚙️ Options de génération")
    col_opt1, col_opt2, col_opt3 = st.columns(3)
    
    with col_opt1:
        use_workflow_data = st.checkbox(
            "📊 Utiliser les données du workflow",
            value=True,
            help="Utilise les données saisies dans l'application (Business Model, finances, etc.)"
        )
    
    with col_opt2:
        show_progress = st.checkbox(
            "📈 Affichage en temps réel",
            value=True,
            help="Affiche les sections au fur et à mesure de leur génération"
        )
    
    with col_opt3:
        split_generation = st.checkbox(
            "🔄 Génération en deux phases",
            value=True,
            help="Sépare la génération en deux parties comme dans Origin.txt"
        )
    
    # Validation et génération
    can_generate = uploaded_file is not None or user_text_input.strip() != "" or use_workflow_data
    
    if not can_generate:
        st.warning("⚠️ Veuillez soit télécharger un document, soit saisir une description, soit cocher 'Utiliser les données du workflow'")
        return
    
    if st.button("🚀 Générer le Business Plan Complet", type="primary", disabled=not can_generate):
        generate_complete_business_plan_cyclique(
            uploaded_file=uploaded_file,
            user_text_input=user_text_input,
            template_nom=template_actuel,
            use_workflow_data=use_workflow_data,
            show_progress=show_progress,
            split_generation=split_generation
        )

def generate_complete_business_plan_cyclique(uploaded_file=None, user_text_input="", template_nom="COPA TRANSFORME", 
                                           use_workflow_data=True, show_progress=True, split_generation=True):
    """Génère un business plan complet avec stratégie cyclique adaptée d'Origin.txt"""
    
    # 1. Préparation des documents et contexte
    documents = []
    combined_content = user_text_input if user_text_input else ""
    
    if uploaded_file:
        documents = process_uploaded_pdf(uploaded_file)
        if documents:
            st.success(f"✅ {len(documents)} documents PDF traités")
    
    # 2. Récupération des données selon les options
    business_data = {}
    financial_tables_text = ""
    
    if use_workflow_data:
        business_data = collect_all_business_data()
        financial_tables = generate_all_financial_tables()
        financial_tables_text = financial_tables.get('formatted_text', '')
        
        if business_data:
            st.success("✅ Données du workflow récupérées")
    
    # 3. Configuration des sections selon le template
    sections_config = get_business_plan_sections_by_template(template_nom)
    
    # 4. Génération cyclique avec stratégie d'Origin.txt
    results = {}
    placeholders = {}
    
    if show_progress:
        # Créer des espaces réservés pour chaque section
        placeholders = {name: st.empty() for name in sections_config.keys()}
    
    # 5. Logique de génération en deux phases (comme Origin.txt)
    if split_generation:
        # Définir le point de séparation 
        section_order = list(sections_config.keys())
        split_section = "Présentation de votre entreprise"
        
        # Séparer les sections en deux groupes
        first_part = []
        second_part = []
        for section in section_order:
            if section == split_section:
                first_part.append(section)
                second_part = section_order[section_order.index(section)+1:]
                break
            else:
                first_part.append(section)
        
        # Génération première partie
        st.markdown("### 🔄 **Phase 1 : Sections fondamentales**")
        progress_bar_1 = st.progress(0)
        
        for i, section_name in enumerate(first_part):
            if show_progress:
                with st.spinner(f"🎯 Génération de {section_name}..."):
                    generate_section_cyclique(
                        section_name, sections_config[section_name], documents,
                        combined_content, financial_tables_text, business_data,
                        results, placeholders, template_nom
                    )
                    combined_content += " " + results[section_name]
            else:
                generate_section_cyclique(
                    section_name, sections_config[section_name], documents,
                    combined_content, financial_tables_text, business_data,
                    results, placeholders, template_nom
                )
                combined_content += " " + results[section_name]
            
            progress_bar_1.progress((i + 1) / len(first_part))
        
        st.success("✅ Phase 1 terminée")
        
        # Génération seconde partie
        st.markdown("### 🔄 **Phase 2 : Sections avancées**")
        progress_bar_2 = st.progress(0)
        
        for i, section_name in enumerate(second_part):
            if show_progress:
                with st.spinner(f"🎯 Génération de {section_name}..."):
                    generate_section_cyclique(
                        section_name, sections_config[section_name], documents,
                        combined_content, financial_tables_text, business_data,
                        results, placeholders, template_nom
                    )
                    combined_content += " " + results[section_name]
            else:
                generate_section_cyclique(
                    section_name, sections_config[section_name], documents,
                    combined_content, financial_tables_text, business_data,
                    results, placeholders, template_nom
                )
                combined_content += " " + results[section_name]
            
            progress_bar_2.progress((i + 1) / len(second_part))
        
        st.success("✅ Phase 2 terminée")
        
    else:
        # Génération continue
        progress_bar = st.progress(0)
        section_list = list(sections_config.keys())
        
        for i, section_name in enumerate(section_list):
            if show_progress:
                with st.spinner(f"🎯 Génération de {section_name}..."):
                    generate_section_cyclique(
                        section_name, sections_config[section_name], documents,
                        combined_content, financial_tables_text, business_data,
                        results, placeholders, template_nom
                    )
                    combined_content += " " + results[section_name]
            else:
                generate_section_cyclique(
                    section_name, sections_config[section_name], documents,
                    combined_content, financial_tables_text, business_data,
                    results, placeholders, template_nom
                )
                combined_content += " " + results[section_name]
            
            progress_bar.progress((i + 1) / len(section_list))
    
    # 6. Génération des fichiers de sortie
    create_export_files_cyclique(results, business_data, template_nom)

def generate_section_cyclique(section_name, section_config, documents, combined_content, 
                            financial_tables_text, business_data, results, placeholders, template_nom):
    """Génère une section individuelle avec la logique cyclique"""
    
    try:
        system_message = section_config["system_message"]
        query = section_config["query"]
        
        # Adaptation du contexte selon la section (comme Origin.txt)
        if section_name in ["Couverture", "Sommaire"]:
            # Sections simples sans contexte complexe
            content = generate_section(
                system_message=system_message,
                user_query=query,
                additional_context=combined_content,
                section_name=section_name
            )
        else:
            # Sections avec contexte business model et financier
            business_model = business_data.get('business_model', st.session_state.get('business_model_precedent', ''))
            
            content = generate_section(
                system_message=system_message,
                user_query=query,
                additional_context=combined_content + "\n\n" + financial_tables_text,
                section_name=section_name
            )
        
        results[section_name] = content
        
        # Affichage en temps réel si demandé
        if placeholders and section_name in placeholders:
            placeholders[section_name].markdown(f"### {section_name}\n{content}")
            
    except Exception as e:
        error_msg = f"❌ Erreur lors de la génération de {section_name}: {str(e)}"
        results[section_name] = error_msg
        
        if placeholders and section_name in placeholders:
            placeholders[section_name].error(error_msg)

def collect_all_business_data() -> Dict[str, Any]:
    """Collecte toutes les données business de l'application avec logique cyclique"""
    data = st.session_state.get("data", {})
    
    return {
        "business_model": st.session_state.get('business_model_precedent', '') or st.session_state.get('business_model_initial', {}),
        "persona": st.session_state.get('persona_data', {}),
        "marche": st.session_state.get('analyse_marche', {}),
        "concurrence": st.session_state.get('concurrence', {}),
        "facteurs_limitants": st.session_state.get('facteurs_limitants_data', {}),
        "arbre_probleme": st.session_state.get('arbre_probleme', {}),
        "informations_generales": data.get("informations_generales", {}),
        "ca_previsions": data.get("ca_previsions", {}),
        "charges_variables": data.get("charges_variables", {}),
        "charges_fixes": data.get("charges_fixes", {}),
        "salaires": data.get("salaires", {}),
        "investissements": data.get("besoins_demarrage", {}),
        "financements": data.get("financements", {})
    }

def generate_all_financial_tables() -> Dict[str, Any]:
    """Génère tous les tableaux financiers et les formate pour le business plan cyclique"""
    
    data = st.session_state.get("data", {})
    
    try:
        # Utiliser notre service de calculs 5 ans
        tableaux_5_ans = calculer_tableaux_financiers_5_ans()
        
        # Formater tous les tableaux pour inclusion dans le business plan
        formatted_tables = format_financial_tables_for_business_plan_cyclique(tableaux_5_ans)
        
        return {
            "raw_data": tableaux_5_ans,
            "formatted_text": formatted_tables,
            "tables_list": list(tableaux_5_ans.keys()) if tableaux_5_ans else []
        }
        
    except Exception as e:
        st.warning(f"Erreur lors de la génération des tableaux financiers: {str(e)}")
        
        # Fallback vers les données exportées du session state (comme Origin.txt)
        return get_financial_tables_from_session()

def get_financial_tables_from_session() -> Dict[str, Any]:
    """Récupère les tableaux financiers depuis le session state (logique Origin.txt)"""
    
    # Récupérer les données exportées de toutes les sections (comme dans Origin.txt)
    export_data = {
        'investissements': st.session_state.get('export_data_investissements', {}),
        'salaires': st.session_state.get('export_data_salaires_charges_sociales', {}),
        'amortissements': st.session_state.get('export_data_detail_amortissements', {}),
        'compte': st.session_state.get('export_data_compte_resultats_previsionnel', {}),
        'soldes': st.session_state.get('export_data_soldes_intermediaires_de_gestion', {}),
        'capacite': st.session_state.get('export_data_capacite_autofinancement', {}),
        'seuil': st.session_state.get('export_data_seuil_rentabilite_economique', {}),
        'bfr': st.session_state.get('export_data_besoin_fonds_roulement', {}),
        'plan_financement': st.session_state.get('export_data_plan_financement_trois_ans', {}),
        'budget_part1': st.session_state.get('export_data_budget_previsionnel_tresorerie_part1', {}),
        'budget_part2': st.session_state.get('export_data_budget_previsionnel_tresorerie_part2', {})
    }
    
    # Formater le texte final (comme dans Origin.txt)
    final_text = ""
    section_titles = {
        'investissements': "Investissements et financements",
        'salaires': "Salaires et Charges Sociales", 
        'amortissements': "Détail des Amortissements",
        'compte': "Compte de résultats prévisionnel",
        'soldes': "Soldes intermédiaires de gestion",
        'capacite': "Capacité d'autofinancement",
        'seuil': "Seuil de rentabilité économique",
        'bfr': "Besoin en fonds de roulement",
        'plan_financement': "Plan de financement à trois ans",
        'budget_part1': "Budget prévisionnel de trésorerie",
        'budget_part2': "Budget prévisionnel de trésorerie (suite)"
    }
    
    for key, title in section_titles.items():
        if export_data[key]:
            final_text += format_table_data_cyclique(export_data[key], title)
    
    return {
        "raw_data": export_data,
        "formatted_text": final_text,
        "tables_list": list(section_titles.keys())
    }

def format_financial_tables_for_business_plan_cyclique(tableaux_data: Dict[str, Any]) -> str:
    """Formate tous les tableaux financiers en texte pour inclusion dans le business plan (style cyclique)"""
    
    if not tableaux_data:
        return "⚠️ Aucune donnée financière disponible"
    
    formatted_text = "\n\n### TABLEAUX FINANCIERS DÉTAILLÉS\n\n"
    
    # Tableaux principaux à inclure (priorité cyclique Origin.txt)
    tables_config = {
        "compte_resultats_5ans": {
            "title": "Compte de Résultats Prévisionnel (5 ans)",
            "description": "Évolution prévisionnelle des revenus et charges sur 5 années"
        },
        "plan_financement_5ans": {
            "title": "Plan de Financement (5 ans)", 
            "description": "Équilibre emplois/ressources sur 5 années"
        },
        "soldes_intermediaires_5ans": {
            "title": "Soldes Intermédiaires de Gestion",
            "description": "Indicateurs de performance financière"
        },
        "capacite_autofinancement_5ans": {
            "title": "Capacité d'Autofinancement",
            "description": "Ressources internes générées par l'activité"
        },
        "seuil_rentabilite_5ans": {
            "title": "Analyse du Seuil de Rentabilité",
            "description": "Point mort et analyse de rentabilité"
        },
        "bfr_5ans": {
            "title": "Besoin en Fonds de Roulement",
            "description": "Calcul et évolution du BFR"
        }
    }
    
    for table_key, config in tables_config.items():
        if table_key in tableaux_data:
            table_data = tableaux_data[table_key]
            
            formatted_text += f"\n#### {config['title']}\n\n"
            formatted_text += f"*{config['description']}*\n\n"
            
            # Formater le tableau selon son type
            if isinstance(table_data, dict) and "table_data" in table_data:
                formatted_text += format_table_to_markdown(table_data["table_data"])
            elif isinstance(table_data, dict) and "data" in table_data:
                formatted_text += format_table_to_markdown(table_data["data"])
            else:
                formatted_text += "Données non disponibles pour ce tableau\n\n"
            
            formatted_text += "---\n\n"
    
    return formatted_text

def format_table_data_cyclique(data: Dict[str, Any], title: str) -> str:
    """Formate les données de tableau en texte (style Origin.txt)"""
    if not data:
        return ""
    
    text = f"\n\n### {title}\n\n"
    
    # Si c'est une structure de table avec table_data
    if isinstance(data, dict) and "table_data" in data:
        table_data = data["table_data"]
        if isinstance(table_data, list) and table_data:
            # Convertir en DataFrame pour le formatage
            try:
                df = pd.DataFrame(table_data)
                text += df.to_markdown(index=False)
                text += "\n\n"
            except:
                # Fallback simple
                for row in table_data:
                    if isinstance(row, dict):
                        for key, value in row.items():
                            text += f"  {key}: {value}\n"
                    text += "\n"
    
    # Si c'est un dictionnaire simple
    elif isinstance(data, dict):
        for key, value in data.items():
            if key != "table_data":  # Éviter la redondance
                text += f"  **{key}**: {value}\n"
        text += "\n"
    
    return text


# Fonction manquante pour compatibilité avec le système existant
def prepare_section_context(section_name: str, business_data: Dict, financial_tables: Dict, user_input: str) -> str:
    """Prépare le contexte spécifique pour chaque section (compatibilité)"""
    
    base_context = f"""
DONNÉES BUSINESS MODEL: {business_data.get('business_model', '')}

INFORMATIONS GÉNÉRALES: {business_data.get('informations_generales', {})}

INFORMATIONS UTILISATEUR: {user_input}
"""
    
    # Contexte spécifique selon la section
    if section_name == "Plan financier":
        # Pour la section financière, inclure tous les tableaux
        return base_context + f"\n\nTABLEAUX FINANCIERS:\n{financial_tables.get('formatted_text', '')}"
    
    elif section_name in ["Résumé Exécutif", "Présentation de votre entreprise"]:
        # Inclure les données business principales
        return base_context + f"""
PERSONA: {business_data.get('persona', {})}
ANALYSE MARCHÉ: {business_data.get('marche', {})}
CONCURRENCE: {business_data.get('concurrence', {})}
"""
    
    else:
        return base_context

def prepare_section_context(section_name: str, business_data: Dict, financial_tables: Dict, user_input: str) -> str:
    """Prépare le contexte spécifique pour chaque section"""
    
    base_context = f"""
DONNÉES BUSINESS MODEL: {business_data.get('business_model', '')}

INFORMATIONS GÉNÉRALES: {business_data.get('informations_generales', {})}

INFORMATIONS UTILISATEUR: {user_input}
"""
    
    # Contexte spécifique selon la section
    if section_name == "Plan financier":
        # Pour la section financière, inclure tous les tableaux
        return base_context + f"\n\nTABLEAUX FINANCIERS:\n{financial_tables.get('formatted_text', '')}"
    
    elif section_name in ["Résumé Exécutif", "Présentation de votre entreprise"]:
        # Inclure les données business principales
        return base_context + f"""
PERSONA: {business_data.get('persona', {})}
ANALYSE MARCHÉ: {business_data.get('marche', {})}
CONCURRENCE: {business_data.get('concurrence', {})}
"""
    
    else:
        return base_context

def get_business_plan_sections_by_template(template_nom="COPA TRANSFORME") -> Dict[str, Dict[str, str]]:
    """Définit les sections du business plan selon le template sélectionné avec style Origin.txt"""
    
    # Récupérer les messages système spécialisés du template
    template_system_messages = get_system_messages(template_nom)
    
    # Structure de base adaptée d'Origin.txt
    base_sections = {
        "Couverture": {
            "system_message": f"""
            Générer cette section du business plan selon le template {template_nom}:
            
            # Canevas de Plans d'Affaires
            **Template :** {template_nom}
            
            Nom du projet ou entreprise
            Secteur d'activité
            Date de création du plan
            
            Générer une couverture professionnelle adaptée au contexte.
            """,
            "query": "Créer une page de couverture professionnelle"
        },
        
        "Sommaire": {
            "system_message": f"""
            Générer cette section du business plan selon le template {template_nom}:
            
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
            
            Afficher le sommaire structuré sous forme de liste numérotée.
            """,
            "query": "Afficher le sommaire du business plan"
        },
        
        "Résumé Exécutif": {
            "system_message": template_system_messages.get("business_plan", f"""
            Vous êtes un expert en développement économique spécialisé dans le template {template_nom}.
            
            Générer cette section du business plan:
            
            ## I. Résumé Exécutif « Executive Summary » / Pitch
            
            Générer deux grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
            - Attirer l'attention du lecteur en 5 minutes et lui donner envie d'en savoir plus
            - Décrire le projet en quelques phrases simples et impactantes
            - Ne pas essayer de tout couvrir, soyez concis et précis
            
            Les éléments clés à générer et qui doivent être contenus dans les paragraphes :
            - **Présentation de la PME** : Nom de l'entreprise et brève description du service/produit fourni
            - **Présentation des porteurs de projet** : Profil des entrepreneurs
            - **Potentiel en termes de taille et de profit** : Démontrez comment l'entreprise fera du profit
            - **Besoin financier** : Montant nécessaire et utilisation prévue
            
            Adaptez le contenu au contexte et aux spécificités du template {template_nom}.
            """),
            "query": "Décrire brièvement le projet, son potentiel de profit et les qualifications de l'équipe."
        },
        
        "Présentation de votre entreprise": {
            "system_message": template_system_messages.get("business_plan", f"""
            Vous êtes un expert en développement économique spécialisé dans le template {template_nom}.
            
            Générer cette section du business plan:

            ## II. Présentation de votre entreprise/projet

            Générer 6 grands paragraphes avec plusieurs lignes, l'objectif pour cette section est de :
            - Parler de votre entreprise/projet de manière plus détaillée
            - Présenter l'équipe managériale clé

            Les éléments clés à générer et qui doivent être contenus dans les paragraphes :
            - **Informations générales sur la PME** : Forme juridique, siège social, coordonnées, couverture géographique
            - **Description détaillée de la PME et objectifs** : Origine, atouts/opportunités, description du projet
            - **Stade d'avancement** : Ce qui a été fait, projets futurs, niveau de maturité, financements acquis
            - **Équipe managériale** : Organigramme, ressources humaines, associés et parts sociales
            - **Analyse SWOT** : Forces, faiblesses, opportunités, contraintes/menaces (de préférence sous forme de tableau)
            - **Business Model Canvas** : Les 9 rubriques bien remplies selon le template {template_nom}
            
            Adaptez le contenu aux spécificités du template {template_nom}.
            """),
            "query": "Présenter l'entreprise de façon complète et structurée selon le template"
        }
    }
    
    # Ajouter les sections spécialisées selon le template
    if template_nom == "COPA TRANSFORME":
        base_sections.update(get_copa_specialized_sections())
    elif template_nom == "Virunga":
        base_sections.update(get_virunga_specialized_sections())
    elif template_nom == "IP Femme":
        base_sections.update(get_ip_femme_specialized_sections())
    
    return base_sections

def get_copa_specialized_sections():
    """Sections spécialisées pour COPA TRANSFORMÉ"""
    return {
        "Présentation de l'offre de produit": {
            "system_message": """
            Vous êtes un expert COPA TRANSFORMÉ spécialisé dans l'agrotransformation et l'autonomisation des femmes en RDC.
            
            ## III. Présentation de l'offre de produit(s) et/ou service(s)
            
            Générer 5 grands paragraphes focalisés sur :
            - **Produits/services agroalimentaires** : Transformation locale, chaînes de valeur
            - **Besoins identifiés** : Sécurité alimentaire, création de valeur ajoutée locale
            - **Description détaillée** : Processus de transformation, qualité, traçabilité
            - **Proposition de valeur unique** : Autonomisation des femmes, développement rural
            - **Aspect genre et environnement** : Impact social, durabilité environnementale
            
            Intégrez les spécificités COPA TRANSFORMÉ : développement économique rural, chaînes de valeur agricoles.
            """,
            "query": "Décrire l'offre dans le contexte COPA TRANSFORMÉ agroalimentaire"
        },
        
        "Étude de marché": {
            "system_message": """
            Expert COPA TRANSFORMÉ - Analyse de marché agroalimentaire RDC.
            
            ## IV. Étude de marché
            
            Analyser selon 8 axes COPA spécialisés :
            1. **Méthodologie** : Étude des chaînes de valeur agricoles, marchés ruraux/urbains
            2. **Marché général** : Secteur agroalimentaire RDC, sécurité alimentaire, import/export
            3. **Demande** : Consommation locale, préférences alimentaires, pouvoir d'achat rural/urbain
            4. **Offre concurrentielle** : Transformateurs locaux, importations, circuits informels
            5. **Environnement** : Politique agricole, réglementation sanitaire, infrastructures rurales
            6. **Partenariats** : Coopératives agricoles, organismes de développement, institutions de financement agricole
            7. **Emplois** : Impact sur l'emploi rural, autonomisation des femmes, jeunes agriculteurs
            8. **CA prévisionnel** : Saisonnalité agricole, circuits de commercialisation
            
            Focalisez sur le contexte rural congolais et la transformation agricole.
            """,
            "query": "Analyser le marché agroalimentaire selon les spécificités COPA TRANSFORMÉ"
        }
    }

def get_virunga_specialized_sections():
    """Sections spécialisées pour Virunga"""
    return {
        "Présentation de l'offre de produit": {
            "system_message": """
            Expert Virunga - Conservation et développement durable.
            
            ## III. Présentation de l'offre de produit(s) et/ou service(s)
            
            Générer selon l'approche Virunga :
            - **Produits/services éco-responsables** : Écotourisme, produits forestiers durables
            - **Besoins environnementaux** : Conservation biodiversité, développement communautaire
            - **Description écologique** : Impact environnemental positif, durabilité
            - **Valeur conservation** : Protection écosystème, revenus communautaires
            - **Approche genre et environnement** : Femmes dans la conservation, éducation environnementale
            """,
            "query": "Décrire l'offre dans le contexte conservation Virunga"
        }
    }

def get_ip_femme_specialized_sections():
    """Sections spécialisées pour IP Femme"""
    return {
        "Présentation de l'offre de produit": {
            "system_message": """
            Expert IP Femme - Autonomisation économique des femmes.
            
            ## III. Présentation de l'offre de produit(s) et/ou service(s)
            
            Générer selon l'approche IP Femme :
            - **Produits/services par les femmes** : Artisanat, services, technologies adaptées
            - **Besoins d'autonomisation** : Indépendance économique, compétences entrepreneuriales
            - **Description inclusive** : Accessibilité, formation, accompagnement
            - **Valeur sociale** : Empowerment, équité genre, impact communautaire
            - **Genre et innovation** : Leadership féminin, innovations sociales
            """,
            "query": "Décrire l'offre dans le contexte autonomisation IP Femme"
        }
    }

def create_export_files_cyclique(results: Dict[str, str], business_data: Dict[str, Any], template_nom: str):
    """Crée les fichiers d'export avec style cyclique Origin.txt"""
    
    st.subheader("📥 Téléchargements")
    
    # Créer le contenu complet avec métadonnées du template
    complete_content = f"""# Business Plan Complet - Template {template_nom}
**Date de génération :** {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}
**Entreprise :** {business_data.get('informations_generales', {}).get('nom_entreprise', 'Non spécifiée')}
**Template utilisé :** {template_nom}

---

"""
    
    # Ajouter toutes les sections générées
    for section_name, content in results.items():
        complete_content += f"\n\n## {section_name}\n\n{content}"
    
    # Options d'export
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Télécharger Word"):
            try:
                word_buffer = generate_word_document_cyclique(results, business_data, template_nom)
                st.download_button(
                    label="⬇️ Business Plan.docx",
                    data=word_buffer,
                    file_name=f"business_plan_{template_nom.lower().replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                st.error(f"Erreur génération Word : {str(e)}")
    
    with col2:
        if st.button("📑 Télécharger Markdown"):
            st.download_button(
                label="⬇️ Business Plan.md",
                data=complete_content,
                file_name=f"business_plan_{template_nom.lower().replace(' ', '_')}.md",
                mime="text/markdown"
            )
    
    with col3:
        if st.button("📊 Données JSON"):
            try:
                export_data = {
                    "template": template_nom,
                    "timestamp": pd.Timestamp.now().isoformat(),
                    "business_data": business_data,
                    "sections": results
                }
                
                import json
                json_data = json.dumps(export_data, indent=2, ensure_ascii=False, default=str)
                
                st.download_button(
                    label="⬇️ Données.json",
                    data=json_data,
                    file_name=f"business_data_{template_nom.lower().replace(' ', '_')}.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"Erreur export JSON : {str(e)}")

def generate_word_document_cyclique(results: Dict[str, str], business_data: Dict[str, Any], template_nom: str):
    """Génère un document Word avec style cyclique et template"""
    from docx import Document
    from docx.shared import Inches
    from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
    from io import BytesIO
    import re
    
    doc = Document()
    
    # En-tête avec informations du template
    header = doc.sections[0].header
    header_para = header.paragraphs[0]
    header_para.text = f"Business Plan - Template {template_nom}"
    header_para.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
    
    # Titre principal
    title = doc.add_heading(f'Business Plan Complet', 0)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # Sous-titre avec template
    subtitle = doc.add_paragraph(f"Template : {template_nom}")
    subtitle.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    subtitle.runs[0].bold = True
    
    # Informations métadonnées
    meta_para = doc.add_paragraph()
    meta_para.add_run("Date de génération : ").bold = True
    meta_para.add_run(pd.Timestamp.now().strftime('%d/%m/%Y %H:%M'))
    meta_para.add_run("\nEntreprise : ").bold = True
    meta_para.add_run(business_data.get('informations_generales', {}).get('nom_entreprise', 'Non spécifiée'))
    
    doc.add_page_break()
    
    # Ajouter chaque section avec traitement markdown basique
    for section_name, content in results.items():
        
        # Titre de section
        doc.add_heading(section_name, 1)
        
        # Traitement du contenu markdown (adapté d'Origin.txt)
        lines = content.split('\n')
        table_data = []
        inside_table = False
        
        for line in lines:
            line = line.strip()
            if not line:
                if table_data:
                    add_table_with_borders_cyclique(doc, table_data)
                    table_data = []
                    inside_table = False
                continue
            
            if line.startswith('###'):
                doc.add_heading(line[3:].strip(), level=3)
            elif line.startswith('##'):
                doc.add_heading(line[2:].strip(), level=2)
            elif line.startswith('#'):
                doc.add_heading(line[1:].strip(), level=1)
            elif line.startswith('|') and '|' in line:
                # Tableau détecté
                if not inside_table:
                    inside_table = True
                if not line.replace('|', '').replace('-', '').replace(' ', '').strip():
                    continue  # Ligne de séparation
                table_data.append([cell.strip() for cell in line.split('|')[1:-1]])
            elif re.match(r'^\d+\.', line):
                doc.add_paragraph(line, style='List Number')
            elif line.startswith('- ') or line.startswith('• '):
                doc.add_paragraph(line[2:], style='List Bullet')
            else:
                if inside_table and table_data:
                    add_table_with_borders_cyclique(doc, table_data)
                    table_data = []
                    inside_table = False
                
                # Traitement du texte en gras **texte**
                para = doc.add_paragraph()
                parts = re.split(r'(\*\*.+?\*\*)', line)
                for part in parts:
                    if part.startswith('**') and part.endswith('**'):
                        run = para.add_run(part[2:-2])
                        run.bold = True
                    else:
                        para.add_run(part)
        
        # Traiter la dernière table si elle existe
        if table_data:
            add_table_with_borders_cyclique(doc, table_data)
    
    # Sauvegarder en buffer
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    return buffer.getvalue()

def add_table_with_borders_cyclique(doc, table_data):
    """Ajoute un tableau avec bordures au document Word (style Origin.txt)"""
    if not table_data:
        return
    
    from docx.enum.table import WD_TABLE_ALIGNMENT
    
    num_cols = len(table_data[0])
    table = doc.add_table(rows=len(table_data), cols=num_cols)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for i, row in enumerate(table_data):
        for j, cell_content in enumerate(row):
            if j < len(table.columns):
                cell = table.cell(i, j)
                cell.text = str(cell_content)
                
                # Style de la première ligne (en-tête)
                if i == 0:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            run.bold = True

def process_uploaded_pdf(uploaded_file):
    """Traite un fichier PDF uploadé (comme dans Origin.txt)"""
    try:
        # Sauvegarder temporairement le fichier
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
        
        # Charger et diviser le document (utilise les fonctions LangChain existantes)
        from services.ai.content_generation import load_and_split_documents
        documents = load_and_split_documents(tmp_file_path)
        
        # Nettoyer le fichier temporaire
        os.unlink(tmp_file_path)
        
        return documents
        
    except Exception as e:
        st.error(f"Erreur lors du traitement du PDF : {str(e)}")
        return []

def process_uploaded_pdf(uploaded_file):
    """Traite un fichier PDF uploadé"""
    # À implémenter si nécessaire
    return []