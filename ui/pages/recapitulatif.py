"""
Page de récapitulatif complet des données financières
"""

import streamlit as st
from typing import Dict, Any

def page_recapitulatif():
    """Page affichant un récapitulatif complet de toutes les données saisies"""
    st.title("Récapitulatif Complet des Données")
    
    data = st.session_state.get("data", {})
    
    # 1. Informations Générales
    st.subheader("1. Informations Générales")
    info = data.get("informations_generales", {})
    if info:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Prénom, nom :** {info.get('prenom_nom', 'Non renseigné')}")
            st.write(f"**Intitulé du projet :** {info.get('intitule_projet', 'Non renseigné')}")
            st.write(f"**Statut juridique :** {info.get('statut_juridique', 'Non renseigné')}")
        with col2:
            st.write(f"**Téléphone :** {info.get('telephone', 'Non renseigné')}")
            st.write(f"**Email :** {info.get('email', 'Non renseigné')}")
            st.write(f"**Ville :** {info.get('ville', 'Non renseigné')}")
            st.write(f"**Type de vente :** {info.get('type_vente', 'Non renseigné')}")
    else:
        st.info("Aucune information générale renseignée")
    
    # 2. Besoins de Démarrage
    st.subheader("2. Besoins de Démarrage")
    besoins = data.get("besoins_demarrage", {})
    total_besoins = data.get("total_besoins", 0.0)
    
    if besoins:
        for besoin, montant in besoins.items():
            if montant > 0:
                st.write(f"• {besoin} : {montant:,.2f} $")
        st.markdown(f"**💰 Total des Besoins de Démarrage : {total_besoins:,.2f} $**")
    else:
        st.info("Aucun besoin de démarrage renseigné")
    
    # 3. Financements
    st.subheader("3. Financements")
    financements_dict = data.get("financements", {})
    total_financement = data.get("total_financement", 0.0)
    
    if financements_dict:
        for financement, details in financements_dict.items():
            if isinstance(details, dict):
                montant = details.get("montant", 0.0)
                if montant > 0:
                    st.write(f"• {details.get('nom', financement)} : {montant:,.2f} $")
            else:
                montant = details
                if montant > 0:
                    st.write(f"• {financement} : {montant:,.2f} $")
        st.markdown(f"**💰 Total des Financements : {total_financement:,.2f} $**")
        
        # Équilibre financier
        if total_financement >= total_besoins:
            st.success(f"✅ Équilibre financier atteint (Excédent: {total_financement - total_besoins:,.2f} $)")
        else:
            st.error(f"❌ Déficit de financement : {total_besoins - total_financement:,.2f} $")
    else:
        st.info("Aucun financement renseigné")
    
    # 4. Charges Fixes sur 5 Années
    st.subheader("4. Charges Fixes Prévisionnelles")
    charges_fixes_dict = data.get("charges_fixes", {})
    
    if charges_fixes_dict:
        # Créer un tableau récapitulatif
        col1, col2, col3, col4, col5 = st.columns(5)
        headers = ["Année 1", "Année 2", "Année 3", "Année 4", "Année 5"]
        
        with col1:
            st.write("**Année 1**")
        with col2:
            st.write("**Année 2**")
        with col3:
            st.write("**Année 3**")
        with col4:
            st.write("**Année 4**")
        with col5:
            st.write("**Année 5**")
        
        # Totaux par année
        totaux = []
        for annee in range(1, 6):
            key = f"annee{annee}"
            total = data.get(f"total_charges_fixes_annee{annee}", 0.0)
            totaux.append(total)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        for i, (col, total) in enumerate(zip([col1, col2, col3, col4, col5], totaux)):
            with col:
                st.write(f"{total:,.0f} $")
    else:
        st.info("Aucune charge fixe renseignée")
    
    # 5. Chiffre d'Affaires Prévisionnel
    st.subheader("5. Chiffre d'Affaires Prévisionnel")
    ca_data = data.get("ca_previsions", {})
    
    if ca_data:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        ca_values = [
            ca_data.get("ca_annee_1", 0.0),
            ca_data.get("ca_annee_2", 0.0),
            ca_data.get("ca_annee_3", 0.0),
            ca_data.get("ca_annee_4", 0.0),
            ca_data.get("ca_annee_5", 0.0)
        ]
        
        with col1:
            st.metric("Année 1", f"{ca_values[0]:,.0f} $")
        with col2:
            st.metric("Année 2", f"{ca_values[1]:,.0f} $", 
                     delta=f"{ca_values[1] - ca_values[0]:,.0f}" if ca_values[0] > 0 else None)
        with col3:
            st.metric("Année 3", f"{ca_values[2]:,.0f} $", 
                     delta=f"{ca_values[2] - ca_values[1]:,.0f}" if ca_values[1] > 0 else None)
        with col4:
            st.metric("Année 4", f"{ca_values[3]:,.0f} $", 
                     delta=f"{ca_values[3] - ca_values[2]:,.0f}" if ca_values[2] > 0 else None)
        with col5:
            st.metric("Année 5", f"{ca_values[4]:,.0f} $", 
                     delta=f"{ca_values[4] - ca_values[3]:,.0f}" if ca_values[3] > 0 else None)
    else:
        st.info("Aucun chiffre d'affaires renseigné")
    
    # 6. Charges Variables
    st.subheader("6. Charges Variables")
    charges_var = data.get("charges_variables", {})
    if charges_var:
        taux = charges_var.get("taux_charges_variables", 0.0)
        st.write(f"**Taux de charges variables :** {taux:.1f}% du CA")
        
        # Calcul des charges variables par année
        if ca_data:
            st.write("**Charges variables prévisionnelles :**")
            col1, col2, col3, col4, col5 = st.columns(5)
            for i, (col, ca) in enumerate(zip([col1, col2, col3, col4, col5], ca_values)):
                charges_var_montant = ca * taux / 100
                with col:
                    st.write(f"Année {i+1}: {charges_var_montant:,.0f} $")
    else:
        st.info("Aucune charge variable renseignée")
    
    # 7. Fonds de Roulement
    st.subheader("7. Fonds de Roulement")
    fonds_roulement = data.get("fonds_roulement", {})
    if fonds_roulement:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Durée crédits clients :** {fonds_roulement.get('duree_credits_clients', 0)} jours")
            st.write(f"**Durée stock :** {fonds_roulement.get('duree_stock', 0)} jours")
        with col2:
            st.write(f"**Durée dettes fournisseurs :** {fonds_roulement.get('duree_dettes_fournisseurs', 0)} jours")
            bfr = fonds_roulement.get('bfr', 0.0)
            st.write(f"**BFR calculé :** {bfr:,.2f} $")
    else:
        st.info("Aucune donnée de fonds de roulement")
    
    # 8. Salaires et Rémunération
    st.subheader("8. Salaires et Charges Sociales")
    salaires = data.get("salaires", {})
    if salaires:
        # Affichage par poste et par année
        for poste, details in salaires.items():
            if isinstance(details, dict) and details.get('salaire_brut', 0) > 0:
                st.write(f"**{poste}:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"Salaire brut: {details.get('salaire_brut', 0):,.0f} $/mois")
                with col2:
                    st.write(f"Charges sociales: {details.get('charges_sociales', 0):.1f}%")
                with col3:
                    cout_total = details.get('salaire_brut', 0) * (1 + details.get('charges_sociales', 0)/100) * 12
                    st.write(f"Coût annuel: {cout_total:,.0f} $")
    else:
        st.info("Aucun salaire renseigné")
    
    # 9. Indicateurs de Rentabilité
    st.subheader("9. Indicateurs de Rentabilité")
    
    # Calculs de base si données disponibles
    if ca_data and charges_var:
        # Marge brute
        ca_annee1 = ca_values[0]
        charges_var_annee1 = ca_annee1 * charges_var.get("taux_charges_variables", 0) / 100
        marge_brute = ca_annee1 - charges_var_annee1
        taux_marge = (marge_brute / ca_annee1 * 100) if ca_annee1 > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Marge brute Année 1", f"{marge_brute:,.0f} $")
        with col2:
            st.metric("Taux de marge", f"{taux_marge:.1f}%")
        with col3:
            # Estimation point mort (simplifié)
            charges_fixes_annee1 = totaux[0] if totaux else 0
            if taux_marge > 0:
                point_mort = charges_fixes_annee1 / (taux_marge / 100)
                st.metric("Point mort estimé", f"{point_mort:,.0f} $")
    else:
        st.info("Données insuffisantes pour calculer la rentabilité")
    
    # 10. Actions recommandées
    st.subheader("10. Recommandations")
    
    recommandations = []
    
    # Vérifications automatiques
    if total_financement < total_besoins:
        recommandations.append("🔴 Augmenter les financements ou réduire les besoins de démarrage")
    
    if not ca_data or sum(ca_values) == 0:
        recommandations.append("🟡 Compléter les prévisions de chiffre d'affaires")
    
    if not charges_var:
        recommandations.append("🟡 Définir le taux de charges variables")
    
    if not salaires:
        recommandations.append("🟡 Préciser les coûts salariaux")
    
    if recommandations:
        for rec in recommandations:
            st.write(rec)
    else:
        st.success("✅ Toutes les données principales sont renseignées")
    
    # Bouton d'export
    st.divider()
    if st.button("📄 Générer le rapport complet", type="primary"):
        st.info("Fonctionnalité d'export en cours de développement")

def afficher_tableau_recapitulatif_financier(data: Dict[str, Any]):
    """Affiche un tableau récapitulatif des données financières principales"""
    
    st.subheader("📊 Tableau de Bord Financier")
    
    # Extraction des données principales
    ca_data = data.get("ca_previsions", {})
    charges_var = data.get("charges_variables", {})
    
    if ca_data:
        # Créer DataFrame pour affichage
        import pandas as pd
        
        annees = ["Année 1", "Année 2", "Année 3", "Année 4", "Année 5"]
        ca_values = [
            ca_data.get("ca_annee_1", 0),
            ca_data.get("ca_annee_2", 0),
            ca_data.get("ca_annee_3", 0),
            ca_data.get("ca_annee_4", 0),
            ca_data.get("ca_annee_5", 0)
        ]
        
        # Calcul charges variables
        taux_cv = charges_var.get("taux_charges_variables", 0) / 100
        charges_var_values = [ca * taux_cv for ca in ca_values]
        
        # Marge brute
        marge_brute_values = [ca - cv for ca, cv in zip(ca_values, charges_var_values)]
        
        # Charges fixes (si disponibles)
        charges_fixes_values = []
        for i in range(1, 6):
            cf = data.get(f"total_charges_fixes_annee{i}", 0)
            charges_fixes_values.append(cf)
        
        # Résultat d'exploitation
        resultat_values = [mb - cf for mb, cf in zip(marge_brute_values, charges_fixes_values)]
        
        # Créer le DataFrame
        df_recap = pd.DataFrame({
            "Indicateur": [
                "Chiffre d'affaires",
                "Charges variables",
                "Marge brute",
                "Charges fixes",
                "Résultat d'exploitation"
            ],
            **{annee: [ca, cv, mb, cf, res] for annee, ca, cv, mb, cf, res in 
               zip(annees, ca_values, charges_var_values, marge_brute_values, 
                   charges_fixes_values, resultat_values)}
        })
        
        # Formater en milliers
        for col in annees:
            df_recap[col] = df_recap[col].apply(lambda x: f"{x:,.0f}")
        
        st.dataframe(df_recap, width='stretch')