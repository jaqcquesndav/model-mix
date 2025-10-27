"""
Pages financières de base - Version simplifiée pour préserver le workflow
"""

import streamlit as st

def page_informations_generales():
    """Page des informations générales - Version simplifiée"""
    st.title("ℹ️ Informations Générales")
    st.info("⚠️ Cette page est en cours de migration vers la nouvelle architecture.")
    
    # Interface basique pour maintenir le workflow
    if "data" not in st.session_state:
        st.session_state.data = {}
    
    if "informations_generales" not in st.session_state.data:
        st.session_state.data["informations_generales"] = {}
    
    info = st.session_state.data["informations_generales"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        info["prenom_nom"] = st.text_input("Prénom et nom", value=info.get("prenom_nom", ""))
        info["intitule_projet"] = st.text_input("Intitulé du projet", value=info.get("intitule_projet", ""))
        info["statut_juridique"] = st.selectbox("Statut juridique", 
                                               ["", "Entreprise individuelle", "SARL", "SAS", "SA"],
                                               index=0 if not info.get("statut_juridique") else 
                                               ["", "Entreprise individuelle", "SARL", "SAS", "SA"].index(info.get("statut_juridique")))
    
    with col2:
        info["telephone"] = st.text_input("Téléphone", value=info.get("telephone", ""))
        info["email"] = st.text_input("Email", value=info.get("email", ""))
        info["ville"] = st.text_input("Ville", value=info.get("ville", ""))
    
    if st.button("💾 Sauvegarder", type="primary"):
        st.success("Informations sauvegardées!")

def page_besoins_demarrage():
    """Page des besoins de démarrage - Version simplifiée"""
    st.title("💰 Besoins de Démarrage")
    st.info("⚠️ Version simplifiée - Utilisez 'Investissements & Financements' pour une version complète.")
    
    if "data" not in st.session_state:
        st.session_state.data = {}
    
    if "besoins_demarrage" not in st.session_state.data:
        st.session_state.data["besoins_demarrage"] = {}
    
    besoins = st.session_state.data["besoins_demarrage"]
    
    # Catégories principales
    st.subheader("Investissements principaux")
    
    col1, col2 = st.columns(2)
    
    with col1:
        besoins["Matériel professionnel"] = st.number_input("Matériel professionnel ($)", 
                                                          value=besoins.get("Matériel professionnel", 0.0), min_value=0.0)
        besoins["Véhicule"] = st.number_input("Véhicule ($)", 
                                            value=besoins.get("Véhicule", 0.0), min_value=0.0)
        besoins["Stock de matières et produits"] = st.number_input("Stock initial ($)", 
                                                                 value=besoins.get("Stock de matières et produits", 0.0), min_value=0.0)
    
    with col2:
        besoins["Matériel de bureau"] = st.number_input("Matériel de bureau ($)", 
                                                      value=besoins.get("Matériel de bureau", 0.0), min_value=0.0)
        besoins["Logiciels, formations"] = st.number_input("Logiciels et formations ($)", 
                                                         value=besoins.get("Logiciels, formations", 0.0), min_value=0.0)
        besoins["Trésorerie de départ"] = st.number_input("Trésorerie de départ ($)", 
                                                        value=besoins.get("Trésorerie de départ", 0.0), min_value=0.0)
    
    # Calcul du total
    total = sum(besoins.values())
    st.session_state.data["total_besoins"] = total
    
    st.metric("Total des besoins", f"{total:,.2f} $")

def page_financement():
    """Page de financement - Version simplifiée"""
    st.title("🏦 Financement")
    st.info("⚠️ Version simplifiée - Utilisez 'Investissements & Financements' pour une version complète.")
    
    if "data" not in st.session_state:
        st.session_state.data = {}
    
    if "financements" not in st.session_state.data:
        st.session_state.data["financements"] = {}
    
    fin = st.session_state.data["financements"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fin["Apport personnel ou familial"] = st.number_input("Apport personnel ($)", 
                                                            value=fin.get("Apport personnel ou familial", 0.0), min_value=0.0)
        fin["Emprunts bancaires"] = st.number_input("Emprunts bancaires ($)", 
                                                  value=fin.get("Emprunts bancaires", 0.0), min_value=0.0)
    
    with col2:
        fin["Subvention d'équipement"] = st.number_input("Subventions ($)", 
                                                       value=fin.get("Subvention d'équipement", 0.0), min_value=0.0)
        fin["Autres sources"] = st.number_input("Autres financements ($)", 
                                              value=fin.get("Autres sources", 0.0), min_value=0.0)
    
    # Calcul du total
    total = sum(fin.values())
    st.session_state.data["total_financement"] = total
    
    st.metric("Total financements", f"{total:,.2f} $")
    
    # Équilibre
    besoins = st.session_state.data.get("total_besoins", 0)
    if besoins > 0:
        if total >= besoins:
            st.success(f"✅ Financement équilibré (Excédent: {total - besoins:,.2f} $)")
        else:
            st.error(f"❌ Déficit de financement: {besoins - total:,.2f} $")

def page_charges_fixes():
    """Page des charges fixes - Version simplifiée"""
    st.title("📋 Charges Fixes")
    st.info("⚠️ Version simplifiée - Données sur 3 ans.")
    
    if "data" not in st.session_state:
        st.session_state.data = {}
    
    if "charges_fixes" not in st.session_state.data:
        st.session_state.data["charges_fixes"] = {}
    
    cf = st.session_state.data["charges_fixes"]
    
    charges_types = ["Loyer", "Électricité", "Eau", "Téléphone/Internet", "Assurances", "Autres charges"]
    
    st.subheader("Charges fixes mensuelles")
    
    for charge in charges_types:
        cf[charge] = st.number_input(f"{charge} ($/mois)", 
                                   value=cf.get(charge, 0.0), min_value=0.0, key=f"cf_{charge}")
    
    # Calcul totaux annuels
    total_mensuel = sum(cf.values())
    total_annuel = total_mensuel * 12
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total mensuel", f"{total_mensuel:,.2f} $")
    with col2:
        st.metric("Total annuel", f"{total_annuel:,.2f} $")
    
    # Stocker pour les autres calculs
    st.session_state.data["total_charges_fixes_annee1"] = total_annuel

def page_chiffre_affaires():
    """Page du chiffre d'affaires - Version simplifiée"""
    st.title("📈 Chiffre d'Affaires")
    st.info("⚠️ Version simplifiée - Prévisions sur 3 ans.")
    
    if "data" not in st.session_state:
        st.session_state.data = {}
    
    if "ca_previsions" not in st.session_state.data:
        st.session_state.data["ca_previsions"] = {}
    
    ca = st.session_state.data["ca_previsions"]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ca["ca_annee_1"] = st.number_input("CA Année 1 ($)", 
                                         value=ca.get("ca_annee_1", 0.0), min_value=0.0)
    with col2:
        ca["ca_annee_2"] = st.number_input("CA Année 2 ($)", 
                                         value=ca.get("ca_annee_2", 0.0), min_value=0.0)
    with col3:
        ca["ca_annee_3"] = st.number_input("CA Année 3 ($)", 
                                         value=ca.get("ca_annee_3", 0.0), min_value=0.0)
    
    # Calcul des évolutions
    if ca.get("ca_annee_1", 0) > 0:
        evol_2 = ((ca.get("ca_annee_2", 0) - ca["ca_annee_1"]) / ca["ca_annee_1"]) * 100
        st.write(f"Évolution Année 2: {evol_2:+.1f}%")
    
    if ca.get("ca_annee_2", 0) > 0:
        evol_3 = ((ca.get("ca_annee_3", 0) - ca["ca_annee_2"]) / ca["ca_annee_2"]) * 100
        st.write(f"Évolution Année 3: {evol_3:+.1f}%")

def page_charges_variables():
    """Page des charges variables - Version simplifiée"""
    st.title("📊 Charges Variables")
    st.info("⚠️ Version simplifiée - Taux unique.")
    
    if "data" not in st.session_state:
        st.session_state.data = {}
    
    if "charges_variables" not in st.session_state.data:
        st.session_state.data["charges_variables"] = {}
    
    cv = st.session_state.data["charges_variables"]
    
    cv["taux_charges_variables"] = st.slider("Taux de charges variables (% du CA)", 
                                            min_value=0.0, max_value=100.0, 
                                            value=cv.get("taux_charges_variables", 40.0), step=0.5)
    
    # Calcul avec le CA
    ca_data = st.session_state.data.get("ca_previsions", {})
    if ca_data.get("ca_annee_1", 0) > 0:
        ca_1 = ca_data["ca_annee_1"]
        charges_var_1 = ca_1 * cv["taux_charges_variables"] / 100
        st.metric("Charges variables Année 1", f"{charges_var_1:,.2f} $")

def page_fonds_roulement():
    """Page fonds de roulement - Version simplifiée"""
    st.title("💼 Fonds de Roulement")
    st.info("⚠️ Version simplifiée - Calcul BFR basique.")
    
    if "data" not in st.session_state:
        st.session_state.data = {}
    
    if "fonds_roulement" not in st.session_state.data:
        st.session_state.data["fonds_roulement"] = {}
    
    fr = st.session_state.data["fonds_roulement"]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fr["duree_credits_clients"] = st.number_input("Durée crédits clients (jours)", 
                                                    value=fr.get("duree_credits_clients", 30), min_value=0)
    with col2:
        fr["duree_stock"] = st.number_input("Durée de stock (jours)", 
                                          value=fr.get("duree_stock", 15), min_value=0)
    with col3:
        fr["duree_dettes_fournisseurs"] = st.number_input("Durée dettes fournisseurs (jours)", 
                                                         value=fr.get("duree_dettes_fournisseurs", 45), min_value=0)
    
    # Calcul BFR simplifié
    ca_data = st.session_state.data.get("ca_previsions", {})
    if ca_data.get("ca_annee_1", 0) > 0:
        ca_journalier = ca_data["ca_annee_1"] / 365
        
        creances = ca_journalier * fr["duree_credits_clients"]
        stock = ca_journalier * fr["duree_stock"] * 0.6  # Approximation
        dettes = ca_journalier * fr["duree_dettes_fournisseurs"] * 0.6
        
        bfr = creances + stock - dettes
        fr["bfr"] = bfr
        
        st.metric("BFR calculé", f"{bfr:,.2f} $")

def page_salaires():
    """Page salaires - Version simplifiée"""
    st.title("👥 Salaires")
    st.info("⚠️ Version simplifiée - Postes principaux.")
    
    if "data" not in st.session_state:
        st.session_state.data = {}
    
    if "salaires" not in st.session_state.data:
        st.session_state.data["salaires"] = {}
    
    salaires = st.session_state.data["salaires"]
    
    st.subheader("Salaires mensuels bruts")
    
    postes = ["Dirigeant", "Employé 1", "Employé 2"]
    
    for poste in postes:
        if poste not in salaires:
            salaires[poste] = {}
        
        col1, col2 = st.columns(2)
        with col1:
            salaires[poste]["salaire_brut"] = st.number_input(f"Salaire {poste} ($/mois)", 
                                                            value=salaires[poste].get("salaire_brut", 0.0), min_value=0.0)
        with col2:
            salaires[poste]["charges_sociales"] = st.number_input(f"Charges sociales {poste} (%)", 
                                                                value=salaires[poste].get("charges_sociales", 25.0), min_value=0.0, max_value=100.0)
    
    # Calcul total
    total_salaires = 0
    total_charges = 0
    
    for poste_data in salaires.values():
        if isinstance(poste_data, dict):
            salaire = poste_data.get("salaire_brut", 0)
            charges = salaire * poste_data.get("charges_sociales", 0) / 100
            total_salaires += salaire
            total_charges += charges
    
    total_cout = (total_salaires + total_charges) * 12
    
    st.metric("Coût salarial annuel", f"{total_cout:,.2f} $")

def page_rentabilite():
    """Page rentabilité - Version simplifiée"""
    st.title("📊 Rentabilité")
    st.info("⚠️ Analyse simplifiée basée sur les données saisies.")
    
    data = st.session_state.get("data", {})
    
    # Récupération des données
    ca_1 = data.get("ca_previsions", {}).get("ca_annee_1", 0)
    taux_cv = data.get("charges_variables", {}).get("taux_charges_variables", 0)
    charges_fixes = data.get("total_charges_fixes_annee1", 0)
    
    if ca_1 > 0:
        charges_var = ca_1 * taux_cv / 100
        marge_brute = ca_1 - charges_var
        resultat = marge_brute - charges_fixes
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Chiffre d'affaires", f"{ca_1:,.0f} $")
        with col2:
            st.metric("Marge brute", f"{marge_brute:,.0f} $", f"{(marge_brute/ca_1*100):.1f}%")
        with col3:
            st.metric("Résultat", f"{resultat:,.0f} $", f"{(resultat/ca_1*100):.1f}%")
        
        # Seuil de rentabilité
        if taux_cv < 100:
            seuil = charges_fixes / (1 - taux_cv/100)
            st.metric("Seuil de rentabilité", f"{seuil:,.0f} $")
            
            if ca_1 >= seuil:
                st.success("✅ Projet rentable dès la première année")
            else:
                st.warning(f"⚠️ Il manque {seuil - ca_1:,.0f} $ de CA pour être rentable")
    else:
        st.warning("Veuillez renseigner le chiffre d'affaires pour voir l'analyse de rentabilité")

def page_tresorerie():
    """Page trésorerie - Version simplifiée"""
    st.title("💰 Trésorerie")
    st.info("⚠️ Analyse simplifiée de la trésorerie.")
    
    data = st.session_state.get("data", {})
    
    tresorerie_depart = data.get("besoins_demarrage", {}).get("Trésorerie de départ", 0)
    bfr = data.get("fonds_roulement", {}).get("bfr", 0)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Trésorerie de départ", f"{tresorerie_depart:,.2f} $")
    with col2:
        st.metric("BFR", f"{bfr:,.2f} $")
    
    if tresorerie_depart > 0 and bfr > 0:
        tresorerie_nette = tresorerie_depart - bfr
        st.metric("Trésorerie nette disponible", f"{tresorerie_nette:,.2f} $")
        
        if tresorerie_nette > 0:
            st.success("✅ Trésorerie suffisante")
        else:
            st.error("❌ Trésorerie insuffisante")

def page_generation_business_plan():
    """Page de génération du business plan - Redirection vers la nouvelle version"""
    st.title("📄 Génération du Business Plan")
    
    st.warning("⚠️ Cette page utilise encore l'ancienne version. Pour une expérience complète avec tous les tableaux financiers intégrés, utilisez l'onglet:")
    st.info("🎯 **Business Plan Complet (Nouveau)**")
    
    st.markdown("### Fonctionnalités de la nouvelle version:")
    st.markdown("""
    - ✅ **Intégration automatique** de tous les tableaux financiers
    - ✅ **9 sections structurées** selon le canevas officiel  
    - ✅ **Analyses détaillées** de chaque élément financier
    - ✅ **Export Word/PDF** professionnel
    - ✅ **Projections 5 ans** au lieu de 3 ans
    """)
    
    if st.button("🚀 Aller vers Business Plan Complet", type="primary"):
        st.info("Cliquez sur l'onglet '🎯 Business Plan Complet (Nouveau)' ci-dessus")