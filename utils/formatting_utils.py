"""
Fonctions utilitaires pour le formatage et l'affichage des données
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Union
import re

def formater_devise(montant: Union[float, int], devise: str = "USD", precision: int = 2) -> str:
    """
    Formate un montant avec la devise
    
    Args:
        montant: Montant à formater
        devise: Code de la devise
        precision: Nombre de décimales
    
    Returns:
        str: Montant formaté
    """
    if montant == 0:
        return f"0 {devise}"
    
    # Gestion des montants très grands
    if abs(montant) >= 1_000_000_000:
        return f"{montant/1_000_000_000:.1f}B {devise}"
    elif abs(montant) >= 1_000_000:
        return f"{montant/1_000_000:.1f}M {devise}"
    elif abs(montant) >= 1_000:
        return f"{montant/1_000:.1f}K {devise}"
    else:
        return f"{montant:,.{precision}f} {devise}"

def formater_pourcentage(valeur: Union[float, int], precision: int = 1) -> str:
    """
    Formate une valeur en pourcentage
    
    Args:
        valeur: Valeur à formater
        precision: Nombre de décimales
    
    Returns:
        str: Valeur formatée en pourcentage
    """
    return f"{valeur:.{precision}f}%"

def formater_nombre(nombre: Union[float, int], precision: int = 2, separateur_milliers: str = ",") -> str:
    """
    Formate un nombre avec séparateur de milliers
    
    Args:
        nombre: Nombre à formater
        precision: Nombre de décimales
        separateur_milliers: Caractère de séparation des milliers
    
    Returns:
        str: Nombre formaté
    """
    if precision == 0:
        return f"{nombre:,.0f}".replace(",", separateur_milliers)
    else:
        return f"{nombre:,.{precision}f}".replace(",", separateur_milliers)

def formater_date(date_obj: Union[datetime, date, str], format_sortie: str = "%d/%m/%Y") -> str:
    """
    Formate une date selon le format spécifié
    
    Args:
        date_obj: Date à formater
        format_sortie: Format de sortie désiré
    
    Returns:
        str: Date formatée
    """
    if isinstance(date_obj, str):
        try:
            # Essaie plusieurs formats d'entrée
            for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]:
                try:
                    date_obj = datetime.strptime(date_obj, fmt).date()
                    break
                except ValueError:
                    continue
        except:
            return str(date_obj)
    
    if isinstance(date_obj, datetime):
        date_obj = date_obj.date()
    
    if isinstance(date_obj, date):
        return date_obj.strftime(format_sortie)
    
    return str(date_obj)

def formater_duree(jours: int) -> str:
    """
    Formate une durée en jours en format lisible
    
    Args:
        jours: Nombre de jours
    
    Returns:
        str: Durée formatée
    """
    if jours < 30:
        return f"{jours} jour{'s' if jours > 1 else ''}"
    elif jours < 365:
        mois = jours // 30
        jours_restants = jours % 30
        if jours_restants == 0:
            return f"{mois} mois"
        else:
            return f"{mois} mois et {jours_restants} jour{'s' if jours_restants > 1 else ''}"
    else:
        annees = jours // 365
        jours_restants = jours % 365
        if jours_restants == 0:
            return f"{annees} an{'s' if annees > 1 else ''}"
        else:
            mois_restants = jours_restants // 30
            return f"{annees} an{'s' if annees > 1 else ''} et {mois_restants} mois"

def creer_tableau_markdown(donnees: List[Dict], headers: List[str], titre: str = "") -> str:
    """
    Crée un tableau au format Markdown
    
    Args:
        donnees: Liste des lignes de données
        headers: Liste des en-têtes
        titre: Titre optionnel du tableau
    
    Returns:
        str: Tableau au format Markdown
    """
    markdown = ""
    
    if titre:
        markdown += f"### {titre}\n\n"
    
    # En-têtes
    markdown += "| " + " | ".join(headers) + " |\n"
    markdown += "|" + "---|" * len(headers) + "\n"
    
    # Données
    for ligne in donnees:
        valeurs = []
        for header in headers:
            valeur = ligne.get(header, "")
            if isinstance(valeur, (int, float)):
                if isinstance(valeur, float) and valeur.is_integer():
                    valeur = int(valeur)
                valeurs.append(str(valeur))
            else:
                valeurs.append(str(valeur))
        markdown += "| " + " | ".join(valeurs) + " |\n"
    
    markdown += "\n"
    return markdown

def formater_liste_puces(elements: List[str], titre: str = "") -> str:
    """
    Formate une liste d'éléments en puces Markdown
    
    Args:
        elements: Liste des éléments
        titre: Titre optionnel
    
    Returns:
        str: Liste formatée en Markdown
    """
    markdown = ""
    
    if titre:
        markdown += f"### {titre}\n\n"
    
    for element in elements:
        markdown += f"- {element}\n"
    
    markdown += "\n"
    return markdown

def formater_section_business_model(titre: str, contenu: str, details: List[str] = None) -> str:
    """
    Formate une section du business model canvas
    
    Args:
        titre: Titre de la section
        contenu: Contenu principal
        details: Liste de détails optionnels
    
    Returns:
        str: Section formatée
    """
    markdown = f"## {titre}\n\n"
    markdown += f"{contenu}\n\n"
    
    if details:
        markdown += "**Détails :**\n"
        for detail in details:
            markdown += f"- {detail}\n"
        markdown += "\n"
    
    return markdown

def extraire_nom_entreprise(texte: str) -> str:
    """
    Extrait le nom d'entreprise d'un texte
    
    Args:
        texte: Texte contenant potentiellement le nom d'entreprise
    
    Returns:
        str: Nom d'entreprise extrait ou chaîne vide
    """
    # Recherche de patterns courants
    patterns = [
        r'entreprise\s+([A-Za-z\s]+)',
        r'société\s+([A-Za-z\s]+)',
        r'PME\s+([A-Za-z\s]+)',
        r'startup\s+([A-Za-z\s]+)',
        r'"([^"]+)"',  # Texte entre guillemets
        r'nom[:\s]+([A-Za-z\s]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, texte, re.IGNORECASE)
        if match:
            nom = match.group(1).strip()
            if len(nom) > 2:  # Nom minimum de 3 caractères
                return nom
    
    return ""

def formater_synthese_financiere(donnees_financieres: Dict) -> str:
    """
    Formate une synthèse financière
    
    Args:
        donnees_financieres: Dictionnaire des données financières
    
    Returns:
        str: Synthèse formatée
    """
    synthese = "## Synthèse Financière\n\n"
    
    # Investissements
    if "investissements" in donnees_financieres:
        total_inv = sum([float(str(v).replace('$', '').replace(',', '').strip()) 
                        for v in donnees_financieres["investissements"].values() 
                        if isinstance(v, (int, float, str)) and 
                        str(v).replace('$', '').replace(',', '').replace('.', '').isdigit()])
        synthese += f"**Total Investissements :** {formater_devise(total_inv)}\n\n"
    
    # Autres indicateurs clés
    indicateurs = [
        ("Seuil de rentabilité", "seuil", "point_mort"),
        ("Besoin en fonds de roulement", "bfr", "total_bfr"),
        ("Capacité d'autofinancement", "capacite", "caf_net")
    ]
    
    for nom, section, cle in indicateurs:
        if section in donnees_financieres and cle in donnees_financieres[section]:
            valeur = donnees_financieres[section][cle]
            synthese += f"**{nom} :** {valeur}\n\n"
    
    return synthese

def nettoyer_contenu_markdown(contenu: str) -> str:
    """
    Nettoie le contenu Markdown en supprimant les éléments indésirables
    
    Args:
        contenu: Contenu Markdown à nettoyer
    
    Returns:
        str: Contenu nettoyé
    """
    # Supprime les balises HTML
    contenu = re.sub(r'<[^>]+>', '', contenu)
    
    # Supprime les espaces multiples
    contenu = re.sub(r'\n\s*\n\s*\n', '\n\n', contenu)
    
    # Supprime les caractères de contrôle
    contenu = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', contenu)
    
    return contenu.strip()

def generer_resume_donnees(donnees: Dict, max_longueur: int = 200) -> str:
    """
    Génère un résumé des données principales
    
    Args:
        donnees: Dictionnaire de données
        max_longueur: Longueur maximale du résumé
    
    Returns:
        str: Résumé des données
    """
    elements_cles = []
    
    # Nom d'entreprise
    if "nom_entreprise" in donnees:
        elements_cles.append(f"Entreprise: {donnees['nom_entreprise']}")
    
    # Secteur
    if "secteur_activite" in donnees:
        elements_cles.append(f"Secteur: {donnees['secteur_activite']}")
    
    # Montants significatifs
    for cle in ["ca_previsionnel", "investissement_total", "resultat_net"]:
        if cle in donnees and isinstance(donnees[cle], (int, float)):
            elements_cles.append(f"{cle}: {formater_devise(donnees[cle])}")
    
    resume = " | ".join(elements_cles)
    
    if len(resume) > max_longueur:
        resume = resume[:max_longueur-3] + "..."
    
    return resume