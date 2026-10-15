# Veille tech’

Veille technologique quotidienne : IA, ServiceNow et ESM, cloud, cybersécurité, régulation et marché du logiciel.
Un briefing chaque matin, une synthèse chaque lundi, une synthèse chaque début de mois.

Site : https://azuyo7.github.io/veille-tech/

## Contenu du dépôt

| Chemin | Rôle |
| --- | --- |
| `index.html` | La page, autonome (aucune étape de build). |
| `data/daily-AAAA-MM.json` | Les briefings quotidiens, un fichier par mois. |
| `data/weekly.json` | Les synthèses hebdomadaires. |
| `data/monthly.json` | Les synthèses mensuelles. |
| `tools/publish.py` | Ajoute ou remplace un rapport dans ces fichiers. |

## Publier un rapport

Depuis la racine du dépôt, avec un rapport déjà validé par `veille_tool.py` :

```
python3 tools/publish.py rapport.json
git add data && git commit -m "Veille du AAAA-MM-JJ" && git push
```

GitHub Pages met le site à jour en une à deux minutes.

## Tester en local

La page lit ses données avec `fetch`, il faut donc la servir en HTTP plutôt que l'ouvrir en double-cliquant :

```
python3 -m http.server 8000
```

puis ouvrir http://localhost:8000.
