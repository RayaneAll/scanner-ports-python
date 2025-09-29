# Exemples d'utilisation du scanner de ports TCP

> ⚠️ **AVERTISSEMENT** : Utilisez uniquement sur des machines autorisées !

## Exemple 1 : Scan de localhost sur les ports 1-1024

**Commande :**
```bash
python3 scanner.py -t 127.0.0.1 -s 1 -e 1024
```

**Sortie attendue :**
```
Scan de 127.0.0.1 sur les ports 1-1024
Timeout: 1.0s, Workers: 50
--------------------------------------------------
Ports ouverts trouvés:
Port 22 ouvert
Port 80 ouvert
Port 443 ouvert
Port 8080 ouvert

Résumé: 4 ports ouverts sur 1024 scannés en 0.73s
```

## Exemple 2 : Scan d'un domaine externe sur les ports 20-25

**Commande :**
```bash
python3 scanner.py -t example.com -s 20 -e 25 --timeout 0.8 --workers 20
```

**Sortie attendue :**
```
Scan de example.com sur les ports 20-25
Timeout: 0.8s, Workers: 20
--------------------------------------------------
Ports ouverts trouvés:
Port 21 ouvert
Port 22 ouvert
Port 23 ouvert
Port 25 ouvert

Résumé: 4 ports ouverts sur 6 scannés en 0.45s
```

## Exemple 3 : Scan avec paramètres personnalisés

**Commande :**
```bash
python3 scanner.py -t 192.168.1.1 -s 1 -e 100 --timeout 2.0 --workers 10
```

**Sortie attendue :**
```
Scan de 192.168.1.1 sur les ports 1-100
Timeout: 2.0s, Workers: 10
--------------------------------------------------
Ports ouverts trouvés:
Port 22 ouvert
Port 80 ouvert

Résumé: 2 ports ouverts sur 100 scannés en 1.23s
```

## Exemple 4 : Scan sans ports ouverts

**Commande :**
```bash
python3 scanner.py -t 192.168.1.254 -s 2000 -e 2010
```

**Sortie attendue :**
```
Scan de 192.168.1.254 sur les ports 2000-2010
Timeout: 1.0s, Workers: 50
--------------------------------------------------
Aucun port ouvert trouvé

Résumé: 0 ports ouverts sur 11 scannés en 0.15s
```

## Exemple 5 : Erreur de résolution DNS

**Commande :**
```bash
python3 scanner.py -t hostinexistant.local -s 1 -e 10
```

**Sortie attendue :**
```
Scan de hostinexistant.local sur les ports 1-10
Timeout: 1.0s, Workers: 50
--------------------------------------------------
Erreur lors du scan: Impossible de résoudre l'hôte: hostinexistant.local
```

## 📝 Notes importantes

- **Temps d'exécution** : Varient selon la latence réseau
- **Workers** : Plus de workers = scan plus rapide mais plus de charge réseau
- **Timeout** : Plus long = plus fiable sur réseaux lents mais plus lent
- **Autorisation** : Toujours vérifier que vous avez l'autorisation avant de scanner

## 🔗 Voir aussi

- [README.md](README.md) - Documentation complète
- [EXPLANATION.md](EXPLANATION.md) - Explications pédagogiques
- [GUIDE_EXECUTION_TESTS.md](GUIDE_EXECUTION_TESTS.md) - Guide pour les tests
