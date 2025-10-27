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
    """Page des besoins de démarrage - Version complète selon l'original"""
    st.title("💰 Besoins de Démarrage")
    st.markdown("### Formulaire complet des besoins d'investissement")
    
    if "data" not in st.session_state:
        st.session_state.data = {}
    
    if "besoins_demarrage" not in st.session_state.data:
        st.session_state.data["besoins_demarrage"] = {}
    
    besoins = st.session_state.data["besoins_demarrage"]
    
    # Liste complète des 17 champs selon l'original
    besoins_items = [
        "Frais d'établissement",
        "Frais d'ouverture de compteurs", 
        "Logiciels, formations",
        "Dépôt de marque",
        "Droits d'entrée",
        "Achat fonds de commerce ou parts",
        "Droit au bail",
        "Enseigne et éléments de communication",
        "Véhicule", 
        "Matériel professionnel",
        "Matériel autre",
        "Matériel de bureau",
        "Stock de matières et produits",
        "Caution ou dépôt de garantie",
        "Frais de dossier",
        "Frais de notaire",
        "Trésorerie de départ"
    ]
    
    # Durée d'amortissement
    st.subheader("Configuration des amortissements")
    duree_amortissement = st.number_input(
        "Durée d'amortissement des investissements (en années) :",
        min_value=1,
        max_value=10,
        value=besoins.get("duree_amortissement", 3)
    )
    besoins["duree_amortissement"] = duree_amortissement
    st.session_state.data["duree_amortissement"] = duree_amortissement
    
    # Saisie des investissements en deux colonnes
    st.subheader("Détail des investissements")
    
    col1, col2 = st.columns(2)
    
    # Répartition des champs en deux colonnes
    items_col1 = besoins_items[:9]  # 9 premiers champs
    items_col2 = besoins_items[9:]  # 8 derniers champs
    
    with col1:
        for item in items_col1:
            besoins[item] = st.number_input(
                f"{item} ($)", 
                value=besoins.get(item, 0.0), 
                min_value=0.0,
                key=f"besoin_{item}"
            )
    
    with col2:
        for item in items_col2:
            besoins[item] = st.number_input(
                f"{item} ($)", 
                value=besoins.get(item, 0.0), 
                min_value=0.0,
                key=f"besoin_{item}"
            )
    
    # Calculs des totaux par catégorie
    st.write("---")
    st.subheader("Récapitulatif des investissements")
    
    # Immobilisations incorporelles
    incorporels = [
        "Frais d'établissement", "Logiciels, formations", "Droits d'entrée", 
        "Frais de dossier", "Frais de notaire"
    ]
    total_incorporels = sum(besoins.get(item, 0.0) for item in incorporels)
    
    # Immobilisations corporelles
    corporels = [
        "Enseigne et éléments de communication", "Véhicule", 
        "Matériel professionnel", "Matériel autre", "Matériel de bureau"
    ]
    total_corporels = sum(besoins.get(item, 0.0) for item in corporels)
    
    # Autres investissements
    autres = [
        "Frais d'ouverture de compteurs", "Dépôt de marque", 
        "Achat fonds de commerce ou parts", "Droit au bail",
        "Stock de matières et produits", "Caution ou dépôt de garantie", 
        "Trésorerie de départ"
    ]
    total_autres = sum(besoins.get(item, 0.0) for item in autres)
    
    # Affichage des totaux
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Immobilisations incorporelles", f"{total_incorporels:,.2f} $")
    with col2:
        st.metric("Immobilisations corporelles", f"{total_corporels:,.2f} $")
    with col3:
        st.metric("Autres investissements", f"{total_autres:,.2f} $")
    
    # Total général
    total_general = total_incorporels + total_corporels + total_autres
    st.session_state.data["total_besoins"] = total_general
    
    st.write("---")
    st.metric("**TOTAL GÉNÉRAL DES BESOINS**", f"{total_general:,.2f} $")
    
    # Sauvegarde des données
    st.session_state.data["besoins_demarrage"] = besoins

def calculer_pret_interet_fixe(montant, taux_annuel, duree_mois):
    """
    Calcule les détails d'un prêt avec intérêts fixes par mois.
    
    Args:
        montant (float): Montant du prêt.
        taux_annuel (float): Taux annuel en pourcentage.
        duree_mois (int): Durée du prêt en mois.
    
    Returns:
        dict: Détails du prêt.
    """
    if montant <= 0 or taux_annuel < 0:
        return {
            "mensualite": 0.0,
            "principal_mensuel": 0.0,
            "interet_mensuel": 0.0,
            "total_a_rembourser": 0.0,
            "interets_totaux": 0.0,
            "interets_annee1": 0.0,
            "interets_annee2": 0.0,
            "interets_annee3": 0.0
        }
    
    if duree_mois <= 0:
        return {
            "mensualite": 0.0,
            "principal_mensuel": 0.0,
            "interet_mensuel": 0.0,
            "total_a_rembourser": 0.0,
            "interets_totaux": 0.0,
            "interets_annee1": 0.0,
            "interets_annee2": 0.0,
            "interets_annee3": 0.0
        }
    
    taux_mensuel = taux_annuel / 100 / 12
    
    if taux_mensuel == 0:
        mensualite = montant / duree_mois
        interet_mensuel = 0.0
    else:
        mensualite = (taux_mensuel * montant) / (1 - (1 + taux_mensuel) ** (-duree_mois))
        interet_mensuel = montant * taux_mensuel
    
    principal_mensuel = montant / duree_mois
    
    total_a_rembourser = mensualite * duree_mois
    
    interets_totaux = interet_mensuel * duree_mois
    
    # Intérêts par année, limités à 12 mois maximum
    interets_annee1 = interet_mensuel * min(duree_mois, 12)
    interets_annee2 = interet_mensuel * min(max(duree_mois - 12, 0), 12)
    interets_annee3 = interet_mensuel * min(max(duree_mois - 24, 0), 12)
    
    return {
        "mensualite": mensualite,
        "principal_mensuel": principal_mensuel,
        "interet_mensuel": interet_mensuel,
        "total_a_rembourser": total_a_rembourser,
        "interets_totaux": interets_totaux,
        "interets_annee1": interets_annee1,
        "interets_annee2": interets_annee2,
        "interets_annee3": interets_annee3
    }

def page_financement():
    """Page de financement - Version complète selon l'original"""
    st.title("🏦 Financement")
    st.markdown("### Structure complète de financement")
    
    if "data" not in st.session_state:
        st.session_state.data = {}
    
    if "financements" not in st.session_state.data:
        st.session_state.data["financements"] = {}
    
    fin = st.session_state.data["financements"]
    
    # Section 1: Apports personnels
    st.subheader("💰 Apports personnels")
    col1, col2 = st.columns(2)
    
    with col1:
        fin["Apport personnel ou familial"] = st.number_input(
            "Apport personnel ou familial ($)", 
            value=fin.get("Apport personnel ou familial", 0.0), 
            min_value=0.0
        )
    
    with col2:
        fin["Apports en nature (en valeur)"] = st.number_input(
            "Apports en nature (en valeur) ($)", 
            value=fin.get("Apports en nature (en valeur)", 0.0), 
            min_value=0.0
        )
    
    # Section 2: Emprunts (3 prêts possibles)
    st.write("---")
    st.subheader("🏦 Emprunts bancaires")
    
    total_emprunts = 0.0
    total_interets_annee1 = 0.0
    total_interets_annee2 = 0.0
    total_interets_annee3 = 0.0
    
    for i in range(1, 4):  # Prêt 1, 2, 3
        pret_name = f"Prêt {i}"
        
        st.markdown(f"**{pret_name}**")
        col1, col2, col3 = st.columns(3)
        
        # Initialiser la structure du prêt si elle n'existe pas
        if pret_name not in fin:
            fin[pret_name] = {"montant": 0.0, "taux": 0.0, "duree": 0}
        
        with col1:
            fin[pret_name]["montant"] = st.number_input(
                f"Montant du {pret_name} ($)",
                value=fin[pret_name].get("montant", 0.0),
                min_value=0.0,
                key=f"montant_pret_{i}"
            )
        
        with col2:
            fin[pret_name]["taux"] = st.number_input(
                f"Taux du {pret_name} (%)",
                value=fin[pret_name].get("taux", 0.0),
                min_value=0.0,
                max_value=50.0,
                key=f"taux_pret_{i}"
            )
        
        with col3:
            fin[pret_name]["duree"] = st.number_input(
                f"Durée du {pret_name} (en mois)",
                value=fin[pret_name].get("duree", 0),
                min_value=0,
                max_value=300,
                key=f"duree_pret_{i}"
            )
        
        # Calculs du prêt
        if fin[pret_name]["montant"] > 0:
            pret_info = calculer_pret_interet_fixe(
                fin[pret_name]["montant"],
                fin[pret_name]["taux"],
                fin[pret_name]["duree"]
            )
            
            total_emprunts += fin[pret_name]["montant"]
            total_interets_annee1 += pret_info["interets_annee1"]
            total_interets_annee2 += pret_info["interets_annee2"]
            total_interets_annee3 += pret_info["interets_annee3"]
            
            # Affichage des détails du prêt
            with st.expander(f"Détails du {pret_name}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Mensualité : {pret_info['mensualite']:.2f} $")
                    st.write(f"Principal mensuel : {pret_info['principal_mensuel']:.2f} $")
                    st.write(f"Intérêt mensuel : {pret_info['interet_mensuel']:.2f} $")
                
                with col2:
                    st.write(f"Total à rembourser : {pret_info['total_a_rembourser']:.2f} $")
                    st.write(f"Intérêts totaux : {pret_info['interets_totaux']:.2f} $")
                
                st.write("**Intérêts par année :**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"Année 1 : {pret_info['interets_annee1']:.2f} $")
                with col2:
                    st.write(f"Année 2 : {pret_info['interets_annee2']:.2f} $")
                with col3:
                    st.write(f"Année 3 : {pret_info['interets_annee3']:.2f} $")
    
    # Section 3: Subventions
    st.write("---")
    st.subheader("🎁 Subventions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Initialiser la structure de subvention si elle n'existe pas
        if "Subvention 1" not in fin:
            fin["Subvention 1"] = {"montant": 0.0}
        
        fin["Subvention 1"]["montant"] = st.number_input(
            "Subvention 1 ($)",
            value=fin["Subvention 1"].get("montant", 0.0),
            min_value=0.0
        )
    
    with col2:
        # Initialiser la structure de subvention si elle n'existe pas
        if "Subvention 2" not in fin:
            fin["Subvention 2"] = {"montant": 0.0}
        
        fin["Subvention 2"]["montant"] = st.number_input(
            "Subvention 2 ($)",
            value=fin["Subvention 2"].get("montant", 0.0),
            min_value=0.0
        )
    
    # Section 4: Autre financement
    st.write("---")
    st.subheader("💼 Autre financement")
    
    fin["Autre financement"] = st.number_input(
        "Autre financement ($)",
        value=fin.get("Autre financement", 0.0),
        min_value=0.0
    )
    
    # Calculs des totaux
    st.write("---")
    st.subheader("📊 Récapitulatif du financement")
    
    total_apports = fin.get("Apport personnel ou familial", 0.0) + fin.get("Apports en nature (en valeur)", 0.0)
    total_subventions = fin["Subvention 1"].get("montant", 0.0) + fin["Subvention 2"].get("montant", 0.0)
    total_autres = fin.get("Autre financement", 0.0)
    total_financement = total_apports + total_emprunts + total_subventions + total_autres
    
    # Stockage des totaux pour utilisation dans d'autres pages
    fin["total_apports"] = total_apports
    fin["total_emprunts"] = total_emprunts
    fin["total_subventions"] = total_subventions
    fin["total_autres"] = total_autres
    fin["total_financement"] = total_financement
    fin["total_interets_annee1"] = total_interets_annee1
    fin["total_interets_annee2"] = total_interets_annee2
    fin["total_interets_annee3"] = total_interets_annee3
    
    # Affichage des totaux
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Apports personnels", f"{total_apports:,.2f} $")
    with col2:
        st.metric("Emprunts", f"{total_emprunts:,.2f} $")
    with col3:
        st.metric("Subventions", f"{total_subventions:,.2f} $")
    with col4:
        st.metric("Autres", f"{total_autres:,.2f} $")
    
    st.write("---")
    st.metric("**TOTAL FINANCEMENT**", f"{total_financement:,.2f} $")
    
    # Comparaison avec les besoins
    total_besoins = st.session_state.data.get("total_besoins", 0.0)
    if total_besoins > 0:
        ecart = total_financement - total_besoins
        if ecart >= 0:
            st.success(f"✅ Financement suffisant : Excédent de {ecart:,.2f} $")
        else:
            st.error(f"❌ Financement insuffisant : Déficit de {abs(ecart):,.2f} $")
    
    # Sauvegarde des données
    st.session_state.data["financements"] = fin

def page_charges_fixes():
    """Page des charges fixes - Version complète avec autofill intelligent sur 5 ans"""
    st.title("📋 Charges Fixes sur 5 Années")
    st.markdown("### Système d'autofill intelligent - Modifiez année 1 pour auto-remplir années 2 à 5")
    
    if "data" not in st.session_state:
        st.session_state.data = {}
    
    data = st.session_state.data
    
    # Liste complète des 15 charges fixes selon l'original
    charges_fixes_predefinies = [
        "Assurances véhicule et RC pro", "Téléphone, internet", "Autres abonnements",
        "Carburant", "Frais de déplacement / hébergement", "Eau, électricité, gaz",
        "Mutuelle", "Fournitures diverses", "Entretien Moto livraison et matériel",
        "Nettoyage des locaux", "Budget publicité et communication", "Emplacements",
        "Expert comptable, avocats", "Frais bancaires et terminal carte bleue", "Taxes, CFE"
    ]
    
    # Initialisation des charges fixes si non présentes
    if "charges_fixes" not in data:
        data["charges_fixes"] = {"annee1": {}, "annee2": {}, "annee3": {}, "annee4": {}, "annee5": {}}
        for charge in charges_fixes_predefinies:
            for annee in ["annee1", "annee2", "annee3", "annee4", "annee5"]:
                data["charges_fixes"][annee][charge] = 0.0
    
    charges_fixes_dict = data["charges_fixes"]
    
    # Fonctions d'autofill intelligent
    def update_year1(charge):
        """Met à jour années 2 à 5 quand année 1 change"""
        year1_key = f"charge_{charge}_annee1"
        year1_val = st.session_state.get(year1_key, 0.0)
        
        # Auto-remplir années 2 à 5 avec la valeur de l'année 1
        for i, annee in enumerate(["annee2", "annee3", "annee4", "annee5"], 2):
            year_key = f"charge_{charge}_annee{i}"
            if not st.session_state.get(f"updated_{year_key}", False):
                st.session_state[year_key] = year1_val
                charges_fixes_dict[annee][charge] = year1_val
    
    def update_year2(charge):
        """Met à jour années 3 à 5 quand année 2 change"""
        year2_key = f"charge_{charge}_annee2"
        year2_val = st.session_state.get(year2_key, 0.0)
        st.session_state[f"updated_{year2_key}"] = True
        
        for i, annee in enumerate(["annee3", "annee4", "annee5"], 3):
            year_key = f"charge_{charge}_annee{i}"
            if not st.session_state.get(f"updated_{year_key}", False):
                st.session_state[year_key] = year2_val
                charges_fixes_dict[annee][charge] = year2_val
    
    def update_year3(charge):
        """Met à jour années 4 et 5 quand année 3 change"""
        year3_key = f"charge_{charge}_annee3"
        year3_val = st.session_state.get(year3_key, 0.0)
        st.session_state[f"updated_{year3_key}"] = True
        
        for i, annee in enumerate(["annee4", "annee5"], 4):
            year_key = f"charge_{charge}_annee{i}"
            if not st.session_state.get(f"updated_{year_key}", False):
                st.session_state[year_key] = year3_val
                charges_fixes_dict[annee][charge] = year3_val
    
    def update_year4(charge):
        """Met à jour année 5 quand année 4 change"""
        year4_key = f"charge_{charge}_annee4"
        year4_val = st.session_state.get(year4_key, 0.0)
        st.session_state[f"updated_{year4_key}"] = True
        
        year5_key = f"charge_{charge}_annee5"
        if not st.session_state.get(f"updated_{year5_key}", False):
            st.session_state[year5_key] = year4_val
            charges_fixes_dict["annee5"][charge] = year4_val
    
    def update_year5(charge):
        """Marque l'année 5 comme modifiée manuellement"""
        year5_key = f"charge_{charge}_annee5"
        st.session_state[f"updated_{year5_key}"] = True
    
    # Interface pour les charges fixes prédéfinies
    st.subheader("💼 Charges Fixes Prédéfinies")
    st.info("💡 **Autofill intelligent** : Modifiez l'année 1 pour auto-remplir les années suivantes")
    
    # Affichage en format tableau avec 5 colonnes
    for charge in charges_fixes_predefinies:
        st.markdown(f"**{charge}**")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # S'assurer que la charge existe dans toutes les années
        for annee in ["annee1", "annee2", "annee3", "annee4", "annee5"]:
            if charge not in charges_fixes_dict[annee]:
                charges_fixes_dict[annee][charge] = 0.0
        
        with col1:
            year1_key = f"charge_{charge}_annee1"
            if year1_key not in st.session_state:
                st.session_state[year1_key] = charges_fixes_dict["annee1"].get(charge, 0.0)
            montant1 = st.number_input(
                f"Année 1 ($)",
                min_value=0.0,
                key=year1_key,
                on_change=update_year1,
                args=(charge,),
                value=st.session_state[year1_key]
            )
            charges_fixes_dict["annee1"][charge] = montant1
        
        with col2:
            year2_key = f"charge_{charge}_annee2"
            if year2_key not in st.session_state:
                st.session_state[year2_key] = charges_fixes_dict["annee2"].get(charge, 0.0)
            montant2 = st.number_input(
                f"Année 2 ($)",
                min_value=0.0,
                key=year2_key,
                on_change=update_year2,
                args=(charge,),
                value=st.session_state[year2_key]
            )
            charges_fixes_dict["annee2"][charge] = montant2
        
        with col3:
            year3_key = f"charge_{charge}_annee3"
            if year3_key not in st.session_state:
                st.session_state[year3_key] = charges_fixes_dict["annee3"].get(charge, 0.0)
            montant3 = st.number_input(
                f"Année 3 ($)",
                min_value=0.0,
                key=year3_key,
                on_change=update_year3,
                args=(charge,),
                value=st.session_state[year3_key]
            )
            charges_fixes_dict["annee3"][charge] = montant3
        
        with col4:
            year4_key = f"charge_{charge}_annee4"
            if year4_key not in st.session_state:
                st.session_state[year4_key] = charges_fixes_dict["annee4"].get(charge, 0.0)
            montant4 = st.number_input(
                f"Année 4 ($)",
                min_value=0.0,
                key=year4_key,
                on_change=update_year4,
                args=(charge,),
                value=st.session_state[year4_key]
            )
            charges_fixes_dict["annee4"][charge] = montant4
        
        with col5:
            year5_key = f"charge_{charge}_annee5"
            if year5_key not in st.session_state:
                st.session_state[year5_key] = charges_fixes_dict["annee5"].get(charge, 0.0)
            montant5 = st.number_input(
                f"Année 5 ($)",
                min_value=0.0,
                key=year5_key,
                on_change=update_year5,
                args=(charge,),
                value=st.session_state[year5_key]
            )
            charges_fixes_dict["annee5"][charge] = montant5
    
    # Section charges fixes personnalisées
    st.subheader("➕ Charges Fixes Personnalisées")
    st.info("Ajoutez vos propres charges fixes non listées ci-dessus")
    
    # Initialiser les charges personnalisées si nécessaire
    if "charges_personnalisees" not in data:
        data["charges_personnalisees"] = []
    
    # Interface pour ajouter une nouvelle charge personnalisée
    with st.expander("🆕 Ajouter une nouvelle charge fixe"):
        col_nom, col_add = st.columns([3, 1])
        with col_nom:
            nouvelle_charge = st.text_input("Nom de la nouvelle charge fixe")
        with col_add:
            st.write("")  # Espacement
            if st.button("Ajouter"):
                if nouvelle_charge and nouvelle_charge not in data["charges_personnalisees"]:
                    data["charges_personnalisees"].append(nouvelle_charge)
                    # Initialiser les valeurs pour toutes les années
                    for annee in ["annee1", "annee2", "annee3", "annee4", "annee5"]:
                        charges_fixes_dict[annee][nouvelle_charge] = 0.0
                    st.success(f"Charge '{nouvelle_charge}' ajoutée !")
                    st.rerun()
                elif nouvelle_charge in data["charges_personnalisees"]:
                    st.warning("Cette charge existe déjà")
    
    # Afficher les charges personnalisées existantes
    if data["charges_personnalisees"]:
        st.markdown("**Charges personnalisées :**")
        for i, charge in enumerate(data["charges_personnalisees"]):
            col_charge, col_delete = st.columns([10, 1])
            
            with col_charge:
                st.markdown(f"**{charge}**")
                col1, col2, col3, col4, col5 = st.columns(5)
                
                # S'assurer que la charge existe dans toutes les années
                for annee in ["annee1", "annee2", "annee3", "annee4", "annee5"]:
                    if charge not in charges_fixes_dict[annee]:
                        charges_fixes_dict[annee][charge] = 0.0
                
                with col1:
                    year1_key = f"charge_perso_{charge}_annee1"
                    if year1_key not in st.session_state:
                        st.session_state[year1_key] = charges_fixes_dict["annee1"].get(charge, 0.0)
                    montant1 = st.number_input(
                        f"Année 1 ($)",
                        min_value=0.0,
                        key=year1_key,
                        on_change=update_year1,
                        args=(charge,),
                        value=st.session_state[year1_key]
                    )
                    charges_fixes_dict["annee1"][charge] = montant1
                
                with col2:
                    year2_key = f"charge_perso_{charge}_annee2"
                    if year2_key not in st.session_state:
                        st.session_state[year2_key] = charges_fixes_dict["annee2"].get(charge, 0.0)
                    montant2 = st.number_input(
                        f"Année 2 ($)",
                        min_value=0.0,
                        key=year2_key,
                        on_change=update_year2,
                        args=(charge,),
                        value=st.session_state[year2_key]
                    )
                    charges_fixes_dict["annee2"][charge] = montant2
                
                with col3:
                    year3_key = f"charge_perso_{charge}_annee3"
                    if year3_key not in st.session_state:
                        st.session_state[year3_key] = charges_fixes_dict["annee3"].get(charge, 0.0)
                    montant3 = st.number_input(
                        f"Année 3 ($)",
                        min_value=0.0,
                        key=year3_key,
                        on_change=update_year3,
                        args=(charge,),
                        value=st.session_state[year3_key]
                    )
                    charges_fixes_dict["annee3"][charge] = montant3
                
                with col4:
                    year4_key = f"charge_perso_{charge}_annee4"
                    if year4_key not in st.session_state:
                        st.session_state[year4_key] = charges_fixes_dict["annee4"].get(charge, 0.0)
                    montant4 = st.number_input(
                        f"Année 4 ($)",
                        min_value=0.0,
                        key=year4_key,
                        on_change=update_year4,
                        args=(charge,),
                        value=st.session_state[year4_key]
                    )
                    charges_fixes_dict["annee4"][charge] = montant4
                
                with col5:
                    year5_key = f"charge_perso_{charge}_annee5"
                    if year5_key not in st.session_state:
                        st.session_state[year5_key] = charges_fixes_dict["annee5"].get(charge, 0.0)
                    montant5 = st.number_input(
                        f"Année 5 ($)",
                        min_value=0.0,
                        key=year5_key,
                        on_change=update_year5,
                        args=(charge,),
                        value=st.session_state[year5_key]
                    )
                    charges_fixes_dict["annee5"][charge] = montant5
            
            with col_delete:
                st.write("")  # Espacement
                if st.button("🗑️", key=f"delete_charge_{i}", help="Supprimer cette charge"):
                    # Supprimer la charge des listes et des données
                    data["charges_personnalisees"].remove(charge)
                    for annee in ["annee1", "annee2", "annee3", "annee4", "annee5"]:
                        if charge in charges_fixes_dict[annee]:
                            del charges_fixes_dict[annee][charge]
                    st.success(f"Charge '{charge}' supprimée !")
                    st.rerun()
    
    # Calculs et résumé
    st.subheader("📊 Résumé des Charges Fixes")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    totaux_annuels = {}
    
    for i, (annee, col) in enumerate(zip(["annee1", "annee2", "annee3", "annee4", "annee5"], [col1, col2, col3, col4, col5]), 1):
        total = sum(charges_fixes_dict[annee].values())
        totaux_annuels[annee] = total
        
        with col:
            st.metric(f"Année {i}", f"{total:,.0f} $")
    
    # Évolution et moyennes
    st.subheader("📈 Analyse d'Évolution")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        moyenne_5_ans = sum(totaux_annuels.values()) / 5
        st.metric("Moyenne 5 ans", f"{moyenne_5_ans:,.0f} $")
    
    with col2:
        if totaux_annuels["annee1"] > 0:
            croissance = ((totaux_annuels["annee5"] / totaux_annuels["annee1"]) - 1) * 100
            st.metric("Croissance totale", f"{croissance:+.1f}%")
        else:
            st.metric("Croissance totale", "N/A")
    
    with col3:
        max_annee = max(totaux_annuels.values())
        st.metric("Pic maximal", f"{max_annee:,.0f} $")
    
    # Sauvegarder les totaux pour les autres calculs
    for i, annee in enumerate(["annee1", "annee2", "annee3", "annee4", "annee5"], 1):
        data[f"total_charges_fixes_annee{i}"] = totaux_annuels[annee]

def page_chiffre_affaires():
    """Page de chiffre d'affaires - Version complète avec autofill mensuel"""
    st.title("📈 Chiffre d'Affaires Prévisionnel")
    st.markdown("### Saisie mensuelle avec autofill intelligent sur 12 mois")
    
    if "data" not in st.session_state:
        st.session_state.data = {}
    
    data = st.session_state.data
    
    # Type de vente depuis les informations générales
    type_vente = data.get("informations_generales", {}).get("type_vente", "Marchandises")
    
    if "chiffre_affaires" not in data:
        data["chiffre_affaires"] = {}
    
    chiffre_affaires_dict = data["chiffre_affaires"]
    
    # Sélection du type de vente
    st.subheader("🎯 Configuration du type d'activité")
    type_vente = st.selectbox(
        "Type de vente",
        ["Marchandises", "Services", "Mixte"],
        index=["Marchandises", "Services", "Mixte"].index(type_vente) if type_vente in ["Marchandises", "Services", "Mixte"] else 0
    )
    
    # Sauvegarder le type de vente
    if "informations_generales" not in data:
        data["informations_generales"] = {}
    data["informations_generales"]["type_vente"] = type_vente
    
    mois = [f"Mois {i}" for i in range(1, 13)]
    
    # Fonctions de mise à jour avec autofill intelligent
    def update_jours_travailles(nom_vente):
        """Auto-remplit les jours travaillés des mois 2-12 avec la valeur du mois 1"""
        key_jours_mois1 = f"{nom_vente}_Mois 1_jours"
        new_val = st.session_state.get(key_jours_mois1, 0)
        for mois_nom in mois[1:]:
            key = f"{nom_vente}_{mois_nom}_jours"
            if not st.session_state.get(f"updated_{key}", False):
                st.session_state[key] = new_val
                chiffre_affaires_dict[key] = new_val

    def update_ca_moyen_jour(nom_vente):
        """Auto-remplit le CA moyen/jour des mois 2-12 avec la valeur du mois 1"""
        key_ca_mois1 = f"{nom_vente}_Mois 1_ca_moyen"
        new_val = st.session_state.get(key_ca_mois1, 0.0)
        for mois_nom in mois[1:]:
            key = f"{nom_vente}_{mois_nom}_ca_moyen"
            if not st.session_state.get(f"updated_{key}", False):
                st.session_state[key] = new_val
                chiffre_affaires_dict[key] = new_val

    def mark_updated(key):
        """Marque un champ comme modifié manuellement"""
        st.session_state[f"updated_{key}"] = True

    def calcul_chiffre_affaires(nom_vente):
        """Calcule le chiffre d'affaires pour un type de vente donné"""
        data_ca = []
        
        st.subheader(f"📊 {nom_vente} - Répartition mensuelle Année 1")
        st.info("💡 Saisissez les données du Mois 1, les autres mois se rempliront automatiquement. Modifiez individuellement si nécessaire.")
        
        # En-têtes du tableau
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        with col1:
            st.write("**Mois**")
        with col2:
            st.write("**Jours travaillés**")
        with col3:
            st.write("**CA moyen/jour ($)**")
        with col4:
            st.write("**CA mensuel ($)**")
        
        st.write("---")
        
        for mois_nom in mois:
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
            
            key_jours = f"{nom_vente}_{mois_nom}_jours"
            key_ca_moyen = f"{nom_vente}_{mois_nom}_ca_moyen"
            key_ca = f"{nom_vente}_{mois_nom}_ca"
            
            with col1:
                st.write(f"**{mois_nom}**")
            
            with col2:
                if mois_nom == "Mois 1":
                    # Mois 1 : déclenche l'autofill
                    montant_jours = st.number_input(
                        f"Jours {mois_nom}",
                        min_value=0,
                        key=key_jours,
                        value=chiffre_affaires_dict.get(key_jours, 0),
                        on_change=update_jours_travailles,
                        args=(nom_vente,),
                        label_visibility="collapsed"
                    )
                else:
                    # Mois 2-12 : peut être modifié individuellement
                    montant_jours = st.number_input(
                        f"Jours {mois_nom}",
                        min_value=0,
                        key=key_jours,
                        value=chiffre_affaires_dict.get(key_jours, 0),
                        on_change=lambda key=key_jours: mark_updated(key),
                        label_visibility="collapsed"
                    )
                chiffre_affaires_dict[key_jours] = montant_jours
            
            with col3:
                if mois_nom == "Mois 1":
                    # Mois 1 : déclenche l'autofill
                    montant_ca_moyen = st.number_input(
                        f"CA moyen {mois_nom}",
                        min_value=0.0,
                        key=key_ca_moyen,
                        value=chiffre_affaires_dict.get(key_ca_moyen, 0.0),
                        on_change=update_ca_moyen_jour,
                        args=(nom_vente,),
                        label_visibility="collapsed"
                    )
                else:
                    # Mois 2-12 : peut être modifié individuellement
                    montant_ca_moyen = st.number_input(
                        f"CA moyen {mois_nom}",
                        min_value=0.0,
                        key=key_ca_moyen,
                        value=chiffre_affaires_dict.get(key_ca_moyen, 0.0),
                        on_change=lambda key=key_ca_moyen: mark_updated(key),
                        label_visibility="collapsed"
                    )
                chiffre_affaires_dict[key_ca_moyen] = montant_ca_moyen
            
            # Calcul automatique du CA mensuel
            ca_mensuel = montant_jours * montant_ca_moyen
            chiffre_affaires_dict[key_ca] = ca_mensuel
            
            with col4:
                st.metric("", f"{ca_mensuel:,.2f}")
            
            data_ca.append({
                "mois": mois_nom,
                "jours_travailles": montant_jours,
                "ca_moyen_jour": montant_ca_moyen,
                "ca_mensuel": ca_mensuel
            })
        
        # Calcul du total année 1
        total_ca_annee1 = sum(item["ca_mensuel"] for item in data_ca)
        chiffre_affaires_dict[f"total_ca_{nom_vente}_annee1"] = total_ca_annee1
        
        st.write("---")
        st.metric(f"**Total Chiffre d'Affaires Année 1 ({nom_vente})**", f"{total_ca_annee1:,.2f} $")
        
        # Pourcentages d'augmentation pour les années 2 et 3
        st.subheader(f"📈 Projections Années 2 à 5 - {nom_vente}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            key_aug_annee2 = f"{nom_vente}_augmentation_annee2"
            pourcentage_augmentation_annee2 = st.number_input(
                f"Augmentation CA Année 1 → 2 (%) - {nom_vente}",
                min_value=-50.0,
                max_value=500.0,
                value=chiffre_affaires_dict.get(key_aug_annee2, 10.0),
                key=key_aug_annee2
            )
            chiffre_affaires_dict[key_aug_annee2] = pourcentage_augmentation_annee2
        
        with col2:
            key_aug_annee3 = f"{nom_vente}_augmentation_annee3"
            pourcentage_augmentation_annee3 = st.number_input(
                f"Augmentation CA Année 2 → 3 (%) - {nom_vente}",
                min_value=-50.0,
                max_value=500.0,
                value=chiffre_affaires_dict.get(key_aug_annee3, 10.0),
                key=key_aug_annee3
            )
            chiffre_affaires_dict[key_aug_annee3] = pourcentage_augmentation_annee3
        
        with col3:
            key_aug_annee4 = f"{nom_vente}_augmentation_annee4"
            pourcentage_augmentation_annee4 = st.number_input(
                f"Augmentation CA Année 3 → 4 (%) - {nom_vente}",
                min_value=-50.0,
                max_value=500.0,
                value=chiffre_affaires_dict.get(key_aug_annee4, 10.0),
                key=key_aug_annee4
            )
            chiffre_affaires_dict[key_aug_annee4] = pourcentage_augmentation_annee4
        
        with col4:
            key_aug_annee5 = f"{nom_vente}_augmentation_annee5"
            pourcentage_augmentation_annee5 = st.number_input(
                f"Augmentation CA Année 4 → 5 (%) - {nom_vente}",
                min_value=-50.0,
                max_value=500.0,
                value=chiffre_affaires_dict.get(key_aug_annee5, 10.0),
                key=key_aug_annee5
            )
            chiffre_affaires_dict[key_aug_annee5] = pourcentage_augmentation_annee5
        
        # Calculs des années 2 à 5
        total_ca_annee2 = total_ca_annee1 * (1 + pourcentage_augmentation_annee2 / 100)
        total_ca_annee3 = total_ca_annee2 * (1 + pourcentage_augmentation_annee3 / 100)
        total_ca_annee4 = total_ca_annee3 * (1 + pourcentage_augmentation_annee4 / 100)
        total_ca_annee5 = total_ca_annee4 * (1 + pourcentage_augmentation_annee5 / 100)
        
        chiffre_affaires_dict[f"total_ca_{nom_vente}_annee2"] = total_ca_annee2
        chiffre_affaires_dict[f"total_ca_{nom_vente}_annee3"] = total_ca_annee3
        chiffre_affaires_dict[f"total_ca_{nom_vente}_annee4"] = total_ca_annee4
        chiffre_affaires_dict[f"total_ca_{nom_vente}_annee5"] = total_ca_annee5
        
        # Affichage des projections
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(f"CA Année 2 ({nom_vente})", f"{total_ca_annee2:,.2f} $")
        with col2:
            st.metric(f"CA Année 3 ({nom_vente})", f"{total_ca_annee3:,.2f} $")
        with col3:
            st.metric(f"CA Année 4 ({nom_vente})", f"{total_ca_annee4:,.2f} $")
        with col4:
            st.metric(f"CA Année 5 ({nom_vente})", f"{total_ca_annee5:,.2f} $")
        
        return total_ca_annee1, total_ca_annee2, total_ca_annee3, total_ca_annee4, total_ca_annee5
    
    # Interface selon le type de vente sélectionné
    totaux_marchandises = [0, 0, 0, 0, 0]
    totaux_services = [0, 0, 0, 0, 0]
    
    if type_vente in ["Marchandises", "Mixte"]:
        totaux_marchandises = calcul_chiffre_affaires("Marchandises")
        st.write("---")
    
    if type_vente in ["Services", "Mixte"]:
        totaux_services = calcul_chiffre_affaires("Services")
        st.write("---")
    
    # Calcul des totaux généraux
    total_ca_annee1 = totaux_marchandises[0] + totaux_services[0]
    total_ca_annee2 = totaux_marchandises[1] + totaux_services[1]
    total_ca_annee3 = totaux_marchandises[2] + totaux_services[2]
    total_ca_annee4 = totaux_marchandises[3] + totaux_services[3]
    total_ca_annee5 = totaux_marchandises[4] + totaux_services[4]
    
    # Sauvegarde des totaux généraux
    data["total_chiffre_affaires_annee1"] = total_ca_annee1
    data["total_chiffre_affaires_annee2"] = total_ca_annee2
    data["total_chiffre_affaires_annee3"] = total_ca_annee3
    data["total_chiffre_affaires_annee4"] = total_ca_annee4
    data["total_chiffre_affaires_annee5"] = total_ca_annee5
    
    # Affichage du récapitulatif final
    if type_vente == "Mixte":
        st.subheader("🎯 Récapitulatif Global")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total CA Année 1", f"{total_ca_annee1:,.2f} $")
        with col2:
            st.metric("Total CA Année 2", f"{total_ca_annee2:,.2f} $")
        with col3:
            st.metric("Total CA Année 3", f"{total_ca_annee3:,.2f} $")
        with col4:
            st.metric("Total CA Année 4", f"{total_ca_annee4:,.2f} $")
        with col5:
            st.metric("Total CA Année 5", f"{total_ca_annee5:,.2f} $")
        
        # Répartition Marchandises vs Services
        if total_ca_annee1 > 0:
            pct_marchandises = (totaux_marchandises[0] / total_ca_annee1) * 100
            pct_services = (totaux_services[0] / total_ca_annee1) * 100
            
            st.write("**Répartition Année 1 :**")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"🛍️ Marchandises : {pct_marchandises:.1f}%")
            with col2:
                st.write(f"🔧 Services : {pct_services:.1f}%")
    
    # Sauvegarde des données
    st.session_state.data = data

def page_chiffre_affaires():
    """Page de chiffre d'affaires - Version complète avec autofill mensuel"""
    st.title("📈 Chiffre d'Affaires Prévisionnel")
    st.markdown("### Saisie mensuelle avec autofill intelligent - 12 mois détaillés")
    
    if "data" not in st.session_state:
        st.session_state.data = {}
    
    data = st.session_state.data
    
    # Configuration du type d'activité
    if "informations_generales" not in data:
        data["informations_generales"] = {}
    
    type_vente = st.selectbox(
        "Type d'activité :",
        ["Marchandises", "Services", "Mixte"],
        index=0 if not data["informations_generales"].get("type_vente") else 
        ["Marchandises", "Services", "Mixte"].index(data["informations_generales"].get("type_vente", "Marchandises"))
    )
    data["informations_generales"]["type_vente"] = type_vente
    
    if "chiffre_affaires" not in data:
        data["chiffre_affaires"] = {}
    
    chiffre_affaires_dict = data["chiffre_affaires"]
    
    # Liste des mois
    mois = [f"Mois {i}" for i in range(1, 13)]
    
    # Fonctions de mise à jour avec autofill intelligent
    def update_jours_travailles(nom_vente):
        """Auto-remplit les jours travaillés pour les mois 2-12 avec la valeur du mois 1"""
        key_jours_mois1 = f"{nom_vente}_Mois 1_jours"
        new_val = st.session_state.get(key_jours_mois1, 0)
        for mois_nom in mois[1:]:
            key = f"{nom_vente}_{mois_nom}_jours"
            if not st.session_state.get(f"updated_{key}", False):
                st.session_state[key] = new_val
                chiffre_affaires_dict[key] = new_val

    def update_ca_moyen_jour(nom_vente):
        """Auto-remplit le CA moyen/jour pour les mois 2-12 avec la valeur du mois 1"""
        key_ca_mois1 = f"{nom_vente}_Mois 1_ca_moyen"
        new_val = st.session_state.get(key_ca_mois1, 0.0)
        for mois_nom in mois[1:]:
            key = f"{nom_vente}_{mois_nom}_ca_moyen"
            if not st.session_state.get(f"updated_{key}", False):
                st.session_state[key] = new_val
                chiffre_affaires_dict[key] = new_val

    def mark_updated(key):
        """Marque un champ comme modifié manuellement"""
        st.session_state[f"updated_{key}"] = True

    def calcul_chiffre_affaires(nom_vente):
        """Interface de calcul du CA pour un type de vente donné"""
        st.subheader(f"💼 Année 1 - {nom_vente}")
        st.info("💡 Saisissez le Mois 1, les autres mois se rempliront automatiquement. Modifiez-les individuellement si nécessaire.")
        
        data_ca = []
        
        # Saisie mensuelle
        for i, mois_nom in enumerate(mois):
            col1, col2, col3 = st.columns(3)
            
            key_jours = f"{nom_vente}_{mois_nom}_jours"
            key_ca_moyen = f"{nom_vente}_{mois_nom}_ca_moyen"
            key_ca = f"{nom_vente}_{mois_nom}_ca"
            
            with col1:
                if mois_nom == "Mois 1":
                    # Premier mois : déclenche l'autofill
                    montant_jours = st.number_input(
                        f"{mois_nom} - Jours travaillés",
                        min_value=0,
                        max_value=31,
                        key=key_jours,
                        value=chiffre_affaires_dict.get(key_jours, 0),
                        on_change=update_jours_travailles,
                        args=(nom_vente,),
                        help="Nombre de jours d'activité dans le mois"
                    )
                else:
                    # Autres mois : peuvent être modifiés individuellement
                    montant_jours = st.number_input(
                        f"{mois_nom} - Jours travaillés",
                        min_value=0,
                        max_value=31,
                        key=key_jours,
                        value=chiffre_affaires_dict.get(key_jours, 0),
                        on_change=lambda key=key_jours: mark_updated(key),
                        help="Modifiable individuellement"
                    )
                chiffre_affaires_dict[key_jours] = montant_jours
            
            with col2:
                if mois_nom == "Mois 1":
                    # Premier mois : déclenche l'autofill
                    montant_ca_moyen = st.number_input(
                        f"{mois_nom} - CA moyen/jour ($)",
                        min_value=0.0,
                        key=key_ca_moyen,
                        value=chiffre_affaires_dict.get(key_ca_moyen, 0.0),
                        on_change=update_ca_moyen_jour,
                        args=(nom_vente,),
                        help="Chiffre d'affaires moyen par jour d'activité"
                    )
                else:
                    # Autres mois : peuvent être modifiés individuellement
                    montant_ca_moyen = st.number_input(
                        f"{mois_nom} - CA moyen/jour ($)",
                        min_value=0.0,
                        key=key_ca_moyen,
                        value=chiffre_affaires_dict.get(key_ca_moyen, 0.0),
                        on_change=lambda key=key_ca_moyen: mark_updated(key),
                        help="Modifiable individuellement"
                    )
                chiffre_affaires_dict[key_ca_moyen] = montant_ca_moyen
            
            # Calcul automatique du CA mensuel
            ca_mensuel = montant_jours * montant_ca_moyen
            chiffre_affaires_dict[key_ca] = ca_mensuel
            
            with col3:
                st.metric(f"CA {mois_nom}", f"{ca_mensuel:,.2f} $")
            
            # Collecte des données pour le tableau récapitulatif
            data_ca.append({
                "mois": mois_nom,
                "jours_travailles": montant_jours,
                "ca_moyen_jour": montant_ca_moyen,
                "ca_mensuel": ca_mensuel
            })
        
        # Calcul du total année 1
        total_ca_annee1 = sum(row["ca_mensuel"] for row in data_ca)
        chiffre_affaires_dict[f"total_ca_{nom_vente}_annee1"] = total_ca_annee1
        
        st.write("---")
        st.metric(f"**Total Chiffre d'Affaires Année 1 ({nom_vente})**", f"{total_ca_annee1:,.2f} $")
        
        # Projections années 2 à 5
        st.subheader(f"📊 Projections Années 2 à 5 - {nom_vente}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            key_aug_annee2 = f"{nom_vente}_augmentation_annee2"
            pourcentage_augmentation_annee2 = st.number_input(
                f"Augmentation Année 1 → 2 (%) - {nom_vente}",
                min_value=-50.0,
                max_value=200.0,
                value=chiffre_affaires_dict.get(key_aug_annee2, 10.0),
                key=key_aug_annee2,
                help="Pourcentage d'évolution du CA entre l'année 1 et 2"
            )
            chiffre_affaires_dict[key_aug_annee2] = pourcentage_augmentation_annee2
        
        with col2:
            key_aug_annee3 = f"{nom_vente}_augmentation_annee3"
            pourcentage_augmentation_annee3 = st.number_input(
                f"Augmentation Année 2 → 3 (%) - {nom_vente}",
                min_value=-50.0,
                max_value=200.0,
                value=chiffre_affaires_dict.get(key_aug_annee3, 15.0),
                key=key_aug_annee3,
                help="Pourcentage d'évolution du CA entre l'année 2 et 3"
            )
            chiffre_affaires_dict[key_aug_annee3] = pourcentage_augmentation_annee3
        
        with col3:
            key_aug_annee4 = f"{nom_vente}_augmentation_annee4"
            pourcentage_augmentation_annee4 = st.number_input(
                f"Augmentation Année 3 → 4 (%) - {nom_vente}",
                min_value=-50.0,
                max_value=200.0,
                value=chiffre_affaires_dict.get(key_aug_annee4, 15.0),
                key=key_aug_annee4,
                help="Pourcentage d'évolution du CA entre l'année 3 et 4"
            )
            chiffre_affaires_dict[key_aug_annee4] = pourcentage_augmentation_annee4
        
        with col4:
            key_aug_annee5 = f"{nom_vente}_augmentation_annee5"
            pourcentage_augmentation_annee5 = st.number_input(
                f"Augmentation Année 4 → 5 (%) - {nom_vente}",
                min_value=-50.0,
                max_value=200.0,
                value=chiffre_affaires_dict.get(key_aug_annee5, 15.0),
                key=key_aug_annee5,
                help="Pourcentage d'évolution du CA entre l'année 4 et 5"
            )
            chiffre_affaires_dict[key_aug_annee5] = pourcentage_augmentation_annee5
        
        # Calculs des totaux années 2 à 5
        total_ca_annee2 = total_ca_annee1 * (1 + pourcentage_augmentation_annee2 / 100)
        total_ca_annee3 = total_ca_annee2 * (1 + pourcentage_augmentation_annee3 / 100)
        total_ca_annee4 = total_ca_annee3 * (1 + pourcentage_augmentation_annee4 / 100)
        total_ca_annee5 = total_ca_annee4 * (1 + pourcentage_augmentation_annee5 / 100)
        
        chiffre_affaires_dict[f"total_ca_{nom_vente}_annee2"] = total_ca_annee2
        chiffre_affaires_dict[f"total_ca_{nom_vente}_annee3"] = total_ca_annee3
        chiffre_affaires_dict[f"total_ca_{nom_vente}_annee4"] = total_ca_annee4
        chiffre_affaires_dict[f"total_ca_{nom_vente}_annee5"] = total_ca_annee5
        
        # Affichage des projections
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(f"Total CA Année 2 ({nom_vente})", f"{total_ca_annee2:,.2f} $")
        with col2:
            st.metric(f"Total CA Année 3 ({nom_vente})", f"{total_ca_annee3:,.2f} $")
        with col3:
            st.metric(f"Total CA Année 4 ({nom_vente})", f"{total_ca_annee4:,.2f} $")
        with col4:
            st.metric(f"Total CA Année 5 ({nom_vente})", f"{total_ca_annee5:,.2f} $")
        
        return total_ca_annee1, total_ca_annee2, total_ca_annee3, total_ca_annee4, total_ca_annee5
    
    # Interface selon le type d'activité
    total_marchandises = [0, 0, 0, 0, 0]
    total_services = [0, 0, 0, 0, 0]
    
    if type_vente in ["Marchandises", "Mixte"]:
        total_marchandises = calcul_chiffre_affaires("Marchandises")
    
    if type_vente in ["Services", "Mixte"]:
        total_services = calcul_chiffre_affaires("Services")
    
    # Calcul des totaux généraux
    st.write("---")
    st.subheader("🎯 Récapitulatif Global du Chiffre d'Affaires")
    
    total_ca_annee1 = total_marchandises[0] + total_services[0]
    total_ca_annee2 = total_marchandises[1] + total_services[1]
    total_ca_annee3 = total_marchandises[2] + total_services[2]
    total_ca_annee4 = total_marchandises[3] + total_services[3]
    total_ca_annee5 = total_marchandises[4] + total_services[4]
    
    # Stockage des totaux généraux
    data["total_chiffre_affaires_annee1"] = total_ca_annee1
    data["total_chiffre_affaires_annee2"] = total_ca_annee2
    data["total_chiffre_affaires_annee3"] = total_ca_annee3
    data["total_chiffre_affaires_annee4"] = total_ca_annee4
    data["total_chiffre_affaires_annee5"] = total_ca_annee5
    
    # Affichage des totaux
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total CA Année 1", f"{total_ca_annee1:,.2f} $")
    with col2:
        st.metric("Total CA Année 2", f"{total_ca_annee2:,.2f} $")
    with col3:
        st.metric("Total CA Année 3", f"{total_ca_annee3:,.2f} $")
    with col4:
        st.metric("Total CA Année 4", f"{total_ca_annee4:,.2f} $")
    with col5:
        st.metric("Total CA Année 5", f"{total_ca_annee5:,.2f} $")
    
    # Évolution du CA
    if total_ca_annee1 > 0:
        evolution_2 = ((total_ca_annee2 - total_ca_annee1) / total_ca_annee1) * 100
        evolution_3 = ((total_ca_annee3 - total_ca_annee2) / total_ca_annee2) * 100 if total_ca_annee2 > 0 else 0
        evolution_4 = ((total_ca_annee4 - total_ca_annee3) / total_ca_annee3) * 100 if total_ca_annee3 > 0 else 0
        evolution_5 = ((total_ca_annee5 - total_ca_annee4) / total_ca_annee4) * 100 if total_ca_annee4 > 0 else 0
        
        st.write("**Évolution du Chiffre d'Affaires :**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(f"📈 Année 1 → 2 : {evolution_2:+.1f}%")
        with col2:
            st.write(f"📈 Année 2 → 3 : {evolution_3:+.1f}%")
        with col3:
            st.write(f"📈 Année 3 → 4 : {evolution_4:+.1f}%")
        with col4:
            st.write(f"📈 Année 4 → 5 : {evolution_5:+.1f}%")
    
    # Analyse de répartition (pour type Mixte)
    if type_vente == "Mixte" and total_ca_annee1 > 0:
        st.write("**Répartition par type d'activité (Année 1) :**")
        col1, col2 = st.columns(2)
        
        pct_marchandises = (total_marchandises[0] / total_ca_annee1) * 100
        pct_services = (total_services[0] / total_ca_annee1) * 100
        
        with col1:
            st.write(f"🛍️ Marchandises : {pct_marchandises:.1f}% ({total_marchandises[0]:,.2f} $)")
        with col2:
            st.write(f"🔧 Services : {pct_services:.1f}% ({total_services[0]:,.2f} $)")
    
    # Sauvegarde des données
    st.session_state.data = data

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

