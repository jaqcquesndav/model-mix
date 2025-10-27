# 🎯 MixBPM - Business Model & Plan Generator

## 🌟 Nouvelle Version Refactorisée !

Cette application a été entièrement refactorisée avec une architecture modulaire et un système de templates multi-organisations. Elle permet de générer des business models et business plans adaptés au contexte de la République Démocratique du Congo.

## 🚀 Démarrage Rapide

### Installation

```bash
# Cloner le projet
git clone [url-du-repo]
cd model-mix

# Installer les dépendances
pip install -r requirements.txt

# Lancer la nouvelle version refactorisée
streamlit run main.py

# Ou lancer l'ancienne version (pour comparaison)
streamlit run mixbpm.py
```

### Test de l'Installation

```bash
# Tester que tous les modules fonctionnent
python test_architecture.py
```

## 🎯 Templates Disponibles

### 🌾 COPA TRANSFORMÉ (Par défaut)
- **Focus :** Transformation agricole et entrepreneuriat rural
- **Secteurs :** Agroalimentaire, Agriculture, Élevage, Pêche, Artisanat, Services ruraux
- **Contexte :** Programme de développement économique axé sur les chaînes de valeur agricoles

### 🌿 VIRUNGA  
- **Focus :** Conservation environnementale et développement durable
- **Secteurs :** Écotourisme, Agriculture durable, Énergies renouvelables, Produits forestiers durables
- **Contexte :** Écosystème de conservation dans la région des Virunga

### 👩‍💼 IP FEMME
- **Focus :** Autonomisation économique des femmes
- **Secteurs :** Artisanat, Commerce, Services de proximité, Beauté, Technologies
- **Contexte :** Initiative pour la promotion de l'entrepreneuriat féminin

## 📋 Processus Guidé

### 1. Configuration Initiale
- Sélectionnez votre template d'organisation dans la sidebar
- Renseignez le nom de votre entreprise
- Choisissez votre secteur d'activité (adapté au template)
- Précisez votre localisation

### 2. Collecte des Données Business
- **Persona PME :** Informations sur votre entreprise, équipe, objectifs
- **Analyse Marché :** Taille du marché, clients cibles, contexte local
- **Concurrence :** Analyse des concurrents directs et indirects  
- **Facteurs Limitants :** Contraintes et défis spécifiques

### 3. Génération Business Model
- **Automatique Complète :** IA génère un business model complet
- **Par Sections :** Génération section par section (9 blocs du canvas)
- **Amélioration Existant :** Optimisation d'un modèle existant

### 4. Données Financières
- Informations générales et besoins de démarrage
- Financement, charges fixes et variables
- Projections de chiffre d'affaires
- Calculs de rentabilité et trésorerie

### 5. Génération Business Plan
- Génération automatique de toutes les sections
- Export Word et PDF
- Intégration des tableaux financiers
- Analyses spécifiques au contexte RDC

## 🏗️ Architecture Technique

```
├── main.py                    # Application principale refactorisée
├── templates/                 # Templates d'organisations
├── services/                  # Logique métier
│   ├── ai/                   # Services d'IA  
│   ├── business/             # Gestion données business
│   ├── financial/            # Calculs financiers
│   └── document/             # Génération documents
├── utils/                     # Fonctions utilitaires
├── ui/                        # Interface utilisateur
│   ├── components.py         # Composants réutilisables
│   └── pages/                # Pages de l'application
└── mixbpm.py                 # Version originale (transition)
```

## ✨ Nouvelles Fonctionnalités

### 🎨 Interface Améliorée
- Sidebar avec configuration centralisée
- Sélection de templates en temps réel
- Indicateurs de progression
- Validation des données en temps réel

### 🤖 IA Contextuelle
- Instructions système adaptées par template
- Génération de contenu spécialisé par organisation
- Suggestions intelligentes contextuelles
- Analyse des risques spécifiques

### 💰 Contexte RDC
- Tous les montants en USD pour stabilité
- Spécificités économiques congolaises
- Secteurs adaptés au contexte local
- Analyses des défis infrastructurels

### 📄 Export Enrichi
- Documents Word avec tableaux formatés
- PDF avec mise en page professionnelle
- Export Excel des données financières
- Synthèses et analyses automatiques

## 🔧 Développement

### Structure Modulaire
- **Separation of Concerns :** Chaque module a une responsabilité claire
- **Extensibilité :** Ajout facile de nouveaux templates
- **Testabilité :** Modules indépendants et testables
- **Maintenabilité :** Code organisé et documenté

### Ajouter un Nouveau Template

1. Créer le fichier `templates/mon_template.py`
2. Définir les constantes (METAPROMPT, SECTEURS, ORGANISATION_TYPE)
3. Ajouter au gestionnaire dans `templates/template_manager.py`
4. Tester avec le script `test_architecture.py`

### Contribuer

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/ma-feature`)
3. Respecter l'architecture modulaire
4. Ajouter des tests
5. Documenter les changements
6. Créer une Pull Request

## 📊 Comparaison Versions

| Aspect | Version Originale | Version Refactorisée |
|--------|------------------|---------------------|
| **Architecture** | Monolithique (8954 lignes) | Modulaire (multiple fichiers) |
| **Templates** | COPA TRANSFORMÉ uniquement | 3 templates (COPA, Virunga, IP Femme) |
| **Maintenance** | Difficile | Facile |
| **Extensibilité** | Limitée | Élevée |
| **Tests** | Aucun | Tests automatisés |
| **Documentation** | Minimale | Complète |

## 🐛 Résolution de Problèmes

### Problèmes d'Import
```bash
# Si erreur d'import de modules
python test_architecture.py

# Vérifier les dépendances
pip install -r requirements.txt
```

### Problèmes LangChain
Les avertissements LangChain sont normaux et n'affectent pas le fonctionnement.

### Données Non Sauvegardées
- Vérifiez que vous cliquez sur "Sauvegarder" dans chaque section
- Les données sont stockées dans le session state de Streamlit
- Rafraîchissement = perte des données non sauvegardées

### Performance
- L'IA peut prendre quelques minutes pour générer le contenu
- Vérifiez votre connexion internet
- Assurez-vous que la clé API OpenAI est configurée

## 📞 Support

- **Documentation :** Consultez `ARCHITECTURE.md` pour les détails techniques
- **Tests :** Utilisez `python test_architecture.py` pour diagnostiquer
- **Issues :** Reportez les bugs via les issues GitHub
- **Questions :** Consultez d'abord la documentation existante

## 🔮 Roadmap

### v2.1 (Prochaine Version)
- [ ] Migration complète des pages financières
- [ ] Tests unitaires complets
- [ ] Documentation interactive

### v2.2 (Future)
- [ ] API REST
- [ ] Multi-langue (FR/EN/LN)
- [ ] Système de plugins
- [ ] Collaboration en temps réel

### v3.0 (Vision)
- [ ] Déploiement cloud
- [ ] Mobile-responsive
- [ ] Intelligence artificielle avancée
- [ ] Intégrations externes

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- COPA TRANSFORMÉ pour le template de base
- Communauté Virunga pour les spécifications environnementales  
- Initiative IP Femme pour l'entrepreneuriat féminin
- Développeurs et contributeurs du projet