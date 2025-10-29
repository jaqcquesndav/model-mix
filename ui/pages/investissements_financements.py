"""
Page des investissements et financements détaillés
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List

def page_investissements_et_financements():
    """Page détaillée des investissements et financements"""
    st.title("📊 Investissements et Financements")
    
    # Récupérer les données
    data = st.session_state.get("data", {})
    
    # Informations du projet
    info_generales = data.get("informations_generales", {})
    projet = info_generales.get("intitule_projet", "N/A")
    porteur = info_generales.get("prenom_nom", "N/A")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Projet :** {projet}")
    with col2:
        st.info(f"**Porteur :** {porteur}")
    
    st.divider()
    
    # Onglets pour organiser l'information
    tab1, tab2, tab3 = st.tabs(["💰 Investissements", "🏦 Financements", "📈 Analyse"])
    
    with tab1:
        afficher_tableau_investissements(data)
    
    with tab2:
        afficher_tableau_financements(data)
    
    with tab3:
        afficher_analyse_financiere(data)

def afficher_tableau_investissements(data: Dict[str, Any]):
    """Affiche le tableau détaillé des investissements"""
    st.subheader("💼 Détail des Investissements")
    
    besoins = data.get("besoins_demarrage", {})
    
    # Catégorisation des investissements
    categories = {
        "Immobilisations incorporelles": [
            "Frais d'établissement",
            "Frais d'ouverture de compteurs", 
            "Logiciels, formations",
            "Dépôt de marque",
            "Droits d'entrée",
            "Achat fonds de commerce ou parts",
            "Droit au bail",
            "Caution ou dépôt de garantie",
            "Frais de dossier",
            "Frais de notaire"
        ],
        "Immobilisations corporelles": [
            "Enseigne et éléments de communication",
            "Véhicule",
            "Matériel professionnel",
            "Matériel autre", 
            "Matériel de bureau"
        ],
        "Besoins en fonds de roulement": [
            "Stock de matières et produits",
            "Trésorerie de départ"
        ]
    }
    
    # Construire le tableau
    tableau_data = []
    total_general = 0
    
    for categorie, elements in categories.items():
        # En-tête de catégorie
        tableau_data.append({
            "Catégorie": f"**{categorie.upper()}**",
            "Montant ($)": "",
            "% du total": "",
            "Amortissement": ""
        })
        
        total_categorie = 0
        for element in elements:
            montant = besoins.get(element, 0.0)
            if montant > 0:  # N'afficher que les éléments avec un montant
                tableau_data.append({
                    "Catégorie": f"  • {element}",
                    "Montant ($)": f"{montant:,.2f}",
                    "% du total": "",
                    "Amortissement": get_duree_amortissement(element)
                })
                total_categorie += montant
        
        # Sous-total de catégorie
        if total_categorie > 0:
            tableau_data.append({
                "Catégorie": f"*Sous-total {categorie}*",
                "Montant ($)": f"**{total_categorie:,.2f}**",
                "% du total": "",
                "Amortissement": ""
            })
            total_general += total_categorie
        
        tableau_data.append({"Catégorie": "", "Montant ($)": "", "% du total": "", "Amortissement": ""})  # Ligne vide
    
    # Total général
    tableau_data.append({
        "Catégorie": "**TOTAL INVESTISSEMENTS**",
        "Montant ($)": f"**{total_general:,.2f}**",
        "% du total": "**100%**",
        "Amortissement": ""
    })
    
    # Calculer les pourcentages
    for row in tableau_data:
        if row["Montant ($)"] and row["Montant ($)"] not in ["", "**"]:
            try:
                montant_str = row["Montant ($)"].replace("**", "").replace(",", "")
                if montant_str:
                    montant = float(montant_str)
                    if total_general > 0 and "•" in row["Catégorie"]:
                        pourcentage = (montant / total_general) * 100
                        row["% du total"] = f"{pourcentage:.1f}%"
            except:
                pass
    
    # Afficher le tableau
    if tableau_data:
        df = pd.DataFrame(tableau_data)
        st.dataframe(df, width='stretch', hide_index=True)
        
        # Graphique de répartition
        if total_general > 0:
            st.subheader("📊 Répartition des Investissements")
            
            # Données pour le graphique
            cat_totaux = {}
            for categorie, elements in categories.items():
                total_cat = sum(besoins.get(elem, 0) for elem in elements)
                if total_cat > 0:
                    cat_totaux[categorie] = total_cat
            
            if cat_totaux:
                df_graph = pd.DataFrame(list(cat_totaux.items()), columns=['Catégorie', 'Montant'])
                st.bar_chart(df_graph.set_index('Catégorie'))
    else:
        st.warning("Aucun investissement renseigné")

def afficher_tableau_financements(data: Dict[str, Any]):
    """Affiche le tableau détaillé des financements"""
    st.subheader("🏦 Plan de Financement")
    
    financements = data.get("financements", {})
    besoins_total = data.get("total_besoins", 0.0)
    
    # Catégorisation des financements
    categories_fin = {
        "Fonds propres": [
            "Apport personnel ou familial",
            "Apports en nature (en valeur)"
        ],
        "Aides et subventions": [
            "Subvention d'équipement",
            "Aide à la création"
        ],
        "Emprunts bancaires": [
            "Prêt 1", "Prêt 2", "Prêt 3"
        ],
        "Autres financements": [
            "Emprunts bancaires",
            "Prêt d'honneur",
            "Autres sources"
        ]
    }
    
    tableau_fin = []
    total_financements = 0
    
    for categorie, elements in categories_fin.items():
        # En-tête de catégorie
        tableau_fin.append({
            "Source de financement": f"**{categorie.upper()}**",
            "Montant ($)": "",
            "Taux (%)": "",
            "Durée (mois)": "",
            "Mensualité ($)": ""
        })
        
        total_categorie = 0
        for element in elements:
            fin_data = financements.get(element, {})
            
            # Gestion des différents formats de données
            if isinstance(fin_data, dict):
                montant = fin_data.get("montant", 0.0)
                taux = fin_data.get("taux", 0.0)
                duree = fin_data.get("duree", 0)
                nom = fin_data.get("nom", element)
            else:
                montant = fin_data if isinstance(fin_data, (int, float)) else 0.0
                taux = 0.0
                duree = 0
                nom = element
            
            if montant > 0:
                # Calcul de la mensualité pour les emprunts
                mensualite = ""
                if taux > 0 and duree > 0:
                    taux_mensuel = taux / 100 / 12
                    if taux_mensuel > 0:
                        mensualite = montant * (taux_mensuel * (1 + taux_mensuel)**duree) / ((1 + taux_mensuel)**duree - 1)
                        mensualite = f"{mensualite:,.2f}"
                
                tableau_fin.append({
                    "Source de financement": f"  • {nom}",
                    "Montant ($)": f"{montant:,.2f}",
                    "Taux (%)": f"{taux:.2f}" if taux > 0 else "-",
                    "Durée (mois)": f"{duree}" if duree > 0 else "-",
                    "Mensualité ($)": mensualite
                })
                total_categorie += montant
        
        # Sous-total de catégorie
        if total_categorie > 0:
            tableau_fin.append({
                "Source de financement": f"*Sous-total {categorie}*",
                "Montant ($)": f"**{total_categorie:,.2f}**",
                "Taux (%)": "",
                "Durée (mois)": "",
                "Mensualité ($)": ""
            })
            total_financements += total_categorie
        
        tableau_fin.append({
            "Source de financement": "", 
            "Montant ($)": "", 
            "Taux (%)": "", 
            "Durée (mois)": "", 
            "Mensualité ($)": ""
        })
    
    # Total général
    tableau_fin.append({
        "Source de financement": "**TOTAL FINANCEMENTS**",
        "Montant ($)": f"**{total_financements:,.2f}**",
        "Taux (%)": "",
        "Durée (mois)": "",
        "Mensualité ($)": ""
    })
    
    # Affichage
    if tableau_fin:
        df_fin = pd.DataFrame(tableau_fin)
        st.dataframe(df_fin, width='stretch', hide_index=True)
        
        # Équilibre besoins/financements
        st.divider()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Besoins", f"{besoins_total:,.2f} $")
        with col2:
            st.metric("Total Financements", f"{total_financements:,.2f} $")
        with col3:
            ecart = total_financements - besoins_total
            if ecart >= 0:
                st.metric("Excédent", f"{ecart:,.2f} $", delta=ecart)
            else:
                st.metric("Déficit", f"{abs(ecart):,.2f} $", delta=ecart)
    else:
        st.warning("Aucun financement renseigné")

def afficher_analyse_financiere(data: Dict[str, Any]):
    """Affiche une analyse financière du plan"""
    st.subheader("📈 Analyse Financière")
    
    besoins_total = data.get("total_besoins", 0.0)
    financements_total = data.get("total_financement", 0.0)
    
    if besoins_total > 0 and financements_total > 0:
        # Ratios financiers
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🎯 Ratios Clés**")
            
            # Taux de couverture
            taux_couverture = (financements_total / besoins_total) * 100
            st.metric("Taux de couverture", f"{taux_couverture:.1f}%")
            
            # Analyse fonds propres
            financements = data.get("financements", {})
            fonds_propres = (
                financements.get("Apport personnel ou familial", 0) +
                financements.get("Apports en nature (en valeur)", 0)
            )
            
            if fonds_propres > 0:
                ratio_fonds_propres = (fonds_propres / besoins_total) * 100
                st.metric("Part fonds propres", f"{ratio_fonds_propres:.1f}%")
            
        with col2:
            st.write("**⚠️ Points d'Attention**")
            
            alertes = []
            
            if taux_couverture < 100:
                alertes.append("🔴 Financement insuffisant")
            elif taux_couverture > 120:
                alertes.append("🟡 Surcapitalisation possible")
            else:
                alertes.append("✅ Équilibre financier correct")
            
            if fonds_propres > 0:
                if ratio_fonds_propres < 20:
                    alertes.append("🔴 Fonds propres faibles (<20%)")
                elif ratio_fonds_propres > 70:
                    alertes.append("🟡 Fonds propres élevés (>70%)")
                else:
                    alertes.append("✅ Structure de financement équilibrée")
            
            for alerte in alertes:
                st.write(alerte)
        
        # Recommandations
        st.divider()
        st.write("**💡 Recommandations**")
        
        if taux_couverture < 100:
            deficit = besoins_total - financements_total
            st.error(f"Rechercher {deficit:,.2f} $ de financement complémentaire")
        
        if fonds_propres > 0 and ratio_fonds_propres < 30:
            st.warning("Envisager d'augmenter l'apport personnel pour faciliter l'obtention d'emprunts")
        
        if taux_couverture >= 100:
            st.success("Plan de financement équilibré - projet financièrement viable")
    
    else:
        st.info("Complétez les données d'investissements et financements pour voir l'analyse")

def get_duree_amortissement(element: str) -> str:
    """Retourne la durée d'amortissement suggérée pour un élément"""
    durees = {
        "Frais d'établissement": "3-5 ans",
        "Logiciels, formations": "3 ans", 
        "Véhicule": "4-5 ans",
        "Matériel professionnel": "5-10 ans",
        "Matériel de bureau": "3-5 ans",
        "Enseigne et éléments de communication": "5 ans"
    }
    return durees.get(element, "Variable")

def calculer_plan_amortissement(montant: float, duree_annees: int) -> List[Dict]:
    """Calcule un plan d'amortissement linéaire"""
    if montant <= 0 or duree_annees <= 0:
        return []
    
    amortissement_annuel = montant / duree_annees
    plan = []
    
    for annee in range(1, duree_annees + 1):
        valeur_debut = montant - (amortissement_annuel * (annee - 1))
        valeur_fin = montant - (amortissement_annuel * annee)
        
        plan.append({
            "Année": annee,
            "Valeur début": round(valeur_debut, 2),
            "Amortissement": round(amortissement_annuel, 2),
            "Valeur fin": round(valeur_fin, 2)
        })
    
    return plan