# Scanner de ports TCP minimal

## Description

Scanner de ports TCP simple et éducatif pour débutants en cybersécurité.
Utilise des connexions socket standard avec threading pour améliorer les performances.

## Pré-requis

- Python 3.8 ou supérieur
- Aucune dépendance externe (utilise uniquement la bibliothèque standard)

## Installation

1. Téléchargez le fichier `scanner.py`
2. Rendez-le exécutable: `chmod +x scanner.py`
3. C'est tout ! Aucune installation supplémentaire nécessaire.

## Utilisation

### Usage de base
```bash
python3 scanner.py --target TARGET [options]
```

### Arguments
- `-t, --target` : Adresse IP ou nom d'hôte à scanner (OBLIGATOIRE)
- `-s, --start` : Port de début (défaut: 1)
- `-e, --end` : Port de fin (défaut: 1024)
- `--timeout` : Timeout par connexion en secondes (défaut: 1.0)
- `--workers` : Nombre de threads (défaut: 50)

### Exemples
```bash
python3 scanner.py -t 127.0.0.1
python3 scanner.py -t example.com -s 20 -e 25
python3 scanner.py -t 192.168.1.1 -s 1 -e 1024 --timeout 0.5 --workers 20
```

## ⚠️ Avertissement légal important

**ATTENTION: Ce scanner ne doit être utilisé QUE sur des machines que vous possédez ou pour lesquelles vous avez une autorisation écrite explicite.**

**Toute utilisation non autorisée est ILLÉGALE et relève de la responsabilité de l'utilisateur.**

**L'utilisation de cet outil sur des systèmes sans permission peut constituer une violation de la loi sur la cybersécurité.**

## 🛡️ Sécurité

Pour signaler une vulnérabilité de sécurité, consultez notre [Politique de sécurité](SECURITY.md).

## Comment ça fonctionne

1. **Résolution DNS** : Le nom d'hôte est converti en adresse IP
2. **Connexion TCP** : Pour chaque port, tentative de connexion socket
3. **Timeout** : Si pas de réponse dans le délai, le port est considéré fermé
4. **Threading** : Plusieurs ports sont scannés en parallèle pour la rapidité
5. **Résultat** : Affichage des ports ouverts et statistiques

## Technique utilisée

- Socket TCP standard (`socket.connect_ex`)
- Timeout configurable pour éviter les blocages
- Threading avec `ThreadPoolExecutor` pour la concurrence
- Gestion d'erreurs robuste (DNS, réseau, etc.)

## Exécution des tests

Pour exécuter les tests unitaires:

```bash
pip install pytest
pytest -q
```

Les tests créent un serveur local temporaire pour vérifier le bon fonctionnement.

## Conseils pour débutants

1. **Ne scanner que des machines autorisées** (votre propre réseau, machines de test)
2. **Ajustez timeout/workers selon votre réseau** (plus lent = timeout plus long)
3. **Vérifiez votre firewall local** qui peut bloquer les connexions sortantes

## Structure du projet

```
scanner-ports-python/
├── scanner.py              # Script principal
├── tests/
│   └── test_scanner.py     # Tests unitaires
├── example_usage.md        # Exemples d'utilisation
├── EXPLANATION.md          # Explications pédagogiques
├── GUIDE_EXECUTION_TESTS.md # Guide pour les tests
├── LICENSE                 # Licence MIT
├── SECURITY.md             # Politique de sécurité
├── README.md              # Ce fichier
└── .gitignore             # Fichiers à ignorer
```

## Auteur

Développé par Cursor - 2024

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Support

Ce projet est éducatif. Pour des questions de sécurité, consultez des experts.