"""
Fonctions utilitaires pour les calculs financiers
"""

import pandas as pd
import numpy as np
from datetime import datetime, date

def calculer_taux_mensuel(taux_annuel):
    """Convertit un taux annuel en taux mensuel"""
    return taux_annuel / 12 / 100

def calculer_pret_interet_fixe(montant, taux_annuel, duree_mois):
    """
    Calcule la mensualité et les détails d'un prêt à intérêt fixe
    
    Args:
        montant (float): Montant du prêt
        taux_annuel (float): Taux d'intérêt annuel en pourcentage
        duree_mois (int): Durée en mois
    
    Returns:
        dict: Détails du prêt (mensualité, total intérêts, etc.)
    """
    if montant <= 0 or taux_annuel <= 0 or duree_mois <= 0:
        return {"mensualite": 0, "total_interets": 0, "total_a_payer": montant}
    
    taux_mensuel = calculer_taux_mensuel(taux_annuel)
    
    if taux_mensuel == 0:
        mensualite = montant / duree_mois
        total_interets = 0
    else:
        mensualite = montant * (taux_mensuel * (1 + taux_mensuel)**duree_mois) / ((1 + taux_mensuel)**duree_mois - 1)
        total_interets = mensualite * duree_mois - montant
    
    return {
        "mensualite": round(mensualite, 2),
        "total_interets": round(total_interets, 2),
        "total_a_payer": round(montant + total_interets, 2),
        "taux_mensuel": round(taux_mensuel * 100, 4)
    }

def calculer_impot_societes(resultat, taux=30):
    """
    Calcule l'impôt sur les sociétés
    
    Args:
        resultat (float): Résultat avant impôt
        taux (float): Taux d'imposition en pourcentage
    
    Returns:
        float: Montant de l'impôt
    """
    if resultat <= 0:
        return 0
    return round(resultat * taux / 100, 2)

def calculer_bfr(ca_annuel, delai_clients, delai_fournisseurs, stock_jours=0):
    """
    Calcule le Besoin en Fonds de Roulement
    
    Args:
        ca_annuel (float): Chiffre d'affaires annuel
        delai_clients (int): Délai de paiement clients en jours
        delai_fournisseurs (int): Délai de paiement fournisseurs en jours
        stock_jours (int): Stock en jours de CA
    
    Returns:
        dict: Détails du BFR
    """
    ca_journalier = ca_annuel / 365
    
    creances_clients = ca_journalier * delai_clients
    dettes_fournisseurs = ca_journalier * delai_fournisseurs * 0.6  # Approximation 60% du CA
    stock = ca_journalier * stock_jours * 0.6  # Approximation coût des stocks
    
    bfr = creances_clients + stock - dettes_fournisseurs
    
    return {
        "creances_clients": round(creances_clients, 2),
        "dettes_fournisseurs": round(dettes_fournisseurs, 2),
        "stock": round(stock, 2),
        "bfr_total": round(bfr, 2)
    }

def calculer_seuil_rentabilite(charges_fixes, marge_variable_pourcentage):
    """
    Calcule le seuil de rentabilité
    
    Args:
        charges_fixes (float): Charges fixes annuelles
        marge_variable_pourcentage (float): Taux de marge variable en pourcentage
    
    Returns:
        dict: Détails du seuil de rentabilité
    """
    if marge_variable_pourcentage <= 0:
        return {"ca_seuil": 0, "point_mort_jours": 0}
    
    ca_seuil = charges_fixes / (marge_variable_pourcentage / 100)
    point_mort_jours = 365 * (charges_fixes / ca_seuil) if ca_seuil > 0 else 365
    
    return {
        "ca_seuil": round(ca_seuil, 2),
        "point_mort_jours": round(point_mort_jours, 0),
        "marge_securite": round(marge_variable_pourcentage, 2)
    }

def calculer_capacite_autofinancement(resultat_net, amortissements, provisions=0):
    """
    Calcule la capacité d'autofinancement
    
    Args:
        resultat_net (float): Résultat net
        amortissements (float): Amortissements de l'exercice
        provisions (float): Provisions constituées
    
    Returns:
        dict: Détails de la CAF
    """
    caf_brute = resultat_net + amortissements + provisions
    
    return {
        "resultat_net": round(resultat_net, 2),
        "amortissements": round(amortissements, 2),
        "provisions": round(provisions, 2),
        "caf_brute": round(caf_brute, 2)
    }

def calculer_amortissement_lineaire(valeur_acquisition, duree_ans):
    """
    Calcule l'amortissement linéaire
    
    Args:
        valeur_acquisition (float): Valeur d'acquisition du bien
        duree_ans (int): Durée d'amortissement en années
    
    Returns:
        dict: Détails de l'amortissement
    """
    if duree_ans <= 0:
        return {"annuite": 0, "taux": 0}
    
    taux = 100 / duree_ans
    annuite = valeur_acquisition / duree_ans
    
    return {
        "annuite": round(annuite, 2),
        "taux": round(taux, 2),
        "valeur_acquisition": round(valeur_acquisition, 2),
        "duree": duree_ans
    }

def calculer_ratios_financiers(ca, resultat_net, total_actif, capitaux_propres, dettes):
    """
    Calcule les principaux ratios financiers
    
    Args:
        ca (float): Chiffre d'affaires
        resultat_net (float): Résultat net
        total_actif (float): Total de l'actif
        capitaux_propres (float): Capitaux propres
        dettes (float): Total des dettes
    
    Returns:
        dict: Ratios financiers calculés
    """
    ratios = {}
    
    # Rentabilité
    ratios["marge_nette"] = round((resultat_net / ca * 100) if ca > 0 else 0, 2)
    ratios["roe"] = round((resultat_net / capitaux_propres * 100) if capitaux_propres > 0 else 0, 2)
    ratios["roa"] = round((resultat_net / total_actif * 100) if total_actif > 0 else 0, 2)
    
    # Endettement
    ratios["ratio_endettement"] = round((dettes / total_actif * 100) if total_actif > 0 else 0, 2)
    ratios["autonomie_financiere"] = round((capitaux_propres / total_actif * 100) if total_actif > 0 else 0, 2)
    
    return ratios

def formater_montant(montant, devise="USD"):
    """
    Formate un montant avec la devise
    
    Args:
        montant (float): Montant à formater
        devise (str): Devise (USD par défaut)
    
    Returns:
        str: Montant formaté
    """
    if montant == 0:
        return f"0 {devise}"
    
    if abs(montant) >= 1000000:
        return f"{montant/1000000:.2f}M {devise}"
    elif abs(montant) >= 1000:
        return f"{montant/1000:.1f}K {devise}"
    else:
        return f"{montant:,.2f} {devise}"

def valider_donnees_financieres(donnees):
    """
    Valide les données financières saisies
    
    Args:
        donnees (dict): Données à valider
    
    Returns:
        dict: Résultat de la validation (valid, errors)
    """
    errors = []
    
    # Vérifications de cohérence
    if donnees.get("ca", 0) < 0:
        errors.append("Le chiffre d'affaires ne peut pas être négatif")
    
    if donnees.get("charges_fixes", 0) < 0:
        errors.append("Les charges fixes ne peuvent pas être négatives")
    
    if donnees.get("taux_marge", 0) < 0 or donnees.get("taux_marge", 0) > 100:
        errors.append("Le taux de marge doit être entre 0 et 100%")
    
    # Vérification des investissements
    investissements = donnees.get("investissements", [])
    for inv in investissements:
        if inv.get("montant", 0) <= 0:
            errors.append(f"Le montant de l'investissement '{inv.get('nom', '')}' doit être positif")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

def extraire_donnees_export(session_state, cle_export):
    """
    Extrait les données d'export du session state
    
    Args:
        session_state: Session state de Streamlit
        cle_export (str): Clé des données d'export
    
    Returns:
        dict: Données extraites ou dictionnaire vide
    """
    return session_state.get(cle_export, {})