"""
Service de calculs et analyses financières
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from datetime import datetime, date
from utils.financial_utils import *

def calculer_tableaux_financiers() -> Dict[str, Any]:
    """
    Calcule tous les tableaux financiers basés sur les données du session state
    
    Returns:
        dict: Tous les tableaux financiers calculés
    """
    resultats = {}
    
    # Récupération des données de base
    donnees_base = {
        'investissements': st.session_state.get('investissements', []),
        'charges_fixes': st.session_state.get('charges_fixes', {}),
        'ca_previsions': st.session_state.get('ca_previsions', {}),
        'charges_variables': st.session_state.get('charges_variables', {}),
        'salaires': st.session_state.get('salaires', {}),
        'financements': st.session_state.get('financements', {})
    }
    
    # Calcul des différents tableaux (utilisant les fonctions 5 ans existantes)
    resultats['investissements'] = calculer_tableau_investissements(donnees_base['investissements'])
    resultats['compte_resultats'] = calculer_compte_resultats_5_ans(donnees_base)
    resultats['soldes_intermediaires'] = calculer_soldes_intermediaires_5_ans(donnees_base)
    resultats['capacite_autofinancement'] = calculer_tableau_caf_5_ans(donnees_base)
    resultats['seuil_rentabilite'] = calculer_tableau_seuil_rentabilite_5_ans(donnees_base)
    resultats['bfr'] = calculer_tableau_bfr_5_ans(donnees_base)
    resultats['plan_financement'] = calculer_plan_financement_5_ans(donnees_base)
    resultats['budget_tresorerie'] = calculer_budget_tresorerie_5_ans(donnees_base)
    
    return resultats

def calculer_tableau_investissements(investissements: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcule le tableau des investissements et financements
    
    Args:
        investissements (list): Liste des investissements
    
    Returns:
        dict: Tableau des investissements calculé
    """
    if not investissements:
        return {"table_data": [], "total_investissement": 0, "total_financement": 0}
    
    table_data = []
    total_investissement = 0
    total_financement = 0
    
    for inv in investissements:
        montant = float(inv.get('montant', 0))
        taux = float(inv.get('taux_financement', 0))
        duree = int(inv.get('duree_financement', 12))
        
        # Calcul du financement si nécessaire
        if taux > 0 and duree > 0:
            details_pret = calculer_pret_interet_fixe(montant, taux, duree)
            montant_financement = details_pret['total_a_payer']
        else:
            montant_financement = montant
        
        table_data.append({
            "Investissements": inv.get('nom', 'N/A'),
            "Taux (%)": f"{taux:.1f}%" if taux > 0 else "N/A",
            "Durée (mois)": str(duree) if duree > 0 else "N/A",
            "Montant ($)": f"{montant:,.2f}"
        })
        
        total_investissement += montant
        total_financement += montant_financement
    
    # Ligne de total
    table_data.append({
        "Investissements": "TOTAL",
        "Taux (%)": "",
        "Durée (mois)": "",
        "Montant ($)": f"{total_investissement:,.2f}"
    })
    
    return {
        "table_data": table_data,
        "total_investissement": total_investissement,
        "total_financement": total_financement,
        "financement_necessaire": total_financement - total_investissement
    }

def calculer_compte_resultats(donnees: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule le compte de résultats prévisionnel sur 3 ans
    
    Args:
        donnees (dict): Données financières de base
    
    Returns:
        dict: Compte de résultats calculé
    """
    table_data = []
    
    # Chiffre d'affaires
    ca_data = donnees.get('ca_previsions', {})
    ca_annees = [
        float(ca_data.get('ca_annee_1', 0)),
        float(ca_data.get('ca_annee_2', 0)),
        float(ca_data.get('ca_annee_3', 0))
    ]
    
    table_data.append({
        "Description": "Chiffre d'affaires",
        "Année 1": f"{ca_annees[0]:,.2f}",
        "Année 2": f"{ca_annees[1]:,.2f}",
        "Année 3": f"{ca_annees[2]:,.2f}"
    })
    
    # Charges variables
    charges_var_data = donnees.get('charges_variables', {})
    taux_charges_var = float(charges_var_data.get('taux_charges_variables', 60)) / 100
    
    charges_var_annees = [ca * taux_charges_var for ca in ca_annees]
    
    table_data.append({
        "Description": "Charges variables",
        "Année 1": f"{charges_var_annees[0]:,.2f}",
        "Année 2": f"{charges_var_annees[1]:,.2f}",
        "Année 3": f"{charges_var_annees[2]:,.2f}"
    })
    
    # Marge brute
    marge_brute = [ca - cv for ca, cv in zip(ca_annees, charges_var_annees)]
    
    table_data.append({
        "Description": "Marge brute",
        "Année 1": f"{marge_brute[0]:,.2f}",
        "Année 2": f"{marge_brute[1]:,.2f}",
        "Année 3": f"{marge_brute[2]:,.2f}"
    })
    
    # Charges fixes
    charges_fixes_data = donnees.get('charges_fixes', {})
    charges_fixes_base = sum([
        float(charges_fixes_data.get('loyer', 0)),
        float(charges_fixes_data.get('electricite', 0)),
        float(charges_fixes_data.get('eau', 0)),
        float(charges_fixes_data.get('telephone', 0)),
        float(charges_fixes_data.get('assurance', 0)),
        float(charges_fixes_data.get('transport', 0)),
        float(charges_fixes_data.get('marketing', 0)),
        float(charges_fixes_data.get('autres_charges', 0))
    ]) * 12  # Mensuel vers annuel
    
    # Croissance des charges fixes (inflation estimée)
    croissance_cf = 1.05  # 5% par an
    charges_fixes_annees = [
        charges_fixes_base,
        charges_fixes_base * croissance_cf,
        charges_fixes_base * (croissance_cf ** 2)
    ]
    
    table_data.append({
        "Description": "Charges fixes",
        "Année 1": f"{charges_fixes_annees[0]:,.2f}",
        "Année 2": f"{charges_fixes_annees[1]:,.2f}",
        "Année 3": f"{charges_fixes_annees[2]:,.2f}"
    })
    
    # Salaires et charges sociales
    salaires_data = donnees.get('salaires', {})
    masse_salariale_base = sum([
        float(salaires_data.get(f'salaire_poste_{i}', 0)) * 12
        for i in range(1, 6)  # Jusqu'à 5 postes
    ])
    
    # Charges sociales (environ 15% en RDC)
    taux_charges_sociales = 0.15
    charges_sociales_base = masse_salariale_base * taux_charges_sociales
    
    total_salaires_charges = [
        masse_salariale_base + charges_sociales_base,
        (masse_salariale_base + charges_sociales_base) * 1.08,  # 8% d'augmentation
        (masse_salariale_base + charges_sociales_base) * (1.08 ** 2)
    ]
    
    table_data.append({
        "Description": "Salaires et charges sociales",
        "Année 1": f"{total_salaires_charges[0]:,.2f}",
        "Année 2": f"{total_salaires_charges[1]:,.2f}",
        "Année 3": f"{total_salaires_charges[2]:,.2f}"
    })
    
    # Amortissements
    amortissements = calculer_amortissements_annuels(donnees.get('investissements', []))
    
    table_data.append({
        "Description": "Amortissements",
        "Année 1": f"{amortissements[0]:,.2f}",
        "Année 2": f"{amortissements[1]:,.2f}",
        "Année 3": f"{amortissements[2]:,.2f}"
    })
    
    # Résultat avant impôt
    total_charges = [
        cv + cf + sal + amort
        for cv, cf, sal, amort in zip(charges_var_annees, charges_fixes_annees, total_salaires_charges, amortissements)
    ]
    
    resultat_avant_impot = [ca - tc for ca, tc in zip(ca_annees, total_charges)]
    
    table_data.append({
        "Description": "Résultat avant impôt",
        "Année 1": f"{resultat_avant_impot[0]:,.2f}",
        "Année 2": f"{resultat_avant_impot[1]:,.2f}",
        "Année 3": f"{resultat_avant_impot[2]:,.2f}"
    })
    
    # Impôt sur les sociétés (30% en RDC)
    impots = [calculer_impot_societes(rai, 30) for rai in resultat_avant_impot]
    
    table_data.append({
        "Description": "Impôt sur les sociétés",
        "Année 1": f"{impots[0]:,.2f}",
        "Année 2": f"{impots[1]:,.2f}",
        "Année 3": f"{impots[2]:,.2f}"
    })
    
    # Résultat net
    resultat_net = [rai - imp for rai, imp in zip(resultat_avant_impot, impots)]
    
    table_data.append({
        "Description": "Résultat net",
        "Année 1": f"{resultat_net[0]:,.2f}",
        "Année 2": f"{resultat_net[1]:,.2f}",
        "Année 3": f"{resultat_net[2]:,.2f}"
    })
    
    return {
        "table_data": table_data,
        "ca_annees": ca_annees,
        "resultat_net": resultat_net,
        "resultat_avant_impot": resultat_avant_impot,
        "marge_brute": marge_brute
    }

def calculer_amortissements_annuels(investissements: List[Dict[str, Any]]) -> List[float]:
    """
    Calcule les amortissements annuels sur 3 ans
    
    Args:
        investissements (list): Liste des investissements
    
    Returns:
        list: Amortissements pour les 3 années
    """
    amortissements_annuels = [0, 0, 0]
    
    for inv in investissements:
        montant = float(inv.get('montant', 0))
        duree_amort = int(inv.get('duree_amortissement', 5))
        
        if duree_amort > 0:
            amortissement_annuel = montant / duree_amort
            
            # Répartir sur les 3 années si applicable
            for annee in range(min(3, duree_amort)):
                amortissements_annuels[annee] += amortissement_annuel
    
    return amortissements_annuels

def calculer_soldes_intermediaires(donnees: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule les soldes intermédiaires de gestion
    
    Args:
        donnees (dict): Données financières
    
    Returns:
        dict: Soldes intermédiaires calculés
    """
    # Récupérer les données du compte de résultats
    compte_resultats = calculer_compte_resultats(donnees)
    
    table_data = []
    
    # Données de base
    ca_annees = compte_resultats['ca_annees']
    marge_brute = compte_resultats['marge_brute']
    
    # Valeur ajoutée (approximation = marge brute)
    table_data.append({
        "Description": "Valeur ajoutée",
        "Année 1": f"{marge_brute[0]:,.2f}",
        "Année 2": f"{marge_brute[1]:,.2f}",
        "Année 3": f"{marge_brute[2]:,.2f}"
    })
    
    # EBE (Excédent Brut d'Exploitation)
    # EBE = Valeur ajoutée - Charges de personnel - Impôts et taxes
    charges_personnel = [
        float(st.session_state.get('salaires', {}).get(f'salaire_poste_{i}', 0)) * 12 * 1.15
        for i in range(3)
    ]
    
    ebe = [va - cp for va, cp in zip(marge_brute, charges_personnel)]
    
    table_data.append({
        "Description": "Excédent Brut d'Exploitation",
        "Année 1": f"{ebe[0]:,.2f}",
        "Année 2": f"{ebe[1]:,.2f}",
        "Année 3": f"{ebe[2]:,.2f}"
    })
    
    # Résultat d'exploitation
    amortissements = calculer_amortissements_annuels(donnees.get('investissements', []))
    resultat_exploitation = [e - a for e, a in zip(ebe, amortissements)]
    
    table_data.append({
        "Description": "Résultat d'exploitation",
        "Année 1": f"{resultat_exploitation[0]:,.2f}",
        "Année 2": f"{resultat_exploitation[1]:,.2f}",
        "Année 3": f"{resultat_exploitation[2]:,.2f}"
    })
    
    # Résultat net (du compte de résultats)
    resultat_net = compte_resultats['resultat_net']
    
    table_data.append({
        "Description": "Résultat net",
        "Année 1": f"{resultat_net[0]:,.2f}",
        "Année 2": f"{resultat_net[1]:,.2f}",
        "Année 3": f"{resultat_net[2]:,.2f}"
    })
    
    return {
        "table_data": table_data,
        "ebe": ebe,
        "resultat_exploitation": resultat_exploitation,
        "valeur_ajoutee": marge_brute
    }

def generer_analyse_financiere(donnees_financieres: Dict[str, Any]) -> str:
    """
    Génère une analyse financière textuelle
    
    Args:
        donnees_financieres (dict): Tous les tableaux financiers
    
    Returns:
        str: Analyse financière formatée
    """
    analyse = "# Analyse Financière\n\n"
    
    # Analyse de rentabilité
    if 'compte_resultats' in donnees_financieres:
        compte = donnees_financieres['compte_resultats']
        ca_annees = compte.get('ca_annees', [0, 0, 0])
        resultat_net = compte.get('resultat_net', [0, 0, 0])
        
        analyse += "## Rentabilité\n\n"
        
        if ca_annees[0] > 0:
            marge_nette_an1 = (resultat_net[0] / ca_annees[0]) * 100
            analyse += f"- Marge nette année 1 : {marge_nette_an1:.1f}%\n"
        
        if len(ca_annees) > 1 and ca_annees[1] > 0:
            croissance_ca = ((ca_annees[1] - ca_annees[0]) / ca_annees[0]) * 100
            analyse += f"- Croissance du CA année 2 : {croissance_ca:.1f}%\n"
        
        analyse += f"- Évolution du résultat net : {resultat_net[0]:,.0f} → {resultat_net[1]:,.0f} → {resultat_net[2]:,.0f} USD\n\n"
    
    # Analyse des investissements
    if 'investissements' in donnees_financieres:
        inv = donnees_financieres['investissements']
        total_inv = inv.get('total_investissement', 0)
        
        analyse += "## Investissements\n\n"
        analyse += f"- Total des investissements : {total_inv:,.2f} USD\n"
        
        if 'compte_resultats' in donnees_financieres and total_inv > 0:
            compte = donnees_financieres['compte_resultats']
            resultat_net = compte.get('resultat_net', [0, 0, 0])
            
            # ROI approximatif
            if resultat_net[0] > 0:
                roi = (resultat_net[0] / total_inv) * 100
                analyse += f"- ROI estimé année 1 : {roi:.1f}%\n"
        
        analyse += "\n"
    
    # Recommandations
    analyse += "## Recommandations\n\n"
    analyse += "- Surveiller étroitement la trésorerie les premiers mois\n"
    analyse += "- Diversifier les sources de revenus pour réduire les risques\n"
    analyse += "- Négocier des délais de paiement favorables avec les fournisseurs\n"
    analyse += "- Mettre en place un suivi mensuel des indicateurs clés\n\n"
    
    return analyse

def sauvegarder_donnees_financieres():
    """Sauvegarde toutes les données financières calculées dans le session state"""
    
    try:
        # Calculer tous les tableaux
        resultats = calculer_tableaux_financiers()
        
        # Sauvegarder dans le session state avec les clés d'export
        st.session_state['export_data_investissements'] = resultats.get('investissements', {})
        st.session_state['export_data_compte_resultats_previsionnel'] = resultats.get('compte_resultats', {})
        st.session_state['export_data_soldes_intermediaires_de_gestion'] = resultats.get('soldes_intermediaires', {})
        st.session_state['export_data_capacite_autofinancement'] = resultats.get('capacite_autofinancement', {})
        st.session_state['export_data_seuil_rentabilite_economique'] = resultats.get('seuil_rentabilite', {})
        st.session_state['export_data_besoin_fonds_roulement'] = resultats.get('bfr', {})
        st.session_state['export_data_plan_financement_trois_ans'] = resultats.get('plan_financement', {})
        
        # Budget trésorerie (divisé en 2 parties)
        budget = resultats.get('budget_tresorerie', {})
        st.session_state['export_data_budget_previsionnel_tresorerie_part1'] = budget.get('part1', {})
        st.session_state['export_data_budget_previsionnel_tresorerie_part2'] = budget.get('part2', {})
        
        st.session_state['derniere_modification'] = datetime.now().isoformat()
        
        return True
        
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde des données financières : {str(e)}")
        return False

def calculer_tableaux_financiers_5_ans() -> Dict[str, Any]:
    """
    Calcule tous les tableaux financiers basés sur les données du session state sur 5 ans
    
    Returns:
        dict: Tous les tableaux financiers calculés sur 5 ans
    """
    resultats = {}
    
    # Récupération des données de base
    donnees_base = {
        'investissements': st.session_state.get('investissements', []),
        'charges_fixes': st.session_state.get('charges_fixes', {}),
        'ca_previsions': st.session_state.get('ca_previsions', {}),
        'charges_variables': st.session_state.get('charges_variables', {}),
        'salaires': st.session_state.get('salaires', {}),
        'financements': st.session_state.get('financements', {})
    }
    
    # Calcul des différents tableaux sur 5 ans
    resultats['compte_resultats_5ans'] = calculer_compte_resultats_5_ans(donnees_base)
    resultats['soldes_intermediaires_5ans'] = calculer_soldes_intermediaires_5_ans(donnees_base)
    resultats['capacite_autofinancement_5ans'] = calculer_tableau_caf_5_ans(donnees_base)
    resultats['seuil_rentabilite_5ans'] = calculer_tableau_seuil_rentabilite_5_ans(donnees_base)
    resultats['bfr_5ans'] = calculer_tableau_bfr_5_ans(donnees_base)
    resultats['plan_financement_5ans'] = calculer_plan_financement_cinq_ans(donnees_base)
    
    return resultats

def calculer_compte_resultats_5_ans(donnees: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule le compte de résultats prévisionnel sur 5 ans
    
    Args:
        donnees (dict): Données financières de base
    
    Returns:
        dict: Compte de résultats calculé sur 5 ans
    """
    table_data = []
    
    # Chiffre d'affaires - extension à 5 ans avec croissance estimée
    ca_data = donnees.get('ca_previsions', {})
    ca_base = [
        float(ca_data.get('ca_annee_1', 0)),
        float(ca_data.get('ca_annee_2', 0)),
        float(ca_data.get('ca_annee_3', 0))
    ]
    
    # Estimation de la croissance pour les années 4 et 5
    if len(ca_base) >= 3 and ca_base[1] > 0 and ca_base[2] > 0:
        taux_croissance = ((ca_base[2] / ca_base[1]) + (ca_base[1] / ca_base[0]) if ca_base[0] > 0 else 1) / 2
        taux_croissance = max(1.0, min(taux_croissance, 1.15))  # Entre 0% et 15%
    else:
        taux_croissance = 1.05  # 5% par défaut
    
    ca_annees = ca_base + [
        ca_base[2] * taux_croissance,
        ca_base[2] * (taux_croissance ** 2)
    ]
    
    table_data.append({
        "Description": "Chiffre d'affaires",
        "Année 1": f"{ca_annees[0]:,.2f}",
        "Année 2": f"{ca_annees[1]:,.2f}",
        "Année 3": f"{ca_annees[2]:,.2f}",
        "Année 4": f"{ca_annees[3]:,.2f}",
        "Année 5": f"{ca_annees[4]:,.2f}"
    })
    
    # Charges variables
    charges_var_data = donnees.get('charges_variables', {})
    taux_charges_var = float(charges_var_data.get('taux_charges_variables', 60)) / 100
    
    charges_var_annees = [ca * taux_charges_var for ca in ca_annees]
    
    table_data.append({
        "Description": "Charges variables",
        "Année 1": f"{charges_var_annees[0]:,.2f}",
        "Année 2": f"{charges_var_annees[1]:,.2f}",
        "Année 3": f"{charges_var_annees[2]:,.2f}",
        "Année 4": f"{charges_var_annees[3]:,.2f}",
        "Année 5": f"{charges_var_annees[4]:,.2f}"
    })
    
    # Marge brute
    marge_brute = [ca - cv for ca, cv in zip(ca_annees, charges_var_annees)]
    
    table_data.append({
        "Description": "Marge brute",
        "Année 1": f"{marge_brute[0]:,.2f}",
        "Année 2": f"{marge_brute[1]:,.2f}",
        "Année 3": f"{marge_brute[2]:,.2f}",
        "Année 4": f"{marge_brute[3]:,.2f}",
        "Année 5": f"{marge_brute[4]:,.2f}"
    })
    
    # Charges fixes avec croissance sur 5 ans
    charges_fixes_data = donnees.get('charges_fixes', {})
    charges_fixes_base = sum([
        float(charges_fixes_data.get('loyer', 0)),
        float(charges_fixes_data.get('electricite', 0)),
        float(charges_fixes_data.get('eau', 0)),
        float(charges_fixes_data.get('telephone', 0)),
        float(charges_fixes_data.get('assurance', 0)),
        float(charges_fixes_data.get('transport', 0)),
        float(charges_fixes_data.get('marketing', 0)),
        float(charges_fixes_data.get('autres_charges', 0))
    ]) * 12
    
    croissance_cf = 1.05  # 5% par an
    charges_fixes_annees = [
        charges_fixes_base * (croissance_cf ** i) for i in range(5)
    ]
    
    table_data.append({
        "Description": "Charges fixes",
        "Année 1": f"{charges_fixes_annees[0]:,.2f}",
        "Année 2": f"{charges_fixes_annees[1]:,.2f}",
        "Année 3": f"{charges_fixes_annees[2]:,.2f}",
        "Année 4": f"{charges_fixes_annees[3]:,.2f}",
        "Année 5": f"{charges_fixes_annees[4]:,.2f}"
    })
    
    # Salaires et charges sociales sur 5 ans
    salaires_data = donnees.get('salaires', {})
    masse_salariale_base = sum([
        float(salaires_data.get(f'salaire_poste_{i}', 0)) * 12
        for i in range(1, 6)
    ])
    
    taux_charges_sociales = 0.15
    charges_sociales_base = masse_salariale_base * taux_charges_sociales
    
    total_salaires_charges = [
        (masse_salariale_base + charges_sociales_base) * (1.08 ** i) for i in range(5)
    ]
    
    table_data.append({
        "Description": "Salaires et charges sociales",
        "Année 1": f"{total_salaires_charges[0]:,.2f}",
        "Année 2": f"{total_salaires_charges[1]:,.2f}",
        "Année 3": f"{total_salaires_charges[2]:,.2f}",
        "Année 4": f"{total_salaires_charges[3]:,.2f}",
        "Année 5": f"{total_salaires_charges[4]:,.2f}"
    })
    
    # Amortissements sur 5 ans
    amortissements = calculer_amortissements_5_ans(donnees.get('investissements', []))
    
    table_data.append({
        "Description": "Dotations aux amortissements",
        "Année 1": f"{amortissements[0]:,.2f}",
        "Année 2": f"{amortissements[1]:,.2f}",
        "Année 3": f"{amortissements[2]:,.2f}",
        "Année 4": f"{amortissements[3]:,.2f}",
        "Année 5": f"{amortissements[4]:,.2f}"
    })
    
    # Résultat avant impôt
    resultat_avant_impot = [
        mb - cf - sc - amort 
        for mb, cf, sc, amort in zip(marge_brute, charges_fixes_annees, total_salaires_charges, amortissements)
    ]
    
    table_data.append({
        "Description": "Résultat avant impôt",
        "Année 1": f"{resultat_avant_impot[0]:,.2f}",
        "Année 2": f"{resultat_avant_impot[1]:,.2f}",
        "Année 3": f"{resultat_avant_impot[2]:,.2f}",
        "Année 4": f"{resultat_avant_impot[3]:,.2f}",
        "Année 5": f"{resultat_avant_impot[4]:,.2f}"
    })
    
    # Impôts sur les sociétés (30% en RDC)
    taux_impot = 0.30
    impots = [max(0, res * taux_impot) for res in resultat_avant_impot]
    
    table_data.append({
        "Description": "Impôts sur les sociétés",
        "Année 1": f"{impots[0]:,.2f}",
        "Année 2": f"{impots[1]:,.2f}",
        "Année 3": f"{impots[2]:,.2f}",
        "Année 4": f"{impots[3]:,.2f}",
        "Année 5": f"{impots[4]:,.2f}"
    })
    
    # Résultat net
    resultat_net = [res - imp for res, imp in zip(resultat_avant_impot, impots)]
    
    table_data.append({
        "Description": "Résultat net",
        "Année 1": f"{resultat_net[0]:,.2f}",
        "Année 2": f"{resultat_net[1]:,.2f}",
        "Année 3": f"{resultat_net[2]:,.2f}",
        "Année 4": f"{resultat_net[3]:,.2f}",
        "Année 5": f"{resultat_net[4]:,.2f}"
    })
    
    return {
        'table_data': table_data,
        'ca_annees': ca_annees,
        'charges_var_annees': charges_var_annees,
        'marge_brute': marge_brute,
        'charges_fixes_annees': charges_fixes_annees,
        'total_salaires_charges': total_salaires_charges,
        'amortissements': amortissements,
        'resultat_avant_impot': resultat_avant_impot,
        'impots': impots,
        'resultat_net': resultat_net
    }

def calculer_amortissements_5_ans(investissements: List[Dict[str, Any]]) -> List[float]:
    """
    Calcule les amortissements annuels sur 5 ans
    
    Args:
        investissements (list): Liste des investissements
    
    Returns:
        list: Amortissements pour chaque année sur 5 ans
    """
    amortissements_annuels = [0.0] * 5
    
    for inv in investissements:
        montant = float(inv.get('montant', 0))
        duree = int(inv.get('duree_amortissement', 5))
        
        amortissement_annuel = montant / duree
        
        # Répartir sur la durée d'amortissement
        for annee in range(min(duree, 5)):
            amortissements_annuels[annee] += amortissement_annuel
    
    return amortissements_annuels

def calculer_soldes_intermediaires_5_ans(donnees: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule les soldes intermédiaires de gestion sur 5 ans
    
    Args:
        donnees (dict): Données financières
    
    Returns:
        dict: Soldes intermédiaires sur 5 ans
    """
    compte_resultats = calculer_compte_resultats_5_ans(donnees)
    
    ca_annees = compte_resultats['ca_annees']
    charges_var = compte_resultats['charges_var_annees']
    marge_brute = compte_resultats['marge_brute']
    charges_fixes = compte_resultats['charges_fixes_annees']
    salaires_charges = compte_resultats['total_salaires_charges']
    amortissements = compte_resultats['amortissements']
    resultat_net = compte_resultats['resultat_net']
    
    table_data = []
    
    # Valeur ajoutée (Marge brute - Autres charges externes)
    valeur_ajoutee = marge_brute
    
    table_data.append({
        "Indicateur": "Valeur ajoutée",
        "Année 1": f"{valeur_ajoutee[0]:,.2f}",
        "Année 2": f"{valeur_ajoutee[1]:,.2f}",
        "Année 3": f"{valeur_ajoutee[2]:,.2f}",
        "Année 4": f"{valeur_ajoutee[3]:,.2f}",
        "Année 5": f"{valeur_ajoutee[4]:,.2f}"
    })
    
    # EBE (Excédent Brut d'Exploitation)
    ebe = [va - cf for va, cf in zip(valeur_ajoutee, charges_fixes)]
    
    table_data.append({
        "Indicateur": "Excédent Brut d'Exploitation (EBE)",
        "Année 1": f"{ebe[0]:,.2f}",
        "Année 2": f"{ebe[1]:,.2f}",
        "Année 3": f"{ebe[2]:,.2f}",
        "Année 4": f"{ebe[3]:,.2f}",
        "Année 5": f"{ebe[4]:,.2f}"
    })
    
    # Résultat d'exploitation
    resultat_exploitation = [e - sc - amort for e, sc, amort in zip(ebe, salaires_charges, amortissements)]
    
    table_data.append({
        "Indicateur": "Résultat d'exploitation",
        "Année 1": f"{resultat_exploitation[0]:,.2f}",
        "Année 2": f"{resultat_exploitation[1]:,.2f}",
        "Année 3": f"{resultat_exploitation[2]:,.2f}",
        "Année 4": f"{resultat_exploitation[3]:,.2f}",
        "Année 5": f"{resultat_exploitation[4]:,.2f}"
    })
    
    table_data.append({
        "Indicateur": "Résultat net",
        "Année 1": f"{resultat_net[0]:,.2f}",
        "Année 2": f"{resultat_net[1]:,.2f}",
        "Année 3": f"{resultat_net[2]:,.2f}",
        "Année 4": f"{resultat_net[3]:,.2f}",
        "Année 5": f"{resultat_net[4]:,.2f}"
    })
    
    return {
        'table_data': table_data,
        'valeur_ajoutee': valeur_ajoutee,
        'ebe': ebe,
        'resultat_exploitation': resultat_exploitation,
        'resultat_net': resultat_net
    }

def calculer_tableau_caf_5_ans(donnees: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule la capacité d'autofinancement sur 5 ans
    
    Args:
        donnees (dict): Données financières
    
    Returns:
        dict: Tableau CAF sur 5 ans
    """
    compte_resultats = calculer_compte_resultats_5_ans(donnees)
    resultat_net = compte_resultats['resultat_net']
    amortissements = compte_resultats['amortissements']
    
    # CAF = Résultat net + Amortissements
    caf = [rn + amort for rn, amort in zip(resultat_net, amortissements)]
    
    # Remboursements d'emprunts (estimation)
    financements = donnees.get('financements', {})
    emprunts = float(financements.get('emprunts_bancaires', 0))
    duree_emprunt = int(financements.get('duree_emprunt', 5))
    remboursement_annuel = emprunts / duree_emprunt if duree_emprunt > 0 else 0
    
    remboursements = [remboursement_annuel] * min(duree_emprunt, 5)
    remboursements.extend([0] * (5 - len(remboursements)))
    
    # Autofinancement net
    autofinancement_net = [c - r for c, r in zip(caf, remboursements)]
    
    table_data = []
    
    table_data.append({
        "Poste": "Résultat de l'exercice",
        "Année 1": f"{resultat_net[0]:,.2f}",
        "Année 2": f"{resultat_net[1]:,.2f}",
        "Année 3": f"{resultat_net[2]:,.2f}",
        "Année 4": f"{resultat_net[3]:,.2f}",
        "Année 5": f"{resultat_net[4]:,.2f}"
    })
    
    table_data.append({
        "Poste": "Dotations aux amortissements",
        "Année 1": f"{amortissements[0]:,.2f}",
        "Année 2": f"{amortissements[1]:,.2f}",
        "Année 3": f"{amortissements[2]:,.2f}",
        "Année 4": f"{amortissements[3]:,.2f}",
        "Année 5": f"{amortissements[4]:,.2f}"
    })
    
    table_data.append({
        "Poste": "Capacité d'Autofinancement (CAF)",
        "Année 1": f"{caf[0]:,.2f}",
        "Année 2": f"{caf[1]:,.2f}",
        "Année 3": f"{caf[2]:,.2f}",
        "Année 4": f"{caf[3]:,.2f}",
        "Année 5": f"{caf[4]:,.2f}"
    })
    
    table_data.append({
        "Poste": "Remboursement emprunt",
        "Année 1": f"{remboursements[0]:,.2f}",
        "Année 2": f"{remboursements[1]:,.2f}",
        "Année 3": f"{remboursements[2]:,.2f}",
        "Année 4": f"{remboursements[3]:,.2f}",
        "Année 5": f"{remboursements[4]:,.2f}"
    })
    
    table_data.append({
        "Poste": "Autofinancement net",
        "Année 1": f"{autofinancement_net[0]:,.2f}",
        "Année 2": f"{autofinancement_net[1]:,.2f}",
        "Année 3": f"{autofinancement_net[2]:,.2f}",
        "Année 4": f"{autofinancement_net[3]:,.2f}",
        "Année 5": f"{autofinancement_net[4]:,.2f}"
    })
    
    return {
        'table_data': table_data,
        'caf': caf,
        'remboursements': remboursements,
        'autofinancement_net': autofinancement_net
    }

def calculer_tableau_seuil_rentabilite_5_ans(donnees: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule le seuil de rentabilité sur 5 ans
    
    Args:
        donnees (dict): Données financières
    
    Returns:
        dict: Tableau seuil de rentabilité sur 5 ans
    """
    compte_resultats = calculer_compte_resultats_5_ans(donnees)
    
    ca_annees = compte_resultats['ca_annees']
    charges_var = compte_resultats['charges_var_annees']
    charges_fixes = compte_resultats['charges_fixes_annees']
    salaires_charges = compte_resultats['total_salaires_charges']
    
    # Coûts fixes totaux = charges fixes + salaires
    couts_fixes_totaux = [cf + sc for cf, sc in zip(charges_fixes, salaires_charges)]
    
    # Taux de marge sur coûts variables
    taux_marge = [(ca - cv) / ca if ca > 0 else 0 for ca, cv in zip(ca_annees, charges_var)]
    
    # Seuil de rentabilité = Coûts fixes / Taux de marge
    seuil_rentabilite = [
        cf / tm if tm > 0 else 0 
        for cf, tm in zip(couts_fixes_totaux, taux_marge)
    ]
    
    # Point mort en jours
    point_mort_jours = [
        (sr / ca * 365) if ca > 0 else 365 
        for sr, ca in zip(seuil_rentabilite, ca_annees)
    ]
    
    table_data = []
    
    table_data.append({
        "Élément": "Ventes réelles",
        "Année 1": f"{ca_annees[0]:,.2f}",
        "Année 2": f"{ca_annees[1]:,.2f}",
        "Année 3": f"{ca_annees[2]:,.2f}",
        "Année 4": f"{ca_annees[3]:,.2f}",
        "Année 5": f"{ca_annees[4]:,.2f}"
    })
    
    table_data.append({
        "Élément": "Coûts variables",
        "Année 1": f"{charges_var[0]:,.2f}",
        "Année 2": f"{charges_var[1]:,.2f}",
        "Année 3": f"{charges_var[2]:,.2f}",
        "Année 4": f"{charges_var[3]:,.2f}",
        "Année 5": f"{charges_var[4]:,.2f}"
    })
    
    table_data.append({
        "Élément": "Coûts fixes",
        "Année 1": f"{couts_fixes_totaux[0]:,.2f}",
        "Année 2": f"{couts_fixes_totaux[1]:,.2f}",
        "Année 3": f"{couts_fixes_totaux[2]:,.2f}",
        "Année 4": f"{couts_fixes_totaux[3]:,.2f}",
        "Année 5": f"{couts_fixes_totaux[4]:,.2f}"
    })
    
    table_data.append({
        "Élément": "Seuil de rentabilité",
        "Année 1": f"{seuil_rentabilite[0]:,.2f}",
        "Année 2": f"{seuil_rentabilite[1]:,.2f}",
        "Année 3": f"{seuil_rentabilite[2]:,.2f}",
        "Année 4": f"{seuil_rentabilite[3]:,.2f}",
        "Année 5": f"{seuil_rentabilite[4]:,.2f}"
    })
    
    table_data.append({
        "Élément": "Point mort (jours)",
        "Année 1": f"{point_mort_jours[0]:.0f}",
        "Année 2": f"{point_mort_jours[1]:.0f}",
        "Année 3": f"{point_mort_jours[2]:.0f}",
        "Année 4": f"{point_mort_jours[3]:.0f}",
        "Année 5": f"{point_mort_jours[4]:.0f}"
    })
    
    return {
        'table_data': table_data,
        'seuil_rentabilite': seuil_rentabilite,
        'point_mort_jours': point_mort_jours
    }

def calculer_tableau_bfr_5_ans(donnees: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule le besoin en fonds de roulement sur 5 ans
    
    Args:
        donnees (dict): Données financières
    
    Returns:
        dict: Tableau BFR sur 5 ans
    """
    compte_resultats = calculer_compte_resultats_5_ans(donnees)
    ca_annees = compte_resultats['ca_annees']
    charges_var = compte_resultats['charges_var_annees']
    
    # Délais standards
    delai_clients = 30  # jours
    delai_stocks = 60   # jours
    delai_fournisseurs = 30  # jours
    
    # Calculs BFR
    creances_clients = [ca * delai_clients / 365 for ca in ca_annees]
    stocks = [cv * delai_stocks / 365 for cv in charges_var]
    dettes_fournisseurs = [cv * delai_fournisseurs / 365 for cv in charges_var]
    
    bfr = [cc + s - df for cc, s, df in zip(creances_clients, stocks, dettes_fournisseurs)]
    
    table_data = []
    
    table_data.append({
        "Élément": f"Crédits clients ({delai_clients} jours)",
        "Année 1": f"{creances_clients[0]:,.2f}",
        "Année 2": f"{creances_clients[1]:,.2f}",
        "Année 3": f"{creances_clients[2]:,.2f}",
        "Année 4": f"{creances_clients[3]:,.2f}",
        "Année 5": f"{creances_clients[4]:,.2f}"
    })
    
    table_data.append({
        "Élément": f"Stocks ({delai_stocks} jours)",
        "Année 1": f"{stocks[0]:,.2f}",
        "Année 2": f"{stocks[1]:,.2f}",
        "Année 3": f"{stocks[2]:,.2f}",
        "Année 4": f"{stocks[3]:,.2f}",
        "Année 5": f"{stocks[4]:,.2f}"
    })
    
    table_data.append({
        "Élément": f"Dettes fournisseurs ({delai_fournisseurs} jours)",
        "Année 1": f"{dettes_fournisseurs[0]:,.2f}",
        "Année 2": f"{dettes_fournisseurs[1]:,.2f}",
        "Année 3": f"{dettes_fournisseurs[2]:,.2f}",
        "Année 4": f"{dettes_fournisseurs[3]:,.2f}",
        "Année 5": f"{dettes_fournisseurs[4]:,.2f}"
    })
    
    table_data.append({
        "Élément": "Besoin en Fonds de Roulement",
        "Année 1": f"{bfr[0]:,.2f}",
        "Année 2": f"{bfr[1]:,.2f}",
        "Année 3": f"{bfr[2]:,.2f}",
        "Année 4": f"{bfr[3]:,.2f}",
        "Année 5": f"{bfr[4]:,.2f}"
    })
    
    return {
        'table_data': table_data,
        'bfr': bfr,
        'creances_clients': creances_clients,
        'stocks': stocks,
        'dettes_fournisseurs': dettes_fournisseurs
    }

def calculer_plan_financement_cinq_ans(donnees: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule le plan de financement sur 5 ans
    
    Args:
        donnees (dict): Données financières
    
    Returns:
        dict: Plan de financement sur 5 ans
    """
    # Récupération des données calculées
    compte_resultats = calculer_compte_resultats_5_ans(donnees)
    caf_data = calculer_tableau_caf_5_ans(donnees)
    bfr_data = calculer_tableau_bfr_5_ans(donnees)
    
    # Données de base
    investissements = donnees.get('investissements', [])
    total_invest_initial = sum(float(inv.get('montant', 0)) for inv in investissements)
    
    # Variation du BFR
    bfr = bfr_data['bfr']
    variation_bfr = [bfr[0]] + [bfr[i] - bfr[i-1] for i in range(1, 5)]
    
    # Remboursements d'emprunts
    remboursements = caf_data['remboursements']
    
    # Besoins totaux
    besoins_totaux = [
        total_invest_initial if i == 0 else 0 + var_bfr + remb 
        for i, (var_bfr, remb) in enumerate(zip(variation_bfr, remboursements))
    ]
    
    # Ressources (CAF + apports/emprunts initiaux)
    financements = donnees.get('financements', {})
    apport_personnel = float(financements.get('apport_personnel', 0))
    emprunts = float(financements.get('emprunts_bancaires', 0))
    subventions = float(financements.get('subventions', 0))
    
    caf = caf_data['caf']
    ressources_totales = [
        (apport_personnel + emprunts + subventions + caf[0]) if i == 0 else caf[i]
        for i in range(5)
    ]
    
    # Variation de trésorerie
    variation_tresorerie = [res - bes for res, bes in zip(ressources_totales, besoins_totaux)]
    
    # Trésorerie cumulée
    tresorerie_cumulee = []
    cumul = 0
    for var in variation_tresorerie:
        cumul += var
        tresorerie_cumulee.append(cumul)
    
    table_data = []
    
    table_data.append({
        "Poste": "Investissements",
        "Année 1": f"{total_invest_initial:,.2f}" if 0 == 0 else "0.00",
        "Année 2": "0.00",
        "Année 3": "0.00",
        "Année 4": "0.00",
        "Année 5": "0.00"
    })
    
    table_data.append({
        "Poste": "Variation BFR",
        "Année 1": f"{variation_bfr[0]:,.2f}",
        "Année 2": f"{variation_bfr[1]:,.2f}",
        "Année 3": f"{variation_bfr[2]:,.2f}",
        "Année 4": f"{variation_bfr[3]:,.2f}",
        "Année 5": f"{variation_bfr[4]:,.2f}"
    })
    
    table_data.append({
        "Poste": "Remboursement d'emprunts",
        "Année 1": f"{remboursements[0]:,.2f}",
        "Année 2": f"{remboursements[1]:,.2f}",
        "Année 3": f"{remboursements[2]:,.2f}",
        "Année 4": f"{remboursements[3]:,.2f}",
        "Année 5": f"{remboursements[4]:,.2f}"
    })
    
    table_data.append({
        "Poste": "Total besoins",
        "Année 1": f"{besoins_totaux[0]:,.2f}",
        "Année 2": f"{besoins_totaux[1]:,.2f}",
        "Année 3": f"{besoins_totaux[2]:,.2f}",
        "Année 4": f"{besoins_totaux[3]:,.2f}",
        "Année 5": f"{besoins_totaux[4]:,.2f}"
    })
    
    table_data.append({
        "Poste": "Capacité d'autofinancement",
        "Année 1": f"{caf[0]:,.2f}",
        "Année 2": f"{caf[1]:,.2f}",
        "Année 3": f"{caf[2]:,.2f}",
        "Année 4": f"{caf[3]:,.2f}",
        "Année 5": f"{caf[4]:,.2f}"
    })
    
    table_data.append({
        "Poste": "Apports/emprunts/subventions",
        "Année 1": f"{apport_personnel + emprunts + subventions:,.2f}",
        "Année 2": "0.00",
        "Année 3": "0.00", 
        "Année 4": "0.00",
        "Année 5": "0.00"
    })
    
    table_data.append({
        "Poste": "Total ressources",
        "Année 1": f"{ressources_totales[0]:,.2f}",
        "Année 2": f"{ressources_totales[1]:,.2f}",
        "Année 3": f"{ressources_totales[2]:,.2f}",
        "Année 4": f"{ressources_totales[3]:,.2f}",
        "Année 5": f"{ressources_totales[4]:,.2f}"
    })
    
    table_data.append({
        "Poste": "Variation de trésorerie",
        "Année 1": f"{variation_tresorerie[0]:,.2f}",
        "Année 2": f"{variation_tresorerie[1]:,.2f}",
        "Année 3": f"{variation_tresorerie[2]:,.2f}",
        "Année 4": f"{variation_tresorerie[3]:,.2f}",
        "Année 5": f"{variation_tresorerie[4]:,.2f}"
    })
    
    table_data.append({
        "Poste": "Trésorerie cumulée",
        "Année 1": f"{tresorerie_cumulee[0]:,.2f}",
        "Année 2": f"{tresorerie_cumulee[1]:,.2f}",
        "Année 3": f"{tresorerie_cumulee[2]:,.2f}",
        "Année 4": f"{tresorerie_cumulee[3]:,.2f}",
        "Année 5": f"{tresorerie_cumulee[4]:,.2f}"
    })
    
    return {
        'table_data': table_data,
        'besoins_totaux': besoins_totaux,
        'ressources_totales': ressources_totales,
        'variation_tresorerie': variation_tresorerie,
        'tresorerie_cumulee': tresorerie_cumulee
    }

def calculer_plan_financement_5_ans(donnees: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule le plan de financement sur 5 ans
    """
    try:
        # Données de financement
        financement = donnees.get('financement', {})
        apport_personnel = financement.get('apport_personnel', 0)
        
        # Prêts
        prets = []
        for i in range(1, 4):
            pret = financement.get(f'pret_{i}', {})
            if pret.get('montant', 0) > 0:
                prets.append(pret)
        
        # Subventions
        subventions = []
        for i in range(1, 3):
            subv = financement.get(f'subvention_{i}', {})
            if subv.get('montant', 0) > 0:
                subventions.append(subv)
        
        # Besoins
        besoins_demarrage = donnees.get('besoins_demarrage', {})
        total_besoins = sum(besoins_demarrage.values())
        
        # Calcul CAF (capacité d'autofinancement)
        caf_data = calculer_tableau_caf_5_ans(donnees)
        caf_annuelle = {}
        if caf_data.get('success'):
            for annee in ['annee_1', 'annee_2', 'annee_3', 'annee_4', 'annee_5']:
                caf_annuelle[annee] = caf_data['tableau'][annee]['caf']
        
        # Calcul BFR
        bfr_data = calculer_tableau_bfr_5_ans(donnees)
        variation_bfr = {}
        if bfr_data.get('success'):
            for annee in ['annee_1', 'annee_2', 'annee_3', 'annee_4', 'annee_5']:
                variation_bfr[annee] = bfr_data['tableau'][annee]['variation_bfr']
        
        plan_financement = {}
        
        for i, annee in enumerate(['annee_1', 'annee_2', 'annee_3', 'annee_4', 'annee_5']):
            # Ressources
            ressources = 0
            if i == 0:  # Première année
                ressources += apport_personnel
                ressources += sum(pret.get('montant', 0) for pret in prets)
                ressources += sum(subv.get('montant', 0) for subv in subventions)
            
            ressources += caf_annuelle.get(annee, 0)
            
            # Emplois
            emplois = 0
            if i == 0:  # Première année
                emplois += total_besoins
            
            emplois += variation_bfr.get(annee, 0)
            
            # Remboursements de prêts
            remboursements = 0
            for pret in prets:
                duree_mois = pret.get('duree_mois', 60)
                if duree_mois > i * 12:  # Le prêt est encore en cours
                    montant_pret = pret.get('montant', 0)
                    taux = pret.get('taux', 5)
                    details_pret = calculer_pret_interet_fixe(montant_pret, taux, duree_mois)
                    remboursements += details_pret['mensualite'] * 12
            
            emplois += remboursements
            
            # Solde
            solde = ressources - emplois
            
            plan_financement[annee] = {
                'ressources': {
                    'apport_personnel': apport_personnel if i == 0 else 0,
                    'prets': sum(pret.get('montant', 0) for pret in prets) if i == 0 else 0,
                    'subventions': sum(subv.get('montant', 0) for subv in subventions) if i == 0 else 0,
                    'caf': caf_annuelle.get(annee, 0),
                    'total_ressources': ressources
                },
                'emplois': {
                    'investissements': total_besoins if i == 0 else 0,
                    'variation_bfr': variation_bfr.get(annee, 0),
                    'remboursements_prets': remboursements,
                    'total_emplois': emplois
                },
                'solde': solde,
                'solde_cumule': sum(plan_financement[a]['solde'] for a in plan_financement.keys()) + solde
            }
        
        return {
            'success': True,
            'plan': plan_financement,
            'resume': {
                'equilibre_global': all(annee_data['solde'] >= 0 for annee_data in plan_financement.values()),
                'solde_final': plan_financement['annee_5']['solde_cumule']
            }
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def calculer_budget_tresorerie_5_ans(donnees: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule le budget de trésorerie mensuel pour les 5 années
    """
    try:
        # Données CA 
        ca_donnees = donnees.get('ca_mensuel', {})
        
        # Données charges fixes avec répartition mensuelle
        charges_fixes_donnees = donnees.get('charges_fixes', [])
        
        # Délais de paiement
        delai_clients = donnees.get('delai_paiement_clients', 30)
        delai_fournisseurs = donnees.get('delai_paiement_fournisseurs', 30)
        
        # Trésorerie initiale
        tresorerie_initiale = donnees.get('tresorerie_initiale', 0)
        
        budget_tresorerie = {}
        tresorerie_cumul = tresorerie_initiale
        
        # Calcul pour 5 années (60 mois)
        for annee in range(1, 6):
            for mois in range(1, 13):
                mois_global = (annee - 1) * 12 + mois
                
                # Encaissements (CA avec délai de paiement)
                if mois_global <= delai_clients // 30:
                    encaissements = 0  # Pas encore d'encaissements
                else:
                    mois_encaissement = mois_global - (delai_clients // 30)
                    if mois_encaissement <= 12:  # Première année
                        encaissements = ca_donnees.get(f'mois_{mois_encaissement}', 0)
                    else:
                        # Années suivantes - extrapolation basée sur les augmentations
                        annee_ca = ((mois_encaissement - 1) // 12) + 1
                        ca_annuel_key = f'annee_{annee_ca}' if annee_ca > 1 else 'annee_1'
                        ca_annuel = ca_donnees.get(ca_annuel_key, 0)
                        encaissements = ca_annuel / 12  # Répartition mensuelle
                
                # Décaissements
                if mois <= 12:  # Première année
                    ca_mois = ca_donnees.get(f'mois_{mois}', 0)
                else:
                    # Années suivantes
                    ca_annuel_key = f'annee_{annee}'
                    ca_annuel = ca_donnees.get(ca_annuel_key, 0)
                    ca_mois = ca_annuel / 12
                
                charges_variables = ca_mois * 0.7  # 70% du CA (inverse de la marge de 30%)
                
                # Charges fixes mensuelles
                charges_fixes_mois = 0
                for charge in charges_fixes_donnees:
                    if charge.get('repartition_mensuelle'):
                        charges_fixes_mois += charge['repartition_mensuelle'].get(f'mois_{mois}', 0)
                    else:
                        charges_fixes_mois += charge.get(f'annee{annee}', 0) / 12
                
                # Charges variables avec délai de paiement fournisseurs
                if mois_global <= delai_fournisseurs // 30:
                    decaissements_variables = 0
                else:
                    mois_paiement = mois_global - (delai_fournisseurs // 30)
                    if mois_paiement <= 12:
                        ca_a_payer = ca_donnees.get(f'mois_{mois_paiement}', 0)
                    else:
                        annee_paiement = ((mois_paiement - 1) // 12) + 1
                        ca_annuel_key = f'annee_{annee_paiement}'
                        ca_annuel_paiement = ca_donnees.get(ca_annuel_key, 0)
                        ca_a_payer = ca_annuel_paiement / 12
                    decaissements_variables = ca_a_payer * 0.7
                
                total_decaissements = charges_fixes_mois + decaissements_variables
                
                # Solde du mois
                solde_mois = encaissements - total_decaissements
                tresorerie_cumul += solde_mois
                
                budget_tresorerie[f'annee_{annee}_mois_{mois}'] = {
                    'encaissements': encaissements,
                    'charges_fixes': charges_fixes_mois,
                    'charges_variables_payees': decaissements_variables,
                    'total_decaissements': total_decaissements,
                    'solde_mois': solde_mois,
                    'tresorerie_cumul': tresorerie_cumul,
                    'tension_tresorerie': tresorerie_cumul < 0
                }
        
        # Analyse des tensions de trésorerie
        mois_deficitaires = [mois for mois, data in budget_tresorerie.items() 
                           if data['tension_tresorerie']]
        
        return {
            'success': True,
            'budget': budget_tresorerie,
            'resume': {
                'tresorerie_finale': tresorerie_cumul,
                'tresorerie_minimale': min(data['tresorerie_cumul'] for data in budget_tresorerie.values()),
                'mois_deficitaires': mois_deficitaires,
                'besoin_financement': abs(min(data['tresorerie_cumul'] for data in budget_tresorerie.values())) if any(data['tension_tresorerie'] for data in budget_tresorerie.values()) else 0
            }
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}