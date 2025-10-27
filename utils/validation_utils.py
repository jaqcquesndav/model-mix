"""
Fonctions utilitaires pour la validation et la gestion des données
"""

import re
import json
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Union

def valider_email(email: str) -> bool:
    """
    Valide le format d'une adresse email
    
    Args:
        email (str): Adresse email à valider
    
    Returns:
        bool: True si l'email est valide
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def valider_telephone(telephone: str) -> bool:
    """
    Valide le format d'un numéro de téléphone
    
    Args:
        telephone (str): Numéro de téléphone à valider
    
    Returns:
        bool: True si le téléphone est valide
    """
    # Accepte différents formats congolais
    pattern = r'^(\+243|0)?[0-9]{9}$'
    return re.match(pattern, telephone.replace(' ', '').replace('-', '')) is not None

def nettoyer_texte(texte: str) -> str:
    """
    Nettoie un texte en supprimant les caractères indésirables
    
    Args:
        texte (str): Texte à nettoyer
    
    Returns:
        str: Texte nettoyé
    """
    if not isinstance(texte, str):
        return str(texte)
    
    # Supprime les caractères de contrôle et espaces multiples
    texte = re.sub(r'\s+', ' ', texte)
    texte = texte.strip()
    
    return texte

def valider_montant(montant: Union[str, float, int]) -> tuple[bool, float]:
    """
    Valide et convertit un montant
    
    Args:
        montant: Montant à valider (string, float ou int)
    
    Returns:
        tuple: (est_valide, montant_converti)
    """
    try:
        if isinstance(montant, str):
            # Supprime les espaces et caractères spéciaux
            montant_clean = re.sub(r'[^\d.,]', '', montant)
            montant_clean = montant_clean.replace(',', '.')
            montant_float = float(montant_clean)
        else:
            montant_float = float(montant)
        
        return montant_float >= 0, max(0, montant_float)
    except (ValueError, TypeError):
        return False, 0.0

def valider_pourcentage(valeur: Union[str, float, int]) -> tuple[bool, float]:
    """
    Valide et convertit un pourcentage
    
    Args:
        valeur: Valeur à valider comme pourcentage
    
    Returns:
        tuple: (est_valide, pourcentage_converti)
    """
    try:
        if isinstance(valeur, str):
            valeur_clean = re.sub(r'[^\d.,]', '', valeur)
            valeur_clean = valeur_clean.replace(',', '.')
            valeur_float = float(valeur_clean)
        else:
            valeur_float = float(valeur)
        
        return 0 <= valeur_float <= 100, max(0, min(100, valeur_float))
    except (ValueError, TypeError):
        return False, 0.0

def valider_donnees_entreprise(donnees: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données générales d'une entreprise
    
    Args:
        donnees (dict): Données de l'entreprise
    
    Returns:
        dict: Résultats de validation
    """
    erreurs = []
    avertissements = []
    
    # Nom de l'entreprise
    nom = donnees.get('nom_entreprise', '').strip()
    if not nom:
        erreurs.append("Le nom de l'entreprise est obligatoire")
    elif len(nom) < 2:
        avertissements.append("Le nom de l'entreprise semble très court")
    
    # Secteur d'activité
    if not donnees.get('secteur_activite'):
        erreurs.append("Le secteur d'activité doit être sélectionné")
    
    # Contact
    email = donnees.get('email', '').strip()
    if email and not valider_email(email):
        erreurs.append("L'adresse email n'est pas valide")
    
    telephone = donnees.get('telephone', '').strip()
    if telephone and not valider_telephone(telephone):
        avertissements.append("Le format du numéro de téléphone pourrait être incorrect")
    
    # Localisation
    if not donnees.get('localisation'):
        avertissements.append("La localisation n'est pas spécifiée")
    
    return {
        'valide': len(erreurs) == 0,
        'erreurs': erreurs,
        'avertissements': avertissements,
        'donnees_nettoyees': {
            'nom_entreprise': nettoyer_texte(nom),
            'email': email.lower() if email else '',
            'telephone': telephone,
            'secteur_activite': donnees.get('secteur_activite', ''),
            'localisation': donnees.get('localisation', '')
        }
    }

def valider_investissement(investissement: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données d'un investissement
    
    Args:
        investissement (dict): Données de l'investissement
    
    Returns:
        dict: Résultats de validation
    """
    erreurs = []
    avertissements = []
    
    # Nom/Description
    nom = investissement.get('nom', '').strip()
    if not nom:
        erreurs.append("La description de l'investissement est obligatoire")
    
    # Montant
    montant_valide, montant = valider_montant(investissement.get('montant', 0))
    if not montant_valide:
        erreurs.append("Le montant de l'investissement n'est pas valide")
    elif montant == 0:
        avertissements.append("L'investissement a un montant de 0")
    
    # Durée d'amortissement
    duree = investissement.get('duree_amortissement', 0)
    try:
        duree = int(duree)
        if duree <= 0:
            erreurs.append("La durée d'amortissement doit être positive")
        elif duree > 20:
            avertissements.append("Durée d'amortissement très longue (>20 ans)")
    except (ValueError, TypeError):
        erreurs.append("La durée d'amortissement doit être un nombre entier")
    
    return {
        'valide': len(erreurs) == 0,
        'erreurs': erreurs,
        'avertissements': avertissements,
        'donnees_nettoyees': {
            'nom': nettoyer_texte(nom),
            'montant': montant,
            'duree_amortissement': duree
        }
    }

def consolider_erreurs(validations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Consolide les résultats de plusieurs validations
    
    Args:
        validations (list): Liste des résultats de validation
    
    Returns:
        dict: Résultat consolidé
    """
    toutes_erreurs = []
    tous_avertissements = []
    
    for validation in validations:
        toutes_erreurs.extend(validation.get('erreurs', []))
        tous_avertissements.extend(validation.get('avertissements', []))
    
    return {
        'valide': len(toutes_erreurs) == 0,
        'erreurs': toutes_erreurs,
        'avertissements': tous_avertissements,
        'nb_erreurs': len(toutes_erreurs),
        'nb_avertissements': len(tous_avertissements)
    }

def serialiser_donnees(donnees: Any) -> str:
    """
    Sérialise des données en JSON en gérant les types spéciaux
    
    Args:
        donnees: Données à sérialiser
    
    Returns:
        str: JSON sérialisé
    """
    def convertir_type(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        return str(obj)
    
    try:
        return json.dumps(donnees, default=convertir_type, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Erreur de sérialisation: {str(e)}"

def deserialiser_donnees(json_str: str) -> Any:
    """
    Désérialise des données JSON
    
    Args:
        json_str (str): Chaîne JSON à désérialiser
    
    Returns:
        Any: Données désérialisées ou None en cas d'erreur
    """
    try:
        return json.loads(json_str)
    except Exception:
        return None

def generer_identifiant_unique() -> str:
    """
    Génère un identifiant unique basé sur la date/heure
    
    Returns:
        str: Identifiant unique
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

def extraire_nombre_depuis_texte(texte: str) -> Optional[float]:
    """
    Extrait le premier nombre trouvé dans un texte
    
    Args:
        texte (str): Texte contenant potentiellement un nombre
    
    Returns:
        float or None: Nombre extrait ou None si aucun trouvé
    """
    pattern = r'[-+]?\d*\.?\d+'
    match = re.search(pattern, str(texte))
    if match:
        try:
            return float(match.group())
        except ValueError:
            pass
    return None

def comparer_donnees(donnees1: Dict, donnees2: Dict) -> Dict[str, Any]:
    """
    Compare deux dictionnaires de données
    
    Args:
        donnees1 (dict): Premier dictionnaire
        donnees2 (dict): Deuxième dictionnaire
    
    Returns:
        dict: Résultat de la comparaison
    """
    differences = {}
    toutes_cles = set(donnees1.keys()) | set(donnees2.keys())
    
    for cle in toutes_cles:
        val1 = donnees1.get(cle)
        val2 = donnees2.get(cle)
        
        if val1 != val2:
            differences[cle] = {
                'avant': val1,
                'apres': val2
            }
    
    return {
        'identiques': len(differences) == 0,
        'differences': differences,
        'nb_differences': len(differences)
    }