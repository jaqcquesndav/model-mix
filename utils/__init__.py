"""
Module d'initialisation des utilitaires
"""

from .financial_utils import (
    calculer_pret_interet_fixe,
    calculer_impot_societes,
    calculer_bfr,
    calculer_seuil_rentabilite,
    calculer_capacite_autofinancement,
    calculer_amortissement_lineaire,
    calculer_ratios_financiers,
    valider_donnees_financieres,
    extraire_donnees_export
)

from .validation_utils import (
    valider_email,
    valider_telephone,
    nettoyer_texte,
    valider_montant,
    valider_pourcentage,
    valider_donnees_entreprise,
    valider_investissement,
    consolider_erreurs,
    serialiser_donnees,
    deserialiser_donnees,
    generer_identifiant_unique,
    extraire_nombre_depuis_texte,
    comparer_donnees
)

from .formatting_utils import (
    formater_devise,
    formater_pourcentage,
    formater_nombre,
    formater_date,
    formater_duree,
    creer_tableau_markdown,
    formater_liste_puces,
    formater_section_business_model,
    extraire_nom_entreprise,
    formater_synthese_financiere,
    nettoyer_contenu_markdown,
    generer_resume_donnees
)

__all__ = [
    # Financial utils
    'calculer_pret_interet_fixe',
    'calculer_impot_societes',
    'calculer_bfr',
    'calculer_seuil_rentabilite',
    'calculer_capacite_autofinancement',
    'calculer_amortissement_lineaire',
    'calculer_ratios_financiers',
    'valider_donnees_financieres',
    'extraire_donnees_export',
    
    # Validation utils
    'valider_email',
    'valider_telephone',
    'nettoyer_texte',
    'valider_montant',
    'valider_pourcentage',
    'valider_donnees_entreprise',
    'valider_investissement',
    'consolider_erreurs',
    'serialiser_donnees',
    'deserialiser_donnees',
    'generer_identifiant_unique',
    'extraire_nombre_depuis_texte',
    'comparer_donnees',
    
    # Formatting utils
    'formater_devise',
    'formater_pourcentage',
    'formater_nombre',
    'formater_date',
    'formater_duree',
    'creer_tableau_markdown',
    'formater_liste_puces',
    'formater_section_business_model',
    'extraire_nom_entreprise',
    'formater_synthese_financiere',
    'nettoyer_contenu_markdown',
    'generer_resume_donnees'
]