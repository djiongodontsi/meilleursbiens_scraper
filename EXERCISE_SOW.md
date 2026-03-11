# Cahier des charges : Scraper d'agents immobiliers

## 1. Objectif du projet

Ce document décrit les exigences du script Python de web scraping que vous êtes chargé de développer. L'objectif est d'extraire les informations de profil de tous les agents du réseau **MeilleursBiens** et de produire un fichier CSV propre et structuré.

---

## 2. Périmètre des travaux

Le script doit exécuter automatiquement le workflow suivant :

**Étape 1 — Scraping de l'annuaire :** Parcourir l'annuaire principal ([https://meilleursbiens.com/agents](https://meilleursbiens.com/agents)) et extraire les URLs des profils individuels de chaque agent listé, en gérant correctement la pagination ou le chargement dynamique.

**Étape 2 — Scraping des profils :** Pour chaque URL de profil individuel (ex. [https://meilleursbiens.com/site/65-nadira-zemani](https://meilleursbiens.com/site/65-nadira-zemani)), extraire les données requises. Vous pouvez utiliser le parsing HTML ou une API interne si elle est exposée dans le trafic réseau.

---

## 3. Données à extraire

Le CSV de sortie doit contenir exactement les colonnes suivantes, dans cet ordre :

| Colonne             | Description                                                |
| ------------------- | ---------------------------------------------------------- |
| `first_name`        | Prénom de l'agent                                          |
| `last_name`         | Nom de l'agent                                             |
| `postal_code`       | Code postal de la zone de l'agent                          |
| `city`              | Ville de l'agent                                           |
| `phone_number`      | Numéro de téléphone                                        |
| `email`             | Adresse e-mail                                             |
| `nb_mandates`       | Nombre de biens actifs en vente/location                   |
| `avg_mandate_price` | Prix moyen des biens actifs                                |
| `nb_sales`          | Nombre de biens vendus/loués                               |
| `linkedin_url`      | URL du profil LinkedIn (si disponible, sinon laisser vide) |

### Exemple de sortie attendue

Pour le profil [https://meilleursbiens.com/site/65-nadira-zemani](https://meilleursbiens.com/site/65-nadira-zemani), la ligne CSV doit être formatée ainsi :

```
Nadira,Zemani,77181,COURTRY,+33682445937,nzemani@meilleursbiens.com,20,259925,31,https://www.linkedin.com/in/nadira-zemani-552387b8/
```

---

## 4. Livrables et spécifications techniques

- **Livrable :** UN seul fichier Python (`.py`) contenant le script complet.
- **Sortie :** Le script doit générer et sauvegarder automatiquement le fichier `.csv` à l'exécution.
- **Robustesse :** Le code doit inclure une gestion d'erreurs solide :
  - Si une information est manquante pour un agent (ex. URL LinkedIn), le champ doit être laissé vide et l'exécution doit continuer sans planter.
  - Si un agent n'a aucun mandat actif ou aucun bien vendu (*"Vendu"*), mettre `0`.
- **Exemple de référence :** Voir le fichier `example_LFimmo_scraper.py` dans ce dossier — c'est un scraper fonctionnel développé pour un réseau immobilier similaire (`lfimmo.fr`). Vous pouvez vous en inspirer pour la structure, le style de code et l'approche technique.

---

## 5. Notes

- Le nombre total d'agents est d'environ **386 agents**.
- Respectez le serveur : ajoutez des délais entre les requêtes.
- Le script doit gérer les erreurs réseau avec des tentatives de réessai.
