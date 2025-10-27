"""
Service de génération de business plan avec intégration des tableaux financiers
"""

import streamlit as st
from typing import Dict, Any, List
from services.ai.content_generation import generate_section
from services.financial.calculations import calculer_tableaux_financiers_5_ans
import pandas as pd

def page_generation_business_plan_integree():
    """Page de génération du business plan avec tableaux financiers intégrés"""
    st.title("🎯 Générateur de Business Plan Complet")
    
    st.info("Cette version intègre automatiquement tous les tableaux financiers dans le plan d'affaires.")
    
    # Upload de fichier optionnel
    uploaded_file = st.file_uploader("📄 Téléchargez un document de référence (PDF)", type="pdf")
    user_text_input = st.text_area("📝 Informations supplémentaires:", height=150)
    
    if st.button("🚀 Générer le Business Plan Complet", type="primary"):
        generate_complete_business_plan(uploaded_file, user_text_input)

def generate_complete_business_plan(uploaded_file=None, user_text_input=""):
    """Génère un business plan complet avec tous les tableaux financiers"""
    
    # 1. Préparation des données
    documents = []
    if uploaded_file:
        # Traitement du fichier PDF
        documents = process_uploaded_pdf(uploaded_file)
    
    # 2. Récupération de toutes les données
    business_data = collect_all_business_data()
    financial_tables = generate_all_financial_tables()
    
    # 3. Génération section par section
    sections = get_business_plan_sections()
    results = {}
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_sections = len(sections)
    
    for i, (section_name, section_config) in enumerate(sections.items()):
        status_text.text(f"Génération de {section_name}...")
        
        # Préparer le contexte spécifique à la section
        context = prepare_section_context(
            section_name, 
            business_data, 
            financial_tables, 
            user_text_input
        )
        
        # Générer la section
        try:
            results[section_name] = generate_section(
                section_config["system_message"],
                section_config["query"],
                documents,
                context,
                financial_tables.get("formatted_text", ""),
                business_model=business_data.get("business_model", ""),
                section_name=section_name
            )
        except Exception as e:
            st.error(f"Erreur lors de la génération de {section_name}: {str(e)}")
            results[section_name] = f"⚠️ Section non générée: {str(e)}"
        
        # Mise à jour de la progress bar
        progress_bar.progress((i + 1) / total_sections)
        
        # Affichage immédiat du résultat
        st.markdown(f"## {section_name}")
        st.markdown(results[section_name])
        st.divider()
    
    status_text.text("✅ Génération terminée!")
    
    # 4. Création des fichiers de sortie
    create_export_files(results, financial_tables)

def collect_all_business_data() -> Dict[str, Any]:
    """Collecte toutes les données business de l'application"""
    data = st.session_state.get("data", {})
    
    return {
        "business_model": st.session_state.get('business_model_precedent', ''),
        "persona": st.session_state.get('persona_data', {}),
        "marche": st.session_state.get('analyse_marche', {}),
        "concurrence": st.session_state.get('concurrence', {}),
        "facteurs_limitants": st.session_state.get('facteurs_limitants_data', {}),
        "arbre_probleme": st.session_state.get('problem_tree_data', {}),
        "informations_generales": data.get("informations_generales", {}),
        "ca_previsions": data.get("ca_previsions", {}),
        "charges_variables": data.get("charges_variables", {}),
        "charges_fixes": data.get("charges_fixes", {}),
        "salaires": data.get("salaires", {}),
        "investissements": data.get("besoins_demarrage", {}),
        "financements": data.get("financements", {})
    }

def generate_all_financial_tables() -> Dict[str, Any]:
    """Génère tous les tableaux financiers et les formate pour le business plan"""
    
    data = st.session_state.get("data", {})
    
    # Utiliser notre nouveau service de calculs 5 ans
    try:
        tableaux_5_ans = calculer_tableaux_financiers_5_ans(data)
        
        # Formater tous les tableaux pour inclusion dans le business plan
        formatted_tables = format_financial_tables_for_business_plan(tableaux_5_ans)
        
        return {
            "raw_data": tableaux_5_ans,
            "formatted_text": formatted_tables,
            "tables_list": list(tableaux_5_ans.keys()) if tableaux_5_ans else []
        }
        
    except Exception as e:
        st.warning(f"Erreur lors de la génération des tableaux financiers: {str(e)}")
        return {
            "raw_data": {},
            "formatted_text": "⚠️ Tableaux financiers non disponibles - Veuillez compléter les données financières",
            "tables_list": []
        }

def format_financial_tables_for_business_plan(tableaux_data: Dict[str, Any]) -> str:
    """Formate tous les tableaux financiers en texte pour inclusion dans le business plan"""
    
    if not tableaux_data:
        return "⚠️ Aucune donnée financière disponible"
    
    formatted_text = "\n\n### TABLEAUX FINANCIERS DÉTAILLÉS\n\n"
    
    # Tableaux principaux à inclure
    tables_config = {
        "compte_resultats_5_ans": {
            "title": "Compte de Résultats Prévisionnel (5 ans)",
            "description": "Evolution prévisionnelle des revenus et charges sur 5 années"
        },
        "plan_financement_5_ans": {
            "title": "Plan de Financement (5 ans)", 
            "description": "Équilibre emplois/ressources sur 5 années"
        },
        "tresorerie_mensuelle": {
            "title": "Budget de Trésorerie Mensuel",
            "description": "Prévisions de trésorerie mois par mois"
        },
        "soldes_intermediaires": {
            "title": "Soldes Intermédiaires de Gestion",
            "description": "Indicateurs de performance financière"
        },
        "seuil_rentabilite": {
            "title": "Analyse du Seuil de Rentabilité",
            "description": "Point mort et analyse de rentabilité"
        },
        "besoin_fonds_roulement": {
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
            
            # Ajouter l'analyse si disponible
            if isinstance(table_data, dict) and "analyse" in table_data:
                formatted_text += f"\n**Analyse:**\n{table_data['analyse']}\n\n"
            
            formatted_text += "---\n\n"
    
    return formatted_text

def format_table_to_markdown(table_data: List[Dict]) -> str:
    """Convertit des données de tableau en format Markdown"""
    
    if not table_data or not isinstance(table_data, list):
        return "Aucune donnée disponible\n\n"
    
    # Créer le DataFrame
    df = pd.DataFrame(table_data)
    
    # Convertir en Markdown
    markdown_table = df.to_markdown(index=False)
    
    return f"{markdown_table}\n\n"

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

def get_business_plan_sections() -> Dict[str, Dict[str, str]]:
    """Définit toutes les sections du business plan avec leurs configurations"""
    
    return {
        "Couverture": {
            "system_message": """
Générer la page de couverture du business plan:

# PLAN D'AFFAIRES

**Nom du projet/entreprise:** [À extraire des données]

**Secteur d'activité:** [À définir selon les données]

**Date:** [Date actuelle]

**Porteur(s) de projet:** [À extraire des informations générales]
""",
            "query": "Créer une page de couverture professional"
        },
        
        "Sommaire": {
            "system_message": """
Générer le sommaire du business plan:

## SOMMAIRE

I. Résumé Exécutif
II. Présentation de l'entreprise/projet  
III. Présentation de l'offre (produits/services)
IV. Étude de marché
V. Stratégie marketing et commerciale
VI. Moyens de production et organisation
VII. Étude des risques
VIII. Plan financier
IX. Annexes
""",
            "query": "Afficher le sommaire structuré du business plan"
        },
        
        "Résumé Exécutif": {
            "system_message": """
Générer le résumé exécutif du business plan:

## I. RÉSUMÉ EXÉCUTIF

L'objectif est d'attirer l'attention en 5 minutes et donner envie d'en savoir plus.

Éléments à inclure (2-3 paragraphes impactants):
- Présentation de l'entreprise et de son offre
- Présentation des porteurs de projet
- Potentiel de marché et de profit
- Besoins financiers

Soyez concis, précis et impactant.
""",
            "query": "Rédiger un résumé exécutif percutant"
        },
        
        "Présentation de votre entreprise": {
            "system_message": """
Générer la présentation détaillée de l'entreprise:

## II. PRÉSENTATION DE L'ENTREPRISE/PROJET

Développer en 6 paragraphes:
1. **Informations générales** (forme juridique, siège, coordonnées)
2. **Description détaillée et objectifs** 
3. **Stade d'avancement** (réalisations, projets futurs)
4. **Équipe managériale** (organigramme, associés)
5. **Analyse SWOT** (forces, faiblesses, opportunités, menaces)
6. **Business Model Canvas** (9 rubriques détaillées)
""",
            "query": "Présenter l'entreprise de façon complète et structurée"
        },
        
        "Présentation de l'offre de produit": {
            "system_message": """
Générer la présentation de l'offre:

## III. PRÉSENTATION DE L'OFFRE (PRODUITS/SERVICES)

Développer en 5 paragraphes:
1. **Noms des produits/services**
2. **Besoins identifiés** sur le marché
3. **Description détaillée** de l'offre
4. **Proposition de valeur unique**
5. **Prise en compte de l'aspect genre**
""",
            "query": "Décrire l'offre produits/services et sa valeur unique"
        },
        
        "Étude de marché": {
            "system_message": """
Générer l'étude de marché:

## IV. ÉTUDE DE MARCHÉ

Analyser en détail:
1. **Taille et tendances du marché**
2. **Segmentation de la clientèle**
3. **Analyse de la concurrence**
4. **Positionnement concurrentiel**
5. **Opportunités et menaces**
""",
            "query": "Analyser le marché cible et l'environnement concurrentiel"
        },
        
        "Stratégie Marketing": {
            "system_message": """
Générer la stratégie marketing:

## V. STRATÉGIE MARKETING ET COMMERCIALE

Détailler:
1. **Segments cibles**
2. **Positionnement**
3. **Mix marketing** (Produit, Prix, Place, Promotion)
4. **Actions commerciales prévues**
5. **Objectifs et indicateurs**
""",
            "query": "Définir la stratégie marketing et commerciale"
        },
        
        "Moyens de production et organisation": {
            "system_message": """
Générer la section moyens et organisation:

## VI. MOYENS DE PRODUCTION ET ORGANISATION

Présenter:
1. **Moyens humains** (équipe, recrutements)
2. **Moyens matériels** (équipements, locaux)
3. **Organisation opérationnelle**
4. **Processus de production/service**
5. **Partenaires clés**
""",
            "query": "Décrire l'organisation opérationnelle et les moyens"
        },
        
        "Étude des risques": {
            "system_message": """
Générer l'étude des risques:

## VII. ÉTUDE DES RISQUES

Identifier et analyser:
1. **Risques commerciaux**
2. **Risques financiers**
3. **Risques opérationnels**
4. **Risques concurrentiels**
5. **Stratégies de mitigation**
""",
            "query": "Identifier les risques et proposer des solutions"
        },
        
        "Plan financier": {
            "system_message": """
Générer l'analyse complète du plan financier:

## VIII. PLAN FINANCIER

Analyser en détail avec tous les tableaux financiers:

1. **Introduction** à l'analyse financière
2. **Analyse des investissements et financements**
3. **Analyse des charges et rentabilité**
4. **Soldes intermédiaires de gestion**
5. **Capacité d'autofinancement et seuil de rentabilité**
6. **Besoin en fonds de roulement**
7. **Plan de financement sur 5 ans**
8. **Trésorerie prévisionnelle**
9. **Synthèse et conclusions financières**

IMPORTANT: Intégrer et commenter TOUS les tableaux financiers fournis.
Pour chaque tableau, fournir une analyse de 2-3 paragraphes.
Conclure chaque analyse par des recommandations concrètes.
""",
            "query": "Analyser en détail tous les éléments financiers avec les tableaux"
        }
    }

def create_export_files(results: Dict[str, str], financial_tables: Dict[str, Any]):
    """Crée les fichiers d'export (Word, PDF)"""
    
    st.subheader("📥 Téléchargements")
    
    # Créer le contenu complet
    complete_content = ""
    for section_name, content in results.items():
        complete_content += f"\n\n## {section_name}\n\n{content}"
    
    # Boutons de téléchargement
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Télécharger en Word"):
            try:
                # Générer le document Word
                word_buffer = generate_word_document(results, financial_tables)
                st.download_button(
                    label="⬇️ Télécharger Business Plan.docx",
                    data=word_buffer,
                    file_name="business_plan_complet.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                st.error(f"Erreur lors de la génération Word: {str(e)}")
    
    with col2:
        if st.button("📑 Télécharger en PDF"):
            st.info("Génération PDF en cours de développement")

def generate_word_document(results: Dict[str, str], financial_tables: Dict[str, Any]):
    """Génère un document Word avec tous les contenus"""
    from docx import Document
    from io import BytesIO
    
    doc = Document()
    
    # Titre principal
    doc.add_heading('PLAN D\'AFFAIRES COMPLET', 0)
    
    # Ajouter chaque section
    for section_name, content in results.items():
        doc.add_heading(section_name, 1)
        
        # Traitement simple du contenu Markdown
        paragraphs = content.split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                doc.add_paragraph(paragraph.strip())
    
    # Sauvegarder en buffer
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    return buffer.getvalue()

def process_uploaded_pdf(uploaded_file):
    """Traite un fichier PDF uploadé"""
    # À implémenter si nécessaire
    return []