"""
Page de détail des amortissements et immobilisations
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List

def page_detail_amortissements():
    """Page détaillée des amortissements"""
    st.title("📋 Détail des Amortissements")
    
    data = st.session_state.get("data", {})
    
    # Informations projet
    info_generales = data.get("informations_generales", {})
    st.info(f"**Projet :** {info_generales.get('intitule_projet', 'N/A')}")
    
    # Onglets
    tab1, tab2, tab3 = st.tabs(["📊 Plan d'amortissement", "📈 Impact annuel", "⚙️ Paramètres"])
    
    with tab1:
        afficher_plan_amortissement_detaille(data)
    
    with tab2:
        afficher_impact_amortissements(data)
    
    with tab3:
        configurer_parametres_amortissement(data)

def afficher_plan_amortissement_detaille(data: Dict[str, Any]):
    """Affiche le plan d'amortissement détaillé sur 5 ans"""
    st.subheader("📊 Plan d'Amortissement Détaillé (5 ans)")
    
    besoins = data.get("besoins_demarrage", {})
    
    # Classification des immobilisations avec durées standard
    immobilisations = {
        "Immobilisations incorporelles": {
            "elements": [
                "Frais d'établissement",
                "Logiciels, formations", 
                "Dépôt de marque",
                "Droits d'entrée",
                "Achat fonds de commerce ou parts",
                "Droit au bail"
            ],
            "duree_defaut": 5
        },
        "Immobilisations corporelles": {
            "elements": [
                "Véhicule",
                "Matériel professionnel",
                "Matériel autre",
                "Matériel de bureau",
                "Enseigne et éléments de communication"
            ],
            "duree_defaut": 5
        }
    }
    
    # Récupérer les paramètres personnalisés
    params_amort = data.get("parametres_amortissement", {})
    
    all_amortissements = []
    
    for categorie, info in immobilisations.items():
        st.write(f"**{categorie}**")
        
        for element in info["elements"]:
            montant = besoins.get(element, 0.0)
            if montant > 0:
                # Durée personnalisée ou par défaut
                duree = params_amort.get(element, {}).get("duree", info["duree_defaut"])
                
                # Calcul du plan d'amortissement
                plan = calculer_plan_amortissement_element(element, montant, duree)
                if plan:
                    all_amortissements.extend(plan)
                    
                    # Affichage résumé
                    amort_annuel = montant / duree
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.write(f"• {element}")
                    with col2:
                        st.write(f"{montant:,.0f} $")
                    with col3:
                        st.write(f"{duree} ans")
                    with col4:
                        st.write(f"{amort_annuel:,.0f} $/an")
        
        st.write("")  # Ligne vide
    
    # Tableau récapitulatif par année
    if all_amortissements:
        st.divider()
        st.subheader("📋 Tableau Récapitulatif par Année")
        
        # Grouper par année
        amort_par_annee = {}
        for item in all_amortissements:
            annee = item["Année"]
            if annee not in amort_par_annee:
                amort_par_annee[annee] = {}
            
            element = item["Élément"]
            amort_par_annee[annee][element] = item["Amortissement"]
        
        # Créer le DataFrame
        df_recap = create_dataframe_amortissements(amort_par_annee)
        st.dataframe(df_recap, use_container_width=True)
        
        # Graphique évolution
        afficher_graphique_amortissements(amort_par_annee)

def afficher_impact_amortissements(data: Dict[str, Any]):
    """Affiche l'impact des amortissements sur les résultats"""
    st.subheader("📈 Impact des Amortissements sur les Résultats")
    
    # Calculer les amortissements annuels
    amortissements_annuels = calculer_amortissements_annuels(data)
    
    if amortissements_annuels:
        # Récupérer données financières
        ca_data = data.get("ca_previsions", {})
        charges_var = data.get("charges_variables", {})
        
        if ca_data:
            # Tableau impact
            years = ["Année 1", "Année 2", "Année 3", "Année 4", "Année 5"]
            ca_values = [
                ca_data.get("ca_annee_1", 0),
                ca_data.get("ca_annee_2", 0), 
                ca_data.get("ca_annee_3", 0),
                ca_data.get("ca_annee_4", 0),
                ca_data.get("ca_annee_5", 0)
            ]
            
            # Calculs
            taux_cv = charges_var.get("taux_charges_variables", 0) / 100
            
            impact_data = []
            for i, (year, ca) in enumerate(zip(years, ca_values), 1):
                amort = amortissements_annuels.get(i, 0)
                charges_variables = ca * taux_cv
                marge_brute = ca - charges_variables
                
                # Impact fiscal (approximation)
                economie_fiscale = amort * 0.30  # Taux d'impôt approximatif
                
                impact_data.append({
                    "Année": year,
                    "CA": f"{ca:,.0f}",
                    "Marge brute": f"{marge_brute:,.0f}",
                    "Amortissements": f"{amort:,.0f}",
                    "% du CA": f"{(amort/ca*100):.1f}%" if ca > 0 else "0%",
                    "Économie fiscale": f"{economie_fiscale:,.0f}"
                })
            
            df_impact = pd.DataFrame(impact_data)
            st.dataframe(df_impact, use_container_width=True, hide_index=True)
            
            # Métriques clés
            col1, col2, col3 = st.columns(3)
            
            total_amortissements = sum(amortissements_annuels.values())
            amort_moyen = total_amortissements / 5 if total_amortissements > 0 else 0
            
            with col1:
                st.metric("Total amortissements 5 ans", f"{total_amortissements:,.0f} $")
            with col2:
                st.metric("Amortissement moyen/an", f"{amort_moyen:,.0f} $")
            with col3:
                economie_totale = total_amortissements * 0.30
                st.metric("Économie fiscale totale", f"{economie_totale:,.0f} $")
    else:
        st.info("Aucun amortissement calculé - vérifiez les investissements")

def configurer_parametres_amortissement(data: Dict[str, Any]):
    """Interface pour configurer les paramètres d'amortissement"""
    st.subheader("⚙️ Configuration des Amortissements")
    
    besoins = data.get("besoins_demarrage", {})
    
    # Initialiser les paramètres s'ils n'existent pas
    if "parametres_amortissement" not in st.session_state.data:
        st.session_state.data["parametres_amortissement"] = {}
    
    params = st.session_state.data["parametres_amortissement"]
    
    st.write("**Durées d'amortissement personnalisées**")
    st.write("*Modifiez les durées selon vos besoins spécifiques*")
    
    # Elements amortissables
    elements_amortissables = [
        "Frais d'établissement",
        "Logiciels, formations",
        "Véhicule", 
        "Matériel professionnel",
        "Matériel autre",
        "Matériel de bureau",
        "Enseigne et éléments de communication"
    ]
    
    col1, col2, col3 = st.columns(3)
    
    for i, element in enumerate(elements_amortissables):
        montant = besoins.get(element, 0.0)
        if montant > 0:
            with [col1, col2, col3][i % 3]:
                # Durée par défaut selon le type
                duree_defaut = get_duree_amortissement_defaut(element)
                
                # Paramètre actuel ou défaut
                if element not in params:
                    params[element] = {"duree": duree_defaut}
                
                # Interface de modification
                st.write(f"**{element}**")
                st.write(f"Montant: {montant:,.0f} $")
                
                new_duree = st.selectbox(
                    "Durée d'amortissement",
                    options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    index=params[element]["duree"] - 1,
                    key=f"duree_{element}"
                )
                
                params[element]["duree"] = new_duree
                
                # Calcul impact
                amort_annuel = montant / new_duree
                st.write(f"Amortissement: {amort_annuel:,.0f} $/an")
                st.write("---")
    
    # Sauvegarder les changements
    if st.button("💾 Sauvegarder les paramètres"):
        st.session_state.data["parametres_amortissement"] = params
        st.success("Paramètres d'amortissement sauvegardés")

def calculer_plan_amortissement_element(element: str, montant: float, duree_annees: int) -> List[Dict]:
    """Calcule le plan d'amortissement pour un élément"""
    if montant <= 0 or duree_annees <= 0:
        return []
    
    amortissement_annuel = montant / duree_annees
    plan = []
    
    for annee in range(1, min(duree_annees + 1, 6)):  # Max 5 ans pour l'affichage
        valeur_debut = montant - (amortissement_annuel * (annee - 1))
        valeur_fin = max(0, montant - (amortissement_annuel * annee))
        
        plan.append({
            "Élément": element,
            "Année": annee,
            "Valeur début": round(valeur_debut, 2),
            "Amortissement": round(amortissement_annuel, 2),
            "Valeur fin": round(valeur_fin, 2)
        })
    
    return plan

def calculer_amortissements_annuels(data: Dict[str, Any]) -> Dict[int, float]:
    """Calcule le total des amortissements par année"""
    besoins = data.get("besoins_demarrage", {})
    params = data.get("parametres_amortissement", {})
    
    amortissements = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    elements_amortissables = [
        "Frais d'établissement",
        "Logiciels, formations", 
        "Véhicule",
        "Matériel professionnel",
        "Matériel autre", 
        "Matériel de bureau",
        "Enseigne et éléments de communication"
    ]
    
    for element in elements_amortissables:
        montant = besoins.get(element, 0.0)
        if montant > 0:
            duree = params.get(element, {}).get("duree", get_duree_amortissement_defaut(element))
            amort_annuel = montant / duree
            
            # Ajouter aux années concernées
            for annee in range(1, min(duree + 1, 6)):
                amortissements[annee] += amort_annuel
    
    return amortissements

def get_duree_amortissement_defaut(element: str) -> int:
    """Retourne la durée d'amortissement par défaut"""
    durees = {
        "Frais d'établissement": 3,
        "Logiciels, formations": 3,
        "Véhicule": 5,
        "Matériel professionnel": 5,
        "Matériel autre": 5,
        "Matériel de bureau": 3,
        "Enseigne et éléments de communication": 5
    }
    return durees.get(element, 5)

def create_dataframe_amortissements(amort_par_annee: Dict) -> pd.DataFrame:
    """Crée un DataFrame pour l'affichage des amortissements"""
    if not amort_par_annee:
        return pd.DataFrame()
    
    # Récupérer tous les éléments
    all_elements = set()
    for annee_data in amort_par_annee.values():
        all_elements.update(annee_data.keys())
    
    # Créer le DataFrame
    data = []
    for element in sorted(all_elements):
        row = {"Élément": element}
        total = 0
        for annee in range(1, 6):
            montant = amort_par_annee.get(annee, {}).get(element, 0)
            row[f"Année {annee}"] = f"{montant:,.0f}" if montant > 0 else "-"
            total += montant
        row["Total"] = f"{total:,.0f}"
        data.append(row)
    
    # Ligne totaux
    row_total = {"Élément": "**TOTAL**"}
    grand_total = 0
    for annee in range(1, 6):
        total_annee = sum(amort_par_annee.get(annee, {}).values())
        row_total[f"Année {annee}"] = f"**{total_annee:,.0f}**"
        grand_total += total_annee
    row_total["Total"] = f"**{grand_total:,.0f}**"
    data.append(row_total)
    
    return pd.DataFrame(data)

def afficher_graphique_amortissements(amort_par_annee: Dict):
    """Affiche un graphique de l'évolution des amortissements"""
    st.subheader("📈 Évolution des Amortissements")
    
    # Préparer données pour le graphique
    years = []
    totals = []
    
    for annee in range(1, 6):
        total = sum(amort_par_annee.get(annee, {}).values())
        years.append(f"Année {annee}")
        totals.append(total)
    
    if any(total > 0 for total in totals):
        df_graph = pd.DataFrame({
            "Année": years,
            "Amortissements": totals
        })
        
        st.line_chart(df_graph.set_index("Année"))
        
        # Analyse de tendance
        if len([t for t in totals if t > 0]) > 1:
            if totals[1] > totals[0]:
                st.info("📈 Tendance croissante des amortissements")
            elif totals[1] < totals[0]:
                st.info("📉 Tendance décroissante des amortissements") 
            else:
                st.info("➡️ Amortissements constants")
    else:
        st.info("Aucune donnée d'amortissement à afficher")